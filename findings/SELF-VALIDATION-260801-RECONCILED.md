# Self-Validation, Reconciled — The Full Soul-File Reaches the Person (260801)

**Supersedes the interim null in `SELF-VALIDATION-260801-three-pass-arc.md`.** That document
reported a null and correctly flagged that we couldn't separate "the pointer doesn't reach" from
"the model can't do the task." Running a stronger model separated them. This is the reconciled
result. Retractions and the correction are kept in the record on purpose.

## The instrument (position-controlled, judge-free of humans)

Forced-choice discrimination: give a model K's real held-out journal excerpt and a hard
near-twin decoy (same milieu — someone who also builds AI, broods on consciousness, walks
outdoors, loves a kid), ask "which is genuinely yours?" Each pair judged in **both slot orders**;
an arm scores correct only if it picks the real excerpt **both ways** (this cancels the primacy /
position bias that produced a spurious below-chance artifact earlier in the day). Chance
consistency = 0.25. `pick1_rate` reported separately — near 0.5 means no position bias.

Arms: **soulfile** (full ~35KB persona), **pointer600** (600 bytes), **placebo** (a *wrong
person's* full file), **bare** (no pointer). Held-out excerpts are journals dated after each
model's knowledge — and for the local model, provably after its 260718 training-corpus freeze.

## Results across three capability tiers

| model | soulfile | pointer600 | placebo (wrong person) | bare | soulfile pick1_rate |
|---|---|---|---|---|---|
| **kimi-k3 (frontier / opus-tier)** | **0.94** | 0.25 | 0.56 | 0.14 | 0.53 (balanced) |
| kimi-k2-thinking (weak) | 0.31 | 0.125 | 0.125 | 0.06 | 0.63 |
| local qwen3.5-2b (trained on K, tiny) | 0.33 | 0.125 | 0.44 | 0.125 | 0.57 |

## What this establishes

1. **The full soul-file confers strong, specific self-recognition on a capable model.** 0.94
   consistency (15/16), with a balanced 0.53 pick-1 rate — so it is real signal, not a position
   artifact. And it is **K-specific**: 0.94 for K's file vs **0.56** for the wrong-person placebo
   vs 0.14 bare. A capable model, given K's soul-file, reliably knows K's real held-out writing
   from a good synthetic twin.

2. **Capability gates the effect.** The two weak models null. The positive-control 2B — which
   *provably* trained on K and can *generate* as K fluently ("a pattern extracted from over 1,500
   of my own journals") — nonetheless cannot *pick* K. **Generation ≠ discrimination:** being
   saturated with a voice shows up as producing it, not as the separate meta-cognitive skill of
   judging "which of these is mine." So a null on a weak model is uninterpretable; only a capable
   model's result speaks to the claim.

3. **The 600-byte pointer does NOT reach the person on the LLM side.** It nulls at chance on
   every model, including the frontier one. This refutes the "a tiny pointer is sufficient"
   sub-claim *for the mind/soul-file layer* — and is worth contrasting with the voice layer, where
   ~3 seconds sufficed. The two layers are not symmetric: a voice pointer selects a vocal state; a
   soul-file must carry enough pattern to individuate a person against a near-twin, and 600 bytes
   does not.

## What this does NOT establish (open, honest)

- **n = 16, one capable model, one design.** 0.94 is strong but needs replication (run twice),
  more capable models, and larger n before it is a load-bearing claim.
- **Decoy quality is the live confound.** If the hard decoys are systematically distinguishable
  for a reason other than "not K" (a stylistic tell of the decoy-generator), the frontier model
  could be exploiting that. A human-graded decoy-fairness check is required.
- **A second, independent, judge-free measure is wanted.** A surprise / likelihood
  (perplexity-conditioned-on-pointer) instrument would confirm 0.94 without any meta-cognition at
  all. It is **parked**: the local server's completion endpoint returns logprobs only for
  generated tokens, so a proper conditioned-perplexity build (llama-perplexity with teacher
  forcing) is the next engineering task — not faked with a crude heuristic.

## The correction, on the record

Earlier today the operator over-read the weak-model / positive-control null as "the discrimination
instrument is invalid." The frontier run corrected it: the instrument is valid, capability gates
it. Keeping the wrong turn visible is the method — the same reason the position-bias artifact and
the falsified pass-1 prediction stay in the record.

## Next

1. Replicate the frontier soulfile arm (run twice; second capable model, e.g. Opus-4.8).
2. Human-grade decoy fairness on a sample.
3. Build the conditioned-perplexity (surprise) instrument as an independent confirmation.
4. Titrate pointer size between 600 bytes and full file to find where individuation switches on.

Runner: `scripts/run_selfvalidation.py`. Interpretation-room transcripts published as playlist
episodes. Voices synthetic, disclosed.
