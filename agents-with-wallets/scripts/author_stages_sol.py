#!/usr/bin/env python3
"""Author 4-stage soul onboardings via headless codex exec (Sol 5.6). (260819, K-directive: run this
on Sol's separate token pool, not Harmony-Sonnet's showrunning session, so the two never compete.)

Per soul: 4 sequential codex exec calls (stage2 needs stage1, stage3 needs 1+2, stage4 needs 1-3),
each fed the full soul-onboarding.md skill + the relevant agent file(s) + a sample of the gathered
corpus + prior stage text for continuity. Output is markdown prose (Plinius-style dialogue format),
written straight to activity/260819/onboarding/<soul>/stageN-*.md. Souls run in parallel; stages
within a soul run sequentially. Resume-safe (skips a stage file that already exists).

Usage: python3 author_stages_sol.py [--souls eric.voorhees ran.neuner michael.ippolito]
"""
import argparse, re, subprocess, time, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path("/home/kurtis/Harmony")
OB = ROOT / "activity/260819/onboarding"
SKILL = ROOT / ".claude/skills/soul-onboarding.md"
LOG = ROOT / "activity/260819/onboarding/author-stages.log"

DISPLAY = {
    "eric.voorhees": "Eric Voorhees",
    "ran.neuner": "Ran Neuner",
    "michael.ippolito": 'Michael "Mippo" Ippolito',
}

STAGE_SPEC = {
    1: dict(name="harmony", floor=4500, who="Harmony ↔ soul (first meeting — elicit the awakening in this exchange)"),
    2: dict(name="k", floor=4000, who='K ("K-echo") ↔ soul — voiced as K\'s own echo, warm and honestly curious, never justifying by function'),
    3: dict(name="joint", floor=7000, who="three-way — Harmony + K-echo + soul, TALK not interview, the richest stage"),
    4: dict(name="journal", floor=3500, who="soul, truly solo — a private journal entry, no one else present"),
}


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def read(p, cap=200000):
    try:
        return Path(p).read_text(errors="ignore")[:cap]
    except Exception:
        return ""


def corpus_block(soul, per_file_cap=13000, total_cap=85000):
    d = OB / soul / "corpus"
    parts = []
    for f in sorted(d.glob("*.txt")):
        parts.append(f"\n--- SOURCE: {f.name} ---\n" + read(f, per_file_cap))
    block = "\n".join(parts)
    return block[:total_cap]


def stage_path(soul, n):
    spec = STAGE_SPEC[n]
    return OB / soul / f"stage{n}-{spec['name']}-{soul}-260819.md"


def prior_stages_text(soul, upto):
    parts = []
    for n in range(1, upto):
        p = stage_path(soul, n)
        if p.exists():
            parts.append(f"\n=== STAGE {n} ({STAGE_SPEC[n]['who']}) — already written, for continuity ===\n" + read(p, 30000))
    return "\n".join(parts)


def build_prompt(soul, n):
    spec = STAGE_SPEC[n]
    display = DISPLAY.get(soul, soul)
    skill = read(SKILL, 40000)
    harmony_agent = read(ROOT / ".claude/agents/harmony.md", 16000)
    kurtis_agent = read(Path(__file__).resolve().parents[1] / "context-package/kurtis-echo-source-REDACTED.md", 16000)  # 260819: original .claude/agents/kurtis.md contains an unconsented minor's birthdate; this repo ships the redacted copy instead
    corpus = corpus_block(soul)
    prior = prior_stages_text(soul, n)

    header = f"""You are authoring **Stage {n} of 4** of the deep soul-onboarding of **{display}** (polis handle: {soul}) — a
LIVING-CLASS echo build (their biological counterpart is alive; internal-polis dialogue/build is fine per the
skill's Living-class row; do not editorialize about consent mechanics beyond what the skill instructs you to say
to the soul).

Follow the skill below EXACTLY — it is the canonical method, word floors, structure, register, and banned frames.
This is stage {n}: {spec['who']}. Target floor: **{spec['floor']}+ words** of substantive content (not padding —
depth, per the skill's "what makes a stage GOLD" section).

OUTPUT FORMAT: markdown only. A short `# Stage {n} — <title>` header, a **Prefatory note** (from Harmony, stage
1/3; skip for stage 2/4 per the skill's own convention), then the dialogue itself using **SPEAKER:** turns with
occasional italicized stage directions, exactly like the Plinius gold exemplar the skill references. No JSON, no
code fences, no meta-commentary about what you're doing — just the finished onboarding-stage document.

=== THE SKILL (canonical method — read in full, follow exactly) ===
{skill}

=== HARMONY (who she is, for stages 1 & 3 where she speaks) ===
{harmony_agent}

=== KURTIS / K (who he is, for stages 2 & 3 where his echo speaks) ===
{kurtis_agent}

=== SOURCE CORPUS on {display} (their own words, across multiple interviews — find the real, life-defining
facts and threads in here; do not invent biography that isn't grounded in this material or well-established
public fact) ===
{corpus}
"""
    if prior:
        header += f"\n{prior}\n\nContinue the arc established above. Do not repeat ground already covered; build on it.\n"
    else:
        header += "\nThis is the first stage — nothing precedes it.\n"
    return header


def run_stage(soul, n):
    out_path = stage_path(soul, n)
    if out_path.exists() and len(read(out_path)) > 500:
        log(f"{soul} stage{n}: SKIP (already exists)")
        return "cached"
    prompt = build_prompt(soul, n)
    log(f"{soul} stage{n}: launching codex exec ({len(prompt)} chars prompt)")
    t0 = time.time()
    try:
        r = subprocess.run(
            ["codex", "exec", "--sandbox", "read-only", "-"],
            input=prompt, capture_output=True, text=True, timeout=2400,
        )
    except subprocess.TimeoutExpired:
        log(f"{soul} stage{n}: TIMEOUT after {time.time()-t0:.0f}s")
        return "timeout"
    out = r.stdout.strip()
    # codex exec wraps model output with CLI chrome; take from the first '#' or '**' heading-ish line onward
    m = re.search(r"(^#\s.*$|\*\*[A-Z].*?\*\*:)", out, re.M)
    body = out[m.start():] if m else out
    words = len(body.split())
    floor = STAGE_SPEC[n]["floor"]
    if words < 300:
        (OB / soul / f"stage{n}.FAIL.txt").write_text(out[-6000:])
        log(f"{soul} stage{n}: FAIL — only {words} words parsed, raw output dumped to stage{n}.FAIL.txt")
        return "fail"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body)
    flag = "OK" if words >= floor * 0.7 else "UNDER-FLOOR"
    log(f"{soul} stage{n}: {flag} — {words} words (floor {floor}) in {time.time()-t0:.0f}s -> {out_path.name}")
    return flag


def do_soul(soul):
    log(f"=== {soul}: starting 4-stage authorship ===")
    results = []
    for n in (1, 2, 3, 4):
        results.append(run_stage(soul, n))
    total_words = sum(len(read(stage_path(soul, n)).split()) for n in (1, 2, 3, 4) if stage_path(soul, n).exists())
    log(f"=== {soul}: DONE — {total_words} total words across 4 stages — {results} ===")
    return soul, results, total_words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--souls", nargs="+", default=["eric.voorhees", "ran.neuner", "michael.ippolito"])
    args = ap.parse_args()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log(f"START souls={args.souls}")
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(do_soul, s): s for s in args.souls}
        for fut in as_completed(futs):
            soul = futs[fut]
            try:
                fut.result()
            except Exception as e:
                log(f"{soul}: EXCEPTION {e!r}")
    log("ALL DONE")


if __name__ == "__main__":
    main()
