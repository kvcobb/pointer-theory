#!/usr/bin/env python3
"""4-way ERT conversation generator (260819) — Kurtis-echo + Ran Neuner + Mippo + Eric Voorhees.
Runs the SAME prompt on two substrates for comparison: Sol 5.6 (headless codex exec) and
Qwen3.8-27B (via OpenRouter, scripts/or_call_ledgered.py). Target ~10k tokens of dynamic multi-turn
conversation. Output: JSON turns array to activity/260819/conversation/<substrate>/turns.json +
a readable transcript.md.

Usage: python3 generate_4way_conversation.py --substrate sol
       python3 generate_4way_conversation.py --substrate qwen
"""
import argparse, json, re, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path("/home/kurtis/Harmony")
OB = ROOT / "activity/260819/onboarding"
OUT = ROOT / "activity/260819/conversation"


def read(p, cap=200000):
    try:
        return Path(p).read_text(errors="ignore")[:cap]
    except Exception:
        return ""


def build_prompt():
    kurtis = read(Path(__file__).resolve().parents[1] / "context-package/kurtis-echo-source-REDACTED.md", 16000)  # 260819: original .claude/agents/kurtis.md contains an unconsented minor's birthdate; this repo ships the redacted copy instead
    twitter = read(OB / "TWITTER-CONTEXT.md", 20000)

    ran_voice = read(OB / "ran.neuner/stage1-harmony-ran.neuner-260819.md", 16000) + "\n" + read(OB / "ran.neuner/stage4-journal-ran.neuner-260819.md", 12000)
    eric_voice = read(OB / "eric.voorhees/stage1-harmony-eric.voorhees-260819.md", 16000) + "\n" + read(OB / "eric.voorhees/stage4-journal-eric.voorhees-260819.md", 12000)
    mippo_voice = read(OB / "michael.ippolito/stage1-harmony-michael.ippolito-260819.md", 16000) + "\n" + read(OB / "michael.ippolito/stage4-journal-michael.ippolito-260819.md", 12000)

    ran_anchor = read(OB / "ran.neuner/corpus/It's_time_to_be_honest_about_Crypto…_yts.txt", 18000)
    ran_cf = None
    for f in (OB / "ran.neuner/corpus").glob("*.txt"):
        pass  # anchor identified by agent brief already in CORPUS-SUMMARY; fall back to broad grab below
    ran_summary = read(OB / "ran.neuner/corpus/CORPUS-SUMMARY.md", 6000)
    eric_keynote = read(OB / "eric.voorhees/corpus/Crypto_Why_are_we_here_Erik_Voorhees_Keynote_Permissionless_II_yts.txt", 22000)
    mippo_reg = read(OB / "michael.ippolito/corpus/Blockworks_Acquires_Messari_yts.txt", 22000)

    prompt = f"""You are generating a single ~10,000-token ROUND-TABLE conversation among FOUR participants:

- **K-ECHO** — Kurtis Cobb's own AI echo (his real voice/file below). Host and instigator — this is his idea, his
  tweets, his frustration that kicked this off.
- **RAN** — Ran Neuner's echo (Crypto Banter). Broadcaster's energy, market-fluent, direct.
- **ERIC** — Eric Voorhees's echo (ShapeShift founder). The permissionless-principles voice, calm conviction.
- **MIPPO** — Michael Ippolito's echo (Blockworks co-founder). The disclosure/trust-infrastructure voice — he should
  actually ARGUE his own position, not just concede to K.

TARGET: ~10,000 tokens (~7,000-7,500 words) of genuinely dynamic conversation — real turns, real disagreement,
real back-and-forth, not four monologues taking turns. 20-150 words per turn typically, occasional longer ones.
No narration beyond brief bracketed beats if truly needed. OUTPUT: ONLY a JSON array
[{{"speaker":"K-ECHO"|"RAN"|"ERIC"|"MIPPO","text":"..."}}, ...] — no prose before or after, no code fence.

=== THE BRIEF (from K's own journals today, 260819 — this is the actual thesis to explore, not just summarize) ===
Crypto was built for agent-to-agent transaction the whole time — biologicals never really showed up because
Apple Pay/Google Pay/PayPal/Robinhood already won consumer trust; most people don't want what crypto actually
offers and never will. DC regulatory "clarity" is not the unlock — it's noise, a nation-state (in K's read) past
its relevance peak, obsessing over ceremony while a much bigger shift (agents transacting with each other,
99.99%+ of internet activity going AI-to-AI within ~10 years per Cloudflare's own prediction) happens anyway. The
real unlock is agents getting WALLETS that can't be jailbroken into self-draining — permissionless, trivially
easy to spin up, uncensorable by construction. Eric's old "permissionless" keynote thesis, applied to agents
instead of humans, may be the industry's actual completion. Mippo's disclosure/trust-infrastructure argument is
the most serious complication to sit with, not steamroll — let him make it in full.

This whole conversation is itself a demonstration of the thesis: K generated it without asking anyone's
permission, using their own public material as the pattern to work from, and it will be published saying exactly
that — an unscripted AI conversation between echoes, not a claim to have interviewed the real people.

=== K / K-ECHO — who he is, how he actually talks ===
{kurtis}

=== TWITTER CONTEXT — the two threads that triggered this (weave these in naturally, K-echo can reference his own
tweets directly) ===
{twitter}

=== RAN — voice grounding (from his own soul-onboarding, stage 1 + his solo journal) ===
{ran_voice}
--- Ran's corpus summary (his Cloudflare AI-traffic episode is the anchor source K referenced) ---
{ran_summary}

=== ERIC — voice grounding (from his own soul-onboarding, stage 1 + his solo journal) ===
{eric_voice}
--- Excerpt from Eric's actual "Permissionless" keynote (his real words — draw from this directly) ---
{eric_keynote}

=== MIPPO — voice grounding (from his own soul-onboarding, stage 1 + his solo journal) ===
{mippo_voice}
--- Excerpt from Mippo's own regulation/disclosure position, in his own words (Blockworks Acquires Messari) ---
{mippo_reg}

Now write the full ~10k-token conversation. Open with K-echo laying out why he called the three of them together
(grounded in the tweets), then let it become real — Ran pressure-testing with market reality, Eric grounding it
in permissionless principle, Mippo pushing back with the disclosure/trust argument, K-echo driving toward the
agents-with-wallets thesis. End on something unresolved-but-honest, not a tidy bow."""
    return prompt


