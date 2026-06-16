# Sign-Problem-Free QMC Letter Style Corpus

This note records local style calibration for rewriting the BAFQMC manuscript toward a PRL-like presentation. The cited papers are style references only. Their physics content should not redirect the claims of the bosonic BAFQMC manuscript.

Local PDF cache:

- `docs/prl_style_corpus/pdfs/1408.2269.pdf`
- `docs/prl_style_corpus/pdfs/1506.05349.pdf`
- `docs/prl_style_corpus/pdfs/1601.01994.pdf`
- `docs/prl_style_corpus/pdfs/1601.05780.pdf`

The PDF cache is ignored by git. Keep only notes and derived analysis under version control.

## Length Calibration

Word counts below are approximate. They were extracted from arXiv PDFs with PyMuPDF and counted before acknowledgments or appendices when a reliable marker was present. The counts include title/author/abstract text and are not APS production word counts.

| Paper | PDF pages | Cut marker | Approx. words before marker | Approx. full-PDF words | Notes |
| --- | ---: | --- | ---: | ---: | --- |
| arXiv:1408.2269, PRB 91, 241117(R) (2015) | 7 | `Appendix` | 4417 | 5336 | Rapid Communication with appendix-like material in same arXiv PDF. |
| arXiv:1506.05349, PRL 115, 250601 (2015) | 7 | `Acknowledgements` | 3677 | 5504 | PRL-style main text plus references/supplement-related material. |
| arXiv:1601.01994, PRL 116, 250601 (2016) | 8 | `Acknowledgments` | 3655 | 6143 | arXiv long version includes appendices after the main article. |
| arXiv:1601.05780, PRL 117, 267002 (2016) | 8 | `Acknowledgement:` | 3765 | 6228 | PDF includes references and supplement after main article. |

Working implication: a realistic main-text target for the BAFQMC manuscript is closer to a compact 4.5--5 page Letter than to an artificially tight 3000-word article. The main text should still remove derivation-heavy passages from Sections II and III.

## Shared Style Patterns

- The opening frames a broad computational obstacle, then quickly identifies the new organizing principle.
- The core result is stated as a principle or sufficient condition before detailed proof.
- Proof sketches in the main text are short and physical. Algebraic details move to appendices or Supplemental Material.
- The central equations are few and high-value. They define the weight, the symmetry condition, and the sign conclusion.
- Examples are chosen to demonstrate the principle, not to exhaust a phase diagram.
- References are dense where the text compresses prior work or background.

## Style Rules For This Manuscript

- Use Fig. 1's four-quadrant classification as the organizing story:
  - RP/TRS systems are sign-free for BAFQMC.
  - Unfrustrated systems are sign-free for SSE/WLQMC.
  - Frustrated systems with RP/TRS form the new computable territory revealed by this work.
- Avoid unnecessary "not ... but ..." framing. State the positive classification or mechanism directly.
- Minimize dashes. Prefer clean sentence structure.
- Keep the Introduction as a continuous motivation, not a list of technical achievements.
- Use the style references for rhythm and compression only. Do not import their claims or emphases into this bosonic paper.
- Use `opencode` as an external prose reviewer after drafting important paragraphs.
- Available local reviewer model: `deepseek/deepseek-v4-pro`, callable through `opencode run -m deepseek/deepseek-v4-pro`.

## Citation Workflow

- Do not add bibliography entries from memory.
- Before editing `references.bib`, verify metadata against arXiv, APS, DOI, Crossref, or publisher pages.
- For every added or changed reference, record what was checked: author list, title, journal, volume, article/page number, year, DOI, and arXiv identifier if relevant.
- Report new or modified references to the author for review.

## Candidate Skill Scope

A future reusable skill should cover:

- PRL-like restructuring of theoretical-physics manuscripts.
- Fig.-driven story alignment.
- Movement of proofs and implementation details into Supplemental Material.
- Reference-verification discipline.
- Optional `opencode` prose review.

It should not include paper-specific claims, benchmark parameters, or private paths.
