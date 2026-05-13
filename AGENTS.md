# Project Notes

This repository contains a theoretical physics manuscript on sign-problem-free bosonic auxiliary-field quantum Monte Carlo, intended to be developed toward a Physical Review Letters style presentation.

## Main Files

- `main.tex`: main manuscript source.
- `SM.tex`: supplemental material source, included by `main.tex`.
- `references.bib`: bibliography database.
- `figures/schematic.pdf`: sign-problem classification schematic.
- `figures/benchmark.pdf`: benchmark figure.
- `.latexmkrc`: build configuration; output goes to `.build/` and the final PDF is copied to `pdf/`.

## Build And Verification

Use:

```bash
latexmk main.tex
```

The configured build runs `pdflatex` with `-interaction=nonstopmode -halt-on-error`. Before claiming a manuscript edit is complete, run the build and inspect warnings that are relevant to changed text, labels, citations, or figures.

Before delivering any manuscript edit to the user:

- Compile the modified manuscript and refresh the PDF artifact in `pdf/`, especially `pdf/main.pdf`.
- Also refresh the diff PDF artifact in `pdf/`, especially `pdf/main-diff.pdf`, using the repository's established diff-generation workflow. If the diff baseline or command is unclear, ask the user which comparison base to use before inventing one.
- Treat build errors and relevant warnings as part of the task. Fix errors or warnings introduced by the edit, then rebuild until the manuscript PDF and diff PDF are both up to date. If any warning cannot be eliminated without changing unrelated manuscript content, report it explicitly.

## Writing Target

- Keep the prose in polished scientific English suitable for APS journals.
- Prefer PRL-like structure: sharp motivation, compact statement of novelty, minimal repetition, and direct connection between formal results and physical consequences.
- Write for the paper's actual audience: readers, referees, and editors. The manuscript should read as a coherent scientific story, not as a record of the author-assistant collaboration.
- Do not insert sentences or paragraphs that explicitly answer the user's prompt, advertise the revision, or call attention to the fact that a requested change was made. Such text is inappropriate in the manuscript because readers do not have the collaboration context.
- Preserve mathematical precision. Do not simplify sign-positivity, regularization, or branch-choice arguments in ways that weaken the claims.
- Keep notation consistent with the current draft: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.
- Use `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` in manuscript prose unless the surrounding style changes globally.
- Prefer concise PRL-style paragraphs in the main text. Put longer derivations, caveats, and implementation details in the Supplemental Material.
- Gradually move the tone from a mathematics-paper style toward a theoretical-physics style. Maintain rigor, but avoid unnecessarily obscure mathematical jargon and explain the physical picture whenever it helps the reader understand the formal result.
- Write with appropriate confidence: the sign-problem-free bosonic auxiliary-field quantum Monte Carlo method proposed here is a highly innovative and important contribution. The prose should make the significance clear.

## Current Manuscript State

- The manuscript currently compiles to an 18-page PDF.
- Main sections present the BAFQMC formalism, reflection positivity, TRS, examples, discussion, and Supplemental Material.
- The benchmark subsection contains an unfinished marker: `To be finished......`
- `Summary and outlook` is currently empty.
- `lipsum` is loaded but no generated filler text is used.
- The current document class is `revtex4-2` with APS-style options matching the repository's PRL-format reference manuscript; the Supplemental Material is kept in the same compiled PDF and set in single-column format.

## Collaboration Guidelines

- Discuss physics-level changes explicitly when they affect claims, assumptions, or theorem conditions.
- For editing requests, make minimal, coherent source changes and preserve unrelated author text.
- For polishing, prioritize clarity, concision, and APS tone over decorative phrasing.
- When adding references, update `references.bib` with complete BibTeX fields and cite them from the text. Verify bibliographic metadata against a reliable source such as the publisher page, DOI record, arXiv record, or other authoritative database before adding or editing a BibTeX entry.
- Check formula changes carefully. Verify algebra, derivations, assumptions, branch choices, and limiting cases when relevant, and keep notation consistent across the main text and Supplemental Material.
- If the user's request is ambiguous or underspecified, ask a clarifying question before making a change that could affect the physics, claims, comparison baseline, or manuscript structure.
- Keep generated build artifacts out of version control; `.build/` and `pdf/` are ignored.
