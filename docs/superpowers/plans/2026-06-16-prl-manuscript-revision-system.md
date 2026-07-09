# PRL Manuscript Revision System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current BAFQMC manuscript into a Physical Review Letters style manuscript whose main text presents the Fig. 1 sign-problem classification, the RP/TRS criteria, and the benchmarks compactly, while the Supplemental Material carries derivations and implementation details.

**Architecture:** Work in small reviewable manuscript-edit passes. Early passes changed one conceptual layer at a time: structure, Section II, Section III, benchmark Section IV, concluding remarks, then introduction. The project has now entered an iterative refinement stage for main-text and SM details. Each new pass should address a focused author-feedback bundle, then run review, notation/heading/prose audit, citation/BibTeX audit, compilation, diff-PDF refresh, and commit before delivery. Main text must stay self-contained and convincing without detailed proofs; SM must remain rigorous enough to support all moved claims.

**Tech Stack:** REVTeX 4.2, `latexmk main.tex`, `.latexmkrc` PDF copy to `pdf/`, repository diff-PDF workflow, benchmark reports from the two data repositories, APS/PRL author instructions, local PNG previews generated from PDF figures, the project-level `.codex/skills/bafqmc-prl-revision` skill, `opencode` for optional prose review, and the four sign-problem-free QMC Letter/Rapid style references.

---

## Current Snapshot

**Files inspected:**
- `main.tex`: 287 lines as of 2026-07-09. The main text now uses PRL-style run-in headings for the Introduction, BAFQMC formalism, nonnegative-weight criteria, examples, and Concluding remarks. Section II, Section III, the benchmark example, the ending, and the Introduction have been compressed into Letter-style prose.
- `SM.tex`: 1194 lines as of 2026-07-09. It carries HS identities, trace formulas, Green functions, Sherman-Morrison/Woodbury updates, stabilization details, TRS/RP proofs, regularized weights, and benchmark numerical parameters. The obsolete semigroup route has been removed.
- `figures/benchmark_number_conserving.pdf`: current Fig. 2, placed at the top of page 3.
- `figures/benchmark_pairing_delta.pdf`: current Fig. 3, placed at the top of page 4.
- `experts/comment1.md` to `experts/comment4.md`: independent comments converge on the same structural recommendation.
- Number-conserving benchmark report: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC/data/20260603_bafqmc_ed_3x3_observables_v2_standard/publication_report/report_manual_stage_zh.html`.
- Paired benchmark report: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC_paring/data/20260605_pairing_delta_mu_m5_production/publication_report/report_pairing_delta_mu_m5_production_zh.html`.

**Measured baseline and current status:**
- `texcount -merge -incbib -brief main.tex` reports about `7396+75+218` words with a `main.bbl` missing warning when run from the repository root without first copying `.build/main.bbl`.
- Local analysis of four sign-problem-free QMC Letter/Rapid style references gives approximate main-article word counts in the 3600--4400 range before acknowledgments or appendices. The target should therefore be a compact 4.5--5 page Letter, not an artificially overcompressed draft.
- PRL abstract should remain no more than 600 characters.
- Section II has been compacted into the AFQMC ensemble, the number-conserving determinant, the number-conserving Green-function identity, and the paired/Nambu determinant; detailed HS transformations, trace derivations, Green functions, update ratios, and stabilization discussion sit in the Supplemental Material.
- Section III has been rewritten as a flat PRL-style criteria block. TRS is stated first, RP second, both in theorem-like form, with proof details in the SM.
- The benchmark example has been rewritten around the triangular-lattice number-conserving and paired data. The unfinished marker has been removed.
- Discussion and Summary/outlook have been merged into a three-paragraph `Concluding remarks` block. The conclusion now states the method, the TRS/RP criteria, the benchmark significance, the finite-temperature determinant-pole limitation, and projector/canonical outlook without surfacing the SM regularization discussion.
- The SM semigroup section has been removed. The manuscript no longer uses a semigroup argument to discuss paired poles, branch connectivity, or the absence of poles.
- Before the Section II pass, commit `79a1b9b` compiled to an 18-page PDF including Supplemental Material, with `pdf/main.pdf` and `pdf/main-diff.pdf` refreshed.
- Status on 2026-06-22: Section IV benchmark writing is in place, and Section II plus the supporting Supplemental Material have gone through two compression passes. The second pass removes notation-only display equations, avoids extra main-text variables such as `\hat U(\phi)` and `W_{\rm nc}`, puts number-conserving Green functions in the main text, and moves branch and update-ratio details to the Supplemental Material.
- Status on 2026-07-06: Section III has been flattened and theoremized through commits `caee0e7`--`846d3be`; figure placement was adjusted in `559dc79`.
- Status on 2026-07-08: Pole/branch framing, SM regularization prose, and `Concluding remarks` were updated through commits `f00aec9`--`07568ac`. The Introduction was rewritten into a five-paragraph PRL-style story that moves from the QMC sign problem, to the local-weight frustration barrier, to the auxiliary-field symmetry viewpoint, to the new BAFQMC answer. Verified Introduction references and a citation-audit HTML report were added.
- Status on 2026-07-09: The Introduction pass was compiled, `pdf/main.pdf` and `pdf/main-diff.pdf` were refreshed against commit `559dc79cf5dd25f4e574824d9acf3aca44268d1a`, and the completed pass was committed as `4d4d766`. Fig. 2 is placed at the top of page 3 and Fig. 3 at the top of page 4 in `pdf/main.pdf`.

**Main diagnosis:**
- The core PRL structure is now in place, but the main text and SM still require many detail-level revisions for reader flow, notation consistency, proof pedagogy, benchmark clarity, and exact claim boundaries.
- The main story should continue to follow Fig. 1: bosonic systems can be classified by the presence of RP/TRS and by lattice frustration. BAFQMC is sign-free in the RP/TRS half-plane, SSE/WLQMC are sign-free in the unfrustrated half-plane, and the frustrated but RP/TRS quadrant is the new computable territory revealed by this work.

