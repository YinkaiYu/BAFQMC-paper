# PRL Manuscript Revision System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current BAFQMC manuscript into a Physical Review Letters style manuscript whose main text presents the Fig. 1 sign-problem classification, the RP/TRS criteria, and the benchmarks compactly, while the Supplemental Material carries derivations and implementation details.

**Architecture:** Work in small reviewable manuscript-edit passes. Each pass changes one conceptual layer: structure, Section II, Section III, benchmark Section IV, concluding remarks, then abstract/introduction. Main text must stay self-contained and convincing without detailed proofs; SM must remain rigorous enough to support all moved claims.

**Tech Stack:** REVTeX 4.2, `latexmk main.tex`, `.latexmkrc` PDF copy to `pdf/`, repository diff-PDF workflow, benchmark reports from the two data repositories, APS/PRL author instructions, local PNG previews generated from PDF figures, the project-level `.codex/skills/bafqmc-prl-revision` skill, `opencode` for optional prose review, and the four sign-problem-free QMC Letter/Rapid style references.

---

## Current Snapshot

**Files inspected:**
- `main.tex`: 685 lines, 6 sections, 11 subsections, many displayed equations.
- `SM.tex`: 578 lines, already contains most proof material needed after compression.
- `figures/benchmark.pdf`: current old Fig. 2, to be replaced.
- `figures/benchmark_number_conserving.pdf`: copied candidate number-conserving benchmark figure for future Fig. 2.
- `figures/benchmark_pairing_delta.pdf`: copied candidate paired Delta benchmark figure for future Fig. 3.
- `experts/comment1.md` to `experts/comment4.md`: independent comments converge on the same structural recommendation.
- Number-conserving benchmark report: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC/data/20260603_bafqmc_ed_3x3_observables_v2_standard/publication_report/report_manual_stage_zh.html`.
- Paired benchmark report: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC_paring/data/20260605_pairing_delta_mu_m5_production/publication_report/report_pairing_delta_mu_m5_production_zh.html`.

**Measured baseline:**
- `texcount -merge -incbib -brief main.tex` reports about `6555+98+159` words with a `main.bbl` missing warning.
- Local analysis of four sign-problem-free QMC Letter/Rapid style references gives approximate main-article word counts in the 3600--4400 range before acknowledgments or appendices. The target should therefore be a compact 4.5--5 page Letter, not an artificially overcompressed draft.
- PRL abstract should remain no more than 600 characters.
- Existing Section II and Section III carry most of the mathematical proof load in the main text.
- Section IV contains `To be finished......`.
- Section V and Section VI should be merged; Section VI is empty.

**Main diagnosis:**
- The manuscript has a strong Letter-level result, but the current main text reads like a proof/methods paper.
- The main story should follow Fig. 1: bosonic systems can be classified by the presence of RP/TRS and by lattice frustration. BAFQMC is sign-free in the RP/TRS half-plane, SSE/WLQMC are sign-free in the unfrustrated half-plane, and the frustrated but RP/TRS quadrant is the new computable territory revealed by this work.

## Revision Principles

- Main text answers: what is the new principle, what are the minimal formulas, why are weights nonnegative, and where is it demonstrated.
- SM answers: how trace formulas, branches, cones, update ratios, regularization, and numerical details are derived.
- Use number-conserving cases first, then paired/non-number-conserving cases.
- Use TRS first in Section III because it follows directly from the number-conserving determinant.
- Use RP second because it is the broader criterion and naturally covers paired slices.
- Do not remove mathematical precision. Move proof details to SM with clean cross references.
- Avoid theorem/proof style in the main text. Use short physical explanations plus the decisive formula.
- Keep the introduction mostly intact until Sections II to V have been rewritten, then adjust it to match the final story.
- Avoid unnecessary "not ... but ..." constructions. State positive claims directly.
- Minimize dashes in manuscript prose.
- Treat the four comparison papers as style references, not as sources that should shape this paper's physics content.
- Use `opencode` for external prose review when drafting high-stakes paragraphs, especially the Introduction.
- Add references generously but only after verifying metadata against authoritative sources. Report every new or changed BibTeX entry for author review.

## Target Main-Text Structure

1. `Introduction`
   - Purpose: introduce the sign-problem classification shown in Fig. 1 and motivate the RP/TRS half-plane as the BAFQMC sign-free domain.
   - Fig. 1 must remain in the main text as a core schematic.

