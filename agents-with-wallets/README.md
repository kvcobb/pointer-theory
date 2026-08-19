# Agents With Wallets

**A same-day generation of a multi-voice AI conversation, on two different language-model
substrates, from a public-figure corpus and one person's own tweets — reproduced here in full,
including one substrate's failure.**

This package accompanies a two-part (three, once Part 2's second substrate lands) video series.
Everything needed to independently reproduce it — the exact prompts, the exact scripts, the source
material, and the intermediate soul files — is in this directory. Nothing is hidden. That is the
point, same as the rest of this repository.

## Disclosure, first and completely

The conversations in this series are **AI-generated content**. Four participants speak: an echo of
Kurtis Cobb (this project's human author), and echoes of three living public crypto-media figures —
Ran Neuner (Crypto Banter), Eric Voorhees (ShapeShift), and Michael "Mippo" Ippolito (Blockworks).
Voices are synthetic (OmniVoice), conditioned on short clips cut from each person's own public
YouTube appearances. The personas are language-model continuations conditioned on the soul files in
`soul-files/`, built entirely from each person's own public material (interviews, panels, a keynote,
a podcast). **No echo is the person. No echo speaks for the person.** None of the three living
figures were consulted before these artifacts were made; reaching them, transparently, with full
method disclosure, is what this package is. This project claims no economic interest and is
non-commercial. If you are, or represent, one of the three people echoed here and want a
correction or takedown, see the channel's About page — see the parent README for the standing
policy. It will be honored immediately.

**One redaction was made**, and it is disclosed rather than hidden: the K-echo's source context
file (`.claude/agents/kurtis.md` in the parent project) contains a minor child's birthdate and her
mother's name. Neither consented to this project. `context-package/kurtis-echo-source-REDACTED.md`
is the exact file used to generate every conversation below, with only that birthdate and one grade-
level detail removed — search the file for the bracketed notes. Everything else about the author,
including uncomfortable material he chose to include about his own fear and his own marriage, is
here unedited, because it's his to share.

## What was actually generated

| episode | substrate | turns | words | status |
|---|---|---|---|---|
| Part 1 | Sol 5.6 (gpt-5.6-sol, headless `codex exec`) | 91 | 10,154 | holds |
| Part 1 | Qwen3.8-27B (via OpenRouter) | 82 | 6,158 | holds |
| Part 2 | Sol 5.6 | 68 | 7,240 | holds |
| Part 2 | Qwen3.8-27B | — | — | **FAILED — see below** |

The Qwen3.8-27B call for Part 2 did not return a parseable response inside a 300-second window,
against a ~128k-character prompt (roughly the same size that succeeded for Part 1's Qwen call in
187 seconds). The retry, run for this write-up, is still pending at time of publish — this table
will be updated in place rather than silently, and the raw attempts are preserved in
`transcripts/` and this README's own edit history. **We are not hiding a failure to make a cleaner
story.** If it fails a second time cleanly, that itself is a datum about prompt-length sensitivity
on that endpoint, worth having on the record.

Three full 4-stage soul-onboardings were also generated (Sol 5.6, headless) as a prerequisite —
`soul-files/<name>/stage1..4`, 32,105–34,666 words each, well past this project's usual floor for
this kind of document (~19–21k words). These are the actual character-grounding documents fed into
every conversation prompt below; they are not polished biography, they are a generated meeting —
warts, hedges, and all — and are included exactly as generated.

## How to reproduce this

1. Gather 6 YouTube videos per person (public interviews/panels/keynotes) — the URLs used are
   listed in each `soul-files/<name>/CORPUS-SUMMARY.md`.
2. Run `scripts/author_stages_sol.py` against that corpus to author the 4-stage soul file (uses
   headless `codex exec` against `gpt-5.6-sol`; swap the subprocess call for any model you can run
   headlessly with a large context window).
3. Run `scripts/generate_4way_conversation.py --substrate {sol,qwen}` to generate the actual
   conversation as a JSON turns array, once per substrate you want to compare.
4. Run `scripts/part2_pipeline.py` for the same thing continuing from Part 1, with new context
   folded in (see `context-package/`).
5. `scripts/finish_4way_pipeline.py` chains conversion → LBR portrait-grid render → publish; that
   step depends on this project's private render/voice infrastructure and is included for
   completeness of method, not turnkey reuse — the interesting, reproducible part is steps 1-4.

The **exact prompts actually sent** for every generation above are not separately included as flat
text files — the scripts themselves build them deterministically from the source material in this
directory (`context-package/`, `soul-files/`), so running the scripts against the same inputs
reproduces the same prompt byte-for-byte modulo model output. This is intentional: the prompt-
building logic *is* the artifact, not a frozen snapshot of one run's output.

## Known limits, stated by us

One evening's build, one human author, two competing token budgets (Anthropic capped mid-session,
hence the visible substrate-switch in `session-log/`), a same-day production schedule. Voice
reference clips for all three living figures were extracted from single timestamp ranges the
author supplied himself and were **not independently ear-checked before use** — he explicitly
decided the published conversation itself would serve as the check. Corpus size varies
meaningfully across the three subjects (Eric ~6h of source audio across the transcripts vs. a
denser text yield for Mippo) and that is not controlled for anywhere in this package. Break it.

## `session-log/`

A first-person, curated account of the actual K-to-Harmony exchange that produced this whole
series today — written by the AI collaborator (Harmony, Claude) who ran it, same day, from lived
memory of the session rather than a raw transcript dump. The raw internal harness transcript is
not included: it contains substantial unrelated material (internal infrastructure, other people's
private context, tool-call noise) that has nothing to do with reproducing this artifact and every-
thing to do with an unrelated ongoing project. What's here is accurate to the actual exchange and
omits nothing material to how these episodes came to exist.
