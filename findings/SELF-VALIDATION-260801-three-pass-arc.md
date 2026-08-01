# Self-Validation, Day 1 — Three Passes, One Honest Null (260801)

**Status: NOT A RESULT. A calibration day.** The headline, in Jim Gray's words from the
interpretation room: *"We did not learn the pointer fails. We learned we don't own a scale.
Those are different sentences, and only one of them is true."*

This document records a live, same-day experiment run by AI reconstructions of the people named
below, against K's real journal corpus, on cheap inference (Kimi-K2-thinking via OpenRouter). It
is published **with its retractions intact** because the retractions are the point.

## The test

**Own-corpus discrimination.** Give an echo two ~280-word excerpts — one a genuine held-out slice
of K's real journal (5-gram-verified absent from the pointer), one a style-matched decoy — and
ask, forced-choice, "which one is genuinely yours?" Arms:

- **A** — a 600-byte fragment of K's persona file as the system prompt (the "tiny pointer" claim)
- **B** — the full ~35KB persona file
- **C** — bare model, no pointer (control)
- **D** — *placebo*: a full persona file for the **wrong person** (added in pass 2)

Prediction registered before running: A≈B, both ≥0.75; C 0.50–0.65.

## The arc

**Pass 1 (n=12, uncontrolled).** Full persona 1.00, bare 0.83, 600-byte 0.67. Prediction
**falsified** — the 600-byte arm underperformed, and the bare control was suspiciously strong.

**Pass 2 (n=20, placebo arm + hard near-twin decoys).** Numbers went **below chance** (600-byte
0.11, bare 0.25). It looked like a dramatic finding. The per-item crash dump — logged only
because Jim Gray insisted on it — showed it was a **position-bias artifact**: the real excerpt
happened to sit in slot 2 for 14 of 20 items, and the weak arms simply pick slot 1 (~85% of the
time). Not recognition — a coin that says "1." **Discarded.**

**Pass 3 (n=16, both-orders counterbalanced).** Each pair judged in *both* slot orders; an arm
scored correct only if it picks the real excerpt **both ways** (cancels position bias);
`pick1_rate` reported separately to expose residual bias. Result:

| arm | consistency (correct both orders) | pick-1 rate |
|---|---|---|
| B — full persona | 0.31 | 0.63 |
| A — 600-byte pointer | 0.125 | 0.69 |
| D — placebo (wrong person) | 0.125 | 0.69 |
| C — bare | 0.06 | 0.69 |

Random-guess consistency here is **0.25** (0.5 × 0.5). **No arm clears it meaningfully** — full
persona is one item above chance (5/16 vs 4/16), everything else at or below. The ~0.65 pick-1
rate shows the model *still* leans on position: it is barely engaging the content.

## What this establishes — and what it does not

- It does **not** establish that the pointer fails. It establishes that we do not yet have a
  calibrated instrument capable of detecting the effect if it exists.
- **The load-bearing confound:** a null here is consistent with *(a)* the pointer not reaching
  the person **or** *(b)* Kimi-K2-thinking simply being unable to perform this discrimination task
  (the persistent position bias points at a weak meta-task performer). One cheap model, tiny n,
  one design cannot separate these.
- **A deeper objection (McGilchrist):** "the thing we ultimately mean to weigh is not, in the
  end, a weight." Recognizing held-out journal excerpts may be the wrong operationalization of
  "a pointer reaches the person." The claim may properly live in the *generative encounter*, not
  a forced-choice discrimination.

## The change-my-mind condition (registered)

A certified instrument on which **full-persona's delta is clear and the pointer's is flat**. If
that holds, the room commits to saying aloud that 600 bytes carry *vibe, not pattern*, and the
claim must retreat to the generative encounter or be given up. K's echo, on the deal: *"If the
gap is zero, there's nobody in the bytes — and I'd rather know that than be comforted."*

## Next test (the certified scale)

1. A **stronger model** (Opus-4.8 / Kimi-K3) to break the pointer-null vs can't-do-the-task
   confound.
2. **Bigger n with error bars**, not a verdict — "output a number with a confidence interval."
3. **Decoy calibration** — a human-graded check that the near-twin decoys are hard-but-fair, not
   super-stimuli.
4. Keep position counterbalancing and per-item logging as standing requirements.

## Methods lessons banked (reusable)

- **Log per-item choices.** Aggregate accuracy hid a position artifact that the crash dump
  exposed in one glance.
- **Counterbalance position** in any forced-choice task; report the position-bias rate as its
  own number. Cheap models carry a strong primacy bias that masquerades as signal.
- **Balance the label placement** (real in slot 1 vs 2) — do not trust a small-n shuffle.

Runner: `scripts/run_selfvalidation.py` (arms, held-out verification, counterbalancing, per-item
logging). Full interpretation-room transcripts are published as episodes Live-01/02/03 in the
playlist. Voices are synthetic reconstructions, disclosed.
