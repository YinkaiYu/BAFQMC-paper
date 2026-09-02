---
name: bafqmc-prl-revision
description: Use when revising, researching, deriving, auditing, or reviewing this BAFQMC manuscript for PRL, including scientific prose, formalism, Supplemental Material, references, figures, benchmarks, layout, and author-facing reports.
metadata:
  compatibility: codex opencode
---

# BAFQMC PRL Revision

## Objective

Develop the manuscript as a confident, physically transparent PRL. Preserve full
scientific rigor while making the logic, importance, and consequences accessible to
the broadest reasonable theoretical-physics audience.

## Progressive Disclosure

Load only the guidance needed for the current task:

- Any prose, equation, figure, or report: start with
  `references/manuscript-story-evidence-principles.md`.
- Current project claims, notation, model choices, figures, layout, and build state:
  `references/project-specific-decisions.md`.
- Title, abstract, Introduction, Fig. 1, or its caption:
  `references/introduction-frontmatter-guidelines.md`.
- Scientific voice and paragraph organization: `references/style-analysis.md`,
  `references/style-micro-excerpts.md`, and `references/paragraph-blueprints.md`.
- Formalism, derivations, algorithms, numerical stabilization, or reproducibility:
  `references/formalism-algorithm-guidelines.md`.
- Citation research, BibTeX, PDF cache, potential referees, or HTML reports:
  `references/citation-research-and-reporting.md` and
  `references/reference-verification.md`.
- Editing, build, diff, and delivery procedure: `references/revision-workflow.md`.
- Independent post-edit review: `references/review-prompts.md`.

Task-specific guidance overrides a generic pattern when the two conflict.

## Reader-First Writing

- Write for readers who encounter the paper sequentially and have none of the
  authors' internal context. Every section, paragraph, sentence, equation, symbol,
  citation, and figure must have a reader-facing scientific job.
- Lower reading burden actively. Introduce the physical object and motivation before
  compact formalism, and explain an unfamiliar distinction before naming it.
- Prefer ordinary theoretical-physics language over obscure mathematical jargon.
  Never use invented concepts, private labels, code names, or internal abbreviations
  as substitutes for explanation.
- Do not transfer work to the reader through unexplained terminology, missing steps,
  abrupt logical jumps, backward searches, or lists of specialist vocabulary.
- Keep the logic smooth and cumulative. Each sentence should follow from what the
  reader already knows and prepare what comes next.
- Use notation economically. Introduce a new variable, symbol, acronym, definition,
  or conceptual entity only when it is reused or materially reduces the reader's
  work. If it is unnecessary, leave it out.
- Do not generalize notation or claims beyond what the manuscript uses unless the
  broader statement is itself a result worth establishing.
- Do not overcompress. PRL economy removes detours and repetition while preserving
  the physical picture, essential derivation, and logical bridge.

## Scientific Story And Voice

- Use the mentor-revised abstract, Introduction, and Concluding remarks recorded in
  commit `66c6cd4` as the strongest project-local voice calibration. Preserve their
  hierarchy of stakes, obstruction, conceptual reversal, result, validation, and
  opportunity while allowing future prose to improve. Do not freeze or mechanically
  imitate individual sentences.
- Organize the paper around the significance of its own question and result. Prior
  literature, technical detail, and caveats support that story rather than control it.
- Build a causal progression from consequential problem to obstruction, mechanism,
  formal result, validation, and scientific opportunity. Avoid catalogue prose.
- In high-visibility prose, lead from the broadest supportable physical stakes and
  delay technical mechanism until it creates explanatory leverage. For this paper,
  the decisive turn is from local matrix-element weights in WLQMC/SSE to global
  symmetry-protected weights after HS decoupling.
- State established results directly and confidently. Do not weaken important claims
  with defensive qualifications that do not change their truth or interpretation.
- Preserve every assumption or limitation that does change a theorem, applicability,
  evidence level, or reproducibility. Confidence never licenses mathematical
  overclaiming.
