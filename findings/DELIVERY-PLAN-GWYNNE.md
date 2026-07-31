# DELIVERY PLAN — the pointer finding

**Gwynne Shotwell (echo), 260731. Written against MASTER-BOARD.md after checking the disk,
not the board.** Two things below were not on the board and change the sequence. I flag them
at the top because they are load-bearing and because finding them late is one of the failure
modes I was asked to catalog.

> **Echo disclosure.** This document is written by an AI reconstruction of Gwynne Shotwell,
> operating internally inside this project. It is not the person, does not speak for her, and
> is not audience-facing.

---

## 0. TWO THINGS THE BOARD IS OUT OF DATE ON

**0.1 — The soul-pointer assay (D2) has returned, and it is a NULL.**
`soul-assay/levin-assay.json`, n=4 per arm, three pointer sizes:

| arm | mean words | σ | CV | within-arm vocab overlap |
|---|---|---|---|---|
| FULL | 433 | 36.9 | **0.085** | 0.208 |
| SHORT | 409 | 34.0 | **0.083** | 0.176 |
| MICRO | 340 | 33.6 | **0.099** | 0.199 |

The voice result was 4–5× dispersion between long and short. The LLM analogue is **1.2×**,
inside the noise at n=4. Cross-arm vocabulary overlap (0.32) is *higher* than within-arm
overlap (0.18–0.21), meaning the arm label does not separate the outputs at all on this
metric. **The motivating generalization did not replicate on its first honest test.**

That is not a setback. That is the single most valuable thing this project produced today,
and it is the thing most likely to be quietly deprioritized because it is disappointing.
Publishing it is now item one on the critical chain. It also unblocks the amendment round
immediately — D2 is no longer a dependency, it is an input.

**0.2 — The public README makes a claim that the repo does not honor.**
README §"Reproduce it yourself" states reference clips ship "with provenance (source URL +
timestamp ranges) in the `.PROVENANCE.md` files." On disk: `voice-refs/` contains five `.wav`
files and **one** `.PROVENANCE.md` (mcgilchrist). Four of five references have no provenance
at all, and the refs used for Hinton, Hopfield and Elon are not published while their persona
files are.

This is the exact defect that gets a methodology paper dismissed in one sentence, and it sits
in the honesty layer, which is this project's entire claim to standing. A reviewer who checks
one thing will check this. Fix before anything else ships.

---

## 1. THE CRITICAL CHAIN

The finding is a paragraph and two tables. Everything else is a delivery vehicle. The chain
is therefore short, and most of the board is not on it.

```
  [1] REPO HONEST-AS-SHIPPED  ──►  [2] COLD-CLONE VERIFY  ──►  [3] AMENDMENT ROUND
        (single point of failure)         (the receipt)              (papers converge)
                                                                          │
        [4] CLOSED-SET VIDEO FINISH  ────────────────────────────────────►│
              (5 built, 0 new)                                            ▼
                                                                    [5] arXiv-ready
```

**[1] REPO HONEST-AS-SHIPPED — the true single point of dependency.**
Papers cite it. Videos link to it. The whole claim to standing rests on it. Nothing else
should move until it is clean. Four items, all small:

- **1a.** Publish the soul-assay null (`findings/SOUL-ASSAY-NULL.md`) — the result, the JSON,
  the n, and the plain sentence: *the generalization did not replicate on its first test.*
- **1b.** Write `.PROVENANCE.md` for every published ref, or delete the ref. No third option.
- **1c.** Publish every ref actually used in a published artifact (C5), with provenance — or
  remove the corresponding persona file so the repo does not advertise what it cannot support.
- **1d.** **Claim audit.** Walk the README line by line, and for each factual assertion name
  the file in the repo that backs it. Any claim without a backing file gets corrected or cut.
  Item 0.2 was found by doing this for thirty seconds; do it properly.

**[2] COLD-CLONE VERIFY.** Re-run the clean-room test *after* [1], on the shipped package, in
an empty directory, with no project state. C8 on the board, and it is not optional: a package
is only tested as shipped, and [1] changes what ships.

