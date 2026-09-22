# Project Notes

This repository contains a theoretical physics manuscript on sign-problem-free bosonic auxiliary-field quantum Monte Carlo, intended to be developed toward a Physical Review Letters style presentation.

## Main Files

- `main.tex`: main manuscript source.
- `SM.tex`: supplemental material source, included by `main.tex`.
- `references.bib`: bibliography database.
- `note/`: research notes and their verification code. Superseded documents are kept in `note/archive/`.
- `figures/schematic.pdf`: sign-problem classification schematic.
- `figures/benchmark_number_conserving.pdf`: number-conserving benchmark figure.
- `figures/benchmark_pairing_delta.pdf`: paired/Nambu benchmark figure.
- `.latexmkrc`: build configuration; output goes to `.build/` and the final PDF is copied to `pdf/`.

## Execution Environment

- Keep the Windows ChatGPT agent in its native PowerShell 7 environment. Use Windows-native tools for source editing, Git operations, and other platform-neutral work.
- Treat Linux as the canonical environment for LaTeX builds, scientific verification, and repository workflows that depend on Linux-only tools. A Windows-native agent must invoke the corresponding `.ps1` WSL launcher when one exists, or use `scripts/run-in-wsl.ps1` for another Linux command; it must not silently substitute a Windows-native toolchain.
- A Linux or WSL agent should run commands directly and must not invoke `wsl.exe` recursively. Both path forms address the same checkout; do not create a second clone.
- Build and scientific verification results are authoritative only from Linux/WSL. If the sandbox exposes `/mnt/<drive>` as read-only, request approval for the command rather than diagnosing the write failure as a toolchain error.

## Build And Verification

From Linux or WSL, use:

```bash
bash ./scripts/build-manuscript.sh
```

The script runs `latexmk main.tex` from the repository root. From native Windows PowerShell 7, use the WSL forwarding entry point instead:

```powershell
.\scripts\build-manuscript.ps1
```

For another Linux-only command from a Windows-native agent, pass one Bash command string through the generic launcher, for example:

```powershell
.\scripts\run-in-wsl.ps1 'python3 note/contraction_semigroups_qmc/reproduce.py check'
```

The configured build runs `pdflatex` with `-interaction=nonstopmode -halt-on-error`. Before claiming a manuscript edit is complete, run the build and inspect warnings that are relevant to changed text, labels, citations, or figures.

Before delivering any manuscript edit to the user:

- Compile the modified manuscript and refresh the PDF artifact in `pdf/`, especially `pdf/main.pdf`.
- Also refresh the diff PDF artifact in `pdf/`, especially `pdf/main-diff.pdf`, using the repository's established diff-generation workflow. If the diff baseline or command is unclear, ask the user which comparison base to use before inventing one.
- Treat build errors and relevant warnings as part of the task. Fix errors or warnings introduced by the edit, then rebuild until the manuscript PDF and diff PDF are both up to date. If any warning cannot be eliminated without changing unrelated manuscript content, report it explicitly.

## Writing Target

