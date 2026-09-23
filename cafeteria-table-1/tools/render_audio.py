#!/usr/bin/env python3
"""Render a cafeteria-table transcript to one audio podcast file with a local OmniVoice server.

    python tools/render_audio.py TRANSCRIPT.md out.mp3 --model "Claude Opus 5.5" [--server http://127.0.0.1:8810] [--gap 0.35] [--force]

1. FREEZES its inputs first: reads the transcript bytes and voices.json once, copies each voice reference into a private
   temp dir, and hashes all of them. Everything after this uses only the frozen copies.
2. Runs tools/check_transcript.py's check() on the frozen text and stops (zero server calls) if it doesn't PASS.
3. One physical line = one turn; "STAGE:" lines are unvoiced and skipped. Each turn is split at sentence ends into
   chunks under 380 characters (a longer sentence is split at word boundaries). Request: model=omnivoice,
   response_format=mp3, num_step=48, ref_audio = the frozen copy, ref_text = the pinned transcript from voices.json.
4. Every returned piece is decoded to identical PCM WAV (24 kHz mono s16), joined with a short pause between turns,
   and encoded to mp3 once, into a TEMP file next to the output.
5. Before publishing: verifies the temp mp3 decodes with a positive duration, and re-hashes the original transcript,
   voices.json and refs. If any of them changed during the render, it stops and publishes nothing.
6. Publishes with a commit contract (see publish()): both destinations are preflighted before any work; an exclusive
   per-output lock prevents concurrent renders; audio is committed first and the receipt LAST, and if the receipt can't
   be committed the audio is rolled back. Without --force, publishing uses os.link (fails if the destination exists; no
   check-then-act race). With --force, old files are moved aside and restored on any failure.
Needs ffmpeg/ffprobe on PATH. The only network calls go to the local server you point it at.
"""
import argparse, fcntl, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
from check_transcript import check
hb = lambda b: hashlib.sha256(b).hexdigest()
hf = lambda p: hb(Path(p).read_bytes())
CAP = 380

def chunks(t, cap=CAP):
    pieces = []
    for s in re.split(r"(?<=[.!?])\s+", t):
        while len(s) >= cap:                       # a sentence longer than the cap: split at the last space before it
            cut = s.rfind(" ", 0, cap - 1)
            cut = cut if cut > 0 else cap - 1
            pieces.append(s[:cut].strip()); s = s[cut:].strip()
        if s: pieces.append(s)
    out, cur = [], ""
    for s in pieces:
        if len(cur) + len(s) + 1 < cap: cur = (cur + " " + s).strip()
        else:
            if cur: out.append(cur)
            cur = s
    if cur: out.append(cur)
    assert all(len(c) < cap for c in out)
    return out