2. `Bosonic Auxiliary-Field Quantum Monte Carlo`
   - Purpose: define the sampled weights and observables.
   - Order: number-conserving determinant first, paired/Nambu metaplectic determinant second.
   - Target: compact enough to avoid derivation mode, with only the displayed equations needed for weights and basic observables.

3. `Symmetry Conditions for Nonnegative Weights`
   - Purpose: state and interpret the two sign-free mechanisms.
   - Order: Kramers TRS first, RP second.
   - Target: criterion statements plus short physical proof sketches, with detailed cone/Kramers proofs in SM.

4. `Frustrated Two-Flavor Bose-Hubbard Model`
   - Purpose: give one model family, explain why it is sign-free in BAFQMC despite frustrated hopping, and present Fig. 2/Fig. 3 benchmarks.
   - Target: enough space to make the model, sign-free mechanism, and two benchmarks clear without turning into a numerical report.

5. `Concluding Remarks`
   - Purpose: merge current Discussion and Summary.
   - Target: concise but not perfunctory.
   - Content: significance, pole limitation, projector BAFQMC outlook.

## Target Figure Plan

- Fig. 1: conceptual sign-problem territory schematic.
  - Must remain in the main text.
  - Interpretation: upper half-plane is sign-free for BAFQMC when RP or TRS is present; right half-plane is sign-free for SSE/WLQMC when the system is unfrustrated; upper-left quadrant is the new computable territory.
  - Local PNG preview: `figures/schematic.png`, ignored by git.

- Fig. 2: number-conserving benchmark.
  - Source PDF: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC/data/20260603_bafqmc_ed_3x3_observables_v2_standard/publication_report/figures/paper_candidate_main_4x2.pdf`.
  - Repo name: `figures/benchmark_number_conserving.pdf`.
  - Local PNG preview: `figures/benchmark_number_conserving.png`, ignored by git.
  - Main facts from report: `3x3` triangular lattice, `U_2` scan at `U_1=0`, `mu=-3.5`, `beta=4`; `U_1` scan at `U_2=1`, `mu=-7`, `beta=1`; `dtau=0.01`; `100000` samples; block size `10000`; observables `rho`, `-E`, `S_{\rm SF}(K)`, `S_{\rm DW}(K)`.

- Fig. 3: paired/Nambu benchmark.
  - Source PDF: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC_paring/data/20260605_pairing_delta_mu_m5_production/publication_report/figures/paper_candidate_main_delta_1x4_linear.pdf`.
  - Repo name: `figures/benchmark_pairing_delta.pdf`.
  - Local PNG preview: `figures/benchmark_pairing_delta.png`, ignored by git.
  - Main facts from report: `3x3` triangular lattice, `U_1=0`, `U_2=1`, `beta=4`, `mu=-5`; scan `Delta=0,0.05,...,0.30`; `dtau=0.01`; `100000` samples; block size `10000`; observables `rho`, `-E`, `S_{\rm SF}(K)`, `S_{\rm DW}(K)`.
  - Required caution: report notes small high-Delta residuals likely tied to time-step or ED-reference floors; main text should state agreement on curve scale and put diagnostic details in SM.

## Open Author Decisions

These must be resolved before edits that change physics claims or figure content.

1. Diff baseline:
   - Default baseline for `pdf/main-diff.pdf`: the previous version or commit containing substantive manuscript-content edits.
   - Ask the author only when this default is ambiguous for a given edit.

2. Reference-corpus workflow:
   - Style references are integrated into the project-level skill at `.codex/skills/bafqmc-prl-revision`.
   - Do not maintain a separate `docs/prl_style_corpus` directory.

## Resolved Author Decisions

- Pairing term in main text should use the report convention: `+\Delta(b^\dagger c^\dagger+bc)`.
- The main-text application/example section should initially use the real positive triangular hopping used in the benchmark.
- Fig. 1 must remain in the main text.
- Section IV is a good first manuscript section to rewrite after repository infrastructure and style corpus are ready.
- The PRL revision skill should be project-level, not global.

## Phase 0: Baseline And Guardrails

**Files:**
- Read: `main.tex`, `SM.tex`, `.latexmkrc`, `references.bib`, `AGENTS.md`.
- Create or update only planning/notes files unless the user authorizes manuscript edits.

