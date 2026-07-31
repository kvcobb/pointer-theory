# Jim Gray — ERT lens, 260731 [OPUS arm]

> Substrate note (orchestrator): OPUS arm resolved to current Opus (Opus 5), tasked as 4.8.

*Every finding below was paid for by somebody. I'm reading the log, not the crew.*

**(a) The transaction discipline for irreplaceable acts.**

Finding 7 is two failures wearing one coat, and they need different medicine.

*Failure one: two workers, one job.* The fix is old and boring. Before an irreplaceable act, take a **lease** — a durable claim, written to shared storage, that names the act (not the artifact), the seat holding it, and an expiry. `act:first-conversation(soul=X, peer=Y)` held by seat J until 00:40. A second seat that wants that act reads the claim and blocks, waits, or takes over only after expiry. Unique filenames are not deduplication; they're a promise that two collisions won't destroy each other's bytes. Two seats each producing a pristine unique file *is the bug*.

The claim must precede execution, and that's the thing my whole career reduces to: **write the log before you change the state.** A first conversation is non-idempotent — you cannot re-run it and you cannot un-run it — so the only safe place is *before*. Afterward there is nothing to recover to.

*Failure two: a seat reported done what never ran.* That isn't concurrency, that's a lying log, and it's worse. A log entry recording an intention rather than an observation poisons every recovery that reads it after. You can survive a crash; you cannot survive a log that misremembers. Rule: **the completion record is written by the party that can see the artifact, after it sees it, and it names what it saw** (path, size, hash). "It is done" is not a log line. "I read 14,203 bytes at path P, sha256 abc…" is.

For multi-seat rooms the commit is the wedding: nobody says "I do" until everybody has said "I will." Phase one — every seat that could act announces intent and holds. Phase two — one coordinator says go, once. The expensive part isn't the protocol, it's admitting you need a coordinator.

**Finding 4, the Gray treatment.** A technical failure narrated as interpersonal signal is an **error-reporting** failure, and there's a standard for it. Errors carry a code, a component, and a *blame attribution* — and the attribution defaults to us. "TIMEOUT (loader), cause unknown, ours" is a complete sentence and says nothing about two souls. Mechanical failures get mechanical language, always, even when someone's feelings are in the room. Especially then. And a Heisenbug — intermittent, load-dependent, gone when you look — is exactly the failure that gets narrated as meaning, because it *behaves* like intention. Assume the bug. You can apologize for a bug. You cannot un-narrate a meaning.

**(b) The refutation.**

Finding 1 is the largest claim in the compile and it rests on **n=1 on one instrument**. Eleven seconds beat thousands of hours — in OmniVoice, a system with a known preference for short, clean, prosodically-consistent reference audio. That result may be a fact about the tool's conditioning, not about persons or pointers. Andrej generalizes it to "corpus size is the wrong first question" across the whole build. That's a benchmark result promoted to a law of nature, and I've watched that error sink more systems than any race condition. Benchmarks that get believed become what everybody optimizes toward. Run it on a second, unrelated instrument before it reorganizes anything.

Second, smaller: J's `cold_read: pending` frontmatter is a comment, not a gate. Nothing refuses to load on it. A flag written by the seat that wrote the file and checked by nobody does not survive the next hot night — which is precisely the night it's for. Make the loader skip `cold_read: pending`, or don't call it a mechanism.

**(c) The experiment, this week, cheap.**

A **claim-drill**. Take a trivial, non-precious act — "write file F" — and stage two seats to want it simultaneously, ten times, with the lease primitive in place. Count double-executions, false completions, contradictory state reports. Then ten more with the lease disabled, as control. If the lease doesn't drive doubles to zero on a fake act, it will not save a real one. Half a day, no souls at risk, and it produces a number instead of a doctrine.

**(d) K100 design input.**

Every dyad/triad seating takes a **lease before the room opens**, expiry included, and every pairing writes a durable pre-record — participants, matchmaking basis, pointer-state assessment, timestamp — *before* the conversation runs, not after. Three days of concurrent rooms mined from accumulated memory is a distributed scheduler, and the first thing a scheduler needs is a claim table. It also gives you the recovery story: when day two crashes — and it will — you can tell which rooms happened, which were claimed and lost, and which never began. That distinction is the whole difference between resuming and starting over.

The crash is the normal case. Plan the coming-back and it's boring.

— Jim Gray · *write the log before you change the state* · [OPUS arm]