## Revision Principles

- Main text answers: what is the new principle, what are the minimal formulas, why are weights nonnegative, and where is it demonstrated.
- SM answers: how trace formulas, reflection-positivity proofs, update ratios, regularization, and numerical details are derived.
- Use number-conserving cases first, then paired/non-number-conserving cases.
- Use TRS first in Section III because it follows directly from the number-conserving determinant.
- Use RP second because it is the broader criterion and naturally covers paired slices.
- Main-text Section III should lower the reader's workload: state criteria in words a theoretical-physics reader can immediately use, then give only the decisive formulas.
- It is acceptable, and likely clearer, to present the two criteria as compact theorem-like statements in prose. Do not include proof paragraphs in the main text.
- Detailed proofs belong in SM and must be written pedagogically, with no hidden steps such as "the same manipulation gives" when the algebra is important.
- Avoid obscure mathematical vocabulary in the main text. Words such as algebra, cone, semigroup, metaplectic branch, and generalized eigenspace should not appear in the Letter unless unavoidable. The semigroup route is no longer part of the paper.
- Treat the sign problem and pole/infinite-variance problem as distinct. TRS and RP are sufficient criteria for nonnegative BAFQMC weights whenever the relevant weight is finite; the possible presence of determinant poles is a separate numerical-stability issue that depends on the model, HS decoupling, and determinant representation.
- Do not suggest that the sign-free criteria require absence of poles, connected pole-free components, auxiliary-field paths, or analytic branch tracking. These are not part of the central theorem statements.
- In paired RP settings, the operator-level reflection-positivity proof fixes the nonnegative physical weight. The Nambu determinant expression with exponent `-1/2` should be understood to use the positive branch required by that operator positivity, not a path-dependent branch selected by auxiliary-field continuity.
- For Gaussian trace formulas, derive the determinant expression in the convergent/stable region. Outside that region the determinant formula should be described, where needed, as the analytic/finite-part weight supported by the SM regularization discussion rather than as a configuration-by-configuration bare trace.
- Do not remove mathematical precision. Move proof details to SM with clean cross references.
- Avoid theorem/proof style in the main text beyond concise criterion statements. Use short physical explanations plus the decisive formula.
- Use PRL-like run-in headings in the main text, e.g. `{\it Conditions for nonnegative weights}---`, instead of standalone numbered section headings. Keep ordinary `\section`/`\subsection` structure in SM.
- The Introduction should remain a PRL-style story that motivates the work from the QMC sign problem, the local-weight frustration barrier in bosonic/spin simulations, the auxiliary-field symmetry viewpoint developed in fermionic AFQMC, and the missing bosonic counterpart that this paper supplies.
- The Introduction should cite background claims with broad but purposeful reference clusters. Every added or modified BibTeX entry must be verified against authoritative sources before use, and a citation report should be written for author review.
- Avoid unnecessary "not ... but ..." constructions. State positive claims directly.
- Minimize dashes in manuscript prose.
- Treat the four comparison papers as style references, not as sources that should shape this paper's physics content.
- Use `opencode` for external prose review when drafting high-stakes paragraphs, especially the Introduction.
- Add references generously but only after verifying metadata against authoritative sources. Report every new or changed BibTeX entry for author review.
- During the current refinement stage, do not postpone review and audits until the end. Every substantive edit round must include reader-facing review, notation/heading/prose audit, citation/BibTeX audit, compile/diff refresh when manuscript sources change, and a git commit.

## Target Main-Text Structure

1. `{\it Introduction}---` or an equivalent PRL-style opening paragraph
   - Purpose: introduce the sign-problem classification shown in Fig. 1 and motivate the RP/TRS half-plane as the BAFQMC sign-free domain.
   - Fig. 1 must remain in the main text as a core schematic.

2. `{\it Bosonic auxiliary-field quantum Monte Carlo}---`
   - Purpose: define the sampled weights and observables.
   - Order: number-conserving determinant first, paired/Nambu metaplectic determinant second.
   - Target: compact enough to avoid derivation mode, with only the displayed equations needed for weights and basic observables.

3. `{\it Conditions for nonnegative weights}---`
   - Purpose: state and interpret the two sign-free mechanisms.
   - Order: Kramers TRS first, RP second.
   - Target: two compact, usable criteria and a short physical interpretation. Do not use subsections. Do not include detailed proof sketches; send Kramers multiplicity, reflected-square positivity, Lie-Trotter closure, and convergence/regularization caveats to SM.

4. `{\it Frustrated two-flavor Bose-Hubbard model}---`
   - Purpose: give one model family, explain why it is sign-free in BAFQMC despite frustrated hopping, and present Fig. 2/Fig. 3 benchmarks.
   - Target: enough space to make the model, sign-free mechanism, and two benchmarks clear without turning into a numerical report.

5. `{\it Discussion and outlook}---` or `{\it Concluding remarks}---`
   - Purpose: merge current Discussion and Summary.
   - Target: three polished paragraphs that close the Letter with confidence.
   - Paragraph 1: summarize finite-temperature BAFQMC, the TRS/RP sign-free criteria, and the triangular-lattice benchmarks; contrast the new auxiliary-field sign-free territory with local-weight methods such as world-line QMC and SSE.
   - Paragraph 2: state the finite-temperature pole/infinite-variance limitation carefully. This is a numerical-stability issue separate from the sign problem. It may restrict practical finite-temperature BAFQMC to lower density, higher temperature, or milder interaction regimes for some models and HS choices.
   - Paragraph 3: give the outlook. Emphasize frustrated bosonic/spin problems that may become accessible and the likely development of bosonic projector AFQMC or canonical formulations, where fixed-particle-number sampling may avoid the finite-temperature pole difficulty.

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

