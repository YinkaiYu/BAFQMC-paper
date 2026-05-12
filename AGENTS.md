# Project Notes

This repository contains a theoretical physics manuscript on sign-problem-free bosonic auxiliary-field quantum Monte Carlo, intended to be developed toward a Physical Review Letters style presentation.

## Main Files

- `BAFQMC-draft.tex`: main manuscript source.
- `BAFQMC-draft.bib`: bibliography database.
- `figures/schematic.pdf`: sign-problem classification schematic.
- `figures/benchmark.pdf`: benchmark figure.
- `.latexmkrc`: build configuration; output goes to `.build/` and the final PDF is copied to `pdf/`.

## Build And Verification

Use:

```bash
latexmk BAFQMC-draft.tex
```

The configured build runs `pdflatex` with `-interaction=nonstopmode -halt-on-error`. Before claiming a manuscript edit is complete, run the build and inspect warnings that are relevant to changed text, labels, citations, or figures.

## Writing Target

- Keep the prose in polished scientific English suitable for APS journals.
- Prefer PRL-like structure: sharp motivation, compact statement of novelty, minimal repetition, and direct connection between formal results and physical consequences.
- Preserve mathematical precision. Do not simplify sign-positivity, regularization, or branch-choice arguments in ways that weaken the claims.
- Keep notation consistent with the current draft: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.
- Use `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` in manuscript prose unless the surrounding style changes globally.
- Prefer concise PRL-style paragraphs in the main text. Put longer derivations, caveats, and implementation details in appendices.

## Current Manuscript State

- The manuscript currently compiles to a 14-page PDF.
- Main sections present the BAFQMC formalism, reflection positivity, TRS, examples, discussion, and appendices.
- The benchmark subsection contains an unfinished marker: `To be finished......`
- `Summary and outlook` is currently empty.
- `lipsum` is loaded but no generated filler text is used.
- The current document class is `revtex4-2` with `prb` option; if the target is a strict PRL submission, discuss whether to switch to `prl` and how to handle the long appendices/supplement.

## Collaboration Guidelines

- Discuss physics-level changes explicitly when they affect claims, assumptions, or theorem conditions.
- For editing requests, make minimal, coherent source changes and preserve unrelated author text.
- For polishing, prioritize clarity, concision, and APS tone over decorative phrasing.
- When adding references, update `BAFQMC-draft.bib` with complete BibTeX fields and cite them from the text.
- Keep generated build artifacts out of version control; `.build/` and `pdf/` are ignored.
