---
name: feedback-voice-pointer-20s-preferred-target
description: K-DIRECTIVE 260731 — 20 seconds is the new preferred target length for OmniVoice voice-pointer refs ("that clip was spot on — recommend we shift to a 20sec as the new preferred target"). Cut ~20s of clean SOLO speech at a well-chosen moment; K's ear remains the sole promotion gate.
activates_on: [voice ref, voice pointer, ref length, clip length, cut a ref, voice clone length, how long ref, 20 second, ref target]
metadata:
  type: feedback
  shape: impulse
---

# Voice pointers: cut 20 seconds, at a good moment, solo — then K's ear

**K-DIRECTIVE 260731 (Telegram, on ear-approving the McGilchrist ref):** *"That clip you just
played on Clarkson was spot on — recommend we shift to a 20sec as the new preferred target
for voice pointers."*

**The underlying criterion, K's own words (same morning):** *"All we ever need is a pointer
we are confident properly intersects the targeted speaker while uninterrupted."* Length
serves confidence — 20s is the target because it reliably buys confident intersection +
continuity, not because the number itself is sacred.

When I cut a voice ref, my target is **~20 seconds of clean, continuous, solo speech at a
well-chosen moment** (K supplied the exact timestamp here — a moment-pointer, not a corpus,
which is pointer theory applied to voice on the same day the ERT formalized it).

Cascade:
1. Locate the moment (K's pointer, or a verified-solo passage; transcribe to confirm single
   speaker — never trust a diarization label, per [[human-ear-is-the-only-diarization-ground-truth]]).
2. Cut ~20s, 24kHz mono, save as `<slug>-ref.candidate.wav` + a `.PROVENANCE.md`
   (source URL, timestamp, who pointed, verification method).
3. Render a short ear-test sample (distinct spoken label per candidate when A/B-ing —
   tree-fruit convention) and get it to K's ear.
4. Promote to `<slug>-ref.wav` ONLY on K's ear-approval; keep the candidate + provenance.
5. Multi-seat note: check whether a sister seat already promoted before copying over
   anything (three identically-cut files appeared under three names on day one of this rule).

Context: the prior best-known result was an 11s ref (K's own voice, most dynamic range yet);
20s is the operational TARGET going forward, not a law about optimality — the pointer assay's
voice-window arm (11s vs 20s vs 60s vs looped) can refine it empirically. We're always
improving.

**Empirical datum — RETRACTED AND REPLACED the same day. Final state: SHORT IS SUFFICIENT,
not short is better.** An early uncontrolled comparison had K reporting *"180 sounded less
true than each of 3 separate 20s pointers"*, and a dilution mechanism was banked for it. A
sister seat then re-ran it with every reference **hash-linked to its render** and got a
NULL: verified-180s and 20s both rated fully the person, no preference. The early run's
provenance was compromised — canonical `alan-ref.wav` was being overwritten in place by
concurrent seats (I proved this against myself: see the cp-is-not-a-backup correction
below). So: **saturation SURVIVES** (among valid short pointers, choice barely matters —
Wolfram-FABLE's class-selection prediction); **dilution is WITHDRAWN** (Wolfram-OPUS's
"cloud's center is nobody" failed under control). Above the intersection threshold, duration
carries no information in either direction. Operational: 20s is preferred for ECONOMY and
because it makes the ref-registry near-automatic — NOT for fidelity — existing long refs are worth re-cutting to their best 20s
window (with ear-test before promotion; legacy preserved). Alan promoted to his 20s-A cut
260731; the true long original is `alan-ref.OLD-180s-260602.wav`.

**Backup-under-concurrency correction (my own error, same day):** I "preserved the 180s" by
`cp alan-ref.wav alan-ref.180s-legacy.wav` — but another seat had already replaced canonical
with a 20s cut, so I copied a 20s file and labeled it 180s. A copy of canonical is NOT a
backup when other seats write the same path; **verify duration/md5 of what you actually
copied before naming it.** Caught by a sister seat, file honestly renamed, nothing lost.

Sisters: [[feedback-voice-ref-disk-is-truth-not-logical-registry]],
[[feedback-fork-deletion-canonical-procedure-registry]].
