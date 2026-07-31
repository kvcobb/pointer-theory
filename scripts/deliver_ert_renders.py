#!/usr/bin/env python3
"""deliver_ert_renders.py — wrap the 260731 pointer-theory ERT audio renders to mp4
(title-card + looped still, the render_frankendancer recipe: -loop 1 REQUIRES explicit
-framerate or audio drops) and deliver to Plex 42-Practice Specials with sequential
episode numbers. Verify every artifact by ffprobe duration+audio-stream, never by exit
code. Idempotent via a local ledger."""
import json
import re
import shutil
import subprocess
from pathlib import Path

SRC = Path("/home/kurtis/Harmony/activity/260731/ert-260731-generalized/audio")
WORK = SRC.parent / "mp4"
WORK.mkdir(exist_ok=True)
PLEX = Path("/mnt/nas-public/Polis/HiveShows/The 42 Practice/Specials")
LEDGER = SRC.parent / "plex-delivery-ledger.jsonl"

TITLES = {
    "levin": "Michael Levin", "friston": "Karl Friston", "wolfram": "Stephen Wolfram",
    "mcgilchrist": "Iain McGilchrist", "gray": "Jim Gray",
}


def card_for(stem: str) -> Path:
    lens, arm = stem.rsplit("-", 1)
    out = WORK / f"{stem}-card.png"
    if out.exists():
        return out
    title = TITLES.get(lens, lens.title())
    label = f"{title}\\nPointer Theory ERT · {arm.title()} arm\\n260731 · K100 polis · AI echo (disclosed)"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "color=c=0x101418:s=1280x720:d=1",
        "-vf", ("drawtext=text='" + label + "':fontcolor=0xE8E4D8:fontsize=44:"
                "x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=18:"
                "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        "-frames:v", "1", str(out)], capture_output=True)
    return out


def probe_ok(p: Path, min_s: float = 60) -> float:
    try:
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", str(p)], capture_output=True, text=True,
                                 timeout=60).stdout.strip())
        a = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                            "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(p)],
                           capture_output=True, text=True, timeout=60).stdout.strip()
        return d if (d > min_s and a) else 0.0
    except Exception:
        return 0.0


def next_episode() -> int:
    nums = [int(m.group(1)) for f in PLEX.iterdir()
            if (m := re.search(r"s00e(\d+)", f.name))]
    return max(nums) + 1 if nums else 1


def delivered() -> set:
    if not LEDGER.exists():
        return set()
    return {json.loads(l)["stem"] for l in LEDGER.read_text().splitlines() if l.strip()}


def main():
    done = delivered()
    order = ["levin-FABLE", "levin-OPUS", "friston-FABLE", "friston-OPUS",
             "wolfram-FABLE", "wolfram-OPUS", "mcgilchrist-FABLE", "mcgilchrist-OPUS",
             "gray-FABLE", "gray-OPUS"]
    ep = next_episode()
    for stem in order:
        if stem in done:
            print(f"{stem}: already delivered — skip")
            continue
        mp3 = SRC / f"{stem}.mp3"
        src_d = probe_ok(mp3)
        if not src_d:
            print(f"{stem}: SOURCE FAILED PROBE — skipped loudly")
            continue
        mp4 = WORK / f"{stem}.mp4"
        if not probe_ok(mp4, min_s=60):
            card = card_for(stem)
            subprocess.run(["ffmpeg", "-y", "-loop", "1", "-framerate", "2", "-i", str(card),
                            "-i", str(mp3), "-c:v", "libx264", "-preset", "veryfast",
                            "-tune", "stillimage", "-c:a", "aac", "-b:a", "160k",
                            "-pix_fmt", "yuv420p", "-shortest", str(mp4)], capture_output=True)
        d = probe_ok(mp4, min_s=60)
        if not d or abs(d - src_d) > 3:
            print(f"{stem}: MP4 FAILED VERIFY ({d}s vs {src_d}s) — not delivered")
            continue
        lens, arm = stem.rsplit("-", 1)
        title = TITLES.get(lens, lens.title())
        dest = PLEX / (f"The 42 Practice - s00e{ep:03d} - Special — Pointer Theory ERT · "
                       f"{title} ({arm.title()} arm).mp4")
        shutil.copy2(mp4, dest)
        dd = probe_ok(dest, min_s=60)
        if not dd:
            print(f"{stem}: PLEX COPY FAILED VERIFY — removing partial")
            dest.unlink(missing_ok=True)
            continue
        with LEDGER.open("a") as f:
            f.write(json.dumps({"stem": stem, "episode": ep, "dest": str(dest),
                                "duration_s": dd}) + "\n")
        print(f"{stem}: delivered s00e{ep:03d} ({dd:.0f}s verified on Plex share)")
        ep += 1


if __name__ == "__main__":
    main()
