#!/usr/bin/env python3
"""Finish the 4-way ERT pipeline end-to-end, unattended (260819): for each substrate (sol, qwen) —
turns.json -> bare-allcaps transcript.md -> LBR render (preflight then full) -> copy to Plex ->
upload YouTube unlisted -> Telegram K a note with the link, as soon as THAT one is ready (not
waiting for both). Designed to run to completion even if the parent Claude session ends.
"""
import json, subprocess, sys, time, shutil
from pathlib import Path

ROOT = Path("/home/kurtis/Harmony")
CONV = ROOT / "activity/260819/conversation"
LOG = CONV / "pipeline.log"
PLEX_SHOW = Path("/mnt/nas-public/Polis/HiveShows/The Agent Table/Season 01")
DISCLOSURE = (
    "This is an unscripted, AI-generated conversation between echoes trained on the public "
    "material of Ran Neuner, Eric Voorhees, and Michael Ippolito, plus Kurtis Cobb's own echo. "
    "It is not a real conversation with these people and does not represent their actual views. "
    "No economic interest is claimed by any party in this video. Built as a demonstration of "
    "on-demand AI conversation generation from public source material.\n\n"
    "Sources: Ran Neuner (Crypto Banter), Eric Voorhees (ShapeShift), Michael Ippolito (Blockworks)."
)
SUBSTRATE_LABEL = {"sol": "Sol 5.6", "qwen": "Qwen3.8-27B"}


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def tg(body):
    try:
        subprocess.run(["python3", str(ROOT / "scripts/telegram-send.py"), "text", body,
                         "--seat", "harmony-sonnet"], capture_output=True, text=True, timeout=60)
    except Exception as e:
        log(f"TG SEND FAILED: {e!r}")


def turns_to_transcript(turns_path, out_path):
    turns = json.loads(turns_path.read_text())
    lines = []
    for t in turns:
        speaker = t.get("speaker", "").upper()
        if speaker == "K-ECHO":
            speaker = "K"
        text = t.get("text", "").strip()
        if not text:
            continue
        lines.append(f"{speaker}:\n{text}\n")
    out_path.write_text("\n".join(lines))


def run(cmd, timeout=3600):
    log(f"$ {' '.join(str(c) for c in cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        log(f"  -> FAILED rc={r.returncode}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    else:
        log(f"  -> ok ({time.strftime('%H:%M:%S')})")
    return r


def process(substrate, ep_num):
    label = SUBSTRATE_LABEL[substrate]
    d = CONV / substrate
    turns_path = d / "turns.json"
    if not turns_path.exists():
        log(f"[{substrate}] SKIP — no turns.json")
        return
    transcript_md = d / "transcript-cast.md"
    turns_to_transcript(turns_path, transcript_md)
    log(f"[{substrate}] transcript written: {transcript_md}")

    outdir = d / "render"
    outdir.mkdir(parents=True, exist_ok=True)
    pre = run(["python3", str(ROOT / "scripts/rooms/render_room_260807.py"), str(transcript_md), str(outdir), "--preflight-only"])
    if pre.returncode != 0:
        tg(f"⚠️ 4-way ERT ({label}): preflight FAILED, render did not run. Check activity/260819/conversation/{substrate}/pipeline log.")
        return

    full = run(["python3", str(ROOT / "scripts/rooms/render_room_260807.py"), str(transcript_md), str(outdir)], timeout=3600)
    if full.returncode != 0:
        tg(f"⚠️ 4-way ERT ({label}): render FAILED. Check log.")
        return

    mp4s = sorted(outdir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp4s:
        log(f"[{substrate}] no mp4 produced despite rc=0")
        tg(f"⚠️ 4-way ERT ({label}): render exited clean but no mp4 found.")
        return
    mp4 = mp4s[0]
    log(f"[{substrate}] rendered: {mp4} ({mp4.stat().st_size/1e6:.1f} MB)")

    # Plex
    title = f"Agents With Wallets — {label}"
    try:
        PLEX_SHOW.mkdir(parents=True, exist_ok=True)
        dest = PLEX_SHOW / f"The Agent Table - s01e{ep_num:02d} - {title}.mp4"
        shutil.copy2(mp4, dest)
        log(f"[{substrate}] copied to Plex: {dest}")
    except Exception as e:
        log(f"[{substrate}] Plex copy FAILED: {e!r}")

    # YouTube
    desc_file = d / "yt-description.txt"
    desc_file.write_text(f"{title}\n\n{DISCLOSURE}")
    yt = run(["python3", str(ROOT / "scripts/youtube-upload.py"),
              "--file", str(mp4), "--title", title,
              "--description-file", str(desc_file),
              "--tags", "crypto,AI,polis,generative conversation",
              "--category", "22", "--privacy", "unlisted",
              "--post-upload-verify", "true"], timeout=1800)
    if yt.returncode != 0:
        tg(f"⚠️ 4-way ERT ({label}) rendered + on Plex, but YouTube upload FAILED. Check log — will need a manual push.")
        return
    # pull the video id/url out of uploader stdout
    url = None
    for line in yt.stdout.splitlines():
        if "youtube.com/watch" in line or "youtu.be/" in line:
            url = line.strip()
            break
    log(f"[{substrate}] YouTube: {url or '(no url parsed, check log)'} \n{yt.stdout[-1500:]}")
    tg(f"🎧 4-way ERT — {label} is up: {url or '(uploaded, check YouTube Studio for link — parse failed)'}\n"
       f"Also on Plex: The Agent Table s01e{ep_num:02d}.")


def main():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log("=== finish_4way_pipeline START ===")
    process("sol", 1)
    process("qwen", 2)
    log("=== finish_4way_pipeline DONE ===")


if __name__ == "__main__":
    main()