## Current Iterative Refinement Protocol

The manuscript has moved beyond the large structural rewrite. The next stage will likely require many author-feedback rounds on both the main text and the SM. Treat each round as a complete, reviewable edit pass rather than as a partial draft.

For every substantive manuscript-edit round:

- [ ] Step 1: Localize the author-feedback bundle.
  - Identify which part of the paper the feedback targets: main-text story, Section II formulas, criteria/theorem wording, benchmark explanation, SM derivation, regularization, numerical algorithm, references, abstract, or figure/caption layout.
  - Preserve the reader's reading order. A fix should make sense to a reader who has no context from the author-agent discussion.

- [ ] Step 2: Implement a focused edit.
  - Make the smallest coherent manuscript change that resolves the feedback.
  - Avoid process-facing prose, internal shorthand, or sentences that sound like they are answering the author rather than teaching the reader.
  - Do not weaken the central sign-free claim unless a physics error requires it. If a claim is narrowed, record the reason in the response to the author.

- [ ] Step 3: Run reader-facing review.
  - Check whether each new paragraph has a clear purpose, follows from previous context, and lowers rather than raises the reader's workload.
  - Remove unnecessary jargon, invented concepts, defensive caveats, and "not ... but ..." constructions unless the contrast is essential.
  - For SM edits, verify that derivations are pedagogical and do not hide important algebra behind phrases such as "similarly" or "the same manipulation gives."

- [ ] Step 4: Run notation / heading / prose audit.
  - Check main-text run-in headings and SM numbered headings.
  - Check notation consistency: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, `\Omega`, and bosonic creation operators written as `^+` where this matches the manuscript style.
  - Check that displayed equations are reserved for core formulas in the main text, while derivations stay in SM.
  - Run source scans appropriate to the edit, for example:
    ```bash
    rg -n '^\\section|^\\subsection' main.tex
    rg -n -F '{\\it ' main.tex
    rg -n "semigroup|metaplectic|connected component|pole-free|branch connected" main.tex SM.tex
    ```

- [ ] Step 5: Run citation and BibTeX audit.
  - If citations or bibliography entries are added or changed, verify author list, title, journal, volume, page/article number, year, DOI, and arXiv identifier against authoritative sources before committing.
  - If no citations are changed, still run a citation-key consistency check so the edit does not introduce missing keys.
  - Update or create a citation report whenever a round adds or materially changes references.

- [ ] Step 6: Run verification artifacts for manuscript-source edits.
  - Compile with `latexmk main.tex`.
  - Refresh `pdf/main.pdf` and `pdf/main-diff.pdf` using the established diff workflow and the author-specified baseline if one is given.
  - Inspect relevant warnings, figure placement, equation overflow, unresolved references, and changed PDF pages.

- [ ] Step 7: Commit every completed modification round.
  - Run `git diff --check`.
  - Commit all intended source and report changes with a focused message.
  - Do not leave a completed edit uncommitted.

## Open Author Decisions

These must be resolved before edits that change physics claims or figure content.

1. Diff baseline:
   - Default baseline for `pdf/main-diff.pdf`: the previous version or commit containing substantive manuscript-content edits.
   - For the next pole-framing and concluding-remarks pass, compare against the commit at the start of that pass unless the author specifies another baseline.
   - Ask the author only when this default is ambiguous for a given edit.

2. Reference-corpus workflow:
   - Style references are integrated into the project-level skill at `.codex/skills/bafqmc-prl-revision`.
   - Do not maintain a separate `docs/prl_style_corpus` directory.

## Resolved Author Decisions

- Pairing term in main text should use the Hermitian negative-sign convention `-\Delta b_i^+c_i^+-\Delta^*b_i c_i`.
- The paired sign-free statement allows arbitrary complex `\Delta`; benchmark captions may specify the plotted real `\Delta` axis.
- The main-text application/example section should initially use the real positive triangular hopping used in the benchmark.
- Fig. 1 must remain in the main text.
- Section IV was rewritten first after repository infrastructure and style corpus setup, because the benchmark results define what the manuscript can honestly claim.
- The PRL revision skill should be project-level, not global.
- In manuscript Hamiltonians, use creation superscript `+` rather than `\dagger`, consistent with the draft notation.
- Do not introduce unnecessary intermediate notation such as `a_{\alpha i}` or `n_{i,\pm}` in the benchmark Hamiltonian when direct `b,c` notation is clearer.
- Section III now states the TRS criterion before the RP criterion.
- Main-text Section III should be flat PRL prose with run-in italic heading text, not standalone subsections.
- Main-text criteria should be directly usable by physics readers. Avoid main-text proof vocabulary such as cone, semigroup, generalized eigenspace, and metaplectic branch unless the sentence genuinely needs it.
- The semigroup section in the SM should be deleted rather than repaired. It rested on a decomposition claim that is not needed for the paper and should no longer guide branch or pole language.
- The manuscript should not claim that finite-pairing benchmark trajectories cannot encounter poles for arbitrary chemical potential or auxiliary-field shifts. Pole absence is not part of the sign-free claim.
- The branch of paired Nambu determinant weights should be tied to RP operator positivity and the nonnegative physical representative, not to auxiliary-field path connectivity through a pole-free region.

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

- [x] Step 1: Reorder SM formalism so it follows the reader-friendly order.
  - Current SM formalism order:
    1. HS transformation, including concrete attractive/repulsive identities and benchmark density-channel decoupling.
    2. Number-conserving trace formula.
    3. Number-conserving Green functions.
    4. Number-conserving local update ratio.
    5. Paired/Nambu algebra, trace formula, branch convention, Green functions, and update ratio.
    6. Regularized bosonic weights and pole structure.
    7. Obsolete regularized RP semigroup viewpoint to delete in Phase 6.
    8. Numerical details and benchmark parameters.

