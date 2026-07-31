#!/usr/bin/env python3
"""OmniVoice local TTS server — thin first-party wrapper (Phase 1, per activity/260531/omnivoice/06-integration-design.md).

Resident k2-fsa/OmniVoice model on the 4090, served behind the SAME OpenAI-/11labs-shaped
envelope Kokoro speaks at :8880, so scripts/render-prepped.py's tts() dispatch barely changes.

- Bind 127.0.0.1:8810 (localhost only; never --share, never 0.0.0.0).
- GET  /health            -> {"status":"ok","model":...,"device":...,"resident":bool}
- POST /v1/audio/speech   -> audio/mpeg (mono, 24kHz, mp3)   [11labs/Kokoro-shaped]
- Voice resolution via scripts/voice/omnivoice-voice-registry.json (logical id -> ref/instruct).
- Mono enforcement is LOAD-BEARING (render-prepped ffmpeg concat silently drops non-mono).
- Fail-loud: any failure -> non-200 + {"error","detail"} so tts()'s status!=200 path fires.

Run (on MarvinGardens, in the omnivoice venv):
    HF_HOME=/home/kurtis/omnivoice/hf_cache \
    /home/kurtis/omnivoice/.venv/bin/python scripts/voice/omnivoice-server.py

Env:
    OMNIVOICE_PORT   (default 8810)
    OMNIVOICE_MODEL  (default k2-fsa/OmniVoice)
    OMNIVOICE_REGISTRY (default scripts/voice/omnivoice-voice-registry.json, then a fallback next to this file)
"""
import io
import os
import json
import subprocess
import pathlib
import threading

import numpy as np
import torch
import soundfile as sf
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

MODEL_ID = os.environ.get("OMNIVOICE_MODEL", "k2-fsa/OmniVoice")
PORT = int(os.environ.get("OMNIVOICE_PORT", "8810"))
SR = 24000
HERE = pathlib.Path(__file__).resolve().parent
REGISTRY_PATH = pathlib.Path(
    os.environ.get("OMNIVOICE_REGISTRY", str(HERE / "omnivoice-voice-registry.json"))
)

app = FastAPI(title="omnivoice-local")
_model = None
_model_lock = threading.Lock()          # one generate at a time (single resident model)


def _load_registry() -> dict:
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text())
        except Exception as e:
            print(f"[registry] WARN failed to parse {REGISTRY_PATH}: {e}")
    return {}


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from omnivoice import OmniVoice
                print(f"[model] loading {MODEL_ID} on cuda:0 (fp16)...", flush=True)
                _model = OmniVoice.from_pretrained(MODEL_ID, device_map="cuda:0", dtype=torch.float16)
                print("[model] resident.", flush=True)
    return _model


def _to_mono_mp3(audio: np.ndarray) -> bytes:
    """24kHz numpy -> mono mp3 bytes. Mono enforcement is non-negotiable (concat silent-drop guard)."""
    a = np.asarray(audio).astype("float32").reshape(-1)        # force mono 1-D
    # write wav to a temp pipe, transcode to mp3 mono via ffmpeg (libmp3lame)
    wav_buf = io.BytesIO()
    sf.write(wav_buf, a, SR, format="WAV", subtype="PCM_16")
    wav_buf.seek(0)
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "wav", "-i", "pipe:0",
         "-ac", "1", "-ar", str(SR), "-c:a", "libmp3lame", "-q:a", "4", "-f", "mp3", "pipe:1"],
        input=wav_buf.read(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg mp3 encode failed: {proc.stderr.decode()[:300]}")
    return proc.stdout


class SpeechReq(BaseModel):
    model: str = "omnivoice"
    input: str
    voice: str | None = None          # logical voice id -> registry; or None for raw instruct
    response_format: str = "mp3"
    instructions: str | None = None   # OpenAI 'instructions' == OmniVoice design 'instruct'
    ref_audio: str | None = None      # inline clone: path to reference wav (bypasses registry) — for validation/candidate builds
    ref_text: str | None = None       # optional transcript of ref_audio
    num_step: int = 32
    speed: float = 1.0


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_ID, "device": "cuda:0",
            "resident": _model is not None, "port": PORT,
            "registry": str(REGISTRY_PATH),
            "registry_voices": [k for k in _load_registry() if not k.startswith("_")]}


@app.post("/v1/audio/speech")
def speech(req: SpeechReq):
    text = (req.input or "").strip()
    if not text:
        return JSONResponse(status_code=400, content={"error": "empty_input", "detail": "input text required"})

    reg = _load_registry()
    ref_audio = ref_text = instruct = None
    num_step, speed = req.num_step, req.speed

    # inline clone (validation / candidate builds): explicit ref_audio bypasses the registry
    if req.ref_audio:
        if not pathlib.Path(req.ref_audio).exists():
            return JSONResponse(status_code=422, content={"error": "ref_audio_missing", "detail": f"{req.ref_audio} not on disk"})
        ref_audio = req.ref_audio
        ref_text = req.ref_text
    elif req.voice and req.voice in reg:
        v = reg[req.voice]
        ref_audio = v.get("ref_audio")
        ref_text = v.get("ref_text")
        instruct = v.get("instruct")
        num_step = v.get("num_step", num_step)
        speed = v.get("speed", speed)
        if ref_audio and not pathlib.Path(ref_audio).exists():
            return JSONResponse(status_code=422,
                                content={"error": "ref_audio_missing", "detail": f"{ref_audio} not on disk for voice '{req.voice}'"})
    elif req.voice:
        return JSONResponse(status_code=404,
                            content={"error": "unknown_voice", "detail": f"'{req.voice}' not in {REGISTRY_PATH.name}"})
    # direct instruct override (design mode without a registry entry)
    if req.instructions:
        instruct = req.instructions

    if not ref_audio and not instruct:
        return JSONResponse(status_code=422,
                            content={"error": "no_voice_spec", "detail": "need a registry 'voice' (clone/design) or 'instructions' (design)"})

    try:
        model = _get_model()
        kwargs = dict(text=text, num_step=num_step, speed=speed)
        if ref_audio:
            kwargs["ref_audio"] = ref_audio
            if ref_text:
                kwargs["ref_text"] = ref_text
        if instruct:
            kwargs["instruct"] = instruct
        with _model_lock:
            out = model.generate(**kwargs)
        audio = out[0] if isinstance(out, (list, tuple)) else out
        audio = np.asarray(audio).astype("float32").reshape(-1)
        # empty/short-audio guard (OmniVoice #44/#163: a 200 can still be garbage)
        if audio.size < int(0.3 * SR) or float(np.abs(audio).max()) < 0.01:
            return JSONResponse(status_code=500,
                                content={"error": "degenerate_audio",
                                         "detail": f"samples={audio.size} peak={float(np.abs(audio).max()):.4f}"})
        mp3 = _to_mono_mp3(audio)
        return Response(content=mp3, media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "generate_failed", "detail": str(e)[:400]})


if __name__ == "__main__":
    print(f"[omnivoice-server] binding 127.0.0.1:{PORT} (localhost only)  registry={REGISTRY_PATH}", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
