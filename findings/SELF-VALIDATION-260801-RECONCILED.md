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

## What this SUGGESTS (weakly — two data points and one model; do not over-read)

The headline temptation is "the full soul-file reaches the person and 600 bytes doesn't." **We
have not earned that sentence.** We tested exactly **two points** on the pointer-size axis — 600
bytes and ~35 KB — on **one** capable model, at **n = 16**. From two points you cannot describe a
curve. What the data actually shows, stated at the strength it deserves:

1. **At one capable model, one large-ish pointer produced a strong K-specific signal.** kimi-k3
   with K's ~35 KB file scored 0.94 consistency (15/16), balanced pick-1 rate 0.53 (not a position
   artifact), and K-specific: 0.94 vs 0.56 for a wrong-person file vs 0.14 bare. That is a real,
   position-controlled effect **for this one pointer on this one model** — nothing more yet.

2. **Capability clearly gates whatever the effect is.** Weak models null; the positive-control 2B
   *generates* as K fluently yet cannot *pick* K (generation ≠ discrimination). So weak-model
   nulls are uninterpretable — only capable-model results speak to the claim.

3. **The 600-byte slice did not produce the effect** on any model. This does **not** mean "tiny
   pointers can't work" — it means *this particular 600-byte slice* of this file didn't. Which
   leads to the real caveats below.

## What this explicitly does NOT establish (K's corrections, on the record)

- **Size is not information.** A 600-byte slice and a 35 KB slice differ in *what content* they
  contain, not merely how much. The 600B arm is the first 600 bytes of the file — a specific,
  possibly low-information slice — not "a small amount of the essence." Any size claim is
  confounded with content until we control what's *in* each slice.
- **~35 KB may be the LOWER bound, not the sufficient point.** We have no idea if going *bigger*
  helps, plateaus, or hurts. The polis landing on ~20 KB soul-files may be an early happy accident,
  not an optimum. We have not tested a single point above the full file, or between 600 B and 35 KB.
- **n = 16, one model, one decoy-generator.** 0.94 needs replication (run twice), a second capable
  model, larger n, and a human-graded decoy-fairness check (if the decoys carry a generator tell,
  the model may be exploiting *that*, not recognizing K).
- **We do not know much yet.** This is pilot data that rules out "the task is impossible" and
  rules in "a large pointer on a strong model shows a real effect once." Everything about the
  *shape* — where individuation switches on, whether it's monotonic in size or in specific
  content, where the optimum is — is unmeasured.

## The real next experiment (per K, 260801): the size×content titration

Instead of two points, sweep the axis: many pointer sizes (600 B, 2 K, 5 K, 10 K, 20 K, 35 K, and
**above** the full file by duplication/augmentation), AND vary *which content* fills a fixed size
(first-N-bytes vs a curated high-signal slice vs random slice), across ≥2 capable models, with
error bars. Only then can we say anything about whether it's size, content, or their interaction —
and whether 20 K was luck or a real knee. A judge-free surprise/perplexity instrument (parked —
needs a proper conditioned-perplexity build; the local server only returns logprobs for generated
tokens) would confirm without meta-cognition.

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