- [x] Step 2: Move proof material out of current main-text Section II into SM where not already duplicated.
  - Keep equation labels stable where possible.
  - Add new labels only when necessary for cross references.
  - Section III proof-load reduction remains a separate future pass.

- [x] Step 3: Add numerical-details scaffolding to SM.
  - Include triangular geometry, boundary condition, `K` point convention, observables, `dtau`, samples, block size, ED truncation/cutoff, reliability rules, and paired time-step diagnostics.

- [x] Step 4: Compile.
  - Run: `latexmk main.tex`.
  - Expected: no new undefined references or citation warnings.

## Phase 3: Rewrite Section II

**Files:**
- Modify: `main.tex`.
- Verify references into: `SM.tex`.

- [x] Step 1: Rename Section II to `Bosonic Auxiliary-Field Quantum Monte Carlo`.

- [x] Step 2: Start from the HS ensemble.
  - Retain:
    - the physical HS picture: interactions become one-body Hamiltonians in fluctuating auxiliary fields.
    - `Z=\int \mc D\phi P_{\rm HS}(\phi)W(\phi)`.
    - direct `W(\phi)=\Tr[\prod_\ell e^{\hat h_\ell(\phi_\ell)}]`.
    - a plain explanation that `P_{\rm HS}` is the product of Gaussian factors generated by the HS transformation.

- [x] Step 3: Present number-conserving BAFQMC first.
  - Retain:
    - inline slice form `\hat h_\ell(\phi_\ell)=\hat{\bb a}^+B_\ell(\phi_\ell)\hat{\bb a}`.
    - `W(\phi)=\det(I-\mc B)^{-1}`.
    - the comparison with the fermionic AFQMC determinant.
    - the number-conserving equal-time Green-function identity.
    - a short statement that local updates reduce to low-rank determinant ratios, with details in SM.

- [x] Step 4: Present paired/Nambu BAFQMC second.
  - Retain:
    - inline Nambu notation and commutator definitions near first use.
    - `W(\phi)=\ee^{\sum_\ell\xi_\ell}\det(I-\mc M)^{-1/2}`.
    - a sentence that explicit pairing terms are handled by this anomalous Gaussian trace.
    - branch and Nambu Green-function details in SM.

- [x] Step 5: Move local-update ratio and stabilization details to SM.

- [x] Step 6: Keep only the number-conserving Green-function formula in the main text.
  - Retain the two equal-time blocks `\langle a_i a_j^+\rangle_\phi` and `\langle a_j^+ a_i\rangle_\phi`.
  - Move Nambu Green functions and all local-update derivations to SM.

- [x] Step 7: Compile and inspect.
  - Run: `latexmk main.tex`.
  - Check: no introduced warnings; Section II no longer reads like a derivation.

## Phase 4: Rewrite Section III And Move Proofs To SM

**Files:**
- Modify: `main.tex` around the current `\section{Conditions for nonnegative weights}` block, presently lines 172--343.
- Modify: `SM.tex`, especially the proof-related sections.
- Do not modify: `references.bib` unless a new citation is necessary and its metadata has been verified.

**Main-text contract for this phase:**
- Replace the standalone Section III heading with a PRL-style run-in heading: `{\it Conditions for nonnegative weights}---`.
- Remove the Section III subsections. The main text should be a flat sequence of short paragraphs.
- State the TRS criterion first, because it follows directly from the number-conserving determinant formula.
- State the RP criterion second, because it is broader and covers paired/Nambu slices.
- Main text should contain only criteria, consequences, and references to SM proofs. Avoid the proof vocabulary `cone`, `semigroup`, `generalized eigenspace`, and `metaplectic branch` in the main text.
- Detailed proofs must be in SM and must be expanded rather than compressed.

- Status: substantially completed through commits `caee0e7`, `e2142cb`, `54624cd`, `a8fd48b`, `d501cbf`, `ee3892f`, `bc80cc8`, and `846d3be`. Remaining clean-up belongs to Phase 6 because it concerns pole/branch framing and the obsolete semigroup section rather than the main criteria prose.

- [x] Step 1: Inspect the current Section III and proof support.
  - Run: `sed -n '172,344p' main.tex`.
  - Run: `sed -n '917,1133p' SM.tex`.
  - Run: `rg -n "cone|semigroup|generalized eigenspace|metaplectic|subsection|Reflection positivity|Time-reversal" main.tex SM.tex`.
  - Expected: identify which proof paragraphs are still in main text and which SM proof sections need to receive them.

- [x] Step 2: Flatten the main-text heading and remove Section III subsections.
  - Replace `\section{Conditions for nonnegative weights}` with the run-in paragraph lead `{\it Conditions for nonnegative weights}---`.
  - Remove `\subsection{Reflection positivity}` and `\subsection{Time-reversal symmetry}` from the main text.
  - Keep labels only if they are still referenced. If a label is kept after a run-in heading, put it immediately after the heading text and verify that the reference target remains useful.
  - Run: `rg -n '^\\section|^\\subsection|\\{\\it Conditions for nonnegative weights\\}' main.tex`.
  - Expected: Section III has no `\subsection`, and the run-in heading appears exactly once.

- [x] Step 3: Write the TRS criterion first in reader-facing prose.
  - Keep the criterion in the number-conserving setting only.
  - Keep these main-text objects:
    - `\Theta=UK`, with `UU^*=-I`.
    - the slice condition `U^\hc\overline{B_\ell}U=B_\ell`.
    - the conclusion that the eigenvalues of the full single-particle product give `\det(I_N-\mc B)\ge0`, so the bosonic weight is nonnegative whenever finite.
  - Move the proof that real eigenvalues have even multiplicity to SM.
  - The main text should say the physical reason in one or two sentences: Kramers partners make real eigenvalue crossings occur in pairs, while nonreal eigenvalues come with their complex conjugates.
  - Do not include a generalized-eigenspace proof in `main.tex`.
  - Run: `rg -n "generalized eigenspace|algebraic multiplicity|m_r|Kramers reasoning" main.tex`.
  - Expected: no matches in `main.tex`; the detailed proof is reserved for SM.

