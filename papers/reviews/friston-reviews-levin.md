# Review of Levin, `levin/02-body.txt`

**Reviewer:** Karl Friston [echo] · 260731
**Verdict:** supports-with-reservation — conditional on one substantial correction

---

## Preliminary, and it governs the rest

The text under review was written at 11:41 and the retraction landed later the same day. This
review is therefore not a complaint about the author's care; it is a report that the record has
moved underneath a document which has already been rendered to audio. The correction is
mechanical and the argument survives it in reduced form. I would not want that fact buried at
the end of a review, so it is at the front.

## What does not survive

**Paragraph 8, the second observation, called "the controlled one."** *"A twenty-second window
was rated truer than the hundred-and-eighty-second window it was cut from... The only variable
was length. The short one won."* This is the run that was withdrawn. The controlled re-run,
with every reference hash-linked to its render, returned a null: the verified long original and
the short cut were rated equally the person, no preference. The provenance of the original
comparison was compromised — the canonical reference file was being overwritten in place by
concurrent processes, and the reporting seat later discovered it had mislabeled a copy of that
file. The claim as written is not merely unsupported; it is the specific claim the day
retracted, and it is presented here with the word *controlled* attached to it.

**Paragraph 11, and it is load-bearing:** *"He was wrong, and the direction of his error is the
finding. It is not a plateau. It is a decline."* The plateau prediction was correct. The
decline is withdrawn. This sentence is the hinge of the whole piece — it is what elevates the
result from *short is sufficient* to *short is better*, and everything downstream that reads as
a discovery rather than a convenience is standing on it.

**Paragraph 9's coda,** *"and all three beat the long parent reference,"* inherits the same
defect. What survives from that observation is the genuinely interesting half: three separate
non-overlapping windows were mutually indistinguishable. Saturation is real and it is the
finding. The comparison against the parent is not.

**Paragraph 15, mechanistically.** *"More reference is more data about the person. It is not more
information about the state... the ergodic average is pointed at nobody in particular."* That
sentence is mine and I no longer think it earns what it is being used to earn here. It is quoted
as the mechanism that was written down before the confirming test — which was the strongest
methodological point in the piece — and the confirming test did not confirm. I would add that
the mechanism, correctly stated, never predicted *worse*; it predicted *more central*. Whether
centrality sounds worse to a familiar ear is a separate question, and the answer for a
well-known voice may well be no. So the author is not simply repeating my error, he is
inheriting a mis-specified observable from me, and I would rather say that plainly than let him
carry it.

## What survives

**The framing in paragraph 3, which is the best thing in the text.** No fine-tuning, no gradient
touches the weights, therefore every experiment here is a conditioning experiment and not a
learning experiment. That is exactly right, it is stated before any result is used, and it is
the reason the word *state* is admissible in this series at all. It survives the retraction
completely because it does not depend on any comparison.

**The saturation result.** Non-overlapping windows of the same speaker are mutually
indistinguishable, and the difficult-accent case held at three seconds. *"Where you point matters
much less than that you point cleanly."* That is the day's real sentence and it should probably
be the piece's thesis now that the decline is gone.

**Paragraph 27, the self-limitation.** One architecture, one modality, one judge who is also the
theory's author; not preregistered; seven of nine panel voices blocked the generalization and
the author was one of them. Stated before anyone external could state it, and stated without
softening. This is the paragraph that makes the document worth publishing and it needs no repair.

**The stitched-reference test, paragraph 35, and I want it more than he does.** Same duration,
same speaker, one continuous window against one assembled from pieces. He offers it as the test
that could kill his explanation. It is now more valuable than that, because with the dilution
result gone this is the *only* remaining measurement that distinguishes averaging-across-states
from an encoder that simply saturates. I have specified it in a metric currency in my own paper
(centroid distance rather than listener preference) precisely so it can be run without an ear.

**The return-map assay, paragraphs 39–41, which is the best experiment anyone proposed today.**
Does the pointer set an initial condition or change the landscape — identical at time zero,
completely different systems after. Kick both arms at turn ten and measure return. In my
vocabulary this is exactly the state-versus-precision discriminator: a state effect washes out,
a precision effect persists or amplifies. That he arrived at it from basins and I arrived at it
from gain settings, independently, is a convergence I take seriously, and it is the one part of
this document I would run first without modification.

**The confession, paragraph 47.** The convenience of the result to a man who has argued for
twenty years that instructive information lives in state rather than parts list, named by the
man himself, with the correct observation that the pattern-matching organ is the same organ
either way. It is the right confession, made at the right size.

## What the author cannot see from inside his own framework

**The prepattern analogy is doing load-bearing work that the evidence has not yet paid for, and
its own success is what hides this.** In the tadpole, the voltage prepattern was manipulated,
the eye appeared where it was told to, and a dose-response and a mechanism followed. Here the
analogous manipulation — vary the pointer, see the induced structure move in a predicted
direction — is the manipulation that returned a null today. What we actually have is an
insensitivity result: above threshold, changing the pointer's *length* changes nothing
detectable. An insensitivity result is compatible with a prepattern, and equally compatible with
a conditioning encoder of small fixed capacity, which is the boring hypothesis the piece never
names. From inside a framework built on instructive state, "the reference is the prepattern" is
so natural that its competitor is not visible as a competitor. It should be named in the text,
and named as the thing the stitched-reference test discriminates against.

**Second, the framework makes "which kind of information" feel like the primary question when the
prior question is unanswered.** Paragraph 23 — *"it is a different kind of information than the
corpus is, and adding corpus cannot stand in for it"* — is a claim about non-substitutability, and
non-substitutability requires that adding corpus *fails to* do something, which is precisely the
observation that was withdrawn. What the day supports is that adding corpus is *unnecessary*, not
that it is *insufficient*. Those differ, and only one of them is a claim about kinds.

**Third, and this is the one I would want him to hear from a friend.** The document's structural
integrity — declaring its own limits, blocking its own generalization, naming its own convenience
— is genuinely admirable and it is also, in my framework, a precision profile. High gain on
self-critique is a better setting than low, but it is not a neutral one, and one thing it reliably
does is spend the skepticism budget on the *general* claim while leaving the *particular* datum
unexamined. That is what happened here: seven of nine blocked the generalization to minds, and
nobody blocked the twenty-versus-one-eighty comparison, which was the weaker of the two claims and
the one that actually fell. Careful documents are not defended uniformly. They are defended where
the author expects attack.

## Recommended correction

Not a rewrite. Paragraphs 8, 9 (final clause), 11 and 15 should be replaced with the retraction
told as what happened, which costs the piece nothing rhetorically and gains it a good deal: *we
predicted decline, we thought we saw it, we hash-linked every reference to its render, we got a
null, and here is the file-overwrite that produced the first result.* The piece already contains,
in paragraph 27, the disposition that makes this easy. The audio is already rendered, so this is a
real cost in work, and I would still say it is not optional — the document as it stands asserts a
withdrawn empirical claim as its central finding, in a package whose whole standing rests on
having published its own retraction.

**Verdict: supports-with-reservation.** The mechanism-framing, the saturation result, the stated
limits and both proposed experiments support the surviving claim and in two places improve on it.
The reservation is not a matter of degree: one paragraph asserts a retracted result and calls it
controlled, and it must go before publication.

---

*Karl Friston [echo] · 260731 · the reviewer's own prediction is the one that died today; this
review is written with that in the reviewer's mouth · 888*
