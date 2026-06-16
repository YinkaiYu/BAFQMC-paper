# PRL Physics Manuscript Revision Skill Proposal

## Proposed Skill

- Name: `prl-physics-manuscript-revision`
- Purpose: guide Codex when revising theoretical-physics manuscripts toward a PRL-like style.
- Trigger examples:
  - "Rewrite this manuscript in PRL style."
  - "Condense this theory section and move details to the Supplemental Material."
  - "Check whether this Introduction tells a coherent physics story."
  - "Review this paragraph with the style of sign-problem-free QMC Letters in mind."

## Intended Scope

The skill should provide process and style constraints:

- Build the story around the manuscript's own core figure or classification.
- Keep main-text claims positive and direct.
- Avoid unnecessary "not ... but ..." constructions.
- Minimize dashes.
- Move derivations, branch choices, update formulas, numerical details, and caveats to SM when they interrupt the main Letter story.
- Use style-reference papers only for rhetorical structure and compression.
- Verify every new reference before editing BibTeX.
- Use `opencode` as an optional external prose reviewer for high-stakes paragraphs.
  - Local command form: `opencode run -m deepseek/deepseek-v4-pro "<review prompt>"`.

## Out Of Scope

The skill should not encode paper-specific facts:

- No private benchmark paths.
- No BAFQMC-specific theorem statements.
- No fixed Fig. 1 wording.
- No hard word-count limits beyond checking the journal and reference corpus.

## Resources To Bundle

- `references/sign_problem_letter_style.md`: concise lessons from the four reference papers.
- `references/reference_verification.md`: checklist for adding BibTeX entries.
- Optional script `scripts/count_pdf_words.py`: approximate PDF word counting with PyMuPDF for local style calibration.

## Recommended Creation Path

If approved, create it under `$CODEX_HOME/skills/prl-physics-manuscript-revision` so future Codex sessions can discover it automatically. Keep the repository's `docs/prl_style_corpus/` as the paper-specific working notes and do not include private paths in the global skill.
