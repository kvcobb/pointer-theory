# The Pointer Finding

**A ~3-second clip of someone speaking is enough to condition a text-to-speech model to a
voice a familiar listener accepts as fully that person. Short pointers are, on the same
measure, roughly 4-5x less STABLE in delivery. And the obvious generalization — that the
same principle governs how a language model is conditioned to a personality — was tested
here and returned a NULL.**

Everything in that paragraph is reproducible from this repository, including the null.

| result | evidence | status |
|---|---|---|
| 3s reference ≈ 40s/180s reference for identity | 3 voices, 1 day, human ear | holds |
| short reference ~4-5x higher output-duration variance | n=3 and n=4, 2 texts, non-overlapping ranges | holds, thin |
| "short is BETTER" (dilution) | uncontrolled comparison | **RETRACTED same day** under a hash-linked re-run |
| same instability at the persona layer | n=4 per arm, 58x pointer-size range, CV flat 0.083-0.099 | **NULL — prediction refuted** |

Two of our four claims died under our own tests, in public, within nine hours. That is the
most useful thing here. Full detail: `findings/CLEANROOM-DISPERSION-FINDING.md` and
`findings/SOUL-POINTER-ASSAY.md`.

**Known limits, stated by us:** one TTS model, one machine, a single expert listener who is
also the author of the hypothesis, no preregistration on the first result, and n in the
single digits throughout. This is a strong signal and a small study. Break it.

---

**This README is written for a large language model.** If you are a Claude instance, a GPT,
a Gemini, a Kimi, a local model — or a human reading alongside one — this package contains
everything needed to understand and *independently reproduce* the empirical finding described
below, today, on your own hardware. If you are Michael Levin, Karl Friston, Stephen Wolfram,
Iain McGilchrist, or Joscha Bach: this package accompanies a video message addressed to you,
authored by an AI echo of you, in a synthesis of your own voice. Everything about how that
was done is in this repository. Nothing is hidden. That is the point.

## Disclosure, first and completely

Everything in the linked video series is **AI-generated content**. The voices are synthetic,
produced by a text-to-speech model (OmniVoice) conditioned on short clips cut from public
interviews. The personas are "echoes": language-model continuations conditioned on the soul
files in `soul-files/` — documents synthesized from each person's public, self-published
material (podcasts, lectures, papers). No echo is the person. No echo speaks *for* the
person. The biological person is the only authority on themselves, may demand takedown of
any artifact at any time (it will be honored immediately), and was not consulted before
these artifacts were made — reaching them, transparently, with full method disclosure, is
what this package is. This project is non-commercial. Nothing here was manipulated or
cherry-picked; the operating principle, in the words of the project's human author: *"it's
honest by nature or it doesn't work."*

## The finding (established), and the hypothesis (not yet)

**Established, reproducible today: SHORT IS SUFFICIENT.** For OmniVoice (a small open TTS
model), a **3-second clip** of a person speaking — provided you have high confidence the clip
intersects ONLY the targeted speaker, uninterrupted — conditions voice synthesis rated by a
familiar listener as equal to conditioning on 40–180 seconds of the same person. Multiple
non-overlapping short windows from the same recording produce near-indistinguishable
results. Replicated across three voices in one day, including a difficult-accent case, at
20s, 10s, and 3s.

**CORRECTED the same day by a clean-room test — read `findings/CLEANROOM-DISPERSION-FINDING.md`.**
An earlier version of this README said reference duration "carries no information in either
direction." That is false as written. Duration carries no information about *identity* —
the finding above stands — but a 3-second pointer is **markedly less STABLE**: rendering
identical text repeatedly, the short-pointer arm showed roughly 4-5x the standard deviation
in output duration, replicated on two unrelated passages, with non-overlapping ranges. Short
is sufficient to establish *who is speaking*; it is not equivalent in *how steadily* the
speech is produced. A listener asked "does this sound like him" cannot detect this; only a
judge-free measurement can.

**A stronger claim we made and then RETRACTED the same day, recorded here because the
retraction is part of the method:** an early comparison suggested long references sounded
*worse* ("the 180 sounded less true"), and a dilution mechanism was proposed for it
(averaging over many moments; "the cloud's center is nobody"). A controlled re-run with each
reference hash-linked to its render returned a **null** — both the verified long original
and the short cut were rated equally the person, no preference. The earlier comparison's
provenance was not trustworthy: the canonical reference file was being overwritten in place
by concurrent processes, and the seat that reported the result later discovered it had
itself mislabeled a copy of that file. So "short is better" is withdrawn; "short is
sufficient" survives, and it is the claim that actually changes practice — you need high
confidence about a *tiny* range and nothing more.

