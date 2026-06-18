---
name: bafqmc-prl-revision
description: Use when revising this BAFQMC manuscript toward PRL style, especially Section IV, Introduction, Fig. 1 framing, reference expansion, or post-edit manuscript review.
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

## Project Decisions

- Fig. 1 remains in the main text and drives the story.
- The Section IV example should initially use real positive triangular hopping, matching the benchmark.
- The pairing term should use the report convention: `+\Delta(b^\dagger c^\dagger+bc)`.
- The expected diff baseline is the previous commit with substantive manuscript-content edits.

## Assets

- Reference-paper PDFs are in `assets/reference-pdfs/`.
- Short style micro-excerpts and sentence patterns are in `references/style-micro-excerpts.md`.
- Paraphrased paragraph blueprints are in `references/paragraph-blueprints.md`.
- Approximate word-count helper: `scripts/count_pdf_words.py`.