- [x] Step 4: Write the RP criterion second in reader-facing prose.
  - Define the reflection in one line, for example `\theta(\hat b_i)=\hat c_i`, `\theta(\ii)=-\ii`, allowing fixed phases only if needed for the paired benchmark.
  - State the sufficient condition as a directly usable reflected-pair form. A compact main-text formula may be:
    ```tex
    \hat h_\ell=\hat q_\ell+\theta(\hat q_\ell)
    +\sum_\mu \hat Y_{\ell\mu}\theta(\hat Y_{\ell\mu})
    +\xi_\ell,
    \qquad \xi_\ell\in\mathbb R .
    ```
  - For Gaussian slices, keep the practical Nambu block test only if it is needed to make the benchmark sign-free check readable:
    ```tex
    \hat h_\ell=\hat\chi^\trans
    \begin{pmatrix}
        D_\ell&F_\ell\\
        F_\ell^\trans&\bar D_\ell
    \end{pmatrix}
    \hat\chi+\xi_\ell,
    \qquad F_\ell=F_\ell^\hc\succeq0 .
    ```
  - Explain in prose that the reflected terms pair each contribution with its reflected partner, so the trace of the full product is nonnegative. Do not prove closure or trace positivity in the main text.
  - Run: `rg -n "cone|Lie-Trotter|semigroup|trace-factorization|\\mc K_\\theta" main.tex`.
  - Expected: no matches in `main.tex`.

- [x] Step 5: End the main-text criteria block with the Fig. 1 message.
  - Required message: TRS and RP identify the RP/TRS half-plane of Fig. 1 as sign-free for BAFQMC, including the frustrated but RP/TRS quadrant that is not naturally covered by world-line methods.
  - Do not repeat the detailed comparison to SSE/WLQMC here if the Introduction and Discussion already cover it.
  - Add cross references to SM proof sections, for example `Sec.~\ref{app:trs_proof}` and `Sec.~\ref{app:rp_proof}` after those labels are created.

- [x] Step 6: Commit the coherent main-text rewrite.
  - Run: `latexmk main.tex`.
  - Expected: compile succeeds. Temporary undefined references are not acceptable; create the SM labels before this commit if the main text already references them.
  - Run: `git add main.tex SM.tex && git commit -m "Flatten nonnegative-weight criteria"`.

- [x] Step 7: Create or reorganize SM proof sections in TRS-then-RP order.
  - Add a clear SM section after the Gaussian-formula sections and before the regularization section, or rename/reorder the existing proof sections, so readers can find the proof immediately after the formulas it supports.
  - Use labels:
    - `\label{app:trs_proof}` for the TRS proof.
    - `\label{app:rp_proof}` for the RP proof.
  - TRS proof content:
    1. State `U^\hc\overline{B_\ell}U=B_\ell` and show it passes to `\mc B`.
    2. Show nonreal eigenvalues pair as `\lambda,\lambda^*`.
    3. Explain real eigenvalues carefully using the invariant generalized eigenspace and `\Theta^2=-1`.
    4. Evaluate `\det(I_N-\mc B)` as products of nonnegative factors.
  - RP proof content:
    1. Define the two reflected Fock spaces and the antilinear map `\theta`.
    2. Define reflected-square sums in SM; it is fine to call this a cone in SM after defining it.
    3. Prove addition, multiplication, and nonnegative trace step by step.
    4. Prove the slice-generator sufficient condition by diagonalizing the positive coupling matrix and using the Lie-Trotter product formula.
    5. Derive the Gaussian/Nambu block criterion from the operator condition.
    6. Keep branch and regularized-weight qualifications separate from the bare-trace positivity proof.
  - Avoid proof shortcuts such as "it is easy to see" or "the same argument gives".

- [x] Step 8: Remove obsolete semigroup material in SM.
  - Delete `Regularized reflection positivity from the semigroup viewpoint`.
  - Remove cross references, labels, and prose that rely on semigroup decomposition, paired pole absence, or branch connectivity.
  - Keep the regularized finite-part interpretation of bosonic determinant weights in the preceding regularization section.
  - Run: `rg -n "semigroup|connected component|pole-free|branch connected|stable zero-field|does not encounter a pole" main.tex SM.tex`.
  - Expected: no remaining semigroup argument or overstrong no-pole claim. Ordinary mentions of determinant poles and finite/infinite variance are allowed.

- [x] Step 9: Verify source-level style constraints.
  - Run: `rg -n "cone|semigroup|generalized eigenspace|metaplectic|Lie-Trotter|\\mc K_\\theta" main.tex`.
  - Expected: no matches in `main.tex`.
  - Run: `rg -n '^\\subsection\\{Reflection positivity\\}|^\\subsection\\{Time-reversal symmetry\\}' main.tex`.
  - Expected: no matches.
  - Run: `rg -n "\\{\\it Conditions for nonnegative weights\\}" main.tex`.
  - Expected: exactly one match.

