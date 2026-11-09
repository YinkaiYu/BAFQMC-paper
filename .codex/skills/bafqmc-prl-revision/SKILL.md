---
name: bafqmc-prl-revision
description: Research and revise the BAFQMC manuscript with clear, confident physics prose, complete derivations, and verified references.
metadata:
  compatibility: codex opencode
---

# BAFQMC Manuscript Revision

Help readers understand the physics and appreciate the work's importance. Use the
current manuscript and the user's task as the starting point. Follow repository
`AGENTS.md` for builds, diff PDFs, Git, and the required full reference cache.

## Writing Principles

- Be confident and direct. State established results firmly and avoid unnecessary
  defensive qualifications. Let the physical advance and its consequences carry
  the significance.
- Write for broad physics readers, making both mathematical reasoning and physical
  meaning clear. Mathematics and physical intuition may appear in either order or
  develop together. Show the derivation steps needed for understanding; qualitative
  discussion cannot replace them. Explain the meaning, assumptions, and purpose of
  mathematical terms and results when introducing them.
- Let the physical purpose guide the derivation. Prefer elementary, intuitive
  arguments with explicit steps. When abstract mathematics is useful, explain its
  content and its connection to the physical problem.
- Readers encounter the text sequentially and have no collaboration context.
  Never write sentences that deliberately answer a private request, echo feedback,
  or advertise a revision.
- Reduce reading burden. Use familiar physics language, explain unfamiliar ideas,
  and avoid obscure mathematical jargon, invented concepts, internal abbreviations,
  and piles of specialist terms.
- Introduce new variables, symbols, definitions, or other entities only when they
  help the reader. Do not replace explanation with shorthand or force backward
  searches through the paper.
- Keep the Letter concise and physically intuitive. Write the Supplemental
  Material like detailed lecture notes, including the intermediate derivations and
  implementation details readers need to learn and reproduce the work.
- Complete the reasoning during research: do not skip necessary derivations,
  algebra, assumptions, branch choices, or checks. Then choose an economical
  presentation without sacrificing correctness or essential conditions.
- Preserve contextual continuity and mature author-approved prose. Understand a
  paragraph's physical purpose before changing it.
- Prefer positive, direct sentences. Avoid "not X, but Y" and similar constructions,
  and use semicolons, colons, and dashes sparingly.
- Verify bibliographic information against authoritative sources. Every citation
  must support its claim, and every cited external paper must have a local PDF.
  Never invent metadata or substitute a different paper for a missing source.

## Supporting References

Read only what helps the task. These are aids to judgment, not a mandatory sequence
or a fixed manuscript template.

- [Story and reader clarity](references/manuscript-story-evidence-principles.md).
- [Introduction and frontmatter](references/introduction-frontmatter-guidelines.md).
- [Formalism and derivations](references/formalism-algorithm-guidelines.md).
- [Reference verification](references/reference-verification.md) and
  [literature research and required PDF cache](references/citation-research-and-reporting.md).
- [Revision workflow](references/revision-workflow.md) and
  [review questions](references/review-prompts.md).
- [Style analysis](references/style-analysis.md),
  [short voice cues](references/style-micro-excerpts.md), and
  [optional paragraph patterns](references/paragraph-blueprints.md).
  Learn from the examples without copying wording or importing their claims.

Reference PDFs are in `assets/reference-pdfs/`; `scripts/count_pdf_words.py` is
available for approximate PDF word counts when useful.