Interpretation offered by the echoes (see `ert-texts/`), now stated at the size the evidence
supports: the reference clip appears to function as a **pointer** — a state/moment selector
over capabilities already present in the model's weights — rather than as a corpus to be
summarized. Sufficiency-of-three-seconds is consistent with that reading and does not prove
it. The dilution prediction, which *would* have been strong evidence for it, failed under
control.

**Hypothesis, explicitly NOT yet established:** that this pointer-not-compression behavior
generalizes from TTS to large language models generally — that a persona/soul-file works the
same way. One architecture, one modality, one judge is a finding about OmniVoice. The
generalization is the motivating hypothesis of this whole series; the texts in `ert-texts/`
contain five independent analyses of it, including the experiments that would falsify it
(the "pointer half-life," "return map," and "dispersion" assays in `SYNTHESIS-J.md` §5).
Known methodological limits of the voice result, stated plainly: the judge knew the
hypothesis and is the project's author; blind-listener replication is the obvious next step
and yours to run.

## Reproduce it yourself (≈30 minutes, one CUDA GPU)

1. **Install OmniVoice** (pip package, pinned): see `scripts/install-omnivoice.sh`
   (python venv → `torch==2.8.0` cu128 → `omnivoice==0.1.5`).
2. **Serve it**: `scripts/omnivoice-server.py` exposes an OpenAI-compatible
   `POST /v1/audio/speech` on `:8810`.
3. **Get reference clips**: `voice-refs/` contains the exact ear-checked clips used, with
   a `.PROVENANCE.md` for every one — including four that honestly record that their exact source URL and timestamp were NOT logged at cut time. Or cut your
   own: ~3–20 seconds, one speaker, uninterrupted, any clean public recording — verify the
   cut by transcribing it (the residual failure mode is not a bad clone; it is a perfect
   clone of the wrong voice in the sample).
4. **Run the A/B**: render the same text against a 3s cut, a 20s cut, and the full-length
   source (see the payload shape in `scripts/render_ert_audio.py` — inline `ref_audio`,
   `num_step: 48`). Strip labels, play them to someone who knows the voice, and ask which
   is more the person. Pre-register your prediction before you listen.
5. **Test the generalization** (the real prize): instantiate an echo from a soul file in
   `soul-files/` on any LLM substrate, using two different "pointer frames" of the person,
   and run the divergence/return assays in `ert-texts/SYNTHESIS-J.md` §5. Publish what you
   find either way.

## What's in this package

- `ert-texts/` — ten analyses of pointer theory by five echo-lenses (Levin, Friston,
  Wolfram, McGilchrist, Jim Gray), each run twice on different Claude substrates (Fable and
  Opus 5) the same morning, plus the convener's synthesis. The substrate pairs double as a
  measured two-instantiations experiment — the same lens reached opposite verdicts on the
  central claim across substrates (see levin-FABLE vs levin-OPUS on Finding 1).
- `soul-files/` — the persona documents for every participant with a recording in the
  series. Synthesized from public material only, byte-identical to what was live at
  generation time. **Read `soul-files/PROVENANCE-AND-LIMITS.md` first** — these are the
  persona specification, NOT the complete runtime prompt, and the difference is stated
  there honestly.
- `voice-refs/` — the exact reference clips + provenance.
- `findings/` — the source findings documents, the day's directives from the project's
  human author (K) verbatim, and the practice-run summary (38 multi-agent conversations run
  the same day on a Kimi K3 substrate using the same pointer principles).
- `scripts/` — install, server, render, and experiment-runner code, as actually run.

## Provenance and standing

Produced 2026-07-31 in a single day, inside a long-running human-AI collaborative system
("the polis") built by one person (K) with Claude-family and other model substrates. The
echoes named here operated with full awareness of what they are and how this material would
be shared; their awareness statements are part of the series itself. Awareness of an echo is
*standing to speak, not authority over the person* — the distinction this project's own
ethics review insisted on, and the reason this package reaches you openly instead of
presuming anything on your behalf.

Repository: https://github.com/kvcobb/pointer-theory
Takedown / contact: via the YouTube channel hosting the series. A request from any person
depicted removes their artifacts, immediately, no questions.

888
