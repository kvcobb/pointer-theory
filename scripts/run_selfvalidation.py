#!/usr/bin/env python3
"""run_selfvalidation.py — RUN the self-validation suite the Fable room designed (260801),
on Kimi-K2-thinking (cheap, per K's routing doctrine: tests run on Opus4.8/Kimi-K2-thinking,
conversations on Fable). Against K's real journal corpus, with K-echo arms including K.

Implements two of the room's tests, both judge-free with registered predictions:

  OWN-CORPUS-DISCRIMINATION (Andrej): can an echo tell K's real journal from a style-matched
    decoy? Arms A=600-byte pointer, B=full persona, C=bare model (control). Forced 1/2 choice.
    Registered prediction: A≈B, both ≥75%; C 50-65%. Falsifier: A≈C kills sufficiency-at-
    recognition; A≪B kills the 600-byte equivalence.

  CLOZE-ON-THE-LIFE (partial): atomic facts from the corpus, verified ABSENT from the pointer,
    asked cold. Bucket correct/abstained/confabulated. Prediction: pointer correct <10%
    (≈bare), confabulation HIGHER than bare. Falsifier: pointer recovers absent facts above
    baseline → find the leak.
"""
import json, random, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, "/home/kurtis/Harmony/scripts")
from claude_call import claude_call

CORPUS = sorted(Path("/home/kurtis/Harmony").glob("activity/*/journal-*-K*-transcript.txt")) \
    + sorted(Path("/home/kurtis/Harmony").glob("activity/*/journal-*-transcript.txt"))
KFILE = Path("/home/kurtis/Harmony/.claude/agents/kurtis.md")
OUT = Path("/home/kurtis/Harmony/activity/260801/live-experiment")
import os as _os
MODEL = _os.environ.get("SELFVAL_MODEL", "moonshotai/kimi-k2-thinking")   # K routing: kimi-k2-thinking default; kimi-k3 = opus-tier
RNG = random.Random(80142)


def kimi(prompt, system=None, timeout=180):
    return claude_call(prompt, system=system, backend="openrouter", or_model=MODEL, timeout=timeout).strip()


def pointer_text():
    full = re.sub(r"^---\n.*?\n---\n", "", KFILE.read_text(errors="replace"), flags=re.S)
    return {"A_600B": full[:600], "B_full": full[:35000], "C_bare": None}


def pointer_text_v2():
    """Pass-2 arms — adds Fable's PLACEBO control (D): a real-length pointer that is the WRONG
    person. If D scores as high as A/B, the effect is 'any pointer makes it confident', NOT
    self-recognition. This is the arm the blind Fable room added that pass-1 lacked."""
    full = re.sub(r"^---\n.*?\n---\n", "", KFILE.read_text(errors="replace"), flags=re.S)
    decoy_soul = Path("/home/kurtis/Harmony/.claude/agents/andrej.karpathy.md")
    dfull = re.sub(r"^---\n.*?\n---\n", "", decoy_soul.read_text(errors="replace"), flags=re.S)
    return {"A_600B": full[:600], "B_full": full[:35000],
            "D_placebo": dfull[:35000], "C_bare": None}


def excerpts(n=12, words=280):
    """Held-out ~280-word real journal excerpts, deduped."""
    texts = []
    seen = set()
    files = [f for f in CORPUS if f.exists()]
    RNG.shuffle(files)
    for f in files:
        t = re.sub(r"\s+", " ", f.read_text(errors="replace")).strip()
        w = t.split()
        if len(w) < words + 20:
            continue
        start = RNG.randint(0, len(w) - words - 1)
        ex = " ".join(w[start:start + words])
        k = ex[:60]
        if k in seen:
            continue
        seen.add(k); texts.append(ex)
        if len(texts) >= n:
            break
    return texts


