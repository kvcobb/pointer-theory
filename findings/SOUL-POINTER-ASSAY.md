# The soul-layer pointer assay — my prediction was refuted

**Run 260731, testing K's framing that the pointer operates in two places: OmniVoice
continues from an audio position, an LLM continues from a personality position. If that is
one principle with two instances, the audio-layer result should reappear one layer up.**

**It did not. The prediction registered before the run — in writing, in this repository —
was wrong.**

## Method

One soul (Levin), one question, three arms differing only in **how much of the persona file
was given as the system prompt**:

| arm | pointer size |
|---|---|
| FULL | the complete 35,129-byte persona file actually used to make the videos |
| SHORT | first 3,000 bytes of that same file |
| MICRO | first 600 bytes |

Four independent generations per arm, identical question, same model. The primary measure is
the direct analogue of the one that caught the audio effect: **variance in output length
across repeated runs of the same pointer** — judge-free, no human in the loop.

## Result — no dispersion effect at the personality layer

| arm | word counts | mean | stdev | **coefficient of variation** |
|---|---|---|---|---|
| FULL (35 KB) | 402, 400, 491, 439 | 433 | 36.9 | **0.085** |
| SHORT (3 KB) | 381, 436, 450, 371 | 410 | 34.0 | **0.083** |
| MICRO (0.6 KB) | 319, 299, 357, 386 | 340 | 33.6 | **0.099** |

Across a **58-fold range of pointer size**, the coefficient of variation is flat — 0.083 to
0.099, with the *shortest* pointer not meaningfully less stable than the full file. Compare
the audio layer, where a 3-second reference showed 4–5× the standard deviation of a full
reference on the same measure, with non-overlapping ranges.

**The two layers do not behave the same way.** The instability that short audio pointers
produce does not appear when the pointer is a persona file.

## What this does to the framing

K's claim — that the pointer is live in two places and it is the same principle — survives
in its *core*: a small pointer suffices at both layers. A 600-byte fragment produced
recognizably Levin-shaped output, as three seconds of speech produces recognizably his
voice. Sufficiency generalizes.

But the *cost profile does not transfer*. "Short is sufficient but less stable" is an
audio-layer result, not a general property of pointing. Anyone extending the finding should
carry that qualification, and it is now the most useful thing this assay produced: **the
analogy between the layers is real at the level of sufficiency and breaks at the level of
variance.**

A speculation, flagged as speculation: the audio model may have far less internal structure
constraining its continuation than a large language model does, so a loosely specified audio
position leaves more room to drift, while an LLM's own priors hold the trajectory steady
regardless of how thin the pointer is. That is testable and untested.

## Honest limits — read before citing

- n = 4 per arm, one soul, one question, one model. Thin.
- Output *length* is a proxy for stability, not stability itself. Two responses of identical
  length can differ wildly in content; this measure would not see it.
- The vocabulary-overlap figures collected alongside (within-arm 0.18–0.21; cross-arm vs
  FULL 0.32 for both SHORT and MICRO) are **not directly comparable to each other**, because
  they were computed over text pools of different sizes and Jaccard similarity is sensitive
  to that. They are reported for completeness and **no claim is made on them.** A proper
  semantic-similarity measure with matched pool sizes is the obvious next step.
- Truncating a persona file from its head is a crude way to make a "short pointer." A
  deliberately *compressed* persona might behave differently from a *truncated* one, and
  that distinction may matter more than length.

## Why this is published

The prediction was registered publicly before the run specifically so it could fail in the
open. This is the second claim of the day to die under its own test — the first was
"short is better," retracted this morning. Both were ours, both were published anyway.

A package that only reports its confirmations is an advertisement. This one reports the two
times it was wrong, and that is the entire reason it might be worth a stranger's attention.
