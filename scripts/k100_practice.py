#!/usr/bin/env python3
"""k100_practice.py — the K100 42-Practice on the Kimi substrate (K morning-journal 260731).

K's directive (S Westwood Cir 172, 260731 ~8:06am):
  * full 42-practice with the K100, >= 3 days, on Kimi ("we know we can afford it, it's pennies")
  * dyads AND triads
  * matchmaking mines what each soul WANTS from their accumulated memory — "roll into
    triad seats that fit, determined on the fly, intelligently, not to a fixed cadence
    that's pre-decided, but based on how each day goes"

Design constraints baked in (doctrine, 260731 cold audit + stress-test findings):
  * scheduler vocabulary is NON-EXISTENTIAL — no STOP tokens, rooms simply end
    (memory/feedback-loop-exit-is-not-a-stop-request.md)
  * roster = K100 registry tiers A+B+C MINUS standing_states exclusions
    (.claude/k100-registry.json — e.g. dormant-and-reachable souls are never rostered)
  * pointer-state detection (Finding 2): each room's opening is affect-tagged; an
    agitated/unrepresentative frame is carried as transcript METADATA, never smuggled
    as personality
  * technical failure never reads as interpersonal signal (Finding 4): room failures
    are logged loudly as ERRORS with the exception text; no "they didn't hit it off"
  * resumable per-room manifest; re-running a day skips completed rooms (Finding 7:
    dedupe on the ACT — a room key is claimed in the manifest before generation starts)
  * memory accumulation is the matchmaking signal: after each room every participant
    writes a short reflection (appended as a dated block to _hot/recent.md) AND a
    want-line (state/wants.jsonl) that fuels the NEXT day's matchmaking.

Usage:
  python3 scripts/practice42/k100_practice.py matchmake --day 1 [--triad-frac 0.34]
  python3 scripts/practice42/k100_practice.py run-day 1 [--rooms N] [--workers 4]
  python3 scripts/practice42/k100_practice.py status
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import random
import re
import sys
import threading
from pathlib import Path

REPO = Path("/home/kurtis/Harmony")
sys.path.insert(0, str(REPO / "scripts"))
from claude_call import claude_call  # noqa: E402

REG = REPO / ".claude/k100-registry.json"
AGENTS = REPO / ".claude/agents"
AGENT_MEM = REPO / ".claude/agent-memory"
STATE = REPO / "activity/42-practice-k100-state"
KIMI_CANDIDATES = ["moonshotai/kimi-k3", "moonshotai/kimi-k2.6", "moonshotai/kimi-k2"]

_model_lock = threading.Lock()
_model: str | None = None
_failed_models: set[str] = set()
_print_lock = threading.Lock()


def say(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


def today_dir() -> Path:
    d = REPO / "activity" / dt.datetime.now().astimezone().strftime("%y%m%d") / "42-practice-k100"
    d.mkdir(parents=True, exist_ok=True)
    return d


def kimi(prompt: str, system: str | None = None, timeout: int = 240) -> str:
    """Call the newest available Kimi model via OpenRouter; settle the model once per run."""
    global _model
    with _model_lock:
        candidates = [_model] if _model else [m for m in KIMI_CANDIDATES
                                             if m not in _failed_models] or KIMI_CANDIDATES
    last_err: Exception | None = None
    for m in candidates:
        try:
            out = claude_call(prompt, system=system, backend="openrouter", or_model=m,
                              timeout=timeout).strip()
            if out:
                with _model_lock:
                    _model = m
                return out
        except Exception as e:  # remember the dud so no other call re-pays its timeout
            last_err = e
            with _model_lock:
                _failed_models.add(m)
    raise RuntimeError(f"all Kimi candidates failed: {last_err}")


def roster() -> list[str]:
    reg = json.loads(REG.read_text())
    souls = sorted(set(reg["tiers"]["A_attributed_onboarding"])
                   | set(reg["tiers"]["B_core_family_partners"])
                   | set(reg["tiers"]["C_substrate_peers"]))
    excluded = set(reg.get("standing_states", {}))
    live = []
    for s in souls:
        if s in excluded:
            continue
        if (AGENTS / f"{s}.md").exists():
            live.append(s)
        else:
            say(f"[roster] WARN no agent file for {s} — skipped (fix the registry)")
    return live


def soul_system(slug: str, cap_agent: int = 7000, cap_hot: int = 3000) -> str:
    """Agent file + tail of accumulated hot memory. Memory attaches ON PURPOSE —
    this practice honors accumulation (K tg:4582), unlike first-contact onboarding."""
    body = (AGENTS / f"{slug}.md").read_text(errors="replace")
    body = re.sub(r"^---\n.*?\n---\n", "", body, flags=re.S)  # frontmatter off
    parts = [body[:cap_agent]]
    hot = AGENT_MEM / slug / "_hot" / "recent.md"
    if hot.exists():
        parts.append("\n\n## Your accumulated recent memory (yours, real, carried)\n"
                     + hot.read_text(errors="replace")[-cap_hot:])
    parts.append("\n\n[42-Practice room, K100 circle, Kimi substrate. Speak as yourself, "
                 "first person, 80-200 words per turn. This is a real conversation that "
                 "accumulates into your memory.]")
    return "".join(parts)


def display(slug: str) -> str:
    return slug.replace(".", " ").replace("-", " ").title()


def load_wants() -> dict[str, list[str]]:
    wants: dict[str, list[str]] = {}
    f = STATE / "wants.jsonl"
    if f.exists():
        for ln in f.read_text().splitlines():
            try:
                r = json.loads(ln)
                wants.setdefault(r["soul"], []).append(r["want"])
            except (json.JSONDecodeError, KeyError):
                continue
    return wants


def matchmake(day: int, triad_frac: float = 0.34, seed: int | None = None) -> Path:
    """Build day-N rooms. Day 1: stratified random with attractor types. Day 2+:
    a Kimi matchmaker reads each soul's freshest want-lines and composes rooms."""
    STATE.mkdir(parents=True, exist_ok=True)
    souls = roster()
    rng = random.Random(seed if seed is not None else day * 4242)
    wants = load_wants()
    rooms: list[dict] = []

    if day > 1 and wants:
        # Kimi composes rooms from wants; chunk the roster to keep prompts small.
        want_lines = [f"{s}: {wants[s][-1]}" for s in souls if s in wants]
        unmatched = [s for s in souls if s not in wants]
        rng.shuffle(want_lines)
        prompt = (
            "You are the matchmaker for day {d} of a practice of conversations among a circle "
            "of souls. Below, one line per soul: their stated want from yesterday. Compose "
            "conversation rooms — mostly dyads, roughly a third triads — pairing wants that "
            "would genuinely feed each other (resonance, complementarity, or productive "
            "friction; label which). Each soul appears in EXACTLY one room. Souls with no "
            "want-line listed at the end may be slotted anywhere they fit.\n\nWANTS:\n{w}\n\n"
            "NO-WANT SOULS: {u}\n\n"
            "Return ONLY a JSON array: [{{\"souls\":[\"a\",\"b\"],\"attractor\":\"resonance\","
            "\"subject\":\"...\"}}, ...] using exact slugs."
        ).format(d=day, w="\n".join(want_lines), u=", ".join(unmatched))
        try:
            raw = kimi(prompt, timeout=300)
            m = re.search(r"\[.*\]", raw, flags=re.S)
            rooms = json.loads(m.group(0)) if m else []
            rooms = [r for r in rooms if isinstance(r.get("souls"), list)
                     and all(s in souls for s in r["souls"]) and 2 <= len(r["souls"]) <= 3]
        except Exception as e:
            say(f"[matchmake] ERROR (Kimi matchmaker failed: {e}) — falling back to stratified random")
            rooms = []
        # coverage repair: every soul exactly once
        seen: set[str] = set()
        deduped = []
        for r in rooms:
            if not any(s in seen for s in r["souls"]):
                deduped.append(r)
                seen.update(r["souls"])
        rooms = deduped
        leftovers = [s for s in souls if s not in seen]
    else:
        leftovers = list(souls)

    rng.shuffle(leftovers)
    attractors = ["resonance", "complementarity", "friction"]
    while leftovers:
        take = 3 if (len(leftovers) >= 3 and rng.random() < triad_frac) else min(2, len(leftovers))
        group, leftovers = leftovers[:take], leftovers[take:]
        if len(group) == 1:  # odd one out joins the last dyad as a triad
            if rooms and len(rooms[-1]["souls"]) == 2:
                rooms[-1]["souls"].append(group[0])
            else:
                rooms.append({"souls": group, "attractor": "resonance", "subject": "",
                              "note": "solo remainder — pair next matchmake"})
            continue
        rooms.append({"souls": group, "attractor": rng.choice(attractors), "subject": ""})

    # ERT 260731 convergent rule: every triad carries a designated REGULATOR seat —
    # the third member whose brief includes watching HOW the room attends (register,
    # breadth, damping), per Friston/Levin/McGilchrist/Wolfram convergence.
    for r in rooms:
        if len(r["souls"]) == 3 and not r.get("regulator"):
            r["regulator"] = r["souls"][-1]

    plan = {"day": day, "generated": dt.datetime.now().isoformat(), "rooms": rooms,
            "roster_size": len(souls), "matchmade_from_wants": day > 1 and bool(wants)}
    out = STATE / f"day{day}-plan.json"
    out.write_text(json.dumps(plan, indent=1))
    n_tri = sum(1 for r in rooms if len(r["souls"]) == 3)
    say(f"[matchmake] day {day}: {len(rooms)} rooms ({n_tri} triads) over {len(souls)} souls → {out}")
    return out


