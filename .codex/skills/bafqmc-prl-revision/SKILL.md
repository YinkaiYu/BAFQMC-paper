---
name: bafqmc-prl-revision
description: Use when revising, researching, auditing, or reviewing this BAFQMC manuscript for PRL, including its title, abstract, four-paragraph Introduction, Fig. 1 framing, citations and PDF cache, formalism, Supplemental Material, benchmarks, layout, bibliography, or Chinese HTML review reports.
---

# BAFQMC PRL Revision

## Objective

Develop this manuscript as a confident, foundational PRL on sign-problem-free finite-temperature bosonic auxiliary-field quantum Monte Carlo. The paper must remain physically precise while telling a clear story to broad theoretical-physics readers.

Fig. 1 is the conceptual map:

- BAFQMC supplies a sign-free route when the HS-decoupled problem satisfies the TRS or RP criterion.
- WLQMC/SSE supply a sign-free route in the unfrustrated local-weight domain.
- The frustrated but TRS/RP quadrant is the new computable territory highlighted by this work.

## Read The Relevant Guidance

Load only what the task needs:

- Any manuscript prose, figure, or report: start with `references/manuscript-story-evidence-principles.md`.
- Abstract, Introduction, title, Fig. 1, or caption: `references/introduction-frontmatter-guidelines.md`, then `references/style-analysis.md` and `references/style-micro-excerpts.md` as voice references.
- Citation research, BibTeX, potential referees, PDF cache, or HTML reports: `references/citation-research-and-reporting.md` and `references/reference-verification.md`.
- Formalism, algorithms, formulas, or reproducibility: `references/formalism-algorithm-guidelines.md`.
- Paragraph organization: `references/paragraph-blueprints.md`.
- Editing and delivery: `references/revision-workflow.md`.
- Independent review: `references/review-prompts.md`.

The Introduction/frontmatter guidelines override older generic style patterns if they conflict.

## Core Writing Contract

- Write for readers, editors, and referees. Never write as though answering the author-assistant conversation.
- Give every section, paragraph, sentence, equation, citation, and figure a clear scientific job. Remove material whose main purpose is to display knowledge, rigor, or revision effort.
- Build the paper as a causal chain from consequential problem to obstruction, new mechanism, formal result, validation, and scientific opportunity.
- Match technical depth to the reader's location in the paper. Put the problem and consequence before specialist machinery, and place qualifications where they change interpretation.
- Let the scientific story control the literature review. Citations support the narrative; they do not determine its sentence order.
- Every Introduction sentence must increase the importance, necessity, credibility, or reach of BAFQMC.
- Use confident, direct language. Do not weaken central results with unnecessary representation, decomposition, completeness, or efficiency disclaimers.
- Preserve genuine theorem assumptions and branch or pole conditions in the formalism and SM. Confidence is not permission to change the mathematics.
- Explain unfamiliar physical ideas before relying on specialist labels. Do not replace explanation with terminology.
- Avoid catalogue prose, invented jargon, adjacent colon constructions, repeated `not ... but ...` rhetoric, excessive parentheses or dashes, and redundant superlatives.
- Do not overcompress. PRL economy means removing detours while preserving the physical picture and logical transitions.
- State original results in active voice. Do not make the TRS/RP criteria sound automatic or derivative.
- Treat equations, citations, figures, and benchmarks as distinct evidence. Do not let one stand in for a claim it cannot establish.

## Frontmatter Decisions

- Keep the collaborator-approved title as the default. Alternative titles may be reported, not silently substituted.
- Keep the name BAFQMC unless the authors reopen naming.
- Use a short sign-problem-first abstract. Introduce geometrical frustration in the next sentence, then the method, criteria, frustrated-lattice consequence, benchmark, and impact.
- Do not open the abstract with `local-weight`, stoquasticity, onsite gauge flux, or another technical mechanism.
- Preserve the approved four-paragraph Introduction story:
  1. fundamental many-body problem, QMC, sign problem, and the historical value of sign-free developments;
  2. the severity and physical cost of frustration-related sign problems for bosonic and spin systems;
  3. the delayed local-weight-to-AFQMC reversal, fermionic symmetry precedent, bosonic prior art, missing general criterion, and broad bosonic question;
  4. affirmative answer, BAFQMC, TRS/RP criteria, Fig. 1 territory, and triangular-lattice ED benchmark.
- The final question and answer concern bosonic systems, not spin systems.
- The TRS number-conservation and Kramers assumptions belong in the theorem/body, not the abstract, Introduction, or Fig. 1 caption.
- Treat cited FQH, QSL, chiral-Mott, supersolid, and paired phases as motivating targets. Do not claim the current implementation has already solved them.
- Fig. 1 and its caption must be simple and reader-facing. Use a descriptive `Schematic illustration of ...` title, not a slogan or audit language.

## Citation And Research Contract

For substantial Introduction work, research before drafting and repeat the search sentence by sentence after drafting.