- [ ] Step 1: Record current compile baseline.
  - Run: `latexmk main.tex`.
  - Expected: `pdf/main.pdf` refreshed by `.latexmkrc`, with any existing warnings recorded.

- [ ] Step 2: Record current length and equation baseline.
  - Run: `texcount -merge -incbib -brief main.tex`.
  - Run: `rg -n '^\\begin\\{equation\\}|^\\section|^\\subsection' main.tex`.
  - Expected: a written baseline in the active revision notes.

- [ ] Step 3: Decide diff baseline with the author.
  - Default to the previous version or commit containing substantive manuscript-content edits.
  - Ask the author only when that base is ambiguous.

## Phase 1: Maintain The Project PRL Revision Skill

**Files:**
- Maintain: `.codex/skills/bafqmc-prl-revision/SKILL.md`.
- Maintain: `.codex/skills/bafqmc-prl-revision/references/*.md`.
- Maintain: `.codex/skills/bafqmc-prl-revision/assets/reference-pdfs/*.pdf`.
- Modify later if approved: no manuscript source files.

- [x] Step 1: Read and summarize the four reference papers.
  - Sources:
    - arXiv:1408.2269 / Phys. Rev. B 91, 241117(R) (2015).
    - arXiv:1506.05349 / Phys. Rev. Lett. 115, 250601 (2015).
    - arXiv:1601.01994 / Phys. Rev. Lett. 116, 250601 (2016).
    - arXiv:1601.05780 / Phys. Rev. Lett. 117, 267002 (2016).
  - Extract only style structure: abstract shape, section rhythm, theorem/proof placement, figure usage, relation between main text and SM.
  - Estimate words in the main article PDFs to calibrate realistic Letter length, recognizing that arXiv/PDF extraction counts are approximate.

- [x] Step 2: Convert style lessons into a reusable local checklist.
  - Include: one-sentence physical principle, two to three core equations, proof sketch only, benchmark/model demonstration, limitations/outlook.

- [x] Step 3: Create a project-level Codex skill.
  - Location: `.codex/skills/bafqmc-prl-revision`.
  - The skill is targeted to this manuscript transformation.
  - It includes reference PDFs, style analysis, paragraph blueprints, review prompts, and citation verification workflow.

## Phase 2: Reorganize Supplemental Material First

**Files:**
- Modify: `SM.tex`.
- Read from: `main.tex`.

- [ ] Step 1: Reorder SM so it follows the future main-text order.
  - Proposed SM order:
    1. Number-conserving trace formula.
    2. Paired/Nambu trace formula and metaplectic branch.
    3. Green functions, observables, and update ratios.
    4. Kramers TRS proof.
    5. Reflection positivity proof and Gaussian slice criterion.
    6. Regularized bosonic weights and pole structure.
    7. Numerical details and benchmark parameters.

- [ ] Step 2: Move proof material out of current main-text II/III into SM where not already duplicated.
  - Keep equation labels stable where possible.
  - Add new labels only when necessary for cross references.

- [ ] Step 3: Add numerical-details scaffolding to SM.
  - Include triangular geometry, boundary condition, `K` point convention, observables, `dtau`, samples, block size, ED truncation/cutoff, reliability rules, and paired time-step diagnostics.

- [ ] Step 4: Compile.
  - Run: `latexmk main.tex`.
  - Expected: no new undefined references or citation warnings.

## Phase 3: Rewrite Section II

**Files:**
- Modify: `main.tex`.
- Verify references into: `SM.tex`.

- [ ] Step 1: Rename Section II to `Bosonic Auxiliary-Field Quantum Monte Carlo`.

- [ ] Step 2: Start from the HS ensemble.
  - Retain only:
    - `Z=\int \mc D\phi P_{\mathrm{aux}}(\phi)W(\phi)`.
    - `W(\phi)=\Tr \hat U(\phi)`.
    - a sentence that `\hat U(\phi)` is a product of bosonic Gaussian slices.

- [ ] Step 3: Present number-conserving BAFQMC first.
  - Retain:
    - `\hat h_\ell=\hat{\bb a}^+B_\ell\hat{\bb a}+\xi_\ell`.
    - `\mc B=\ee^{B_1}\cdots\ee^{B_L}`.
    - `W_{\rm nc}=\ee^{\sum_\ell\xi_\ell}\det(I-\mc B)^{-1}`.
    - one compact Green-function identity.