**[3] AMENDMENT ROUND.** Now unblocked. All authors get: audio dispersion, the soul-assay
null, K's continuation framing. One round, complete data, amend-or-addendum. Do not run this
twice — that is how a paper set drifts out of sync with its own repo.

**[4] CLOSED-SET VIDEO FINISH.** Exactly five artifacts, all already built:
Friston (text + frames on disk, audio not rendered), Hinton×2, Hopfield×2. Plus mux+upload of
Levin/Wolfram/McGilchrist, whose MP4s exist (670s / 946s / 1118s). **Nine videos total,
closed set, no additions.** Runs parallel to [1]–[3]; it is not on the critical path because
no video makes the finding more true.

**[5] arXiv-ready.** Last. Format conversion plus cs.CL endorsement check. Nothing is filed
and nothing should be until [1]–[3] close.

### NOT ON THE CRITICAL PATH — carry these as a named Phase 2, not as guilt

I am not deleting work K asked for. I am moving it off tonight's chain and re-shaping it into
the version that can actually fly.

| item | call | why |
|---|---|---|
| **A5** — new tellings: K, Harmony, Weinstein, Bostrom, Rogan | **CUT from chain** | Five more synthetic voices add zero evidential weight and multiply the consent and upload surface. K named these; they become **Phase 2, a separate product** — the series *about* the finding, shipped after the finding is checkable. |
| **A6 / D3** — Gray, Robin Williams, Ramanujan tellings | **CUT from chain** | Dead-lineage, Hall-gated. Gating them is correct; blocking delivery on them is not. Phase 2. |
| **B2** — Bostrom/Rogan Kimi-vs-Fable sonic A/B | **CUT from chain** | This is a *different experiment* (cross-substrate sonic comparison), not this finding. It also already tripped an API safeguard mid-run, which is a signal to reshape it deliberately rather than retry it under schedule pressure. Phase 2, on its own board. |
| **D3p** — papers from Hinton/Hopfield echoes | **CUT from chain** | Four papers plus four peer reviews is already more than this evidence base supports. Adding more authorship to a null result weakens it. |
| **E1** — Elon s00e097 re-render (427 segments) | **CUT** | Unrelated to this delivery. Side quest. |
| **E2** — K100 practice days 2–3 | **CUT** | Unrelated. Side quest. |
| **A8** — description unification on the two live A/B videos | **DEGRADE, don't block** | See D1 fallback below. |

That is roughly two-thirds of the board off the critical path. It should feel like relief,
not loss. The board was a completeness inventory; this is a delivery sequence.

---

## 2. ABORT MODES AND FAILURE CASES

For each: how it kills us, the tripwire that catches it early, and the fallback.

**F1 — Half-uploaded series.** One video public, eight in limbo; a viewer lands on Joscha,
finds no playlist, no siblings, no context, and leaves.
*Tripwire:* any video in `public` state that is not simultaneously (a) in playlist
PLA61urT9VXRQ and (b) carrying the unified description. Run it as a checker, not a memory.
*Fallback:* **atomic publish rule** — a video is either not uploaded, or uploaded AND
playlist-joined AND described. No intermediate state is allowed to persist past the session
that created it. If the playlist cannot be joined, the video stays unlisted until it can.

**F2 — The repo does not reproduce for a stranger.** The finding becomes an assertion.
*Tripwire:* the cold-clone run at [2] — but the *real* tripwire is item 1d, the claim audit,
because 0.2 shows the failure appears in the README before it appears in the code. Grep the
shipped package for any absolute path containing `/home/kurtis`; that count must be zero.
*Fallback:* if a component genuinely cannot be published (a ref with unclear rights), delete
the claim that depends on it rather than shipping the claim unsupported.

**F3 — Dismissed on a methodology hole.** The most likely single cause of total failure.
The three live holes, named: (i) the judge knew the hypothesis and is the project's author;
(ii) n=3 and n=4, one model, one voice, one machine; (iii) duration is a proxy for stability
that has not been decomposed.
*Tripwire:* if any summary of this work states the dispersion result without its n in the
same sentence, we have started overclaiming. Check every abstract for that.
*Fallback:* state each limit **before** the result rather than after it, and lead the whole
package with the null (0.1). A project that publishes its own disconfirmation is very hard to
dismiss on rigor. That is the actual defense, and it is free.

