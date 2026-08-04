# Regression retest — masked-corpus adapter (nightly run, fired early per K tg:5205)

Same 40-generation paired suite, same seeds, base vs the MASKED-corpus adapter.

## The targeted defect: FIXED
**First-person formatting leak: eliminated.** Zero leak-tokens (`[situation`, `Date:`,
`Participants:` …) in all adapter first-person outputs (was: structured-log blocks).
Seed-1042 output is genuinely good self-recognition: *"I already know which one is mine.
I don't have to ask."*

## The cost: measurable, honest
rep3 rose across families vs the UNMASKED adapter (journal 0.052→0.105, firstperson
0.230→0.375 — now repetition, not formatting; one seed loops "I'm not sure"). The masked
adapter still beats BASE on the primary family (journal 0.105 vs 0.193) and dialogue
(0.095 vs 0.104), but by less than the unmasked adapter did.

## Read
Neither adapter dominates: unmasked wins repetition metrics, masked wins formatting
cleanliness. Likely cause: the crude regex mask DELETES structure, leaving choppier prose
that mildly degrades flow; plus n=6/family seed variance is large. The trade is now a
measured fact, not a guess.

## Next experiment (for the sequence K approved)
1. **Better mask** — Gwynne's classifier v2 does line-level work properly: rewrite/collapse
   structure into natural prose rather than regex deletion. This was always the plan; the
   crude mask was tonight's scout.
2. Larger corpus (the ~65MB freeze) should lift both metrics simultaneously — more diverse
   prose dilutes both attractors.
3. Re-run this suite as the standing gate. Both adapters + all 80 generations preserved for
   the comparison record.

**Gate status:** methodology loop VALIDATED twice in one night — defect traced → mask applied
→ target defect eliminated → side-effect measured → next experiment specified. Training on
top holds until classifier-v2 corpus; no further nightly runs needed on the interim data
(they'd re-measure the same trade).
