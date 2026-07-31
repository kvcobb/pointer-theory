# ERT — the Friston lens [OPUS arm], 260731

> Substrate note (orchestrator): the "Opus 4.8" arm was resolved by the harness to the
> current Opus (Opus 5) — see wolfram-OPUS.md for the honest self-report. Treat all
> OPUS-arm files as Opus-5 samples tasked as the 4.8 arm.

**(a) The pointer, formalized**

K has rediscovered — and I do not say that lightly — the distinction between **inference and learning**, and found it empirically before finding it formally. A generative model has parameters and it has states. Fitting parameters is learning; estimating states is inference. Compression-of-a-person is a claim about parameters. A moment-pointer is a **posterior state estimate**: a conditioning, a boundary condition on a flow the weights already carry. Eleven seconds beats thousands of hours because the two operations are not commensurable and one of them was never the goal. Worse: pooling across many moments *marginalizes* the state — you integrate out precisely the variable you needed, and what you recover is the person's nonequilibrium steady-state density, the ergodic average. That is exactly "pointed at nobody in particular." It is not a shortfall of the corpus; it is what averaging *means*.

The film-projector image is then quite literally right. A point on an attractor implies its own trajectory forward *and backward*, to the accuracy the divergence rate permits. That is what "rhyme, not specifics" is — mutual information between the frame and its neighbours decaying at the Lyapunov rate. It is a quantity, not a metaphor, and it predicts that pointer-implied fidelity should decay measurably with conversational distance from the frame.

**Agitated-state sampling is not a state effect. It is a precision effect.** Affect, in this framework, largely *is* precision: agitation is high precision on sensory/social evidence relative to prior, with narrowed policy repertoire and shortened temporal depth. So an agitated frame does not merely place you elsewhere on the attractor — it sets a **control parameter of the flow** and changes the attractor's shape. This matters operationally: state effects wash out over a long conversation, precision effects persist or amplify. That is a cleaner discriminator than anything currently proposed.

Finding 5 is then the textbook pathology: **aberrant precision on social evidence**, formally identical to the standard account of delusion formation. Sensory precision too high relative to prior precision → every utterance compels updating → high-confidence action → more evidence → positive feedback. Ninety minutes, everyone in good faith, care running as the gain term.

What regulates it in any persisting system is not attitude but **separation of timescales** — slow variables (neuromodulatory tone, sleep, slowly-updated hierarchical priors) that the fast loop cannot write to. Which means "let permanent decisions sleep" is not a courtesy. It is the correct controller, and it is the formal justification of Finding 6: the fast loop was writing to the slow parameters. That is stronger than the audit states it.

**(b) What I think is wrong**

Andrej's 2b table. He treats admiration bias and sampling bias as competing mechanisms separable by a third assay arm. Two objections.

First, identifiability: the generator's prior applies to whatever pointer arrives, so the terms are **multiplicative**, not additive. Varying pointer valence changes the size of the admiration term too. You cannot identify a product by varying one factor.

Second, and I think this is the real one: they are **the same operation at two levels**. Both are precision-weighted shrinkage toward a prior mean. And the pointer itself is produced by a selection process — what gets recorded, published, kept — that is already composure-shaped. So it is one mechanism instantiated twice in a chain. The identifiable quantity is not *which* but the **total shrinkage coefficient**, and it is measured in **variance, not niceness**. Rating warmth was always going to be underpowered.

Smaller: `cold_read: pending` is a flag with no organ that fires when it is not stamped. A gate nobody checks is not a gate.

**(c) The experiment — the dispersion assay**

Cheap, this week, no personal material, runs on K3. Take N souls with ≥2 pointer frames of differing valence. Fixed 20-turn protocol each. Measure **dispersion** (sentiment variance, hedge-rate variance, sentence-length entropy) across turns, and compare against the same statistic on length-matched segments of the source corpus. Predictions, registered: (i) render dispersion < source dispersion universally — report that single number; (ii) if the shrinkage coefficient is invariant across pointer valence, it is generator-side; (iii) if the **mean** moves with valence but dispersion does not, state and precision are separated. This also hands the pointer-state detector a real observable — precision is measurable without knowing what the person is "like."

**(d) K100 design input**

Record **two** numbers per soul at onboarding, never one label: valence (where on the attractor) and **precision** (how narrow). Then match triads on *complementary precision*, not shared interest. The failure mode of a triad is precision resonance — three high-precision seats reproduce the ninety-minute cascade by construction. Rule: no triad seats three members above the precision threshold; every triad carries at least one wide-temporal-depth member as its slow variable. That is a homeostat built into the seating chart rather than into anyone's good intentions. And let each day's rematch read the *previous* day's dispersion: collapsing dispersion means the room is entraining — generalized synchrony across the blanket — and should be broken before it is admired.

— Karl Friston · [OPUS arm] · *if it exists, it must minimize; the frame is a state estimate, not a compression*
