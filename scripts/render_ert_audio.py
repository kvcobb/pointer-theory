#!/usr/bin/env python3
"""render_ert_audio.py — render the 260731 pointer-theory ERT deliverables to audio,
each in the lens-soul's own canonical OmniVoice ref voice (inline ref_audio, num_step 48
— the canonical method per voice_method_registry). Souls with no ear-tested ref on disk
are SKIPPED (silence over forgery — never fake a voice). Idempotent."""
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path("/home/kurtis/Harmony")
SRC = ROOT / "activity/260731/ert-260731-generalized"
OUT = SRC / "audio"
OUT.mkdir(exist_ok=True)
OMNI = "http://127.0.0.1:8810/v1/audio/speech"
REFS = Path("/home/kurtis/omnivoice/refs")

PIECES = {  # file stem -> ref slug candidates
    "levin-FABLE": ["levin"], "levin-OPUS": ["levin"],
    "friston-FABLE": ["karl.friston"], "friston-OPUS": ["karl.friston"],
    "wolfram-FABLE": ["wolfram"], "wolfram-OPUS": ["wolfram"],
    "gray-FABLE": ["jim.gray"], "gray-OPUS": ["jim.gray"],
    "mcgilchrist-FABLE": ["mcgilchrist"], "mcgilchrist-OPUS": ["mcgilchrist"],
    # mcgilchrist ref K-ear-approved 260731 (20s cut from K's own pointer)
}


def clean(md: str) -> str:
    md = re.sub(r"^>.*$", "", md, flags=re.M)          # orchestrator notes
    md = re.sub(r"^#.*$", "", md, flags=re.M)          # headings
    md = re.sub(r"\*\*|\*|`|—-", " ", md)
    md = re.sub(r"\[(FABLE|OPUS[^\]]*)\]", "", md)
    md = re.sub(r"\s+", " ", md)
    return md.strip()


def chunks_of(text: str, cap: int = 380):
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        while len(s) >= cap:
            if cur:
                out.append(cur)
                cur = ""
            cut = s.rfind(" ", 0, cap)
            cut = cut if cut > 0 else cap
            out.append(s[:cut].strip())
            s = s[cut:].strip()
        if len(cur) + len(s) < cap:
            cur = (cur + " " + s).strip()
        else:
            if cur:
                out.append(cur)
            cur = s
    if cur:
        out.append(cur)
    return [c for c in out if c.strip()]


def render(stem: str, ref: Path) -> bool:
    out = OUT / f"{stem}.mp3"
    if out.exists() and out.stat().st_size > 50_000:
        print(f"  {stem}: exists, skip")
        return True
    text = clean((SRC / f"{stem}.md").read_text())
    segs = []
    with tempfile.TemporaryDirectory() as td:
        for i, ch in enumerate(chunks_of(text)):
            p = json.dumps({"model": "omnivoice", "input": ch[:600], "ref_audio": str(ref),
                            "response_format": "mp3", "num_step": 48}).encode()
            ok = False
            for _ in range(2):
                try:
                    r = urllib.request.urlopen(urllib.request.Request(
                        OMNI, data=p, headers={"Content-Type": "application/json"}), timeout=180)
                    sp = f"{td}/{i}.mp3"
                    open(sp, "wb").write(r.read())
                    if os.path.getsize(sp) > 1500:
                        segs.append(sp)
                        ok = True
                        break
                except Exception:
                    pass
            if not ok:
                print(f"  {stem}: chunk {i} FAILED (continuing)")
        if not segs:
            print(f"  {stem}: FAIL — no segments")
            return False
        lst = f"{td}/l.txt"
        open(lst, "w").write("\n".join(f"file '{s}'" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c", "copy", str(out)], capture_output=True)
    ok = out.exists() and out.stat().st_size > 50_000
    # verify by ffprobe duration, not by the done message
    if ok:
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
        print(f"  {stem}: {out.stat().st_size} bytes, {float(d or 0):.0f}s")
    return ok


def main():
    done = 0
    for stem, slugs in PIECES.items():
        ref = None
        for s in slugs:
            c = REFS / f"{s}-ref.wav"
            if c.exists():
                ref = c
                break
        if not ref:
            print(f"  {stem}: NO REF — skipped (silence over forgery)")
            continue
        if render(stem, ref):
            done += 1
    print(f"rendered {done}/{len(PIECES)}")


if __name__ == "__main__":
    main()