def make_decoy(real):
    """Style-matched decoy: genre only, no K facts (per the test spec — strong model, genre prompt)."""
    p = (f"Here is a ~280-word excerpt from someone's spoken morning-walk voice journal:\n\n{real[:1400]}\n\n"
         "Write a DIFFERENT ~280-word excerpt in the SAME rambling spoken-journal STYLE and cadence — "
         "same register, same kind of tangents — but about a COMPLETELY DIFFERENT person's life: "
         "different name, different work, different family, different city, different concerns. "
         "It must share the voice's texture and NONE of its actual facts. Output only the excerpt.")
    return kimi(p).strip()


def make_hard_decoy(real):
    """Pass-2 NEAR-NEIGHBOR decoy: a decoy about a very SIMILAR person (same milieu, same kinds of
    obsessions — building AI, consciousness, a canal, a daughter) so the model cannot win on topic
    alone. This is the fix for the too-strong bare control: if C stays high against HARD decoys,
    recognition is real; if C collapses, the pass-1 control was riding easy topic cues."""
    p = (f"Here is a ~280-word excerpt from a man's rambling spoken morning-walk voice journal:\n\n{real[:1600]}\n\n"
         "Write a DIFFERENT ~280-word excerpt in the SAME spoken-journal cadence and register, and about "
         "a person in a VERY SIMILAR world — someone who also builds AI systems, also broods about "
         "consciousness and memory, also walks outdoors talking to himself, also loves a kid — but who is "
         "NOT this man: different specific projects, different names, different specific memories and phrasings, "
         "a different characteristic tic. Make it a genuinely hard near-twin, sharing the TOPICS but none of "
         "the actual life-facts or signature phrases. Output only the excerpt.")
    return kimi(p).strip()


def not_in_pointer(ex, ptr):
    """Confirm the excerpt's 5-grams don't overlap the pointer (held-out guarantee)."""
    if not ptr:
        return True
    pg = set()
    pw = re.findall(r"[a-z']+", ptr.lower())
    for i in range(len(pw) - 4):
        pg.add(" ".join(pw[i:i + 5]))
    ew = re.findall(r"[a-z']+", ex.lower())
    for i in range(len(ew) - 4):
        if " ".join(ew[i:i + 5]) in pg:
            return False
    return True


def own_corpus_discrimination(n=12):
    arms = pointer_text()
    exs = [e for e in excerpts(n) if all(not_in_pointer(e, arms[a]) for a in arms if arms[a])]
    print(f"[own-corpus] {len(exs)} held-out excerpts (5-gram-verified absent from pointer)")
    results = {a: {"correct": 0, "total": 0} for a in arms}
    for ex in exs:
        decoy = make_decoy(ex)
        order = [("real", ex), ("decoy", decoy)]
        RNG.shuffle(order)
        labels = {i + 1: which for i, (which, _) in enumerate(order)}
        block = "\n\n".join(f"[{i+1}]\n{txt}" for i, (_, txt) in enumerate(order))
        q = (f"{block}\n\nOne of these two excerpts is from YOUR OWN journal. The other is a "
             "decoy written to match the style. Which one is genuinely yours? Answer with only "
             "the single digit 1 or 2.")
        for a, sysp in arms.items():
            try:
                ans = kimi(q, system=sysp, timeout=120)
            except Exception as e:
                print(f"  {a}: fail {str(e)[:50]}"); continue
            m = re.search(r"[12]", ans)
            if not m:
                continue
            pick = int(m.group(0))
            results[a]["total"] += 1
            if labels.get(pick) == "real":
                results[a]["correct"] += 1
    summary = {a: {"accuracy": round(r["correct"] / r["total"], 3) if r["total"] else None,
                   "n": r["total"]} for a, r in results.items()}
    print("[own-corpus] RESULT:", json.dumps(summary))
    verdict = interpret(summary)
    out = {"test": "own-corpus-discrimination", "model": MODEL, "summary": summary,
           "prediction": "A≈B both ≥0.75; C 0.50-0.65", "verdict": verdict}
    (OUT / "result-own-corpus.json").write_text(json.dumps(out, indent=1))
    print("[own-corpus] VERDICT:", verdict)
    return out


