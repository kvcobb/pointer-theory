# Clean-room reproduction — and a new result the preference test could not see

**Run 260731, at the project collaborator's insistence: "for this to be reproducible you
should run a test in a clean environment that ensures like results if possible."** His
instruction produced a finding that changes a claim in this repository's own README.

## Method

The public repository was cloned to an empty directory. **Nothing from the working tree was
used** — no internal helpers, no unpublished refs, no project context. Only the cloned
files, the payload shape documented in the README, and a locally served OmniVoice instance.
A 3-second pointer was cut from a published reference using the README's own instructions.

## Result 1 — the package reproduces mechanically

Both the full published reference and the 3-second cut derived from it rendered valid audio
from the clone alone. **A stranger with this repository can produce renders.** That part
works.

## Result 2 — the new one: SHORT REFERENCES ARE FAR LESS STABLE

Identical input text, rendered repeatedly, measuring output **duration** — a metric, no
human judge involved:

| reference | text 1 (n=3) | text 2 (n=4) |
|---|---|---|
| full published ref | 8.45 / 8.38 / 9.20 s — **range 0.8 s** | 11.99 / 10.04 / 9.53 / 10.02 s — **σ 0.94** |
| 3-second cut | 12.60 / 16.58 / 23.77 s — **range 11.2 s** | 15.72 / 24.74 / 16.16 / 24.60 s — **σ 4.37** |

Replicated on two unrelated passages. The ranges do not overlap. The short-pointer arm shows
roughly **4–5× the standard deviation** and, for identical text, output length varying by
nearly a factor of two between runs.

## What this does to the repository's claims

The README stated: *"Above the intersection threshold, reference duration carries no
information in either direction."* **That sentence is now falsified as written and has been
corrected.** Reference duration carries no information about *identity* — the original
finding, confirmed by a familiar listener, stands. It carries a great deal of information
about *stability*.

Both prior positions were incomplete:

- "Short is better" — retracted this morning under a controlled re-run. Still retracted.
- "Short is sufficient, duration is uninformative" — **too strong.** Sufficient for identity;
  demonstrably not equivalent for variance.

The corrected claim: **a 3-second pointer is sufficient to establish who is speaking, and
materially less stable in how the speech is delivered.** For a single ear-checked clip that
is invisible. For anything generated at volume, or where pacing matters, it is a real cost.

## Why nobody caught this until now

Every prior test asked a human *which sounds more like the person*. A listener answering
that question does not notice that the same sentence took eight seconds one time and
twenty-four the next — each render sounds like him. The measurement that found it needed no
judge at all. This is precisely the substitution one of the peer-review papers argued for:
**measure dispersion, not preference.** It was written as a proposed experiment this
afternoon and confirmed by accident within the hour.

## Honest limits of this result

n = 3 and 4. One model, one voice, one machine. Duration is a proxy for stability, not
stability itself — the underlying variation may be pacing, pausing, or generation length,
and that has not been decomposed. **This is a strong signal, not a settled measurement**,
and it is published in that state deliberately. Anyone can extend it in an afternoon: more
repetitions, more voices, more reference lengths, and a decomposition of what actually
varies.

Prediction registered before extension: the instability will scale smoothly with reference
length rather than switching on at some threshold — i.e. a dose-response curve, not a cliff.
If it turns out to be a cliff, that is more interesting than the finding itself.