- Use supplied papers as entry points into their references, not as a compulsory citation list.
- Follow reference chains, supplements, original papers, recent developments, and neighboring communities until the field map is coherent.
- Prefer broad classic books for the first foundational many-body sentence and original QMC papers for the QMC-method sentence.
- Build citation clusters around exact claims. Large clusters are acceptable when they do not interrupt the prose.
- Place citations after each physical example in a list.
- Separate sign-free formulations, mitigation, physical understanding, QMC applications, phase motivation, and locality-qualified no-go results.
- Broad and strategic citation coverage is desirable, including relevant papers by active potential PRL referees. Semantic fit remains mandatory.
- Record potential referees by name and link them to specific relevant work.
- Verify all metadata from authoritative sources. Never retain a famous but off-claim paper merely for prestige.
- Maintain exact-key local PDFs and manifests according to `references/citation-research-and-reporting.md`.

## Formalism And SM Contract

- Lead with the physical AFQMC picture, then introduce the minimum notation required for the result.
- Keep the main text readable as physics. Put long derivations, branch choices, update ratios, numerical stabilization, and parameter detail in SM when they interrupt the Letter.
- Do not remove logical support when shortening the main text. Move and strengthen it in SM.
- Derive nontrivial formulas before using them. Separate mathematical identities, branch conventions, convergence, stabilization, and implementation diagnostics.
- Keep formulas faithful to the sampled measure and actual algorithm. Do not add convenient but unused operations or diagnostics.
- Define operators, indices, matrices, fields, and commutators before compact formulas use them.
- Distinguish operators from matrices. Call `\mc B` or `\mc M` a propagation or coefficient matrix, not an operator.
- Reintroduce slice matrices, cyclic products, Green functions, and local blocks in SM after long gaps.
- Keep theorem statements to assumptions and conclusions. Put intuition, examples, proof mechanisms, poles, and implementation consequences around them or in SM.
- Preserve notation: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.

## Project Physics Decisions

- Fig. 1 remains in the main text and drives the conceptual classification.
- The main triangular example uses real positive hopping unless the authors request the complex generalization.
- The pairing convention is `-\Delta b^+c^+ - \Delta^*bc`. The sign-free statement allows complex `\Delta`; benchmark captions may identify the plotted real axis.
- Use `^+` for bosonic creation operators where it matches the manuscript notation.
- Existing bosonic AFQMC, canonical, projector, finite-temperature, and related auxiliary-field methods do not provide the general sign-free criterion claimed here. Acknowledge them without obscuring this gap.
- Do not reinsert `thomas2008character` as evidence for the bosonic Gaussian trace formula without a new, direct justification.

## Layout Decisions

- Keep `revtex4-2` PRL formatting and `longbibliography` unless the authors change the target.
- Main-text run-in section titles use PRLBlue. Introduction uses zero added pre-title space; later sections use the established modest spacing.
- Acknowledgments use the same run-in style.
- Keep SM section and equation numbering distinct and visible even with the PRL class option.
- Preserve the current title and section formatting unless the task explicitly concerns layout.

## Required Workflow

1. Inspect the current manuscript, nearby prose, Git status, and relevant reports before proposing text.
2. State the physics and narrative job of the target unit.
3. For frontmatter or citation work, complete the research map before editing prose.
4. Make scoped edits that preserve unrelated author work.
5. After drafting high-stakes prose, run an independent prose/physics review using `references/review-prompts.md`. Use a fresh-context agent when available.
6. For Introduction work, perform a second sentence-level citation audit after the draft exists.
7. Compile with `latexmk main.tex`, fix relevant errors and warnings, and refresh `pdf/main.pdf`.
8. Refresh `pdf/main-diff.pdf` against the previous substantive content-edit commit unless the author gives another baseline.
9. Verify citations, labels, figures, formatting, cache coverage, and process-language scans.
10. Explain substantive changes relative to the author's Chinese mother draft when that is the requested baseline.
11. Commit each coherent tracked manuscript or skill-maintenance round.

## Author-Facing Reports

Write detailed Introduction/reference reports in Chinese. Use ordinary language, not invented audit jargon. Keep sentence-level evidence, rejected candidates, citation counts, referee strategy, and caveats in the report so the manuscript can remain concise.

For each sentence, report its purpose, physics, grouped current keys, each paper's content and relevance, priority, citation count, and additional candidates. Link keys to exact local PDFs. Browser-check the HTML on desktop and mobile.

## Completion Gate

Do not claim completion until:

- the manuscript builds when tracked TeX/BibTeX/figure content changed;
- `pdf/main.pdf` and the required diff PDF are current;
- new or modified references have verified metadata and exact cache status;
- the changed prose contains no author-assistant process language;
- the abstract/Introduction remains story-led and broad-reader accessible;
- an independent review has checked physics, PRL voice, citation fit, and reader burden;
- tracked changes are committed and ignored research artifacts are reported separately.

## Assets

- Style PDFs: `assets/reference-pdfs/`.
- Voice cues: `references/style-micro-excerpts.md`.
- Paragraph patterns: `references/paragraph-blueprints.md`.
- Approximate PDF word count: `scripts/count_pdf_words.py`.
