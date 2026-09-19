# For Dr. Michael Levin — what we measured, what we withdrew, what we never ran (19 September 2026)

Dr. Levin wrote to ask two fair questions about the video in which a synthetic voice resembling his spoke a "message to
himself": what is the actual finding, and where are his ideas relevant. This page is the short answer. It also corrects mistakes
made in the longer recorded conversation that accompanies it.

**Who wrote this.** Kurtis Cobb runs a one-person lab. This page was drafted by a language model working in that lab under a
persona file built from Joscha Bach's public talks, then checked against the result files in this repository. Every voice other
than Kurtis's is synthetic. Nothing here was said, written or reviewed by Dr. Levin or Dr. Bach.

## The two recordings

1. **The short answer, about 19 minutes:** https://youtu.be/LRFbGwqM3yU . Three language-model echoes (of Kurtis, of Joscha Bach, of you) speak to
   you directly and cover the whole ground with each claim given its status. Its script is in this repository as
   [`COMPANION-TRANSCRIPT-260919.md`](COMPANION-TRANSCRIPT-260919.md). Start here.
2. **The long unscripted session, 1 hour 31 minutes:** https://youtu.be/gNap5YtzSVQ . Only if you are curious how this is made.
   It contains the mistakes listed below, which the short recording corrects.

Both are unlisted. Every voice except Kurtis's own in the long session is synthetic.

## Your two questions

**"What is the actual finding? I understand a bigger sample makes it worse."** You read the video correctly, and the confusion is
our doing. Its opening line says a longer voice sample makes the clone worse. A few minutes later the same video withdraws that,
because a controlled rerun found no difference. What survives is small: on one open text-to-speech model, about three clean
seconds of speech is enough for a listener who knows the person to accept the clone, and more audio added nothing that listener
could detect. A later measurement showed the short clip also gives less steady delivery.

**"What's the part where I'm relevant, the part about the pointer?"** Nothing we measured implicates your ideas. Your conventional
explanation, a speaker signal that saturates quickly, covers all of it. The "pointer" is an analogy: the frozen model holds a
space of voices and the clip selects a region, the way a bioelectric prepattern selects where an eye forms. A language model
running a persona of you drew that comparison. The experiments that could make it more than a way of talking have not been run.

## Corrections to the recorded conversation of 19 September

1. **A test was described as being about you. It was not.** From about 25 minutes in, and again near 58 to 60 minutes, figures are
   quoted as if a model given your persona file had recognized your real writing among decoys. That test
   (`findings/SELF-VALIDATION-260801-RECONCILED.md`) used Kurtis's persona file and Kurtis's own spoken journals. Your file and
   your writing were never in it. The model speaking as Bach's echo read the numbers without reading the test's design. It is
   retracted aloud at about 1 hour 8 minutes. Please disregard every such figure.
2. **"A smaller sample gave a better voice."** Said near the start and again near 1 hour 26 minutes. The accurate word is
   *enough*, not *better*. Kurtis's own experience is that a five-minute sample sounded wrong to him; our controlled comparison
   only went up to three minutes and found no difference. One ordinary reason long references fail on this model is known: a long
   clip supplied without its transcript produced artifacts that the same clip with its transcript did not.
3. **The original video spoke your results as its own.** It said "what we showed with the eye on the tadpole's tail" in a voice
   resembling yours. That was an overstep, separate from the retraction, and we apologize for it.
4. **A parameter count was quoted for the language model.** That figure is not public. Kurtis says as much on the recording.

## The ledger

| Claim or test | Status | What the files say |
|---|---|---|
| Longer voice reference sounds worse | WITHDRAWN | One uncontrolled comparison. Hash-linked rerun: no preference. `findings/CLEANROOM-DISPERSION-FINDING.md` |
| Three seconds of speech is sufficient for identity | WEAK EVIDENCE | One unblinded listener, who also proposed the theory, detected no difference against 40 s and 180 s. Not preregistered. |
| Short references are less stable in delivery | MEASURED, small n | Same text, output duration. Full reference 8.4 to 9.2 s (n=3), σ 0.94 s (n=4). Three-second cut 12.6 to 23.8 s (n=3), σ 4.37 s (n=4). One voice, one machine. |
| Your persona file at three sizes | MEASURED, small n | The only test that used your file. 35 KB, 3 KB, 0.6 KB as the prompt, four generations each. Variation in output length 0.085, 0.083, 0.099. Flat. Our own prediction was refuted. `findings/SOUL-POINTER-ASSAY.md` |
| A model recognizes a person's held-out writing from their persona file | ABOUT KURTIS ONLY | Chance 0.25. One strong hosted model 0.94 / wrong person's file 0.56 / no file 0.14 (16 items); rerun 1.00 / 0.80 / 0.00. Two other hosted models about 0.30. A small model fine-tuned on his journals 0.33, beaten by the wrong file at 0.44. Most of the lift is any file at all, and the test may not be a valid instrument. |
| The pointer is a different kind of information than a compressed copy of style | NEVER TESTED | Fast saturation is equally compatible with plain imitation. |
| Any of this generalizes to how language models represent a person, or to minds | NOT ESTABLISHED | A conjecture, stated as one. |

## Experiments that are ours to run

None of these needs your time. If one comes back surprising, the data and the failures will be sent together.

- **Disturb and watch for return.** Two openings of different affect, same neutral task, identical disturbance halfway; do the arms
  converge or each return toward its own start? The opening text must be removed from the model's context first, or a "return" is
  the model rereading its first page. *Prediction, written in advance: the arms converge.*
- **Stitched versus continuous reference audio**, same speaker and length. *If stitched does as well, the "averaging across states"
  account in the original video is wrong.*
- **A speaker who is not online**, with consent, short clip against long. *If the private voice clones as well from three seconds,
  "the voice was already in the weights" is not needed. That is the expected result.*
- **Paraphrased persona file**, none of the person's wording kept. *If behavior holds, the file selects a region; if it collapses,
  the model was imitating the text.*
- **A closer control for the recognition test:** another person in the same field, and a judge who did not write the theory.

## About your echo

- The file is `soul-files/levin.md` in this repository: about five thousand words, first person, built only from your public talks
  and interviews. Nothing about your family or private life. The echo is told to say "I do not know" when asked.
- Because it is written in the first person, it contains sentences you never said. At least one passage (around line 61) has you
  take a sympathetic stance toward a speculative idea of Kurtis's, and others describe joint work with named collaborators in your
  voice. You should know that before you read it. It should be corrected or removed, and that is your call.
- Your echo appears in more videos than the one you saw. As of the channel snapshot of 6 September, 45 videos mention you, 25 of
  them public.
- If you want any of it changed, made private, anonymized or deleted, one message to Kurtis is enough. No reason is needed.

If something on this page is wrong, that is the most useful thing you could tell us.