- For research notes, read [`note/AGENTS.md`](note/AGENTS.md). Use a gradual, lecture-style explanation suited to physicists, with clear physical motivation, essential derivations, and economical notation. These note-specific instructions govern presentation in `note/`.
- Keep the prose in polished scientific English suitable for APS journals.
- Prefer PRL-like structure: sharp motivation, compact statement of novelty, minimal repetition, and direct connection between formal results and physical consequences.
- Treat the mentor-revised abstract, Introduction, and Concluding remarks established in commit `66c6cd4` as the primary local calibration for high-visibility prose. Learn the information hierarchy and rhetorical moves rather than copying isolated phrases.
- Begin high-visibility sections at the broadest level justified by the evidence: establish why the problem matters across the relevant physics communities, identify the concrete obstruction, then introduce technical machinery only when it performs the conceptual turn.
- Build the central story as a paradigm shift from local matrix-element positivity in WLQMC/SSE to global symmetry-protected weights after HS decoupling. State this physical distinction before adding formal detail.
- Use confident language to expose a proved contribution: `formulate`, `establish`, `rigorously prove`, `unifying principles`, and `opens a route` are appropriate when supported. Confidence must come from theorem, benchmark, or clearly delimited outlook evidence, not from decorative superlatives.
- Present benchmarks as validation of the construction, not as a detached numerical report. A conclusion should synthesize the new organizing principle, the demonstrated evidence, the separate pole/variance issue, and concrete next algorithmic directions.
- The central framing follows Fig. 1: bosonic sign-problem-free regions are classified by the presence of RP/TRS and by lattice frustration. BAFQMC covers the RP/TRS half-plane; SSE/WLQMC covers the unfrustrated half-plane; the frustrated but RP/TRS quadrant is the new computable territory revealed by this work.
- For substantial PRL restructuring, style analysis, Section IV rewriting, Introduction rewriting, or post-edit review, use the project-level skill at `.codex/skills/bafqmc-prl-revision/SKILL.md`.
- Write for a broad physics readership with no access to our collaboration context. Build the argument sequentially from physical motivation, explain necessary concepts before using them, and avoid logical jumps so readers can follow the theory and appreciate its significance.
- Do not insert sentences or paragraphs that explicitly answer the user's prompt, advertise the revision, or call attention to the fact that a requested change was made. Such text is inappropriate in the manuscript because readers do not have the collaboration context.
- Preserve mathematical precision. Do not simplify sign-positivity, regularization, or branch-choice arguments in ways that weaken the claims.
- Keep notation consistent with the current draft: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, and `\Omega`.
- When communicating with the user, write all inline and display mathematics in standard LaTeX and do not use the manuscript's custom macros, so formulas render correctly in ChatGPT Desktop.
- For new or revised manuscript formulas, write bosonic creation operators as `^+` rather than `^\dagger` or `^{\hc}` when this matches the surrounding notation. In physical model Hamiltonians, prefer explicit `b,c` operators and explicit Hermitian-conjugate terms over introducing short-lived flavor aliases such as `a_{\alpha i}`.
- Use `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` in manuscript prose unless the surrounding style changes globally.
- Prefer concise PRL-style paragraphs in the main text. Make the Supplemental Material a detailed, lecture-style account with the intermediate steps, assumptions, and implementation details needed to learn and reproduce the work.
- Explain formal results and derivations through their physical meaning while maintaining rigor. Avoid obscure mathematical jargon, strings of technical terms, invented labels, internal shorthand, and unnecessary abbreviations that shift effort to the reader.
- Introduce new variables, notation, and concepts only when needed; prefer familiar conventions and reuse established notation to minimize the reader's burden.
- State supported contributions directly and confidently. Avoid unnecessary defensive qualifications that obscure or weaken their significance, while retaining essential assumptions and limits.
- Avoid negative-then-positive constructions such as "not X, but Y"; state the intended point directly. Use semicolons, colons, and dashes sparingly.
- Reference coverage should be broad, correct, and purposeful. Add references whenever a condensed logical step relies on known background or when the reader needs a route to the underlying literature.

## Current Manuscript State

- The manuscript currently compiles to a 25-page PDF including the Supplemental Material.
- Main-text sections present the BAFQMC formalism, TRS and RP criteria, triangular-lattice benchmarks, and Concluding remarks, followed by the Supplemental Material.
- The benchmark discussion and Concluding remarks are populated; no unfinished marker remains in the manuscript.
- `lipsum` is loaded but no generated filler text is used.
- The current document class is `revtex4-2` with APS-style options matching the repository's PRL-format reference manuscript; the Supplemental Material is kept in the same compiled PDF and set in single-column format.

## Git Working Practices

- Follow `.gitattributes` and `.editorconfig`: use LF for text files except `.bat` and `.cmd` (CRLF). Preserve existing source content; do not change global Git settings to hide line-ending differences.
- Before declaring this shared Windows/WSL checkout clean, check `git status --short --untracked-files=all` with both Windows Git and WSL Git. From native PowerShell, run the WSL check through `scripts/run-in-wsl.ps1`; from WSL, invoke Windows Git through Windows interoperability without nesting `wsl.exe`. If either check is unavailable, report that limitation rather than claiming both environments are clean. Investigate discrepancies with `git diff` and `git ls-files --eol` before attributing them to an editor refresh issue.
- After completing and validating a coherent set of changes, commit it promptly. Each completed editing round must include its local Git commit.
- Before delivering the result, inspect `git status --short` and resolve all remaining staged, unstaged, and untracked changes. Finish with a clean working tree. Do not leave completed work uncommitted or merely staged for a later turn.
- Review remaining changes and group commits by purpose. Preserve existing source work, and keep local build output, previews, and temporary review files in ignored directories. Do not discard work just to make Git status clean.

## Collaboration Guidelines

- Discuss physics-level changes explicitly when they affect claims, assumptions, or theorem conditions.
- For editing requests, make minimal, coherent source changes and preserve unrelated author text. Check the surrounding paragraphs for continuity, physical motivation, and logical progression even after a local edit.
- For polishing, prioritize clarity, concision, and APS tone over decorative phrasing.
- When adding references, update `references.bib` with complete BibTeX fields and cite them from the text. Verify bibliographic metadata against a reliable source such as the publisher page, DOI record, arXiv record, or other authoritative database before adding or editing a BibTeX entry.
- Reference metadata must not be guessed. Before adding or changing any bibliography entry, check author list, title, journal, volume, page/article number, year, DOI, and arXiv identifier where applicable. Report newly added or modified references to the user for author review.
- Check formula changes carefully. Verify algebra, derivations, assumptions, branch choices, and limiting cases when relevant, and keep notation consistent across the main text and Supplemental Material.
- If the user's request is ambiguous or underspecified, ask a clarifying question before making a change that could affect the physics, claims, comparison baseline, or manuscript structure.
- Keep generated build artifacts out of version control; `.build/` and `pdf/` are ignored.
- Generated PNG previews of PDF figures are local inspection artifacts and should stay ignored by git.