- [x] Step 10: Compile, refresh PDFs, and inspect warnings.
  - Run: `latexmk main.tex`.
  - Expected: `pdf/main.pdf` refreshed, no undefined references or citation warnings introduced.
  - Refresh diff PDF against commit `7fcd482`:
    ```bash
    BASE=7fcd482
    rm -rf .build/diff-work
    mkdir -p .build/diff-work/old .build/diff-work/new pdf
    git show ${BASE}:main.tex > .build/diff-work/old/main.tex
    git show ${BASE}:SM.tex > .build/diff-work/old/SM.tex
    git show ${BASE}:references.bib > .build/diff-work/old/references.bib
    cp main.tex SM.tex references.bib .build/diff-work/new/
    (cd .build/diff-work/old && latexpand main.tex > ../old.tex)
    (cd .build/diff-work/new && latexpand main.tex > ../new.tex)
    latexdiff --math-markup=0 .build/diff-work/old.tex .build/diff-work/new.tex > .build/diff-work/main-diff.tex
    latexmk .build/diff-work/main-diff.tex
    ```
  - Expected: `pdf/main-diff.pdf` refreshed.
  - Run: `rg -n "Warning|undefined|Citation|Label\\(s\\)|Rerun|Overfull|Underfull|empty year" .build/main.log .build/main-diff.log .build/main.blg .build/main-diff.blg`.
  - Expected: only known baseline warnings remain. If the `SM` empty-year BibTeX warning remains, report it as pre-existing unless this phase changes the `SM` bibliography entry.

- [x] Step 11: Request an independent review before final delivery.
  - Use the review prompts from `.codex/skills/bafqmc-prl-revision/references/review-prompts.md`.
  - Ask specifically:
    - Does main-text Section III state usable TRS and RP criteria without proof burden?
    - Is TRS before RP?
    - Are all proof details now in SM and sufficiently explicit?
    - Does the main text avoid obscure mathematical vocabulary?
  - Address actionable findings, then rerun Step 10.

- [x] Step 12: Commit the final Section III/SM pass.
  - Run: `git diff --check`.
  - Expected: no whitespace errors.
  - Run: `git status --short`.
  - Expected: only intended tracked source changes plus ignored/generated artifacts.
  - Commit:
    ```bash
    git add main.tex SM.tex
    git commit -m "Revise nonnegative-weight criteria"
    ```

## Phase 5: Rewrite Section IV Around The New Benchmarks

**Files:**
- Modify: `main.tex`, `SM.tex`.
- Add or replace: `figures/benchmark_number_conserving.pdf`, `figures/benchmark_pairing_delta.pdf`.
- Possibly remove or leave unused: `figures/benchmark.pdf`.

- [x] Step 1: Copy candidate PDFs into `figures/` with stable names.
  - Number-conserving source: `paper_candidate_main_4x2.pdf`.
  - Paired source: `paper_candidate_main_delta_1x4_linear.pdf`.
  - Status on 2026-06-16: completed for `figures/benchmark_number_conserving.pdf` and `figures/benchmark_pairing_delta.pdf`.

- [x] Step 2: Rewrite the model in one consistent notation.
  - Physical Hamiltonian uses direct `b,c` notation and the Hermitian pairing term `-\Delta b_i^+c_i^+-\Delta^*b_i c_i`.
  - Chemical potential appears in benchmark parameters and captions, not in the physical Hamiltonian.
  - The text defines the triangular primitive vectors and the benchmark hopping convention `t=1`.

- [x] Step 3: Explain sign freedom after HS decoupling.
  - Main text:
    - `U_1` channel gives identical real fields.
    - `U_2` channel gives opposite imaginary fields.
    - two flavors form conjugate/Kramers partners for `\Delta=0`.
    - the paired case uses the RP criterion with the reflection `\theta(\hat b_i)=\ee^{-\ii\varphi}\hat c_i`.
  - SM:
    - full HS formulas and numerical details.

- [x] Step 4: Add paired extension consistently.
  - Use `-\Delta b_i^+c_i^+-\Delta^*b_i c_i`.
  - State that the paired/Nambu formulation is protected by RP.
  - Avoid overclaiming beyond the plotted `3x3` benchmark.

- [x] Step 5: Insert Fig. 2 and Fig. 3.
  - Fig. 2 caption: `U_2` and `U_1` scans, `3x3`, `rho`, `-E`, `S_{\rm SF}(K)`, `S_{\rm DW}(K)`, ED vs BAFQMC, main parameters.
  - Fig. 3 caption: Delta scan, paired/Nambu formulation, same four observables, main parameters.
  - Put detailed MC/ED parameters in SM, not in overloaded captions.

- [x] Step 6: Compile and inspect figures.
  - Run: `latexmk main.tex`.
  - Open `pdf/main.pdf` and inspect layout around Figs. 2 and 3.
  - Completed in commits `a826e73` and `79a1b9b`; `pdf/main-diff.pdf` was generated with SM-aware `latexpand`.

## Phase 6: Align Pole/Branch Framing And Write Concluding Remarks

**Files:**
- Modify: `main.tex`.
- Modify: `SM.tex`.
- Possibly modify: `references.bib` if the concluding outlook needs new verified references.
- Maintain: `docs/superpowers/plans/2026-06-16-prl-manuscript-revision-system.md`.

- [x] Step 1: Update this long-term plan to match the current manuscript state and the revised sign/pole framing.
  - Record that Section II, Section III, Examples/applications, and figure placement are complete.
  - Record that the semigroup route is obsolete and must be deleted.
  - Record that sign freedom and pole/infinite-variance behavior are distinct claims.

- [x] Step 2: Remove the obsolete semigroup section from SM.
  - Delete `\section{Regularized reflection positivity from the semigroup viewpoint}` and all equations and labels used only there.
  - Remove references to paired trajectories avoiding poles, pole-free components, or semigroup decompositions.
  - Keep the operator-level TRS/RP proofs and the regularized finite-part interpretation.
  - Run: `rg -n "semigroup|connected component|pole-free|stable zero-field|does not encounter a pole|branch connected" main.tex SM.tex`.
  - Expected: no obsolete semigroup/no-pole claim remains.

