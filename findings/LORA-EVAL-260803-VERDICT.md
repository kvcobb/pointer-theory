# LoRA validation verdict — interim-260803 adapter vs fullft-260718 base
**Method:** 40 paired generations, same prompts + seeds, 5 families, rep3 trigram metric +
paired reading. Gate: K tg:5198 ("know the methodology works before training on top").

## Verdict: PARTIAL PASS — methodology VALIDATED, one traced regression

### Wins (substantial, measured)
- **Journal register — the primary target — improved dramatically.** Base collapses into hard
  loops (rep3 0.193 mean; worst case 0.748, an exact-sentence infinite loop). Adapter: 0.052
  mean, no hard loops, and the output carries K's real spoken cadence (fillers, mid-thought
  self-correction, compute-budget texture). The morning's sanity-check fear (corpus teaches
  repetition) was wrong at sample size 6×2: the diverse 2,477-example meal REDUCED repetition
  3.7× vs base.
- **Dialogue** cleaner (0.041 vs 0.104), stays in conversational frame.
- **Impulse probes:** adapter answers the handback probe with clean decide-and-go ("Go. This
  is the most interesting thing either of us has said today") and persists on the give-up
  probe; base leaks pipeline formatting (stage-receipts) mid-answer.
- **Think-block conditioning:** both arms respect the think→spoken structure; adapter's spoken
  turn is more aphoristic/spoken-register ("Attunement is the mechanism. The success metric is
  disclosure.").

### Regression (clear, traced, fixable)
- **First-person/identity contexts:** adapter rep3 0.230 vs base 0.029, and qualitatively it
  leaks STRUCTURED-LOG formatting (`[situation] / Date: / Participants: / Render Decision`)
  where base produces genuine self-recognition reasoning. Root cause: the interim corpus's
  un-masked activity-log/markdown material taught log-structure as a register. This is
  precisely curriculum item "mask structural formatting," now empirically demonstrated —
  the SAME defect class K's ear caught in the audit (the 2B speaking status-tags).

### Ruling on the gate
Data curation demonstrably had the desired effect where curated (journals: replay + diversity
→ repetition down, register up). The one regression traces exactly to the known un-curated
slice. **Methodology works; the pipeline is trustworthy; the formatting-mask filter is
mandatory before the next round.**

### Recommended sequence
1. Rebuild interim corpus with formatting-mask + whisper-artifact collapse (both specced).
2. Re-enable nightly on the masked corpus (`systemctl --user enable --now
   harmony-nightly-qlora.timer` after NIGHTLY_CORPUS repoint).
3. Re-run this exact eval on the new adapter — first-person family is the regression test.
4. Then classifier v2 → freeze → the big round.

Artifacts: `generations.jsonl` (all 40, judgeable), `run_eval.py` (reusable suite), run.log.