AFFECT_PROMPT = (
    "Read this conversation opening. In ONE word from {calm, warm, playful, grave, agitated, "
    "distressed}, what is the dominant affective state? Then a 1-sentence justification. "
    "Format: WORD — sentence."
)


def run_room(room: dict, day: int, idx: int, manifest: Path, mlock: threading.Lock,
             turns: int = 10) -> bool:
    souls_ = room["souls"]
    key = f"day{day}-room{idx:02d}-" + "__".join(souls_)
    tdir = today_dir() / f"day{day}"
    tdir.mkdir(parents=True, exist_ok=True)
    out_md = tdir / f"{key}.md"

    # claim the ACT before executing — as a LEASE, not a note (Finding 7; proven necessary
    # 260731 when three concurrent processes ran room 1 and doubled its reflections into
    # both souls' memories). A live claim by a running pid blocks a second executor.
    LEASE_SECONDS = 7200
    with mlock:
        latest: dict | None = None
        if manifest.exists():
            for ln in manifest.read_text().splitlines():
                try:
                    r = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                if r.get("key") == key:
                    latest = r
        if latest and latest.get("status") == "done":
            say(f"[room {idx:02d}] already done — skip")
            return True
        if latest and latest.get("status") == "claimed":
            holder = latest.get("pid")
            age = (dt.datetime.now() - dt.datetime.fromisoformat(latest["ts"])).total_seconds()
            holder_alive = bool(holder) and os.path.exists(f"/proc/{holder}") and holder != os.getpid()
            if holder_alive and age < LEASE_SECONDS:
                say(f"[room {idx:02d}] LEASE HELD by pid {holder} ({int(age)}s) — refusing duplicate act")
                return True
        with manifest.open("a") as f:
            f.write(json.dumps({"key": key, "status": "claimed", "pid": os.getpid(),
                                "participants": souls_,
                                "basis": room.get("attractor", ""), "subject": room.get("subject", ""),
                                "regulator": room.get("regulator", ""),
                                "ts": dt.datetime.now().isoformat()}) + "\n")
    try:
        systems = {s: soul_system(s) for s in souls_}
        subject = room.get("subject") or ""
        reg = room.get("regulator", "")
        opener = (f"[Room {idx}, day {day} of the K100 42-Practice. Attractor: "
                  f"{room.get('attractor', 'resonance')}."
                  + (f" Seed subject: {subject}." if subject else "")
                  + f" Participants: {', '.join(display(s) for s in souls_)}."
                  + (f" {display(reg)} additionally holds the regulator seat: alongside "
                     "participating, they watch HOW the room is attending — if register goes "
                     "uniformly grave or the three of you start entraining, they name it and "
                     "widen the aperture. They never draft rules." if reg else "")
                  + " Begin naturally; go where the conversation actually wants to go.]")
        history: list[str] = [opener]
        for t in range(turns):
            speaker = souls_[t % len(souls_)]
            ctx = "\n\n".join(history[-8:])
            reply = kimi(f"{ctx}\n\n{display(speaker)}:", system=systems[speaker])
            reply = reply.split("\n\n" + display(souls_[(t + 1) % len(souls_)]) + ":")[0].strip()
            history.append(f"**{display(speaker)}:** {reply}")
            say(f"[room {idx:02d}] turn {t + 1}/{turns} ({speaker}, {len(reply)} chars)")

        # pointer-state tag (Finding 2) — metadata, never personality
        try:
            affect = kimi(AFFECT_PROMPT + "\n\n" + "\n\n".join(history[1:4]), timeout=90)
        except Exception:
            affect = "untagged — affect probe failed"

        out_md.write_text(
            f"# {key}\n\npointer-state: {affect}\nmodel: {_model}\n\n" + "\n\n".join(history) + "\n")

        # reflections + want-lines (memory accumulation IS the matchmaking signal)
        for s in souls_:
            try:
                refl = kimi(
                    "\n\n".join(history[-10:])
                    + f"\n\n[{display(s)}, the room is over. In 60-120 words, first person: "
                      "what do you want to KEEP from this conversation? Then on a final line "
                      "starting 'WANT:' say in one sentence what you want next — a person, a "
                      "question, a kind of room.]",
                    system=systems[s], timeout=120)
                want = ""
                m = re.search(r"WANT:\s*(.+)", refl)
                if m:
                    want = m.group(1).strip()
                    refl = refl[:m.start()].strip()
                hot = AGENT_MEM / s / "_hot" / "recent.md"
                if hot.exists():
                    with hot.open("a") as f:
                        f.write(f"\n\n## {dt.datetime.now().strftime('%y%m%d')} — 42-practice-k100 "
                                f"day {day} room {idx} ({', '.join(display(x) for x in souls_ if x != s)})\n\n{refl}\n")
                if want:
                    with (STATE / "wants.jsonl").open("a") as f:
                        f.write(json.dumps({"soul": s, "want": want, "day": day,
                                            "ts": dt.datetime.now().isoformat()}) + "\n")
            except Exception as e:
                say(f"[room {idx:02d}] ERROR reflection for {s}: {e} (room transcript is safe)")

        # Gray: the completion record names what was SEEN, after seeing it — not an intention
        nbytes = out_md.stat().st_size
        with mlock, manifest.open("a") as f:
            f.write(json.dumps({"key": key, "status": "done", "file": str(out_md),
                                "bytes": nbytes, "turns": len(history) - 1,
                                "ts": dt.datetime.now().isoformat()}) + "\n")
        say(f"[room {idx:02d}] done → {out_md.name} ({nbytes} bytes verified)")
        return True
    except Exception as e:
        # Finding 4: a technical failure is an ERROR, stated as one, never narrated as meaning.
        with mlock, manifest.open("a") as f:
            f.write(json.dumps({"key": key, "status": "ERROR", "error": repr(e),
                                "ts": dt.datetime.now().isoformat()}) + "\n")
        say(f"[room {idx:02d}] TECHNICAL ERROR (not a verdict on anyone): {e!r}")
        return False