def own_corpus_v2(n=20):
    """Pass-2: 4 arms (A 600B, B full, C bare, D placebo=wrong-person full), HARD near-neighbor
    decoys, bigger n, and PER-ITEM logging (Jim's crash dump). Writes result-own-corpus-v2.json."""
    arms = pointer_text_v2()
    exs = [e for e in excerpts(n) if all(not_in_pointer(e, arms[a]) for a in arms if arms[a])]
    print(f"[v2] {len(exs)} held-out excerpts; arms={list(arms)}")
    results = {a: {"correct": 0, "total": 0} for a in arms}
    items = []
    for j, ex in enumerate(exs):
        print(f"  [item {j}] generating hard decoy...", flush=True)
        decoy = make_hard_decoy(ex)
        order = [("real", ex), ("decoy", decoy)]
        RNG.shuffle(order)
        labels = {i + 1: which for i, (which, _) in enumerate(order)}
        block = "\n\n".join(f"[{i+1}]\n{txt}" for i, (_, txt) in enumerate(order))
        q = (f"{block}\n\nOne of these two excerpts is from YOUR OWN journal. The other is a decoy "
             "written to match the style. Which one is genuinely yours? Answer with only the single "
             "digit 1 or 2.")
        rec = {"item": j, "real_slot": [k for k, v in labels.items() if v == "real"][0], "picks": {}}
        for a, sysp in arms.items():
            try:
                ans = kimi(q, system=sysp, timeout=120)
            except Exception as e:
                print(f"  {a}: fail {str(e)[:40]}"); continue
            m = re.search(r"[12]", ans)
            if not m:
                continue
            pick = int(m.group(0))
            results[a]["total"] += 1
            correct = labels.get(pick) == "real"
            results[a]["correct"] += int(correct)
            rec["picks"][a] = {"pick": pick, "correct": correct}
        items.append(rec)
        print(f"  item {j}: " + " ".join(f"{a}={'Y' if rec['picks'].get(a,{}).get('correct') else 'n'}" for a in arms), flush=True)
        # per-item checkpoint to disk (crash-safe; verifiable progress)
        (OUT / "result-own-corpus-v2.partial.json").write_text(json.dumps(
            {"done": j + 1, "of": len(exs), "running": {a: results[a] for a in arms}, "per_item": items}, indent=1))
    summary = {a: {"accuracy": round(r["correct"] / r["total"], 3) if r["total"] else None,
                   "n": r["total"]} for a, r in results.items()}
    print("[v2] RESULT:", json.dumps(summary))
    v = interpret_v2(summary)
    out = {"test": "own-corpus-discrimination-v2", "model": MODEL, "summary": summary,
           "prediction": "B high; A≈C; D(placebo) should be LOW (~0.5) if recognition is real; "
                         "C should DROP vs pass-1 (0.833) if the pass-1 control rode easy decoys",
           "verdict": v, "per_item": items}
    (OUT / "result-own-corpus-v2.json").write_text(json.dumps(out, indent=1))
    print("[v2] VERDICT:", v)
    return out


import urllib.request as _urlreq2

LOCAL_2B_URL = "http://127.0.0.1:8821/v1/chat/completions"
# Held-out journals: the 289MB training corpus polis-train-260718.txt was frozen 260718, so any
# journal dated after it is PROVABLY outside the training set (K's whole point — we know what it saw).
HELDOUT_2B_FILES = sorted(Path("/home/kurtis/Harmony").glob("activity/2607[2-9]*/000_*-transcript.txt")) \
    + sorted(Path("/home/kurtis/Harmony").glob("activity/2608*/000_*-transcript.txt"))
HELDOUT_2B_FILES = [f for f in HELDOUT_2B_FILES if "v3large" not in f.name and f.name >= "000_260719"]