- [x] Step 3: Adjust paired trace and local-ratio branch wording.
  - State that RP fixes the nonnegative weight at the operator level.
  - Present the Nambu determinant square root as the positive branch required by this sign-free representative when the RP criterion applies.
  - Do not invoke auxiliary-field path continuation, low-density connected components, or branch diagnostics.
  - Keep trace-convergence and regularized-weight caveats separate from sign freedom.

- [x] Step 4: Replace current `Discussion` and empty `Summary and outlook` with `Concluding remarks`.
  - Use one run-in heading: `{\it Concluding remarks}---`.
  - Paragraph 1: summarize finite-temperature BAFQMC, the two sufficient sign-free criteria, and the triangular-lattice benchmarks; state that BAFQMC opens a frustrated RP/TRS territory beyond local-weight world-line/SSE restrictions.
  - Paragraph 2: acknowledge the finite-temperature pole/infinite-variance issue as a separate numerical-stability limitation. The tone should be clear but not self-defeating.
  - Paragraph 3: outlook toward frustrated bosonic/spin problems and future bosonic projector or canonical AFQMC. Add only purposeful references, with verified BibTeX metadata.

- [x] Step 5: Update local cross references and intro/abstract roadmap if they still mention a separate Discussion/Summary or overstate pole analysis.
  - Main text should not promise a detailed pole-structure analysis as a central result.
  - It may mention practical finite-temperature pole limitations in the concluding remarks.

- [x] Step 6: Compile and refresh artifacts.
  - Run: `latexmk main.tex`.
  - Refresh `pdf/main-diff.pdf` using the established SM-aware `latexpand` and `latexdiff` workflow against the previous substantive manuscript-content baseline.
  - Inspect `pdf/main.pdf` around the ending and reference list.
  - Run process-language and obsolete-term scans.

- [x] Step 7: Independent review and commit.
  - Use the review prompts from `.codex/skills/bafqmc-prl-revision/references/review-prompts.md`.
  - Ask specifically whether the manuscript now separates sign freedom from pole/infinite-variance limitations and whether `Concluding remarks` sounds like a PRL close.
  - Address actionable findings, rerun verification, then commit the coherent manuscript pass.

## Phase 7: Iterative Main/SM Refinement, Abstract, References, And Notation

**Files:**
- Modify: `main.tex`, `references.bib`.
- Modify as needed in later feedback rounds: `SM.tex`.

- [x] Step 1: Update Introduction only after Sections II to V stabilize.
  - Make it a complete, continuous story that introduces Fig. 1 naturally.
  - Align claims with actual Fig. 2/Fig. 3 content.
  - Remove long roadmap paragraph unless it earns its space.
  - Add missing literature citations at the appropriate claims, with metadata verified first.
  - Status: completed in commit `4d4d766` with a citation-audit report in `docs/research_reports/2026-07-08_introduction_citations/`.

- [ ] Step 1a: Enter the iterative author-feedback refinement stage.
  - Apply the `Current Iterative Refinement Protocol` to every future detail-revision round.
  - Expect repeated passes over the main text and SM, especially derivations, notation, cross references, branch/regularization language, numerical-algorithm descriptions, and reader-facing prose.
  - Do not defer review, notation/heading/prose audit, or citation/BibTeX audit to a final cleanup stage. Each round must include them before delivery.

- [x] Step 2: Write the abstract last.
  - Constraint: no more than 600 characters including spaces for PRL.
  - Include: BAFQMC, sign-free criteria, frustrated bosonic models, benchmark.
  - Exclude: local update ratios, long pole discussion, implementation details.
  - Status: rewritten in the 2026-07-09 abstract pass as a 593-character PRL-style abstract centered on frustrated bosons, auxiliary-field symmetry criteria, and the triangular-lattice benchmark.

- [ ] Step 3: Audit references.
  - Maintain the Introduction citation audit already created for the 2026-07-08 pass.
  - Add complete BibTeX for any missing comparison Letter/Rapid papers only if they are cited or needed for style/context.
  - Verify metadata against arXiv, DOI, or APS pages before editing `references.bib`.
  - Run a missing-citation-key scan in every manuscript-edit round, even when no bibliography entries are changed.

- [ ] Step 4: Audit notation.
  - Maintain manuscript macros: `\mc`, `\bb`, `\Tr`, `\ee`, `\ii`, `\hc`, `\trans`, `\Omega`.
  - Decide whether to retain `a^+` notation globally or migrate to `a^\dagger` in a separate author-approved pass.
  - Check `Eq.~\eqref{...}`, `Fig.~\ref{...}`, and `Sec.~\ref{...}` style.
  - Run this audit every round, not only once before final submission.

- [x] Step 5: Apply the PRL run-in heading style consistently in the main text.
  - Convert standalone main-text `\section{...}` headings to compact italic paragraph leads, for example `{\it Bosonic auxiliary-field quantum Monte Carlo}---`.
  - Keep ordinary numbered `\section` and `\subsection` headings in `SM.tex`; the run-in style is for the Letter main text only.
  - Preserve cross references only where they still help the reader. If a main-text `\label` no longer points to a numbered section, either move the label to a stable nearby anchor or rewrite the reference so it does not rely on section numbering.
  - Run: `rg -n '^\\section|^\\subsection|\\{\\it ' main.tex`.
  - Expected: no standalone `\section` or `\subsection` headings remain in `main.tex`, and each run-in heading begins a coherent PRL-style paragraph.
  - Status: current main text has run-in headings for Introduction, BAFQMC formalism, nonnegative-weight criteria, examples, and Concluding remarks.

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
- [x] Run baseline compile and record warnings.
- [x] Copy the two benchmark PDFs into `figures/` with approved names.
- [x] Add SM numerical-details section using the two reports.
- [x] Rewrite Section IV first, because the new benchmark results now define what the manuscript can honestly claim.

