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
- Do not make the main text more general than the paper actually uses. Avoid unused channel indices, optional scalar-factor caveats, or conditional language that suggests unpresented cases.
- Define physical indices, operators, and commutators before relying on compact formulas. Avoid terse "if" formulations when the method always has that structure.
- Distinguish operators from matrices in prose. Call $\mc B$ or $\mc M$ a single-particle propagation matrix or coefficient matrix, not an operator.
- Preserve notation: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.

## Formalism Rules

- In Sec. II, start from the physical HS picture: auxiliary fields decouple interactions into one-body Hamiltonians, and AFQMC samples spacetime auxiliary-field configurations.
- Use "HS transformation"; avoid invented shorthand such as "HS reduction".
- Do not spend displayed equations on notation-only definitions. Put vectors, commutators, and matrix conventions inline near their first use.
- Avoid nested main-text notation when a direct formula is readable. Prefer `W(\phi)=\Tr[\prod_\ell e^{\hat h_\ell(\phi_\ell)}]` over introducing an extra `\hat U(\phi)`.
- Define the HS measure in physical terms as the Gaussian factors actually used in the manuscript. For the current continuous-field presentation, write the direct product of real Gaussian weights rather than previewing unused field types.
- Present number-conserving BAFQMC before paired/Nambu BAFQMC. Use `W(\phi)` unless a new symbol removes real complexity.
- In the main number-conserving trace formula, omit optional scalar factors such as `\xi_\ell` unless they are active in the formula being discussed.
- Explain the bosonic determinant by comparing it with the fermionic AFQMC determinant: the bosonic formula is an inverse determinant built from `I-\mc B`. Avoid saying Bose statistics "change the sign" because that can be confused with the sign problem.
- Cite established trace-formula sources when a formula is known from prior bosonic AFQMC literature, and use SM for this manuscript's derivation or convention.
- For Nambu formulas, state the normal-ordering constant explicitly. In this manuscript it enters through `\xi_\ell(\phi_\ell)` and can affect update ratios even though it is absent from the propagation matrix.
- Keep metaplectic branch choices, Nambu Green functions, and update-ratio derivations in SM unless the author explicitly asks for them in the main text.
- Avoid forward references from the main body to later main-text sections. Cite SM for derivations.

## Supplemental Material Rules

- Organize detailed formalism from simple to general: HS transformation, number-conserving trace formula, number-conserving Green functions, number-conserving local update, then paired/Nambu formulas.
- Give concrete HS examples for attractive and repulsive density channels, including the benchmark decoupling, before abstract implementation details.
- Include update ratios for the number-conserving case before paired/Nambu update ratios.
- Keep derivations rigorous and followable in SM. Do not compress algebraic steps so aggressively that a reader cannot reproduce identities such as `a U = U \mc B a`, Green-function relations, determinant ratios, or branch choices.
- In SM, explain Metropolis importance sampling as a ratio of the full auxiliary-field measure. Include every factor that changes under a proposal: determinant or square-root determinant ratio, HS Gaussian ratio, and any normal-ordering/scalar-constant ratio.
- For paired/Nambu updates, describe the metaplectic branch as a continuous branch fixed from a known reference configuration. Keep this at the physical algorithm level; do not import code-internal storage variables or implementation-specific names unless the user explicitly asks.
- Use the one-column SM width. Avoid line breaks and `aligned` environments whose only purpose is saving two-column space; keep multi-line equations only when they clarify a derivation or a large block matrix.
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