- [ ] Step 4: Present paired/Nambu BAFQMC second.
  - Retain:
    - `\hat\chi=(\hat{\bb a},\hat{\bb a}^+)^\trans`.
    - `\mc M=\ee^{A_1}\cdots\ee^{A_L}`.
    - `W_{\rm p}=\ee^{\sum_\ell\xi_\ell}\det(I-\mc M)^{-1/2}`.
    - one sentence on the metaplectic branch fixed by continuity.

- [ ] Step 5: Move local-update ratio and stabilization details to SM.

- [ ] Step 6: Compile and inspect.
  - Run: `latexmk main.tex`.
  - Check: no introduced warnings; Section II no longer reads like a derivation.

## Phase 4: Rewrite Section III

**Files:**
- Modify: `main.tex`.
- Modify if needed: `SM.tex`.

- [ ] Step 1: Rename Section III to `Symmetry Conditions for Nonnegative Weights`.

- [ ] Step 2: Put TRS first.
  - Retain:
    - `\Theta=UK`, `UU^*=-I`.
    - `U^\hc\overline{B_\ell}U=B_\ell`.
    - determinant factorization showing nonnegativity.
    - two-flavor block form only if it supports the model section.
  - Move generalized-eigenspace proof to SM.

- [ ] Step 3: Put RP second.
  - Retain:
    - reflection map definition in one line.
    - reflected-square sufficient condition.
    - Gaussian block criterion with positive reflected coupling if needed.
  - Move cone closure, trace-factorization proof, Lie-Trotter proof, and semigroup discussion to SM.

- [ ] Step 4: End Section III with the physical point.
  - Required message: the RP/TRS half-plane in Fig. 1 is sign-free for BAFQMC, including the frustrated RP/TRS quadrant.

- [ ] Step 5: Compile and inspect.
  - Run: `latexmk main.tex`.
  - Check: the section states criteria rather than proving every lemma.

## Phase 5: Rewrite Section IV Around The New Benchmarks

**Files:**
- Modify: `main.tex`, `SM.tex`.
- Add or replace: `figures/benchmark_number_conserving.pdf`, `figures/benchmark_pairing_delta.pdf`.
- Possibly remove or leave unused: `figures/benchmark.pdf`.

- [ ] Step 1: Copy candidate PDFs into `figures/` with stable names.
  - Number-conserving source: `paper_candidate_main_4x2.pdf`.
  - Paired source: `paper_candidate_main_delta_1x4_linear.pdf`.
  - Status on 2026-06-16: completed for `figures/benchmark_number_conserving.pdf` and `figures/benchmark_pairing_delta.pdf`.

- [ ] Step 2: Rewrite the model in one consistent notation.
  - Include chemical potential in the grand-canonical discussion.
  - Use a distinct symbol for hopping matrix, such as `T`, to avoid conflict with single-particle propagator `\mc B`.
  - Use `\hat n_{i,\pm}` for the two interaction channels.

- [ ] Step 3: Explain sign freedom after HS decoupling.
  - Main text:
    - `U_1` channel gives identical real fields.
    - `U_2` channel gives opposite imaginary fields.
    - two flavors form conjugate/Kramers partners.
    - the same slice also has an RP interpretation where appropriate.
  - SM:
    - full HS formulas and decoupled slice matrix.

- [ ] Step 4: Add paired extension consistently.
  - Use `+\Delta(b^\dagger c^\dagger+bc)`.
  - State that the paired/Nambu formulation is protected by RP.
  - Avoid overclaiming beyond the plotted `3x3` benchmark.

- [ ] Step 5: Insert Fig. 2 and Fig. 3.
  - Fig. 2 caption: `U_2` and `U_1` scans, `3x3`, `rho`, `-E`, `S_{\rm SF}(K)`, `S_{\rm DW}(K)`, ED vs BAFQMC, main parameters.
  - Fig. 3 caption: Delta scan, paired/Nambu formulation, same four observables, main parameters.
  - Put detailed MC/ED parameters in SM, not in overloaded captions.

- [ ] Step 6: Compile and inspect figures.
  - Run: `latexmk main.tex`.
  - Open `pdf/main.pdf` and inspect layout around Figs. 2 and 3.

## Phase 6: Merge Discussion And Summary

**Files:**
- Modify: `main.tex`.
- Possibly modify: `SM.tex`.

- [ ] Step 1: Replace current `Discussion` and empty `Summary and outlook` with `Concluding Remarks`.

