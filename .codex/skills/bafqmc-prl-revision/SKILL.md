---
name: bafqmc-prl-revision
description: Use when revising this BAFQMC manuscript toward PRL style, especially Section II formalism, Supplemental Material restructuring, Section IV benchmarks, Introduction/Fig. 1 framing, references, or post-edit review.
---

# BAFQMC PRL Revision

## Core Principle

This project is organized around the Fig. 1 sign-problem classification:
BAFQMC is sign-free in the RP/TRS half-plane; SSE/WLQMC are sign-free in the unfrustrated half-plane; the frustrated but RP/TRS quadrant is the new computable territory.

Write the manuscript as a Letter that makes this classification, the RP/TRS criteria, and the two benchmark figures immediately clear to theoretical-physics readers.

## Required Workflow

1. Before drafting or rewriting, read the relevant reference:
   - Style and reference-letter voice: `references/style-analysis.md`.
   - Sentence patterns and style cues: `references/style-micro-excerpts.md`.
   - Paragraph structure patterns: `references/paragraph-blueprints.md`.
   - Revision procedure and review loop: `references/revision-workflow.md`.
   - Citation additions: `references/reference-verification.md`.
   - Independent review prompts: `references/review-prompts.md`.
2. For high-stakes prose, especially the Introduction, run an `opencode` prose review after a draft exists.
3. After each substantive manuscript-edit round, request a fresh independent-context agent review using the prompts in `references/review-prompts.md`. Require findings first, concrete corrections, and file/line references where possible.
4. Compile with `latexmk main.tex` before claiming manuscript edits are complete. Refresh the diff PDF against the previous substantive content-edit version unless the user specifies another baseline.

## Writing Rules

- State positive claims directly. Avoid unnecessary "not ... but ..." logic.
- Minimize dashes.
- Do not insert process-facing sentences that answer the author’s prompt or advertise a revision.
- Use reference Letters as tone and rhythm models only; do not import their physics claims.
- Keep the main text readable as physics. Move derivations, branch-choice details, update ratios, and numerical parameters to SM when they interrupt the story.
- Preserve notation: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.

## Formalism Rules

- In Sec. II, start from the physical HS picture: auxiliary fields decouple interactions into one-body Hamiltonians, and AFQMC samples spacetime auxiliary-field configurations.
- Use "HS transformation"; avoid invented shorthand such as "HS reduction".
- Do not spend displayed equations on notation-only definitions. Put vectors, commutators, and matrix conventions inline near their first use.
- Avoid nested main-text notation when a direct formula is readable. Prefer `W(\phi)=\Tr[\prod_\ell e^{\hat h_\ell(\phi_\ell)}]` over introducing an extra `\hat U(\phi)`.
- Define the HS measure in physical terms as products of Gaussian factors from the HS transformation.
- Present number-conserving BAFQMC before paired/Nambu BAFQMC. Use `W(\phi)` unless a new symbol removes real complexity.
- In the main number-conserving trace formula, omit optional scalar factors such as `\xi_\ell`; state once that scalar factors are absorbed into the HS weight when present, and leave the detailed convention to SM.
- Explain the bosonic determinant by comparing it with the fermionic AFQMC determinant: the bosonic formula has `I-\mc B` and the inverse determinant.
- Keep metaplectic branch choices, Nambu Green functions, and update-ratio derivations in SM unless the author explicitly asks for them in the main text.
- Avoid forward references from the main body to later main-text sections. Cite SM for derivations.

## Supplemental Material Rules

- Organize detailed formalism from simple to general: HS transformation, number-conserving trace formula, number-conserving Green functions, number-conserving local update, then paired/Nambu formulas.
- Give concrete HS examples for attractive and repulsive density channels, including the benchmark decoupling, before abstract implementation details.
- Include update ratios for the number-conserving case before paired/Nambu update ratios.
- Keep derivations rigorous in SM, but avoid duplicating model motivation or benchmark narrative from the main text.

## Project Decisions

- Fig. 1 remains in the main text and drives the story.
- The Section IV example should initially use real positive triangular hopping, matching the benchmark.
- The Section IV pairing term should use the Hermitian negative-sign convention: `-\Delta b^+c^+ - \Delta^*bc`. The sign-free claim allows arbitrary complex `\Delta`; benchmark captions may specify the plotted real `\Delta` axis.
- The expected diff baseline is the previous commit with substantive manuscript-content edits.

## Assets

- Reference-paper PDFs are in `assets/reference-pdfs/`.
- Short style micro-excerpts and sentence patterns are in `references/style-micro-excerpts.md`.
- Paraphrased paragraph blueprints are in `references/paragraph-blueprints.md`.
- Approximate word-count helper: `scripts/count_pdf_words.py`.