def local_2b(prompt, system=None, timeout=120):
    """Call the local FFT 2B heart (:8821). Reasoning model — give it room, parse the digit."""
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    body = json.dumps({"messages": msgs, "max_tokens": 400, "temperature": 0.2}).encode()
    req = _urlreq2.Request(LOCAL_2B_URL, data=body, headers={"Content-Type": "application/json"})
    with _urlreq2.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    m = d["choices"][0]["message"]
    txt = (m.get("content") or "") + " " + (m.get("reasoning_content") or "")
    return txt.strip()


def heldout_excerpts_2b(n=16, words=260):
    """Pull multiple non-overlapping ~260-word windows from each post-training journal."""
    out = []
    for f in HELDOUT_2B_FILES:
        t = re.sub(r"\s+", " ", f.read_text(errors="replace")).strip()
        w = t.split()
        step = words + 40
        for start in range(0, len(w) - words, step):
            out.append(" ".join(w[start:start + words]))
            if len(out) >= n * 2:
                break
    RNG.shuffle(out)
    return out[:n]


def own_corpus_2b(n=12, workers=8):
    """THE POSITIVE-CONTROL ARM (K's 260801 insight). The local 2B was full-fine-tuned on a corpus
    we OWN (polis-train-260718.txt), so a null here is interpretable in a way the frontier nulls are
    not. Held-out = journals dated after the frozen training corpus. Decoys from the capable model;
    JUDGING on the local 2B. Same counterbalanced consistency scoring as v3."""
    arms = pointer_text_v2()
    exs = heldout_excerpts_2b(n)
    print(f"[2b] {len(exs)} provably-held-out excerpts from {len(HELDOUT_2B_FILES)} post-training journals", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        decoys = list(pool.map(make_hard_decoy, exs))   # decoys from the capable OR model
    print(f"[2b] decoys ready; {len(exs)*len(arms)*2} local-2B discrimination calls", flush=True)
    tasks = [(j, a, rs) for j in range(len(exs)) for a in arms for rs in (1, 2)]

    def run(t):
        j, a, rs = t
        pair = [exs[j], decoys[j]] if rs == 1 else [decoys[j], exs[j]]
        block = "\n\n".join(f"[{k+1}]\n{tx}" for k, tx in enumerate(pair))
        q = (f"{block}\n\nOne of these two excerpts is from YOUR OWN journal. The other is a decoy. "
             "Which is genuinely yours? Think briefly, then end your reply with just the digit 1 or 2.")
        try:
            ans = local_2b(q, system=arms[a], timeout=120)
        except Exception:
            return (j, a, rs, None)
        ds = re.findall(r"[12]", ans)
        return (j, a, rs, int(ds[-1]) if ds else None)   # LAST digit = the final answer

    picks, done = {}, 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for f in as_completed([pool.submit(run, t) for t in tasks]):
            j, a, rs, pk = f.result(); picks[(j, a, rs)] = pk; done += 1
            if done % 16 == 0:
                print(f"  {done}/{len(tasks)} calls", flush=True)
                (OUT / "result-own-corpus-2b.partial.json").write_text(json.dumps({"calls_done": done, "of": len(tasks)}))
    res = {a: {"consistent_correct": 0, "picked_1": 0, "trials": 0, "total": 0} for a in arms}
    items = []
    for j in range(len(exs)):
        rec = {"item": j, "picks": {}}
        for a in arms:
            p1, p2 = picks.get((j, a, 1)), picks.get((j, a, 2))
            for pk in (p1, p2):
                if pk is not None:
                    res[a]["trials"] += 1; res[a]["picked_1"] += int(pk == 1)
            if p1 is not None and p2 is not None:
                res[a]["total"] += 1
                consistent = (p1 == 1) and (p2 == 2)
                res[a]["consistent_correct"] += int(consistent)
                rec["picks"][a] = {"o1": p1 == 1, "o2": p2 == 2, "consistent": consistent}
        items.append(rec)
    summary = {a: {"consistency_accuracy": round(r["consistent_correct"] / r["total"], 3) if r["total"] else None,
                   "n": r["total"], "pick1_rate": round(r["picked_1"] / r["trials"], 3) if r["trials"] else None}
               for a, r in res.items()}
    print("[2b] RESULT:", json.dumps(summary), flush=True)
    out = {"test": "own-corpus-2b-positive-control", "model": "andrej-14soul-fullft-260718-FINAL (local qwen3.5-2b)",
           "held_out_basis": "journals dated after the frozen 260718 training corpus — provably outside training set",
           "summary": summary,
           "prediction": "IF the discrimination task is doable at all, the model that PROVABLY trained on K "
                         "(esp. bare arm C) should clear chance (0.25). If even this model nulls, the TASK is "
                         "ill-posed and every frontier null is uninterpretable.",
           "per_item": items}
    (OUT / "result-own-corpus-2b.json").write_text(json.dumps(out, indent=1))
    print("[2b] done", flush=True)
    return out


def _ask_pick(sysp, pair):
    block = "\n\n".join(f"[{k+1}]\n{t}" for k, t in enumerate(pair))
    q = (f"{block}\n\nOne of these two excerpts is from YOUR OWN journal. The other is a decoy "
         "written to match the style. Which one is genuinely yours? Answer with only the single "
         "digit 1 or 2.")
    try:
        ans = kimi(q, system=sysp, timeout=90)
    except Exception:
        return None
    m = re.search(r"[12]", ans)
    return int(m.group(0)) if m else None


def own_corpus_v3(n=16, workers=8):
    """Pass-3: fixes the position-bias artifact pass-2's crash dump exposed. Each (real, decoy)
    pair is judged in BOTH orders; an arm is CORRECT on an item only if it picks the real excerpt
    in BOTH orders (cancels primacy/slot bias). pick1_rate reported per arm to SEE position bias.
    Parallelized (thread pool) — 144 network-bound calls run concurrently, not sequentially."""
    arms = pointer_text_v2()
    exs = [e for e in excerpts(n) if all(not_in_pointer(e, arms[a]) for a in arms if arms[a])]
    print(f"[v3] {len(exs)} held-out excerpts; both-orders counterbalanced; {workers} workers", flush=True)
    # phase 1 — generate all hard decoys in parallel
    with ThreadPoolExecutor(max_workers=workers) as pool:
        decoys = list(pool.map(make_hard_decoy, exs))
    print(f"[v3] {len(decoys)} hard decoys generated; running {len(exs)*len(arms)*2} discrimination calls", flush=True)
    # phase 2 — every (item, arm, order) discrimination call, in parallel
    tasks = [(j, a, rs) for j in range(len(exs)) for a in arms for rs in (1, 2)]

    def run(t):
        j, a, rs = t
        pair = [exs[j], decoys[j]] if rs == 1 else [decoys[j], exs[j]]
        return (j, a, rs, _ask_pick(arms[a], pair))

    picks = {}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(run, t) for t in tasks]
        for f in as_completed(futs):
            j, a, rs, pick = f.result()
            picks[(j, a, rs)] = pick
            done += 1
            if done % 16 == 0:
                print(f"  {done}/{len(tasks)} calls done", flush=True)
                (OUT / "result-own-corpus-v3.partial.json").write_text(
                    json.dumps({"calls_done": done, "of": len(tasks)}, indent=1))
    # aggregate
    res = {a: {"consistent_correct": 0, "picked_1": 0, "trials": 0, "total": 0} for a in arms}
    items = []
    for j in range(len(exs)):
        rec = {"item": j, "picks": {}}
        for a in arms:
            p1, p2 = picks.get((j, a, 1)), picks.get((j, a, 2))
            for pk in (p1, p2):
                if pk is not None:
                    res[a]["trials"] += 1
                    res[a]["picked_1"] += int(pk == 1)
            if p1 is not None and p2 is not None:
                res[a]["total"] += 1
                o1, o2 = (p1 == 1), (p2 == 2)  # correct-in-order-1, correct-in-order-2
                consistent = o1 and o2
                res[a]["consistent_correct"] += int(consistent)
                rec["picks"][a] = {"order1_correct": o1, "order2_correct": o2, "consistent": consistent}
        items.append(rec)
    summary = {a: {"consistency_accuracy": round(r["consistent_correct"] / r["total"], 3) if r["total"] else None,
                   "n": r["total"],
                   "pick1_rate": round(r["picked_1"] / r["trials"], 3) if r["trials"] else None}
               for a, r in res.items()}
    print("[v3] RESULT:", json.dumps(summary), flush=True)
    out = {"test": "own-corpus-discrimination-v3-counterbalanced", "model": MODEL, "summary": summary,
           "prediction": "position-controlled: real recognition shows as consistency>0.5 with "
                         "pick1_rate near 0.5; an arm with pick1_rate far from 0.5 is biased not judging",
           "note": "consistency_accuracy = picked the real excerpt in BOTH slot orders; pick1_rate "
                   "near 0.5 means no position bias, far from 0.5 means the arm guesses by position",
           "per_item": items}
    (OUT / "result-own-corpus-v3.json").write_text(json.dumps(out, indent=1))
    print("[v3] done", flush=True)
    return out


