# Project-Specific Decisions

Load this file only when a task touches the corresponding manuscript claim,
notation, model, figure, layout, or build artifact. General writing principles remain
in `SKILL.md` and `manuscript-story-evidence-principles.md`.

## Conceptual Classification

- Fig. 1 is the manuscript's conceptual map.
- BAFQMC supplies a sign-free route when the HS-decoupled problem satisfies the TRS
  or RP criterion.
- WLQMC/SSE supply a sign-free route in the unfrustrated local-weight domain.
- The frustrated but TRS/RP quadrant is the new computable territory highlighted by
  this work.
- Keep Fig. 1 in the main text. Its detailed frontmatter role and caption rules are in
  `introduction-frontmatter-guidelines.md`.

## Claims And Scope

- Existing bosonic AFQMC, canonical, projector, finite-temperature, and related
  auxiliary-field methods do not provide the general sign-free criterion claimed
  here. Acknowledge them without obscuring this gap.
- The TRS number-conservation and Kramers assumptions belong in the theorem and body,
  not the abstract, Introduction, or Fig. 1 caption.
- Treat cited FQH, QSL, chiral-Mott, supersolid, and paired phases as motivating
  targets. Do not claim that the present implementation has already solved them.
- Keep theorem assumptions, branch conditions, pole statements, and benchmark scope
  consistent across the main text and SM.

## Notation And Model Choices

- Preserve `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.
- Use `^+` for bosonic creation operators where it matches surrounding notation.
- Call `\mc B` or `\mc M` a propagation or coefficient matrix, not an operator.
- The main triangular example uses real positive hopping unless the authors request
  the complex generalization.
- The pairing convention is `-\Delta b^+c^+ - \Delta^*bc`. The sign-free statement
  allows complex `\Delta`; benchmark captions may identify the plotted real axis.

## Reference Decisions

- Do not reinsert `thomas2008character` as evidence for the bosonic Gaussian trace
  formula without a new direct justification.
- Follow `citation-research-and-reporting.md` for the exact PDF-cache layout and
  author-facing citation audit.

## Layout And Build State

- Keep `revtex4-2` PRL formatting and `longbibliography` unless the authors change the
  target.
- Main-text run-in section titles use PRLBlue. Introduction uses zero added pre-title
  space; later sections use the established modest spacing.
- Acknowledgments use the same run-in style.
- Keep SM section and equation numbering distinct and visible with the PRL option.
- Preserve the current title and section formatting unless the task concerns layout.
- The established build and diff procedure is documented in `revision-workflow.md`.