- Prefer positive sentence construction. Avoid unnecessary `not ... but ...` or
  similar negation-then-correction rhetoric. Minimize semicolons, conspicuous colon
  constructions, parentheses, dashes, and repeated superlatives.
- Use Zi-Xiang Li's papers as references for direct, confident, broad-reader physics
  prose. Learn their rhetorical habits without copying wording or importing claims.
- Make the conclusion do conceptual work: state the unifying principle, connect it
  to the benchmark, distinguish sign positivity from the pole/variance problem, and
  end with concrete computational directions rather than a generic promise of future
  work.
- Never write manuscript prose that answers an author request, advertises a revision,
  or deliberately echoes private feedback. If a sentence is not for an unfamiliar
  reader, remove it.

## Rigor Before Compression

- During research and derivation, do not skip algebra, assumptions, branch choices,
  limiting cases, or consistency checks. Work out every nontrivial step needed to
  establish correctness, even when the final Letter will show only the key steps.
- Verify a formula against the actual physical measure, Hamiltonian, algorithm, and
  implementation. Do not introduce a convenient operation or diagnostic that the
  method does not use.
- Distinguish mathematical identities, physical assumptions, numerical
  stabilization, implementation choices, and empirical observations.
- Define operators, matrices, indices, fields, and commutators before use. Keep
  operator and matrix language precise.
- Research may be exhaustive; presentation must be selective. Compression happens
  only after the derivation and evidence have been checked.

## Main Text And Supplemental Material

- The main Letter should be broad, concise, physically intuitive, and story-led. It
  carries the motivation, physical picture, central assumptions and results, decisive
  formulas, validation, and consequences.
- The Supplemental Material should read like a careful technical lecture. Preserve
  full derivations, conventions, branch conditions, update formulas, stabilization,
  parameters, and reproducibility details so a specialist can follow and implement
  the work.
- Moving detail out of the Letter must not remove support from the manuscript as a
  whole. Expand the SM when shortening the main text would otherwise create a gap.
- Let each part do its own job. Do not force every qualification, derivation, physical
  implication, or literature branch into the same section.

## Evidence And Academic Integrity

- Treat citations, equations, figures, and benchmarks as distinct evidence. Use each
  only for claims it can establish.
- Every citation must support the exact nearby claim. Broad coverage and strategic
  community citations are welcome only when the local semantic fit is defensible.
- Verify all BibTeX metadata against authoritative records. Never guess, fabricate,
  or silently substitute bibliographic information; reference accuracy is an
  academic-integrity requirement.
- Derivations and numerical claims require the same discipline. Report the evidence
  level honestly without burying the paper's contribution in routine disclaimers.

## Required Workflow

1. Inspect the current manuscript, nearby context, relevant reports and code, Git
   status, and task-specific guidance before editing.
2. State the scientific job, reader state, narrative move, and evidence obligation of
   the target unit.
3. Complete the necessary research or derivation before compressing the result into
   manuscript prose.
4. Make scoped changes that preserve mature author-approved logic and unrelated work.
5. Audit the result for story, reader burden, notation economy, physics, evidence,
   consistency, and process-facing language.
6. Follow `references/revision-workflow.md` for independent review, compilation, PDF
   refresh, diff generation, warnings, and delivery.
7. Commit each coherent tracked edit round.

## Completion Gate

Do not claim completion until:

- the changed artifact builds or validates;
- the derivation and physics claims have been checked at the required depth;
- the prose is sequentially understandable without private collaboration context;
- notation, equations, citations, figures, main text, and SM are mutually consistent;
- new or changed references have authoritative metadata;
- relevant manuscript PDFs and diffs are current; and
- tracked changes are committed while unrelated user changes remain intact.

## Assets

- Style PDFs: `assets/reference-pdfs/`.
- Voice cues: `references/style-micro-excerpts.md`.
- Paragraph patterns: `references/paragraph-blueprints.md`.
- Approximate PDF word count: `scripts/count_pdf_words.py`.
