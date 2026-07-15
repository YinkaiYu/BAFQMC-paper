# Citation Research, Evidence Cache, And Reports

Use this file for citation research throughout the manuscript, bibliography audits, reviewer coverage, PDF caching, and HTML research reports. It applies the general story-and-evidence method in `manuscript-story-evidence-principles.md`; the Introduction examples below illustrate the method rather than limiting it.

## Research Before Writing

Do not begin by searching a few keywords and attaching the first matching reviews. Build the field map first.

1. Read the current sentence and identify its exact evidence obligations.
2. Use author-provided papers and reviews only as entry points.
3. Inspect their reference lists, the references of the most relevant cited papers, and supplements when they contain a literature map.
4. Follow the chain to original results, classic foundations, modern reviews, recent developments, and active research groups.
5. Search beyond the supplied seeds for missing communities and newer work.
6. Only after the field map is coherent should citations be selected and prose revised.
7. After drafting, run a second sentence-by-sentence search from the current Introduction to find omissions, better sources, and citations that do not actually support the claim.

Examples of useful entry points include the project's arXiv context papers and broad sign-problem reviews. They are not automatically citations. Their main value may be the literature and conceptual distinctions they reveal.

## Evidence Obligations By Sentence

Split a sentence into claims before selecting references. A sentence can contain several citation clusters.

For example, the first-paragraph impact sentence has three conceptual clusters:

1. QMC's major physical achievements;
2. the ongoing development of sign-problem-free formulations;
3. a deepening understanding of the sign problem and the avoid/mitigate methods it inspired.

The third cluster may use two adjacent `\cite` commands when the prose distinguishes understanding from mitigation. Record all keys under the correct subcluster.

For a list of physical phenomena, place citations immediately after each example. Do not make the author or reader reverse-engineer one large end-of-sentence pile.

## Source Selection

Priority is semantic fit first, authority second, strategic coverage third.

- Prefer original method or result papers for concrete historical claims.
- Use classic textbooks for broad foundational framing, not as substitutes for original QMC method history.
- Use reviews as maps and entry points; do not present them as original criteria or discoveries.
- A highly cited paper is not suitable if it does not discuss the claim. Marshall 1955, for example, is important for bipartite antiferromagnetic sign structure but does not belong in a sentence about the historical development of sign-problem-free QMC.
- Distinguish exact sign-free formulations, sign mitigation, constrained or phaseless approximations, and physical studies made possible by sign-free QMC.
- Distinguish locality-qualified no-go results from claims about arbitrary nonlocal or determinant QMC formulations.
- Do not infer that a phase paper proves a sign barrier. Phase papers establish the physical target; method and no-go papers establish computational obstruction.

## Breadth And Strategic Citations

Broad citation coverage is an explicit project goal, provided it does not disrupt the narrative or misrepresent the literature.

- Include relevant work from neighboring communities and active groups, including papers that may help prospective PRL referees recognize their field in the manuscript.
- Identify potential referees by name, not only by community. Favor scholars active in recent years and record the papers that make them relevant.
- Include recent work even when citation counts are low, while retaining classic high-authority anchors.
- Large citation clusters are acceptable. Compress the prose, not the evidence.
- Do not insert a sentence solely to cite a person. Find the legitimate claim that the paper supports, or keep it as a report-level candidate.

## Metadata Verification

Before adding or changing BibTeX, verify against primary or authoritative sources:

- complete author list;
- exact title;
- journal, volume, page or article number, and year;
- DOI;
- arXiv identifier and version when relevant.

Use publisher pages, DOI/Crossref, arXiv records, and author or institutional repositories. Never guess metadata from memory. Check that the cached PDF title and authors match the intended record.

Report every added or modified BibTeX key and its verification source for author review.

## Citation Counts

Research reports should give a citation-count snapshot for current and candidate literature when feasible.

- Name the database and snapshot date.
- Do not compare counts from different databases as though they were one scale.
- Treat counts as a guide to prominence, not a substitute for relevance or recency.
- Preserve genuinely new papers with few or zero citations when their content is directly relevant.

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

## Chinese HTML Report

When the author requests an Introduction or reference audit, write a detailed standalone HTML report in Chinese. It should be readable as an author-facing research document, not a log of agent actions.

For each current abstract, Introduction, or Fig. 1 sentence, include:

- the exact English sentence;
- its narrative purpose;
- its position in the story;
- physics that needs explanation or scope control;
- current citation keys, grouped by the actual conceptual cluster or `\cite` position;
- what each cited paper actually does;
- why it supports this sentence;
- priority A/B/C;
- citation count, database, and date;
- additional candidates and their tradeoffs.

Compare substantive writing changes with the author's Chinese mother draft, not with previous agent reports. Previous reports are research inputs, not the author's evaluation baseline.

Avoid invented audit jargon or unexplained new concepts. Use ordinary Chinese and explain domain terms before relying on them.

Make every citation key a relative hyperlink to the exact local PDF when one exists. For multi-cluster sentences, list every key under its cluster rather than reporting only a total count. Validate all links from the report path.

End with cache status, metadata uncertainties, access-controlled exceptions, and a compact author decision list. Browser-check desktop and mobile layouts and click at least one manuscript PDF and one candidate PDF.

## Research Report Versus Manuscript

The report may be exhaustive; the manuscript must remain story-led. Use the report to preserve caveats, alternatives, rejected sources, citation counts, and referee strategy. Transfer only the minimum prose needed to make the paper compelling and correct.