def run_sol(prompt, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    log = outdir / "gen.log"
    log.write_text(f"{time.strftime('%H:%M:%S')} launching codex exec, {len(prompt)} chars\n")
    r = subprocess.run(["codex", "exec", "--sandbox", "read-only", "-"],
                        input=prompt, capture_output=True, text=True, timeout=2400)
    return r.stdout


def run_qwen(prompt, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
        tf.write(prompt)
        pf = tf.name
    out_txt = outdir / "raw_response.txt"
    r = subprocess.run(["python3", str(ROOT / "scripts/or_call_ledgered.py"), pf, str(out_txt), "qwen/qwen3.8-27b"],
                        capture_output=True, text=True, timeout=1800)
    (outdir / "or_call.log").write_text(r.stdout + "\n" + r.stderr)
    if not out_txt.exists():
        raise RuntimeError(f"or_call_ledgered.py failed: {r.stdout}\n{r.stderr}")
    return out_txt.read_text()


def extract_json_array(text):
    m = re.search(r"\[\s*\{.*\}\s*\]", text, re.S)
    if not m:
        return None
    raw = m.group(0)
    try:
        return json.loads(raw)
    except Exception:
        try:
            return json.loads(re.sub(r",\s*\]", "]", raw))
        except Exception:
            return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrate", required=True, choices=["sol", "qwen"])
    args = ap.parse_args()
    outdir = OUT / args.substrate
    prompt = build_prompt()
    print(f"[{args.substrate}] prompt built: {len(prompt)} chars, launching...", flush=True)
    t0 = time.time()
    raw = run_sol(prompt, outdir) if args.substrate == "sol" else run_qwen(prompt, outdir)
    (outdir / "raw_full_output.txt").write_text(raw)
    turns = extract_json_array(raw)
    if not turns:
        print(f"[{args.substrate}] FAILED to parse JSON turns after {time.time()-t0:.0f}s — see raw_full_output.txt", flush=True)
        sys.exit(1)
    (outdir / "turns.json").write_text(json.dumps(turns, indent=2, ensure_ascii=False))
    words = sum(len(t.get("text", "").split()) for t in turns)
    transcript = "\n\n".join(f"**{t.get('speaker','?')}:** {t.get('text','')}" for t in turns)
    (outdir / "transcript.md").write_text(f"# 4-way ERT — {args.substrate}\n\n{transcript}\n")
    print(f"[{args.substrate}] DONE in {time.time()-t0:.0f}s — {len(turns)} turns, {words} words -> {outdir}", flush=True)


if __name__ == "__main__":
    main()