def publish(tmp_out, tmp_rec, out, rec_path, force):
    """Commit contract: audio first, receipt LAST; if the receipt can't be committed, the audio is rolled back, so a
    published output always has its receipt. Without --force both are published with os.link, which fails if the
    destination exists (exclusive, no clobber, no check-then-act race). With --force the old files are moved aside
    first and restored if anything fails."""
    backups = []
    try:
        for d in (out, rec_path):                              # re-check right before touching anything
            if d.is_symlink() or (d.exists() and not d.is_file()): raise RuntimeError(f"{d} is not a regular file")
        if force:
            for d in (out, rec_path):
                if d.exists():
                    bak = d.with_name(f".{d.name}.bak-{os.getpid()}"); os.replace(d, bak); backups.append((bak, d))
        os.link(tmp_out, out)                                  # FileExistsError if someone else created it meanwhile
        try:
            os.link(tmp_rec, rec_path)
        except BaseException:
            out.unlink()                                       # roll the audio back: no audio without its receipt
            raise
    except BaseException as e:
        for bak, d in backups:                                 # restore anything --force moved aside
            if not d.exists(): os.replace(bak, d)
        raise RuntimeError(f"publish failed, nothing published ({type(e).__name__}: {e})")
    for bak, _ in backups:
        bak.unlink()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("transcript"); ap.add_argument("out")
    ap.add_argument("--model", required=True); ap.add_argument("--server", default="http://127.0.0.1:8810")
    ap.add_argument("--gap", type=float, default=0.35); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    raw = Path(a.out); out = raw.parent.resolve() / raw.name     # resolve the directory only; NEVER follow the leaf
    rec_path = out.with_name(out.name + ".receipt.json")
    # preflight BOTH destinations before any work (and again under the lock, and again in publish())
    def dest_check():
        for d in (out, rec_path):
            if d.is_symlink(): sys.exit(f"{d} is a symlink; refusing")
            if d.exists():
                if not a.force: sys.exit(f"{d} exists; pass --force to overwrite")
                if not d.is_file(): sys.exit(f"{d} exists and is not a regular file; refusing")
    dest_check()
    # one render per output at a time: an exclusive, non-blocking lock scoped to this output
    lock = open(out.with_name(f".{out.name}.lock"), "w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: sys.exit(f"another render holds the lock for {out}")
    dest_check()
    # 1. freeze
    tr_bytes = Path(a.transcript).read_bytes(); vj_bytes = (HERE / "voices.json").read_bytes()
    voices = json.loads(vj_bytes)["voices"]
    frozen = {"transcript": hb(tr_bytes), "voices_json": hb(vj_bytes)}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); refdir = td / "refs"; refdir.mkdir()
        refs = {}
        for label, v in voices.items():
            src = HERE / v["ref_audio"]; dst = refdir / f"{label}{src.suffix}"; shutil.copyfile(src, dst)
            refs[label] = dst; frozen[f"ref:{label}"] = hf(dst)
        # 2. check on the frozen text, before any server call
        try: r = check(a.transcript, a.model, text=tr_bytes.decode(), voices=voices)
        except ValueError as e: sys.exit(str(e))
        if not r["PASS"]: sys.exit("transcript failed check_transcript: " + json.dumps(r))
        turns = []
        for line in tr_bytes.decode().splitlines():
            if not line.strip() or line.startswith("STAGE: "): continue
            label, text = line.split(":", 1); turns.append((label, text.strip()))
        # 3-4. render into temp
        n_chunks, parts = 0, []
        wav = lambda src, dst: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(dst)], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(a.gap), "-c:a", "pcm_s16le", str(td / "gap.wav")], check=True)
        for i, (label, text) in enumerate(turns):
            v = voices[label]
            for j, ch in enumerate(chunks(text)):
                body = {"model": "omnivoice", "input": ch, "response_format": "mp3", "num_step": 48, "ref_audio": str(refs[label])}
                if v.get("ref_text"): body["ref_text"] = v["ref_text"]
                req = urllib.request.Request(a.server + "/v1/audio/speech", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                m = td / f"{i:04d}-{j:02d}.mp3"; m.write_bytes(urllib.request.urlopen(req, timeout=300).read())
                w = m.with_suffix(".wav"); wav(m, w); parts.append(w); n_chunks += 1
            parts.append(td / "gap.wav")
            print(f"turn {i+1}/{len(turns)} {label}", flush=True)
        (td / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts))
        tmp_out = out.with_name(f".{out.name}.tmp-{os.getpid()}.mp3")
        try:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(td / "list.txt"), "-c:a", "libmp3lame", "-b:a", "128k", str(tmp_out)], check=True)
            # 5. verify the result and check for input drift
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(tmp_out)], capture_output=True, text=True, check=True).stdout.strip() or 0)
            if dur <= 0: raise RuntimeError("encoded file has no duration")
            now = {"transcript": hf(a.transcript), "voices_json": hf(HERE / "voices.json")}
            now.update({f"ref:{label}": hf(HERE / v["ref_audio"]) for label, v in voices.items()})
            drift = sorted(k for k in frozen if now.get(k) != frozen[k])
            if drift: raise RuntimeError(f"inputs changed during the render ({', '.join(drift)}); nothing published")
            health = None
            try:
                h = json.loads(urllib.request.urlopen(a.server + "/health", timeout=10).read())
                health = {k: h.get(k) for k in ("status", "model", "device", "resident")}
            except Exception as e: health = {"error": str(e)}
            rec = {"output": str(out), "output_sha256": hf(tmp_out), "duration_s": round(dur, 3), "frozen_inputs_sha256": frozen,
                   "model_declared": a.model.strip(), "turns": len(turns), "chunks": n_chunks,
                   "settings": {"num_step": 48, "chunk_cap": CAP, "gap_s": a.gap}, "server": a.server, "server_health": health,
                   "finished": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
            tmp_rec = out.with_name(f".{out.name}.receipt.tmp-{os.getpid()}.json"); tmp_rec.write_text(json.dumps(rec, indent=1))
            publish(tmp_out, tmp_rec, out, rec_path, a.force)
        finally:
            for p in (tmp_out, out.with_name(f".{out.name}.receipt.tmp-{os.getpid()}.json")):
                if p.exists(): p.unlink()
    print("wrote", out, "and", str(out) + ".receipt.json")

if __name__ == "__main__":
    try: main()
    except RuntimeError as e: sys.exit(str(e))
