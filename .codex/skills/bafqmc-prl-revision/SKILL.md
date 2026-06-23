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
5. When adding algorithmic or benchmark-reproducibility details, inspect the corresponding implementation and run reports first. Translate what you learn into physics-algorithm prose and equations; do not expose code-internal names unless they are necessary for reproducibility.

## Writing Rules

- State positive claims directly. Avoid unnecessary "not ... but ..." logic.
- Minimize dashes.
- Do not insert process-facing sentences that answer the author’s prompt or advertise a revision.
- Use reference Letters as tone and rhythm models only; do not import their physics claims.
- Keep the main text readable as physics. Move derivations, branch-choice details, update ratios, and numerical parameters to SM when they interrupt the story.
- When main-text material is shortened, preserve or expand the removed logical detail in SM if it supports a formula, branch choice, update ratio, or numerical claim. Do not make the total manuscript less reproducible by moving fast in the main text.
- Do not make the main text more general than the paper actually uses. Avoid unused channel indices, optional scalar-factor caveats, or conditional language that suggests unpresented cases.
- Avoid forward references from an early section to later benchmark choices unless the reader has already met that object. Early formalism should cite SM for derivations and examples, not preview later narrative steps.
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
- Describe particle-number conservation as a property of the one-body evolution being considered, not as a decoupling class that implies unused alternatives.
- In the main number-conserving trace formula, omit optional scalar factors such as `\xi_\ell` unless they are active in the formula being discussed.
- Explain the bosonic determinant by comparing it with the fermionic AFQMC determinant through the two concrete differences: `I+\mc B` becomes `I-\mc B`, and the determinant appears in the denominator. Avoid saying Bose statistics "change the sign" because that can be confused with the sign problem.
- Cite established trace-formula sources when a formula is known from prior bosonic AFQMC literature, and use SM for this manuscript's derivation or convention.
- For Nambu formulas, track scalar normal-ordering factors separately from matrix products and include those scalar factors in update ratios when they change under a proposal.
- Introduce Nambu formulas as needed by a stated pairing term in `\hat h_\ell`; do not start a paragraph with an unexplained technical requirement.
- Keep metaplectic branch choices, Nambu Green functions, and update-ratio derivations in SM unless the author explicitly asks for them in the main text.
- Avoid forward references from the main body to later main-text sections. Cite SM for derivations.

## Supplemental Material Rules

- Organize detailed formalism from simple to general: HS transformation, number-conserving trace formula, number-conserving Green functions, number-conserving local update, then paired/Nambu formulas.
- Give concrete HS examples for attractive and repulsive density channels, including the benchmark decoupling, before abstract implementation details.
- Include update ratios for the number-conserving case before paired/Nambu update ratios.
- Keep derivations rigorous and followable in SM. Do not compress algebraic steps so aggressively that a reader cannot reproduce identities such as `a U = U \mc B a`, Green-function relations, determinant ratios, or branch choices.
- Avoid phrases such as "repeating the same manipulation" when the omitted step is needed to check a formula. Write the determinant factorization, branch continuation, and local-block reduction explicitly.
- Do not introduce intermediate symbols unless they remove real complexity. A one-use symbol that hides the object the reader must evaluate usually increases the burden.
- In SM, explain Metropolis importance sampling as a ratio of the full auxiliary-field measure. Include every factor that changes under a proposal: determinant or square-root determinant ratio, HS Gaussian ratio, and any normal-ordering/scalar-constant ratio.
- In sign-free Metropolis formulas, write the physical acceptance ratio as a real nonnegative quantity and avoid unnecessary absolute values. If finite-precision code represents a sign-free ratio as complex, discuss phase monitoring or branch diagnostics separately from the mathematical acceptance formula.
- For paired/Nambu updates, describe the metaplectic branch through local continuation from the identity update for each proposal. State benchmark-specific pole-distance and phase diagnostics separately, and keep the discussion at the physical algorithm level.
- For implementation-backed benchmark details, include the HS fields used, initialization distribution, local proposal distribution and widths, warmup procedure, stabilization cadence, production statistics, and exact-diagonalization truncation checks when available.
- When a benchmark uses conjugate reflected sectors, spell out the algorithmic consequence in SM: determinant ratios, Green functions, and local updates can be evaluated in one sector and reconstructed by complex conjugation in the partner sector.
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
