# Figure 1 exploration review

Historical review of the initial A/B/C concepts. These are not the final palette
choices; see [the current production guide](README.md).

## Outcome

Three alternatives were completed without replacing the manuscript's current
`figures/schematic.pdf`. All figure PDFs contain vector artwork only, with embedded
text fonts. SVG text is converted to outlines for portable appearance; individual
paths remain editable. The comparison sheet presents the same exported PDFs.

| Candidate | Intended width | Height | Smallest text |
| --- | ---: | ---: | ---: |
| A: local loop and global field | 86 mm | 89.44 mm | 7.0 pt |
| B: auxiliary-field landscape | 178 mm | 70.34 mm | 6.9 pt |
| C: illustrated classification | 128 mm | 107.97 mm | 7.5 pt |

A is the strongest fit to the current single-column figure. B makes the auxiliary
field configuration more prominent and is the preferred direction for a larger
visual treatment. C is the closest to the original classification, with the most
literal integration of physical objects into the four regions. B and C should not
be reduced to 86 mm without redesigning their typography and composition.

## Physics and visual checks

- The hopping arrows close around a triangle; the three expansion-factor signs
  are negative for the positive-hopping convention in the manuscript. The square
  example in C has an even number of negative factors and a positive loop product.
- Purple waves denote direct interactions. After HS, particles couple to the
  field background while lattice bonds remain present. B has three particles on
  both sides of its HS arrow; A and C have two.
- A small trace arrow connects the auxiliary-field picture to the global weight.
  TRS/RP explicitly qualifies the positive result.
- C retains a red local loop inside the frustrated TRS/RP cell, so it does not
  imply that the global criterion removes negative local hopping factors.
- An independent review found no remaining material visual or physical issues
  after these corrections.
- Generation completed in WSL with warnings promoted to errors. PDF dimensions,
  single-page outputs, vector-only content, and text bounds passed validation.
  The PDF comparison sheet was rendered and visually inspected.

## Caption material for later adoption

For A or B:

**Local and global weights in bosonic QMC.** (a) Arrows follow a closed hopping
path on a frustrated triangle. For positive hopping, the three off-diagonal
expansion factors are negative and their product gives a negative loop weight.
(b) HS decoupling replaces direct interactions, shown by purple waves, with
coupling to an auxiliary-field background. Tracing over the bosons at fixed fields
gives the global weight, whose nonnegativity is protected by the TRS or RP criterion.
(c) Sign-free regimes classified by frustration and the HS-decoupled criterion.
BAFQMC covers the upper half and WLQMC/SSE the right half; the highlighted
upper-left region is the frustrated regime accessible through BAFQMC.

For C, use the same physical definitions without panel letters, explaining that
the negative local loop remains in the upper-left region while the global
auxiliary-field weight is nonnegative. The lower-right square illustrates a
positive product of four hopping factors.

## Repository validation

The working tree initially contained a manuscript revision in `main.tex`,
`SM.tex`, and `references.bib`. A separate active task continued editing these
files during the figure exploration. This figure study changes none of their
text and commits only its own files.

The initial manuscript snapshot compiled successfully in WSL (33 pages), as did
a prose diff against `d4276e6` (39 pages). That temporary diff used separately
expanded old/new sources, side-by-side periodic tables, and resolved historical
references. Equation markup was disabled because latexdiff could not handle the
existing equation restructuring. The parallel manuscript task subsequently
refreshed the canonical PDFs again using its own workflow; its outputs take
precedence. The temporary snapshot is not delivered as a current manuscript
revision.

The successful snapshot builds had no unresolved references/citations, overfull
boxes, or stuck floats. They retained REVTeX's default-font-size and nameref
label-hook notices and a few underfull paragraphs. Figure generation itself
completed without warnings.

The separate report `docs/research_reports/2026-09-10_trs_branch_issue/README.md`
records an ongoing issue with analytic continuation of paired Gaussian weights.
The trace arrows in these concept figures refer to the fixed-field bosonic trace
in the validity domain of the positivity criterion, not to unrestricted
continuation across poles. This scope must be respected in any eventual caption
and theorem revision; it is not encoded as extra labels in the artwork.