- [ ] Step 2: Write three compact paragraphs.
  - Paragraph 1: conceptual result and new computable territory.
  - Paragraph 2: finite-temperature pole limitation and practical regime.
  - Paragraph 3: projector BAFQMC and model-building outlook.

- [ ] Step 3: Move detailed discussions to SM.
  - Infinite-variance analogy.
  - nonphysical auxiliary-field configurations.
  - density cap in paired formulations.
  - regularized interpretation.

- [ ] Step 4: Compile.
  - Run: `latexmk main.tex`.

## Phase 7: Finalize Introduction, Abstract, References, And Notation

**Files:**
- Modify: `main.tex`, `references.bib`.

- [ ] Step 1: Update Introduction only after Sections II to V stabilize.
  - Make it a complete, continuous story that introduces Fig. 1 naturally.
  - Align claims with actual Fig. 2/Fig. 3 content.
  - Remove long roadmap paragraph unless it earns its space.
  - Add missing literature citations at the appropriate claims, with metadata verified first.

- [ ] Step 2: Write the abstract last.
  - Constraint: no more than 600 characters including spaces for PRL.
  - Include: BAFQMC, sign-free criteria, frustrated bosonic models, benchmark.
  - Exclude: local update ratios, long pole discussion, implementation details.

- [ ] Step 3: Audit references.
  - Add complete BibTeX for the four comparison Letter/Rapid papers if missing.
  - Verify metadata against arXiv, DOI, or APS pages before editing `references.bib`.

- [ ] Step 4: Audit notation.
  - Maintain manuscript macros: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, `\Omega`.
  - Decide whether to retain `a^+` notation globally or migrate to `a^\dagger` in a separate author-approved pass.
  - Check `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` style.

## Phase 8: Verification Before Each Delivered Manuscript Edit

**Files:**
- Build artifacts: `.build/`, `pdf/main.pdf`, `pdf/main-diff.pdf`.

- [ ] Step 1: Compile.
  - Run: `latexmk main.tex`.
  - Expected: `pdf/main.pdf` refreshed.

- [ ] Step 2: Inspect warnings.
  - Focus on changed text, labels, citations, equations, and figures.
  - Fix introduced warnings before delivery.

- [ ] Step 3: Refresh diff PDF.
  - Use the repository's established diff workflow.
  - Default comparison base: the previous substantive manuscript-content edit commit.
  - Expected: `pdf/main-diff.pdf` refreshed.

- [ ] Step 4: Inspect PDF.
  - Check page count, figure placement, caption readability, equation overflow, unresolved references, and the absence of unfinished markers.

- [ ] Step 5: Report residual risks.
  - If a warning cannot be eliminated without unrelated changes, state it explicitly.

## Phase 9: Independent Review Loop

**Review agents to use after each major pass:**

- Physics consistency reviewer:
  - Check TRS/RP assumptions, determinant sign logic, branch statements, regularization claims, and benchmark-claim wording.

- PRL style reviewer:
  - Compare the current draft to the four sign-problem-free QMC Letter/Rapid style references.
  - Check whether the main text presents the Fig. 1 classification and new territory before the mathematical proof.
  - Check for unnecessary "not ... but ..." constructions and excessive dashes.

- `opencode` prose reviewer:
  - Use for major prose passages after a draft exists.
  - Prompt it to check clarity, flow, and PRL-like concision without changing the physics claims.
  - Local command: `opencode run -m deepseek/deepseek-v4-pro "<prompt>"`.

- Figure and benchmark reviewer:
  - Check that Fig. 2/Fig. 3 captions match report parameters.
  - Check that ED/BAFQMC agreement is described accurately.
  - Check that time-step caveats are in SM or concise main-text language.

## First Suggested Execution Block

Use this sequence for the next working turn after author decisions:

- [x] Create project-level `.codex/skills/bafqmc-prl-revision`.
- [x] Integrate arXiv PDFs and style-reference analysis into the project skill assets.
- [ ] Run baseline compile and record warnings.
- [ ] Copy the two benchmark PDFs into `figures/` with approved names.
- [ ] Add SM numerical-details section using the two reports.
- [ ] Rewrite Section IV first, because the new benchmark results now define what the manuscript can honestly claim.

This starts with the repository infrastructure and style calibration, then moves to the unfinished application section. The Introduction should be rewritten after the core results and benchmark narrative are stable.