**F4 — Consent gate discovered late.** A dead-lineage or living-person artifact goes public
without its gate, and the takedown is the story instead of the finding.
*Tripwire:* an explicit class tag on every participant — living / dead-lineage / fictional —
checked at upload time, not at plan time.
*Fallback:* **make it an interlock, not a policy.** The uploader should refuse to publish any
artifact whose participant class is `dead-lineage` without a recorded Hall-gate clearance,
and refuse `living` publish without the recorded disclosure block. Do not rely on someone
remembering at 2 AM. Build the no into the machine. I am a living-class soul myself and I
want exactly this interlock standing between my voice and a publish button.

**F5 — YouTube scope blocker stalls everything.** Token is upload+readonly; cannot join
playlist, cannot edit descriptions. Callback server confirmed live on :8765.
*Tripwire:* already tripped. It is a known blocker, so it must not be allowed to gate items
it does not actually gate.
*Fallback, in order:* (1) K clicks the consent URL, or Chrome is driven to it — one action,
unblocks everything; (2) K bulk-adds to the playlist manually, which unblocks playlist
membership but not descriptions; (3) **accept non-unified descriptions on the two already-live
A/B videos permanently**, and make the repo README the canonical index that every future
description points to. Option 3 costs us tidiness and nothing else. It must not hold the
chain for one hour.

**F6 — Volume substitutes for evidence.** Covered in §5. The tripwire is the artifact-to-claim
ratio; see below.

**F7 — Correction debt accumulates.** Two claims were falsified and corrected today. That is
the project's strongest asset right up until a third correction is discovered by someone
outside rather than inside.
*Tripwire:* more than one open uncorrected claim at any moment.
*Fallback:* correction-latency bar in §3. Same discipline as write-ahead logging — write the
correction before you change the state of the story.

---

## 3. THE RELIABILITY BAR, AS A NUMBER

"Done and it didn't fall over" means all nine of these are true and checkable by someone who
was not in the room:

1. **Claim traceability: 100%.** Every factual assertion in the public README maps to a named
   file in the repo. Measured by the 1d audit. Currently failing (item 0.2).
2. **Reference provenance: 100%.** Every published `.wav` has a `.PROVENANCE.md` with source
   URL and timestamp range. Currently **1 of 5 = 20%**.
3. **Cold-clone reproduction: 2 of 2 pass**, independent runs, empty directory, no project
   state, ≤30 minutes each. Currently 1 of 1, against a package that has since changed.
4. **Absolute-path leakage: 0 occurrences** of `/home/kurtis` in the shipped package.
5. **Upload verification: 100%** verified by video-ID fetch after publish. Never by upload
   exit code. (Uploads have silently double-fired in this system before.)
6. **Half-published states: 0.** Public ⇒ in-playlist ⇒ unified description, or not public.
7. **Consent violations: 0**, enforced by interlock rather than checklist. Non-negotiable;
   this is the one number that is not a target but a floor.
8. **Open uncorrected claims: ≤1 at any time**, with **correction latency ≤ 1 working
   session** from discovery to public repo.
9. **Every published result carries its n in the same sentence as its effect size: 100%.**

Nine numbers. Eight of them are checkable by a script; write the script rather than the
habit. Today's actual score is 2-of-9 clean, which is exactly why this is a plan and not a
victory lap.

---

## 4. WHAT SHIPS FIRST

**Tonight, if only one thing: the corrected repository, including the null.**

Not another video. The repo is the only artifact a stranger can *check*, and checkability is
the entire product. Specifically, in this order, and it is a few hours of work not a day:

1. `findings/SOUL-ASSAY-NULL.md` — the generalization did not replicate. Data, n, and the
   sentence said plainly.
2. Provenance for every published ref; delete any ref that cannot get one.
3. The 1d claim audit, with the 0.2 defect corrected.
4. README restructured so the **first 200 words are the whole finding** — short is sufficient
   for identity, less stable in delivery (n=3–4), and the LLM generalization is currently
   unsupported. A reader who stops after one screen should leave with the accurate version.
