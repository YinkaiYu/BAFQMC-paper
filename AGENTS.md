# Project Notes

This repository contains the BAFQMC theoretical-physics manuscript.
Public preprint: https://arxiv.org/abs/2610.31541

## Repository And Tools

- Main sources are `main.tex`, `SM.tex`, and `references.bib`; figures are in `figures/`.
- Research notes and verification code are in `note/`. Read `note/AGENTS.md` when working there.
- Use `.codex/skills/bafqmc-prl-revision/SKILL.md` for manuscript research and revision.
- Inspect the current sources and relevant Git history as needed. Historical drafts are references, not a substitute for the current manuscript.
- On native Windows, use PowerShell for editing and Git. Linux/WSL is the canonical environment for LaTeX builds and scientific verification. Use the repository's `.ps1` launchers; do not substitute a Windows LaTeX toolchain.
- From Linux/WSL, run the corresponding scripts directly without nesting WSL. Both environments address the same checkout.

## Writing

- Apply the reader-friendly exposition principles below to manuscripts, notes, reports, and conversations with the user, including answers to physics questions.
- Make the physical picture clear and develop derivations step by step, explaining the connections between equations. Use mathematical terminology only when it helps; explain indispensable unfamiliar terms in language familiar to physicists.
- Answer the question directly. Keep attention on the physics the user asks about, without unsolicited negations, unrelated alternatives, or defensive qualifications that distract from the explanation.
- Write confidently and directly. Make the importance and physical consequences of the work clear. Avoid unnecessary defensive qualifications that weaken established results or make the argument harder to read.
- Write for a broad physics readership. Establish physical motivation before technical machinery, and build the argument with smooth physical and logical progression.
- Readers have none of our collaboration context. Manuscript prose must serve their understanding, never deliberately answer an author request or advertise a revision.
- Lower the reader's burden. Prefer familiar physics language over obscure mathematical jargon, invented concepts, internal shorthand, or lists of specialist terminology.
- Introduce new variables, notation, abbreviations, and conceptual entities only when necessary. Do not save writing effort by transferring explanation or backward searches to the reader.
- Keep the main text concise and physically intuitive. Make the Supplemental Material a detailed lecture that lets readers learn, follow, and reproduce the work without missing intermediate steps.
- During research and derivation, work through all necessary algebra, assumptions, branch choices, and consistency checks. Concise presentation must rest on complete reasoning.
- Preserve scientific accuracy and essential conditions while stating results firmly. Avoid habitual defensive weakening.
- Prefer direct positive sentences. Avoid "not X, but Y" and similar negation-then-correction constructions; use semicolons, colons, and dashes sparingly.
- Preserve current notation and nearby author-approved prose. Use standard LaTeX rather than manuscript macros when explaining mathematics in chat.
- Use bosonic creation operators `^+` where consistent with the draft, and `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` for references.

## References And Evidence

- Each citation must support the nearby claim. Use broad, purposeful coverage without disrupting the physical story.
- Verify every new or modified BibTeX entry against authoritative records, including authors, title, publication details, DOI, and arXiv identifier where applicable. Never guess bibliographic metadata; its correctness is an academic-integrity requirement.
- Every external reference cited in the main text or SM must have a local PDF cache. Maintain `local_reference_pdfs/manuscript/<citation_key>.pdf` and the cache manifests when citations change. Follow the skill's cache guidance. Report access limitations explicitly; do not substitute unrelated files or claim complete coverage when files are missing.

## Build And Delivery

When manuscript sources, bibliography, or figures change, refresh both `pdf/main.pdf` and `pdf/main-diff.pdf` and inspect relevant warnings and layout.

Native Windows:

```powershell
.\scripts\build-manuscript.ps1
.\scripts\build-diff.ps1 <baseline>
```

Linux/WSL:

```bash
bash ./scripts/build-manuscript.sh
bash ./scripts/build-diff.sh <baseline>
```

The default diff baseline is the previous substantive content-edit commit, unless the user specifies another comparison. Resolve it from Git history; ask only if genuinely ambiguous. For other Linux commands from Windows, use `scripts/run-in-wsl.ps1`.

Documentation-only edits do not require a manuscript build. Validate the changed documentation and its references instead.

## Git And Collaboration

- Keep edits coherent and scoped to the request; preserve unrelated author work. Discuss changes to physics claims, assumptions, or theorem conditions explicitly.
- Follow `.gitattributes` and `.editorconfig`; preserve LF text endings. Do not change global Git settings to hide discrepancies.
- Commit each completed, validated editing round. Preserve and report pre-existing or unrelated changes rather than discarding or committing them merely to make the checkout clean.
- Before claiming this shared checkout is clean, check `git status --short --untracked-files=all` with both Windows and WSL Git. Report unavailable checks; investigate discrepancies with `git diff` and `git ls-files --eol`.
- Keep build products, PDF previews, and temporary review artifacts in ignored locations such as `.build/` and `pdf/`.