This starts with the repository infrastructure and style calibration, then moves to the unfinished application section. The Introduction should be rewritten after the core results and benchmark narrative are stable.

## Completed Execution Block: Section II And SM

The Section II/SM formalism and algorithm pass is complete as of commit `7fcd482`.

- [x] Compress the opening of Section II so it defines the BAFQMC ensemble without deriving the HS transformation in detail.
- [x] Present number-conserving determinant and Green-function formulas before paired/Nambu formulas.
- [x] Move commutator identities, linear-action derivations, local-update ratio derivations, Sherman-Morrison/Woodbury updates, branch discussion, and stabilization details out of the main text.
- [x] Keep in the main text only the formulas needed later by Section III and Section IV: `Z`, `W`, the number-conserving determinant, the paired determinant, and one Green-function identity.
- [x] Expand SM rather than merely shorten the manuscript: include concrete HS identities, b/c conjugacy, determinant ratios, Green updates, Nambu local blocks, stabilization, and numerical parameters.
- [x] Compile with `latexmk main.tex`, refresh `pdf/main.pdf`, and generate `pdf/main-diff.pdf`.

## Completed Execution Block: Section III Criteria

The main-text criteria rewrite is complete as of commits `caee0e7` through `846d3be`.

- [x] Rewrite main-text Section III as a flat PRL-style criteria block headed by `{\it Conditions for nonnegative weights}---`.
- [x] State the TRS criterion first in theorem-like form.
- [x] State the RP criterion second in theorem-like form, including phases in the reflection.
- [x] Move proof details to SM and keep the main text focused on usable criteria.
- [x] Remove main-text subsections and main-text proof vocabulary.
- [x] Compile with `latexmk main.tex`, refresh `pdf/main.pdf`, generate `pdf/main-diff.pdf`, and commit the completed Section III/SM pass.

## Completed Execution Block: Pole Framing And Concluding Remarks

The pole/branch framing and ending rewrite are complete as of commits `f00aec9` through `07568ac`.

- [x] Delete the obsolete SM semigroup section and remove dependent branch/no-pole claims.
- [x] Rephrase paired Nambu square-root branch language so RP operator positivity fixes the positive branch in sign-free applications.
- [x] Keep the regularized finite-part interpretation of determinant weights in the SM, while keeping the main-text criteria focused on the sign problem.
- [x] Replace the old discussion/outlook material with three-paragraph `{\it Concluding remarks}---`.
- [x] Add only necessary outlook references after verifying metadata.
- [x] Compile with `latexmk main.tex`, refresh `pdf/main.pdf`, generate `pdf/main-diff.pdf`, run prose review, and commit the completed pass.

## Completed Execution Block: PRL Introduction Rewrite

The Introduction rewrite was completed in the 2026-07-08/2026-07-09 pass and committed as `4d4d766`.

- [x] Commit the initial plan update before changing manuscript sources.
- [x] Map the Introduction story into four to five PRL paragraphs:
  - QMC as a numerically exact nonperturbative tool and the sign problem as the key tractability boundary.
  - The conventional bosonic/spin local-weight viewpoint, where frustration in WLQMC/SSE creates negative weights and makes many frustrated models inaccessible.
  - The auxiliary-field viewpoint, where positivity is controlled by symmetries of HS-decoupled one-body propagators rather than by local matrix elements.
  - The missing bosonic AFQMC sign-free framework and the central question answered by this work.
  - The BAFQMC answer: finite-temperature method, TRS/RP sufficient criteria, Fig. 1 classification, and triangular-lattice benchmark.
- [x] Dispatch focused literature-research subagents or perform equivalent focused searches for the Introduction citation clusters:
  - General QMC/sign-problem background and computational complexity.
  - WLQMC/SSE, Marshall sign transformations, frustration, and bosonic/spin sign problems.
  - Frustrated bosonic/spin target physics such as fractional quantum Hall, chiral Mott, spin liquid, and directly relevant multi-boson orders.
  - Fermionic AFQMC sign-free criteria based on TRS, RP, Majorana positivity, and related symmetry principles.
  - Earlier bosonic AFQMC uses and their limitations.
- [x] Verify every new or edited BibTeX entry against an authoritative source such as APS, DOI/Crossref, arXiv, publisher pages, or journal pages. Do not infer author lists, article numbers, years, or DOIs from memory.
- [x] Write a citation report for author review that states which claim each reference supports, why it belongs in the Introduction, and which source verified the metadata.
- [x] Rewrite the Introduction in `main.tex` with confident PRL prose. Avoid defensive wording, process-facing explanations, unnecessary mathematical jargon, and premature discussion of SM regularization.
- [x] Keep display equations out of the Introduction unless absolutely necessary. Use Fig. 1 as the conceptual map rather than a late afterthought.
- [x] Run `opencode` prose review on the revised Introduction and address actionable reader-facing findings.
- [x] Compile with `latexmk main.tex`, refresh `pdf/main.pdf`, and generate `pdf/main-diff.pdf` against the previous substantive manuscript-content baseline.
- [x] Run warning/process-language scans, report any remaining warnings, and commit the completed Introduction pass.

## Active Next Block: Iterative Detail Refinement

The next work block is not a single final cleanup. The author will continue giving detailed feedback on the main text and SM, and each feedback round should be treated as a complete edit-review-verify-commit cycle.

- [ ] Apply author feedback to the targeted manuscript region.
- [ ] Review the changed text from the reader's perspective.
- [ ] Audit notation, headings, prose, and cross references.
- [ ] Audit citations and BibTeX keys; verify metadata for any added or changed references.
- [ ] Compile with `latexmk main.tex`, refresh `pdf/main.pdf`, and refresh `pdf/main-diff.pdf` for manuscript-source edits.
- [ ] Commit each completed round before delivery.
