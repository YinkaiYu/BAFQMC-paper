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

1. Before drafting or rewriting, read only the reference files relevant to the task:
   - PRL voice and paragraph shape: `references/style-analysis.md`, `references/style-micro-excerpts.md`, `references/paragraph-blueprints.md`.
   - Section II, SM derivations, algorithms, and reproducibility: `references/formalism-algorithm-guidelines.md`.
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
- Open each section by naming the new physics or algorithmic question it answers. Do not begin by restating a result from the previous section unless the restatement is needed for the transition.
- For theorem-like criteria, keep the statement to assumptions and conclusion. Put determinant intuition, proof mechanisms, examples, pole issues, and implementation consequences in surrounding prose or SM.
- Apply an economy-of-notation rule. Do not introduce scalar factors, auxiliary variables, diagnostics, or branch parameters unless they are used by the local result and reduce the reader's work.
- Define physical indices, operators, and commutators before relying on compact formulas. Avoid terse "if" formulations when the method always has that structure.
- Distinguish operators from matrices in prose. Call $\mc B$ or $\mc M$ a single-particle propagation matrix or coefficient matrix, not an operator.
- Preserve notation: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.

## Formalism And SM Principles

- Lead with the physical AFQMC picture, then introduce the minimum notation needed for the result.
- Keep the main text compact and reader-facing. Use prose to lower the reader's workload, and reserve displayed equations for core results rather than intermediate notation.
- Do not let compression remove logical support. Move the support to SM and make it more reproducible there.
- Derive before claiming. For every nontrivial formula or implementation-backed relation, show the object being manipulated, the algebraic step, and the condition under which it is used.
- Keep formulas faithful to the physical sampling measure and to the algorithm actually used. Do not add mathematical operations or diagnostics for explanatory convenience.
- Separate mathematical identities, branch conventions, numerical stabilization, and implementation diagnostics as distinct claims.
- Prefer reader-facing explanations over author-facing emphasis. A paragraph should sound like it belongs in a paper, not like a reply to a revision note.
- In SM, teach the algorithm from the definitions already established in the manuscript. Reintroduce objects such as slice matrices, cyclic products, Green functions, and local blocks before using them after a long gap.

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