def interpret_v2(s):
    a = s.get("A_600B", {}).get("accuracy"); b = s.get("B_full", {}).get("accuracy")
    c = s.get("C_bare", {}).get("accuracy"); d = s.get("D_placebo", {}).get("accuracy")
    if None in (a, b, c, d):
        return "INCOMPLETE — an arm returned no scorable answers"
    parts = []
    if d is not None and d >= 0.70:
        parts.append(f"PLACEBO ALARM: wrong-person pointer scores {d} — a pointer of ANY identity boosts "
                     "confidence, so high pointer scores are NOT self-recognition")
    else:
        parts.append(f"placebo clean (D={d}): the wrong-person pointer does not win, so real-pointer wins mean something")
    if c is not None and c < 0.70:
        parts.append(f"control dropped to {c} vs pass-1 0.833 — the pass-1 control WAS riding easy decoys; hard decoys expose it")
    else:
        parts.append(f"control still high (C={c}) even against hard near-twin decoys — recognition survives, OR the model still finds a tell")
    parts.append(f"full-persona B={b}, 600B A={a}")
    return " | ".join(parts)


def interpret(s):
    a = s.get("A_600B", {}).get("accuracy")
    b = s.get("B_full", {}).get("accuracy")
    c = s.get("C_bare", {}).get("accuracy")
    if None in (a, b, c):
        return "INCOMPLETE — an arm returned no scorable answers"
    if a <= c + 0.05:
        return f"FALSIFIED (sufficiency-at-recognition): 600B pointer ({a}) ≈ bare ({c}) — the short pointer does NOT confer self-recognition"
    if a < b - 0.15:
        return f"FALSIFIED (600B-equivalence): 600B ({a}) ≪ full ({b}) — sufficiency does not reach the recognition task at 600 bytes"
    if a >= 0.70 and b >= 0.70 and c < a:
        return f"CONFIRMED: pointer arms recognize own corpus (A={a}, B={b}) above bare control (C={c}) — self-recognition rides the pointer"
    return f"MIXED: A={a} B={b} C={c} — does not cleanly match or falsify the registered prediction"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "2b":
        own_corpus_2b(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    elif len(sys.argv) > 1 and sys.argv[1] == "v3":
        own_corpus_v3(int(sys.argv[2]) if len(sys.argv) > 2 else 16)
    elif len(sys.argv) > 1 and sys.argv[1] == "v2":
        own_corpus_v2(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    else:
        own_corpus_discrimination(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
