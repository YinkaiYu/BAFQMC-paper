# Introduction And Frontmatter Guidelines

Use this file for the title, abstract, Introduction, Fig. 1, its caption, or any report that evaluates them. It applies the general method in `manuscript-story-evidence-principles.md` to the current frontmatter. These are author-approved narrative constraints, not a request to preserve every current sentence forever.

## Governing Principle

The Introduction exists to make the paper's result feel important and inevitable. Literature review is evidence, not the organizing principle. Every sentence must advance the BAFQMC story by doing at least one of the following:

- broaden the physical stakes;
- intensify the computational obstruction;
- prepare or execute the conceptual reversal;
- establish a successful precedent for symmetry-protected QMC;
- isolate the missing bosonic principle;
- state the result, its reach, or its validation.

Do not turn the Introduction into a taxonomy of neighboring methods or terminology. A correct mini-review can still be a bad Introduction if it interrupts the story.

## Audience And Confidence

- Write for broad PRL readers first, then QMC specialists. Introduce unfamiliar ideas before relying on them.
- Use confident, direct claims. The work is a foundational and important advance.
- Do not add defensive qualifiers merely to display rigor. Put theorem assumptions and genuine limitations where readers need them in the formalism or SM.
- In ordinary field usage, a model is called sign-problem-free when a sign-free formulation exists. Do not repeatedly add phrases such as `in a chosen representation or decomposition` in the abstract or Introduction.
- Do not claim that BAFQMC has already solved the FQH, QSL, chiral-Mott, supersolid, or paired-superfluid models cited as motivation. It is acceptable to present them as long-standing targets that the new route may help unlock.
- The title is collaborator-approved and remains the default. Keep the name BAFQMC unless the authors revisit it.

## Abstract

Use a short sign-problem-first arc:

1. The sign problem limits numerically exact QMC.
2. Geometrical frustration makes the barrier acute for interacting bosons.
3. State the sign-problem-free finite-temperature BAFQMC method and the TRS/RP sufficient conditions.
4. State that the route remains sign-free on frustrated lattices where WLQMC/SSE remain sign-problematic.
5. Give the triangular-lattice finite-temperature ED benchmark.
6. End with a strong but supportable expansion-of-reach statement.

The first two sentences should be short and forceful. Do not begin with `local-weight`, `stoquastic`, onsite gauge flux, local matrix-element signs, or another specialist mechanism. Those details repel broad readers before the result appears. Geometrical frustration is the motivating pressure point, not the paper's entire subject.

Do not put the number-conserving scope of the TRS theorem in the abstract. Do not end with an unsupported slogan such as symmetry becoming the universal organizing principle of all exact simulations or the work reshaping the whole field.

## Four-Paragraph Introduction

Preserve this architecture unless the authors explicitly approve a new story.

### Paragraph 1: Many-Body Physics, QMC, And The Sign Problem

Open with one short sentence that places interacting quantum many-body systems among the basic challenges of modern physics. Classic, broad textbooks are appropriate here.

Then introduce QMC with original method papers rather than another textbook cluster. The established local pattern is a broad set spanning determinant/auxiliary-field, projector, world-line/worm, and SSE traditions, with BSS, Scalapino--Sugar, Hirsch, Sugiyama--Koonin, Prokofev, and Sandvik as representative anchors.

Explain QMC and the sign problem step by step for non-specialists:

1. QMC rewrites the partition function as a configuration sum or integral.
2. Importance sampling explores an exponentially large configuration space.
3. This requires nonnegative probabilistic weights.
4. Negative or complex weights lead to cancellations.
5. Resolving those cancellations typically costs exponentially more effort.
6. No generic polynomial-time cure is expected, while important physical classes can avoid or mitigate the problem.

End by pre-establishing the value of this paper. The intended logic is that QMC's continuing impact rests on the ongoing development of sign-problem-free formulations and a deepening physical understanding of the sign problem. This sentence can carry broad citation clusters covering:

- major physical achievements enabled by QMC;
- sign-problem-free formulations for important models;
- work that deepens understanding of the sign problem;
- methods that avoid or mitigate it.

Use `ongoing development`, not `repeated discoveries`.

### Paragraph 2: Make The Bosonic/Spin Barrier Severe

State the familiar field-level association between geometrical frustration and the sign problem in bosonic or spin systems. Explain the intuitive closed-loop incompatibility of off-diagonal hopping or exchange signs without turning the paragraph into a stoquasticity lecture.

Recognize exceptional bases, clusters, or regroupings in one compressed clause, then return immediately to the broad obstruction. This paragraph should emphasize:

- most frustrated bosonic and spin systems still lack sign-problem-free QMC formulations;
- some chiral topological classes have locality-qualified intrinsic-sign obstructions;
- the barrier blocks unbiased large-scale access to important quantum matter.

List motivating phenomena with citations attached immediately to each example, not one undifferentiated citation pile at the end. Suitable categories include bosonic FQH states, frustrated supersolids, chiral Mott phases and bosonic DQCPs, multiparticle or paired superfluids, and QSLs.

Do not introduce the phrase `conventional local-weight picture` in this paragraph. The delayed explanation is the dramatic turn at the start of paragraph 3. Do not spend the paragraph praising special-case cures; they are acknowledged for fairness, while the narrative purpose is to establish the scale of the unresolved problem.

### Paragraph 3: Reverse The Local-Frustration Consensus

Open with a clear reversal. The apparent identification of frustration with the sign problem hides an assumption: WLQMC and SSE assemble sampled weights from local matrix elements.

Contrast this with a method usually associated with interacting fermions. AFQMC first decouples interactions with auxiliary fields, traces out the original quantum degrees of freedom at fixed fields, and samples the resulting global Gaussian or determinant weight. This physical picture must be explicit. It explains why local matrix-element frustration no longer dictates the global sign.

Then establish the fermionic precedent:

- fermionic determinants can still be negative;
- global symmetries of the decoupled Hamiltonian can protect positivity;
- TRS, RP, and related structures provide sign-free routes;
- these criteria enabled extensive large-scale fermionic QMC physics.

The last point is a useful place for a broad, purposeful cluster of major applications and active colleagues. Keep it as one compact success statement rather than a catalogue of subfields.

Return to bosons and state the historical gap plainly. Bosonic AFQMC and related auxiliary-field methods exist, including projector, finite-temperature, canonical, and static-cluster lines. They did not provide a general sign-problem-free criterion. When negative or complex weights arise, exact work is limited to small systems or larger simulations require biased approximations. Do not bury this simple novelty statement under unnecessarily narrow qualifiers.

End with a broad question about using Hamiltonian symmetries to solve the sign problem in bosonic systems. Do not mention AFQMC or spin in the question itself.

### Paragraph 4: Answer And Deliver

Begin with `The answer is affirmative.` or an equally direct answer. Then state:

1. the finite-temperature BAFQMC method;
2. TRS and RP as two general sufficient conditions for nonnegative configuration weights;
3. the frustrated sign-free territory summarized by Fig. 1;
4. the resulting route toward unbiased simulations of frustrated bosonic matter;
5. the triangular two-flavor Bose-Hubbard benchmark and finite-temperature ED agreement.

Do not add number-conserving or Kramers details here. The theorem statement in the body carries that scope. Do not weaken the contribution with unnecessary efficiency, completeness, or sampling disclaimers.

## Fig. 1 And Caption

- Fig. 1 is a simple conceptual schematic for readers who may jump directly from the abstract.
- Use a neutral descriptive title such as `Schematic illustration of ...` rather than a campaign slogan.
- Define the frustration axis, the TRS/RP criterion axis, the BAFQMC half-plane, the WLQMC/SSE half-plane, and the two important upper quadrants.
- Keep the image and caption intuitive. A schematic need not carry every theorem caveat.
- Do not use audit language such as `certified`, or defensive text such as `does not classify all formulations or guarantee efficient sampling`.
- Do not insert wording that sounds tailored to an author's private request. Readers do not know the revision conversation.
- The TRS number-conservation assumption belongs in the theorem and body, not this caption.

## Language And Rhythm

- Prefer short, concrete sentences at conceptual turning points.
- Avoid repeated superlatives such as `some of the most` followed by `among the most`.
- Avoid inflated adjectives such as `unrivaled` when `powerful` or a direct factual claim suffices.
- Minimize parentheses and dashes. Prefer a normal sentence when the information matters.
- Avoid conspicuous colon constructions in adjacent paragraphs and repeated `not ... but ...` rhetoric.
- Avoid invented phrases that have no established reader meaning, such as `frustrated local dynamics`.
- Do not compress so aggressively that transitions become abrupt or the physical picture disappears.
- Do not expand by listing specialist terms. Add explanatory steps or physical consequences instead.

## Final Reader Test

For every sentence, ask:

1. What does a broad reader learn before encountering specialist terminology?
2. How does this sentence increase the importance, necessity, credibility, or reach of BAFQMC?
3. Could the same citation evidence be carried without interrupting the story?
4. Does the sentence belong in the paper without knowledge of the author-assistant conversation?

If the sentence mainly proves that the writer surveyed the literature, rewrite or remove it.