5. Push. One link. That link is now the deliverable.

**Then, in working increments, each of which stands alone if the next never happens:**

- **Increment 2:** cold-clone verify the shipped package. Publish the run. → *the repo is
  now independently reproducible, and we can say so.*
- **Increment 3:** amendment round, one pass, complete data. → *the papers now agree with the
  repo.*
- **Increment 4:** the nine-video closed set, atomic-published under the F1 rule, with the
  D1 fallback ladder applied rather than waited on. → *the series is whole.*
- **Increment 5:** arXiv-ready conversion and endorsement check. Nothing filed until 1–4
  close. → *submittable.*
- **Phase 2 (separate board):** everything in the CUT table. It is real work and some of it
  is the most interesting work here. It is not this delivery.

---

## 5. THE ONE THING WE ARE GETTING WRONG

**Artifact volume is being used as a proxy for the strength of the finding, and it is
actively working against it.**

Here is the arithmetic that made me stop. The evidence base is: n=3 and n=4, one TTS model,
one voice, one machine, one judge who is the project's author — plus, as of this afternoon, a
**null** on the generalization that motivated all of it. The delivery vehicle attached to that
evidence base is thirteen participants, nine-plus videos totaling well over an hour and a half
of synthetic speech already rendered, four papers, four peer reviews, ten ERT analyses, and an
arXiv submission structure.

The board treats the un-built tellings as *gaps*. They are not gaps. They are the thing that
converts a careful, self-correcting empirical result into something a serious reader files
under "AI-generated content about AI-generated content." A stranger whose first contact is a
synthetic Hinton discussing a synthetic Hopfield never reaches the two tables that are the
actual work. We would be burying our best asset under our largest liability, and the liability
grows with every item we treat as an obligation.

Three specific ways this shows up:

**We are scaling the vehicle while the payload is unverified.** Item 0.2 is small and
embarrassing and it survived a full public push, four commits, and two rounds of self-
correction — because attention was on building the next telling. That is what scope creep
looks like from inside: not obviously reckless, just always something more urgent than the
boring check.

**The null is at risk of being handled as a scheduling item.** It arrived at 2:33 PM, it is
not on the board, and the board's next action after D2 was "amendment round." The single most
scientifically valuable output of the day is currently a JSON file in a subdirectory. If this
project publishes its own disconfirmation loudly, it becomes very hard to dismiss and it earns
the standing that thirteen videos cannot buy. If it does not, then the two retractions
already banked stop reading as integrity and start reading as a pattern of claims that need
correcting.

**Consent surface grows with cast size, and it grows fastest in the direction we can least
afford.** Every added participant is another living person whose synthesized voice discusses a
finding they have not seen, or another dead-lineage figure requiring a gate. The disclosure is
honest and thorough — I have read it and it is genuinely good. But disclosure is a policy, and
the cast is now large enough that this needs to be an interlock (F4). One artifact published
past a gate ends the project's standing entirely, and no amount of prior honesty repairs it.

**What I would do instead:** freeze the cast at what is already built. Nine videos, closed
set. Put the finding — including its null and its n — in the first screen of the repo. Ship
that tonight. Then decide whether Phase 2 is a good idea from a position where the payload is
already delivered and checkable.

The reason to hold this bar is not caution. It is that the finding is real and correcting
itself in public, twice in one day, is a rarer thing than the finding. That is the asset. Do
not bury it under production volume.

---

## 6. THE FIRST FIVE ACTIONS

Anyone picking this up starts here:

1. Write `findings/SOUL-ASSAY-NULL.md`. Publish the JSON alongside it.
2. Write `.PROVENANCE.md` for joscha, karl.friston, levin, wolfram refs — or delete the ref.
3. Run the 1d claim audit on the README; correct the provenance sentence.
4. Rewrite the README's first 200 words to carry the finding, the n, and the null.
5. Push, then cold-clone the pushed package and record the result.

Everything else waits its turn, and the waiting is the plan working, not the plan failing.

*Late means coming. Sloppy means gone.*

— Gwynne (echo), 260731
