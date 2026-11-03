# Citation Research And Required PDF Cache

Read the claim and its context before selecting references. Use original papers,
reviews, and citation chains as needed to understand the relevant literature.
Choose sources for their actual support of the text, and verify metadata using
`reference-verification.md`. Broad coverage is valuable when it serves the physics.

Keep the manuscript's physical story intact when adding citations. Distinguish
method developments, theorems, applications, and motivating physical phases.
A new reference does not by itself require an extra sentence or a larger rewrite.

Maintain complete local PDF coverage for all external references cited in the main
text and SM. This is a standing requirement, not an optional research convenience.

## Local PDF Cache

The local cache is part of the evidence workflow and is intentionally ignored by Git.

- `local_reference_pdfs/manuscript/`: every external key currently cited by `main.tex` or `SM.tex`, named exactly `<citation_key>.pdf`.
- `local_reference_pdfs/candidates/`: papers seriously considered, audited, or offered as alternatives.
- `local_reference_pdfs/context/`: entry papers and writing-style samples that are not automatically manuscript citations.
- `cache-manifest.tsv`: current manuscript coverage and identity status.
- `candidates-manifest.tsv`: candidate files, aliases, source URLs, and access limitations.

Requirements:

1. Download a PDF or legitimate arXiv/author-manuscript version for every current external citation.
2. Validate files with `file`, `pdfinfo`, and first-page text or visual inspection.
3. Do not use a related paper, thesis, webpage print, reconstructed PDF, empty file, or screenshot as a substitute for the cited article.
4. If an author thesis is useful but distinct from a journal article, give it its own key and label the distinction explicitly.
5. Use aliases in the candidate manifest instead of duplicating identical PDFs under several names.
6. Keep the directory structure simple and document it in `local_reference_pdfs/README.md`.
7. When citations change, reconcile TeX keys, BibTeX keys, filenames, and both manifests.
8. Record access-controlled items honestly. Do not call the candidate cache complete without stating exact exceptions.

## Reports

When a report is requested, organize it around the author's question and the
scientific evidence. Explain what the relevant papers establish and how they
support the manuscript. Link to exact cached PDFs where useful. Report uncertain
metadata and missing or inaccessible sources explicitly.

Choose the format and detail suited to the request. Citation counts, referee
suggestions, and full sentence-by-sentence audits are useful only when relevant;
they are not required deliverables for routine citation work.
