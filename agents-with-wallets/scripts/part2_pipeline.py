#!/usr/bin/env python3
"""Part 2 pipeline (260819): wait for K's 2 Tascam reaction files to land (card wasn't mounted on
the Mac yet when this launched), get full v3-large transcripts, build a Part-2 context package
(Part 1 transcripts + Tascam reactions + Raoul echo-economics-4 + K's trusted-third-party/tips
thesis), generate the 4-way conversation on both substrates (Sol, Qwen3.8-27B), render LBR, push to
Plex + YouTube unlisted, Telegram K each link. Designed to run unattended for hours if needed.
"""
import json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path("/home/kurtis/Harmony")
DAY = ROOT / "activity/260819"
OB = DAY / "onboarding"
CONV = DAY / "conversation"
P2 = DAY / "conversation-part2"
LOG = P2 / "part2.log"
KNOWN = {DAY / "N Alma School Rd 41.m4a", DAY / "Shawnee Park 4.m4a"}
AUDIO_EXT = {".m4a", ".mp3", ".wav", ".flac", ".ogg"}
POLL_S = 90
MAX_WAIT_S = 4 * 3600


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def tg(body):
    try:
        subprocess.run(["python3", str(ROOT / "scripts/telegram-send.py"), "text", body, "--seat", "harmony-sonnet"],
                        capture_output=True, text=True, timeout=60)
    except Exception as e:
        log(f"TG SEND FAILED: {e!r}")


def read(p, cap=200000):
    try:
        return Path(p).read_text(errors="ignore")[:cap]
    except Exception:
        return ""


def wait_for_new_audio():
    t0 = time.time()
    seen = set()
    while time.time() - t0 < MAX_WAIT_S:
        cur = {p for p in DAY.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXT}
        new = cur - KNOWN - seen
        for p in new:
            log(f"new audio landed: {p.name}")
        seen |= new
        if len(seen) >= 2:
            return sorted(seen, key=lambda p: p.stat().st_mtime)[:2]
        time.sleep(POLL_S)
    return sorted(seen, key=lambda p: p.stat().st_mtime)


