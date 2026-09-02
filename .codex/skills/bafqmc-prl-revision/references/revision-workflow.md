# Revision Workflow

Use this workflow for every substantive manuscript-edit round. Start with
`manuscript-story-evidence-principles.md`; section-specific references refine this
workflow but do not replace it.

## Frame The Edit

Before changing prose, write down four things for the target unit:

1. **Scientific job:** what must the reader understand, believe, or remember?
2. **Reader state:** what has already been defined, and what is still unfamiliar?
3. **Narrative move:** does this unit establish a problem, reverse an assumption,
   introduce a mechanism, prove a result, validate it, or state its consequence?
4. **Evidence obligation:** which statements need citations, equations, proof,
   numerical comparison, or a figure?

Then inspect the current text, nearby sections, reports, figures, bibliography, and
Git history. For mature prose, identify the author-approved baseline and preserve
its purpose unless new evidence reveals a real scientific or logical defect.

## Research Before Rewriting

- Build enough subject context to distinguish central results, accepted background,
  open questions, and neighboring work.
- Use references as evidence for an already understood scientific story. Do not let
  the order in which papers were found determine the paragraph structure.
- When adding a citation to settled prose, first test whether the existing sentence
  can carry it. Do not insert a literature-facing sentence solely to mention a paper.
- Decide which detail belongs in the Letter, which belongs in the SM, and which
  belongs only in an author-facing report.
- Follow `reference-verification.md` for every new or changed bibliography entry.

## Draft And Revise

- Keep edits local unless notation, cross-references, figures, or claims require
  coordinated changes.
- Preserve equation labels and established notation where possible.
- Build paragraphs by causal logic, not by a fixed template or literature taxonomy.
- Explain the physical picture before compressing it into specialist terminology.
- Keep confidence proportional to the demonstrated result. Remove routine defensive
  qualifications, but preserve assumptions that change the theorem or conclusion.
- Do not introduce process-facing prose or language that answers the author-assistant
  conversation.
- For this project, preserve the current pairing convention
  `-\Delta b^+c^+ - \Delta^*bc` and the approved triangular-lattice example unless
  the authors reopen those decisions.

## Post-Draft Audits

Read the changed text once for each independent question:

1. **Story:** does every paragraph advance the scientific argument?
2. **Sentence purpose:** does every sentence earn its place?
3. **Reader burden:** are concepts introduced before use, with no unexplained jump?
4. **Evidence:** is every externally checkable claim supported by the right kind of
   source or derivation?
5. **Precision layer:** are technical caveats placed where readers need them?
6. **Voice:** does the text sound like a paper for readers rather than revision notes?
7. **Mentor calibration:** does high-visibility prose preserve the hierarchy of broad
   stakes, concrete obstruction, conceptual reversal, proved result, validation, and
   specific opportunity established in commit `66c6cd4`, without copying its wording
   or adding unsupported intensifiers?
8. **Consistency:** do notation, claims, captions, equations, and SM agree?

After high-stakes prose, use `review-prompts.md` with a fresh-context reviewer when
available. For a researched Introduction, repeat the citation search sentence by
sentence after the draft is stable; this second pass is for missing or better
evidence, not an invitation to replace the approved narrative.

## Build And Deliver

When TeX, BibTeX, or tracked figure content changed:

1. Compile:

```bash
latexmk main.tex
```

2. Refresh `pdf/main.pdf`.
3. Refresh `pdf/main-diff.pdf` against the previous substantive content-edit commit,
   unless the author specifies another baseline. When using `latexpand`, run it from
   the old and new source directories so `\input{SM.tex}` expands the matching SM.
4. Run a process-language scan on changed manuscript files:

```bash
rg -n "we add|as requested|this revision|to address|we now clarify|requested benchmark|the manuscript currently|this addresses|we have added|we now modify" main.tex SM.tex
```

5. Inspect relevant warnings, citations, labels, figure placement, page flow, and the
   visual diff.

When only skill or report files changed, validate those artifacts instead of running
an irrelevant manuscript build. Commit every coherent tracked edit round.

## Review Gates

A round is not complete until:

- The changed artifact builds or validates.
- The changed section has no unfinished markers.
- Figure references and captions match the actual figures.
- New or changed references have verified metadata.
- The prose preserves the intended scientific job and causal story.
- A fresh independent review has checked reader-friendliness, style fit, physics
  claims, evidence fit, and process-facing language when the edit warrants it.
