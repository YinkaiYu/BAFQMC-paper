# Style Analysis Of Reference Sign-Problem-Free QMC Letters

Use this file when drafting, condensing, or reviewing main-text prose. The papers are style models, not physics templates. Mimic their confidence, economy, and rhythm while preserving the BAFQMC manuscript's own Fig. 1 classification and bosonic claims.

## Length And Page Rhythm

Approximate text counts from local arXiv PDFs:

| Paper | Pages in PDF | Main-text cut marker | Approx. words before marker | Use for |
| --- | ---: | --- | ---: | --- |
| arXiv:1408.2269 / PRB 91, 241117(R) | 7 | Acknowledgement | 3738 | Rapid Communication pacing with explicit algorithm and examples. |
| arXiv:1506.05349 / PRL 115, 250601 | 7 | Acknowledgements | 3677 | "Guiding principle" rhetoric and compact theorem-to-model flow. |
| arXiv:1601.01994 / PRL 116, 250601 | 8 | Acknowledgments | 3655 | Two sufficient conditions stated early, examples following. |
| arXiv:1601.05780 / PRL 117, 267002 | 8 | Acknowledgement | 3765 | Classification principle, table/figure guided narrative, concise conclusion. |

Implication: do not overcompress this manuscript to a skeletal 3000-word draft. Aim for a compact 4.5--5 page main text where the reader can follow motivation, formulas, criteria, and benchmarks without opening SM.

## Common Introduction Pattern

The introductions usually move in this sequence:

1. Name a broad computational obstacle in one sentence.
2. State why it matters physically, often with several literature citations in one compact sentence.
3. Identify the limitation of existing sign-free principles or algorithms.
4. Introduce a new representation, symmetry, or classification principle.
5. State what is proven and what new model territory follows.
6. Move quickly to the core formula, table, schematic, or model.

For this manuscript:

1. Start from bosonic/spin QMC and sign-free domains.
2. Introduce the RP/TRS versus frustration classification in Fig. 1.
3. Explain that BAFQMC gives the RP/TRS half-plane.
4. Emphasize the upper-left quadrant, frustrated but RP/TRS, as the new computable territory.
5. Then state BAFQMC weight formulas, criteria, and triangular benchmarks.

Avoid starting with a generic QMC tutorial. The reader should reach the new classification quickly.

## Per-Paper Style Notes

### arXiv:1408.2269 / PRB Rapid

Main voice:

- Opens with a direct discovery claim and immediately names the method.
- Uses a concrete model quickly to show that the method is operational.
- Alternates between algorithmic formulas and sign-free consequences.
- Uses short transitions such as "To explicitly illustrate..." and "Similarly..." to move from principle to construction.

What to emulate:

- Confidence in naming the method and its domain.
- Fast movement from conceptual statement to Hamiltonian and weight.
- Clear statement that the method handles finite-temperature and projector variants when true.

What to avoid:

- The phrase "In this paper" can sound old-fashioned; use sparingly.
- Do not overuse "Especially" or "Moreover" when a direct sentence is cleaner.

### arXiv:1506.05349 / PRL

Main voice:

- Frames the result as a "guiding principle".
- Introduces a mathematical structure, then immediately explains how it guides sign-free simulation design.
- Uses compact proof logic: a determinant property, then an application to QMC weights.
- Connects the criterion to multiple algorithms and models without expanding every case.

What to emulate:

- Use "principle", "criterion", "guideline", and "matrix structure" in a disciplined way.
- State the abstract condition before the examples.
- Keep proof sketches compressed.

What to avoid:

- The paper sometimes uses contrastive rhetoric. In this manuscript, prefer direct positive classification.

### arXiv:1601.01994 / PRL

Main voice:

- Begins with the sign problem as the obstacle, then introduces a new perspective.
- States "two sufficient conditions" early.
- Uses theorem-like structure, but the main flow still keeps examples close to the criteria.
- The tone is rigorous and categorical: conditions are proven, model classes follow.

What to emulate:

- Early declaration of the two positivity mechanisms.
- Clear naming of the two mechanisms.
- Examples that are framed as new sign-free regions, not as exhaustive phase studies.

What to avoid:

- Do not make the main text feel like a theorem/proof document. For this BAFQMC manuscript, theorem-level details should be in SM.

### arXiv:1601.05780 / PRL

Main voice:

- Opens with a fundamental open issue.
- Presents a classification principle.
- Uses a compact table and symmetry classes as a reader-facing map.
- Ends by explaining why the classification enlarges the sign-free landscape.

What to emulate:

- Fig. 1 should function like the table/classification in this paper.
- Make the classification visible early and return to it when discussing examples.
- Use "systematic classification" and "principle" only when the surrounding text states what is classified and why it matters.

What to avoid:

- Do not import the Majorana periodic-table logic into the bosonic paper. The analogy is rhetorical, not conceptual content for this manuscript.

## Introduction Blueprint For This Manuscript

Use this skeleton when rewriting the Introduction:

1. **Obstacle and domain.** One compact paragraph on sign-free QMC for bosons/spins and why sign structure controls access to frustrated quantum matter.
2. **Classification map.** Introduce Fig. 1 as a classification by RP/TRS and frustration. State the two sign-free half-planes.
3. **Gap.** Explain that bosonic AFQMC needs a Gaussian trace formula and positivity criteria, including paired/Nambu formulations and pole control.
4. **This work.** State finite-temperature BAFQMC, number-conserving TRS, RP including paired fields, and triangular benchmarks.
5. **Significance.** Identify the upper-left quadrant as the new computable territory and connect it to the benchmark model.

Each paragraph should have one purpose. Avoid a final roadmap paragraph unless it improves readability.

## Tone And Sentence Habits

The reference papers use direct, high-confidence claims:

- "We present..." and "we show..." rather than apologetic or procedural language.
- "This provides..." to connect a theorem to a computational consequence.
- "A class of..." to make a broad result concrete.
- "The key observation..." before a short mathematical condition.
- "As shown in the Supplemental Material..." sparingly, after the main result is already understandable.

Useful tone for this manuscript:

- "The classification in Fig. 1 separates two sign-free mechanisms for bosonic simulations."
- "BAFQMC makes the upper half-plane accessible whenever the HS-decoupled propagators satisfy RP or TRS."
- "The triangular-lattice benchmarks test the frustrated RP/TRS quadrant directly."
- "The paired benchmark probes the same sign-free principle in Nambu space."

Avoid:

- "In response to this issue..." or any collaboration-process wording.
- Overexplaining what the reader supposedly believes.
- Repeated "not ... but ..." constructions.
- Long strings of dashes.

## Common Adjectives And Nouns

The useful vocabulary is restrained and technical:

- adjectives: fundamental, general, rigorous, sufficient, efficient, explicit, systematic, sign-free, frustrated, interacting, unbiased, exact, auxiliary-field, finite-temperature, nonnegative
- nouns: principle, criterion, classification, representation, symmetry, decomposition, determinant, weight, propagator, benchmark, model class, territory, mechanism
- verbs: formulate, establish, prove, identify, classify, demonstrate, benchmark, extend, guarantee, reveal, open

For this manuscript, prefer "classification", "criterion", "sign-free route", "computable territory", "nonnegative weight", and "HS-decoupled propagator" over vague terms such as "interesting", "novel idea", or "powerful method".

## Common Sentence Shapes To Imitate

- Broad obstacle: "The sign problem remains a central obstacle for unbiased simulations of ..."
- Principle statement: "We identify a symmetry criterion under which the configuration weight is nonnegative."
- Classification statement: "The resulting classification separates the BAFQMC sign-free domain from the local-weight sign-free domain."
- Formula setup: "For a fixed auxiliary-field configuration, the bosonic degrees of freedom can be traced exactly, giving ..."
- Criterion-to-model bridge: "This condition is imposed after HS decoupling and is therefore directly testable in the one-body propagators."
- Benchmark bridge: "We demonstrate the construction on a frustrated two-flavor Bose-Hubbard model on the triangular lattice."

Avoid sentence shapes that sound like revision commentary:

- "To address the concern..."
- "We now rewrite..."
- "This section has been shortened..."
- "As requested..."

## Section Flow To Emulate

The reference Letters do not give every proof step in the main text. Their flow is:

- Motivation and principle.
- Minimal algebraic object.
- Main condition.
- One-paragraph proof sketch or consequence.
- Model/example.
- Numerical or conceptual validation.
- Brief limitations/outlook.

For this manuscript:

- Section II should be formula-first: `Z`, number-conserving weight, paired weight, basic Green function.
- Section III should state TRS/RP criteria and give only the physical proof sketch.
- Section IV should read as the model and benchmark realization of Fig. 1's upper-left quadrant.
- Concluding Remarks should summarize the new classification and finite-temperature pole limitation without turning into a methods paper.

## Figure And Table Style

The reference papers often use one conceptual table/figure to carry the principle. Fig. 1 should play that role here.

Use Fig. 1 in the prose as the map, not as decoration:

- First mention: define axes and sign-free half-planes.
- Later mention: identify the upper-left quadrant as the target of the benchmarks.
- Final mention if useful: state that RP/TRS provide a constructive route into that quadrant.

## Typical Paragraph Length

The extracted arXiv text often has long OCR paragraphs because of PDF formatting, but the conceptual rhythm is short:

- Intro paragraphs: one idea each.
- Criteria paragraphs: statement, formula, consequence.
- Example paragraphs: model, sign-free reason, observable/baseline.

In this manuscript, prefer 5--8 sentence paragraphs for the Introduction and 3--5 sentence paragraphs inside technical sections.

## Common Failure Modes To Catch

- Replacing Fig. 1's classification with an inaccurate slogan about frustration.
- Explaining all algebra before the reader knows why the result matters.
- Moving all caveats into the main text and losing the Letter story.
- Describing benchmark plots as a numerical report rather than proof-of-principle evidence.
- Adding references without verifying metadata.