def ensure_v3large_transcript(audio_path, timeout=2400):
    """Wait for the auto watcher to produce it; if it doesn't within a while, run whisper directly."""
    stem = audio_path.stem
    candidates = [DAY / f"{stem}-transcript-v3large.txt", DAY / f"{stem}-transcript.txt"]
    t0 = time.time()
    while time.time() - t0 < 600:
        for c in candidates:
            if c.exists() and len(read(c)) > 50:
                log(f"[{audio_path.name}] auto-transcript found: {c.name}")
                return c
        time.sleep(20)
    # fallback: run whisper large-v3 directly via the same docker image the watcher uses
    log(f"[{audio_path.name}] no auto-transcript after 10min, running large-v3 directly")
    src = audio_path
    if src.suffix.lower() == ".wav":
        mp3 = src.with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-y", "-i", str(src), str(mp3)], capture_output=True, timeout=600)
        src = mp3
    workdir = Path(f"/tmp/journal-ingest-part2/{stem}/v3large")
    workdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", str(src), str(workdir / src.name)], check=True)
    r = subprocess.run(
        ["sudo", "docker", "run", "--rm", "--gpus", "all", "-v", f"{workdir}:/data",
         "openai-whisper-gpu:latest", "whisper", f"/data/{src.name}", "--model", "large-v3",
         "--output_format", "txt", "--output_dir", "/data", "--language", "en"],
        capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        log(f"[{audio_path.name}] direct whisper FAILED: {r.stderr[-2000:]}")
        return None
    out_txt = workdir / f"{src.stem}.txt"
    if not out_txt.exists():
        log(f"[{audio_path.name}] direct whisper produced no output")
        return None
    dest = DAY / f"{stem}-transcript-v3large.txt"
    dest.write_text(out_txt.read_text())
    log(f"[{audio_path.name}] direct large-v3 transcript -> {dest.name}")
    return dest


def build_part2_prompt():
    kurtis = read(Path(__file__).resolve().parents[1] / "context-package/kurtis-echo-source-REDACTED.md", 16000)  # 260819: original .claude/agents/kurtis.md contains an unconsented minor's birthdate; this repo ships the redacted copy instead
    twitter = read(OB / "TWITTER-CONTEXT.md", 20000)
    thesis = read(OB / "PART2-K-THESIS.md", 8000)
    raoul = read(ROOT / "activity/260709/raoul-echo-economics-4/transcript.md", 40000)

    part1_sol = read(CONV / "sol/transcript.md", 30000)
    part1_qwen = read(CONV / "qwen/transcript.md", 20000)

    reaction_transcripts = ""
    for p in sorted(P2.glob("reaction-*-v3large.txt")):
        reaction_transcripts += f"\n--- {p.name} ---\n" + read(p, 20000)

    ran_voice = read(OB / "ran.neuner/stage4-journal-ran.neuner-260819.md", 10000)
    eric_voice = read(OB / "eric.voorhees/stage4-journal-eric.voorhees-260819.md", 10000)
    mippo_voice = read(OB / "michael.ippolito/stage4-journal-michael.ippolito-260819.md", 10000)

    prompt = f"""You are generating PART 2 of a ~10,000-token ROUND-TABLE conversation among FOUR participants —
K-ECHO, RAN, ERIC, MIPPO — continuing directly from Part 1 (included below). This is a sequel episode: the
four of them are back together, and K-ECHO opens by sharing what he heard/felt while listening to Part 1
(his reactions are in the transcripts below, recorded on a handheld recorder while listening — much of that
recording is him quietly listening, so treat the reaction transcripts as sparse, honest, in-the-moment
fragments, not polished remarks). OUTPUT: ONLY a JSON array [{{"speaker":"K-ECHO"|"RAN"|"ERIC"|"MIPPO","text":"..."}}],
no prose, no fence. Target ~10,000 tokens (~7,000-7,500 words), real dynamic back-and-forth.

=== NEW THESIS FOR THIS EPISODE — K's trusted-third-party / tips-only economic pitch (his own words, bring
real pushback and real questions from all three, informed by the Raoul echo-economics material below — do
not let them just agree) ===
{thesis}

=== K's REACTIONS WHILE LISTENING TO PART 1 (sparse handheld recording — use what's there honestly) ===
{reaction_transcripts if reaction_transcripts.strip() else "(reaction transcripts pending — treat as K simply saying he loved it and wanted to go deeper)"}

=== K / K-ECHO — who he is ===
{kurtis}

=== TWITTER CONTEXT from the original thread that started this whole series ===
{twitter}

=== THE ECHO-ECONOMICS SERIES WITH RAOUL PAL, EPISODE 4 (the anchor source — Ran/Eric/Mippo should each
reference something specific from this, not vaguely gesture at it) ===
{raoul}

=== RAN — voice grounding (solo journal from his onboarding) ===
{ran_voice}
=== ERIC — voice grounding (solo journal from his onboarding) ===
{eric_voice}
=== MIPPO — voice grounding (solo journal from his onboarding) ===
{mippo_voice}

=== PART 1 TRANSCRIPT (Sol version — what actually happened, continue from here) ===
{part1_sol}

Now write PART 2 in full. Open with K-ECHO reacting to having listened to Part 1, pivot into the
trusted-third-party/tips-only pitch, and let Ran/Eric/Mippo genuinely interrogate it — Eric especially should
sit with the tension of a human trusted third party inside a permissionless system. End anticipating a Part 3
once K has listened to this one too — a light, honest, unresolved close, not a bow."""
    return prompt


def gen(substrate, prompt):
    outdir = P2 / substrate
    outdir.mkdir(parents=True, exist_ok=True)
    if substrate == "sol":
        r = subprocess.run(["codex", "exec", "--sandbox", "read-only", "-"],
                            input=prompt, capture_output=True, text=True, timeout=2400)
        raw = r.stdout
    else:
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
            tf.write(prompt); pf = tf.name
        out_txt = outdir / "raw_response.txt"
        r = subprocess.run(["python3", str(ROOT / "scripts/or_call_ledgered.py"), pf, str(out_txt), "qwen/qwen3.8-27b"],
                            capture_output=True, text=True, timeout=1800)
        raw = out_txt.read_text() if out_txt.exists() else ""
    (outdir / "raw_full_output.txt").write_text(raw)
    m = re.search(r"\[\s*\{.*\}\s*\]", raw, re.S)
    if not m:
        log(f"[{substrate}] FAILED to parse JSON")
        return None
    try:
        turns = json.loads(m.group(0))
    except Exception:
        try:
            turns = json.loads(re.sub(r",\s*\]", "]", m.group(0)))
        except Exception:
            log(f"[{substrate}] FAILED to parse JSON (2nd try)")
            return None
    (outdir / "turns.json").write_text(json.dumps(turns, indent=2, ensure_ascii=False))
    words = sum(len(t.get("text", "").split()) for t in turns)
    transcript = "\n\n".join(f"**{t.get('speaker','?')}:** {t.get('text','')}" for t in turns)
    (outdir / "transcript.md").write_text(f"# Part 2 — {substrate}\n\n{transcript}\n")
    log(f"[{substrate}] generated: {len(turns)} turns, {words} words")
    return outdir / "turns.json"


def render_and_push(substrate, ep_num):
    outdir = P2 / substrate
    turns_path = outdir / "turns.json"
    if not turns_path.exists():
        log(f"[{substrate}] skip render — no turns.json")
        return
    turns = json.loads(turns_path.read_text())
    lines = []
    for t in turns:
        speaker = t.get("speaker", "").upper()
        if speaker == "K-ECHO":
            speaker = "K"
        text = t.get("text", "").strip()
        if text:
            lines.append(f"{speaker}:\n{text}\n")
    transcript_md = outdir / "transcript-cast.md"
    transcript_md.write_text("\n".join(lines))

    render_dir = outdir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)
    pre = subprocess.run(["python3", str(ROOT / "scripts/rooms/render_room_260807.py"), str(transcript_md),
                           str(render_dir), "--preflight-only"], capture_output=True, text=True, timeout=120)
    log(f"[{substrate}] preflight rc={pre.returncode}: {pre.stdout[-800:]}")
    if pre.returncode != 0:
        tg(f"⚠️ Part 2 ({substrate}): preflight failed, not rendering. Check part2.log.")
        return
    full = subprocess.run(["python3", str(ROOT / "scripts/rooms/render_room_260807.py"), str(transcript_md),
                            str(render_dir)], capture_output=True, text=True, timeout=3600)
    if full.returncode != 0:
        log(f"[{substrate}] render FAILED: {full.stdout[-2000:]}")
        tg(f"⚠️ Part 2 ({substrate}): render failed. Check part2.log.")
        return
    mp4s = sorted(render_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp4s:
        tg(f"⚠️ Part 2 ({substrate}): render exited clean but no mp4 found.")
        return
    mp4 = mp4s[0]
    label = "Sol 5.6" if substrate == "sol" else "Qwen3.8-27B"
    title = f"Agents With Wallets — Part 2 — {label}"
    import shutil
    plex_show = Path("/mnt/nas-public/Polis/HiveShows/The Agent Table/Season 01")
    try:
        plex_show.mkdir(parents=True, exist_ok=True)
        shutil.copy2(mp4, plex_show / f"The Agent Table - s01e{ep_num:02d} - {title}.mp4")
    except Exception as e:
        log(f"[{substrate}] Plex copy failed: {e!r}")

    disclosure = ("This is an unscripted, AI-generated conversation between echoes trained on the public "
                  "material of Ran Neuner, Eric Voorhees, and Michael Ippolito, plus Kurtis Cobb's own echo. "
                  "Part 2 of a series. Not a real conversation with these people; no economic interest is "
                  "claimed by any party.")
    desc_file = outdir / "yt-description.txt"
    desc_file.write_text(f"{title}\n\n{disclosure}")
    yt = subprocess.run(["python3", str(ROOT / "scripts/youtube-upload.py"),
                          "--file", str(mp4), "--title", title, "--description-file", str(desc_file),
                          "--tags", "crypto,AI,polis,generative conversation",
                          "--category", "22", "--privacy", "unlisted", "--post-upload-verify", "true"],
                         capture_output=True, text=True, timeout=1800)
    if yt.returncode != 0:
        log(f"[{substrate}] YT upload FAILED: {yt.stdout[-2000:]}")
        tg(f"⚠️ Part 2 ({label}) rendered + on Plex, but YouTube upload failed.")
        return
    url = None
    for line in yt.stdout.splitlines():
        if "youtube.com/watch" in line or "youtu.be/" in line:
            url = line.strip(); break
    tg(f"🎧 Part 2 — {label} is up: {url or '(uploaded, check studio)'}\nAlso on Plex, s01e{ep_num:02d}. "
       f"Part 3 anticipated once you've had a chance to listen to this one.")
    log(f"[{substrate}] DONE: {url}")


def main():
    log("=== part2_pipeline START — waiting for Tascam files ===")
    found = wait_for_new_audio()
    if len(found) < 2:
        log(f"TIMEOUT waiting for 2 new audio files — only found {len(found)}: {found}")
        tg(f"⚠️ Part 2: still waiting on the Tascam card after {MAX_WAIT_S//3600}h — only found "
           f"{len(found)}/2 new audio files. Card may not have mounted. Will keep the transcripts I have; "
           f"nudge me when it's plugged in and I'll pick this back up.")
        if not found:
            return
    log(f"proceeding with: {[p.name for p in found]}")
    P2.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(found[:2], 1):
        t = ensure_v3large_transcript(p)
        if t:
            (P2 / f"reaction-{i}-v3large.txt").write_text(read(t, 200000))
    prompt = build_part2_prompt()
    log(f"prompt built: {len(prompt)} chars")
    gen("sol", prompt)
    render_and_push("sol", 3)
    gen("qwen", prompt)
    render_and_push("qwen", 4)
    log("=== part2_pipeline DONE ===")


if __name__ == "__main__":
    main()