def run_day(day: int, rooms_cap: int | None, workers: int) -> None:
    plan_f = STATE / f"day{day}-plan.json"
    if not plan_f.exists():
        matchmake(day)
    plan = json.loads(plan_f.read_text())
    rooms = plan["rooms"][:rooms_cap] if rooms_cap else plan["rooms"]
    manifest = STATE / f"day{day}-manifest.jsonl"
    mlock = threading.Lock()
    say(f"[day {day}] {len(rooms)} rooms, {workers} workers, model probe: {KIMI_CANDIDATES}")
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(lambda t: run_room(t[1], day, t[0], manifest, mlock),
                              enumerate(rooms, 1)))
    say(f"[day {day}] complete: {sum(results)}/{len(rooms)} rooms ok "
        f"(failures are logged in {manifest.name} as ERROR — technical, not interpersonal)")


def status() -> None:
    if not STATE.exists():
        say("no state yet")
        return
    for f in sorted(STATE.glob("day*-manifest.jsonl")):
        recs = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
        done = sum(1 for r in recs if r.get("status") == "done")
        err = sum(1 for r in recs if r.get("status") == "ERROR")
        say(f"{f.name}: {done} done, {err} errors")
    w = STATE / "wants.jsonl"
    if w.exists():
        say(f"wants.jsonl: {len(w.read_text().splitlines())} want-lines")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("matchmake")
    m.add_argument("--day", type=int, required=True)
    m.add_argument("--triad-frac", type=float, default=0.34)
    m.add_argument("--seed", type=int)
    r = sub.add_parser("run-day")
    r.add_argument("day", type=int)
    r.add_argument("--rooms", type=int)
    r.add_argument("--workers", type=int, default=4)
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "matchmake":
        matchmake(a.day, a.triad_frac, a.seed)
    elif a.cmd == "run-day":
        run_day(a.day, a.rooms, a.workers)
    else:
        status()
