# TRS periodic table and main-text proof sketches

Date: 2026-09-15. Author-specified comparison baseline: `1b207e7`.

## Purpose and scope

The table identifies the two fundamental bosonic TRS classes at a glance. The
adjacent paragraphs explain why they protect Gaussian weights, after the reader
has encountered the number-conserving Kramers criterion and its two-flavor block
example. The narrative proceeds from sector decomposition to the determinant and
commutator signs that establish positivity. The evidence is the existing detailed
proof in SM Sec. VI and the split-orthogonal determinant theorem already cited as
`wang2015prl`.

The changes are confined to the main-text table and its accompanying discussion,
plus the matching “Sign-problematic” column name in the SM. The TRS and RP theorem
conditions, regularization discussion, and benchmarks are preserved. No bibliography
entry was added or changed.

## Presentation

- Table lettering uses sans-serif `\footnotesize`, smaller than the 10-point body.
  The headers and both fundamental entries use the same size in bold.
- Every column is centered. Full names are linked by equality signs:
  `{-,-} = Kramers class` and `{+,+,+} = Split-orthogonal class`.
- The header is slate navy (`#273B52`), alternating rows are pale gray-blue
  (`#F3F6FA` and `#E5ECF4`), and both fundamental entries use blue (`#23588C`).
- Single-line rows are 14.5 points high; the two-line row is 26 points with a
  12-point baseline separation. The header is 22 points high, and the complete
  table is 106 points high. An additional 6 points separates the caption and table.
- Class names in the prose are italic and underlined. Each class has a compact
  proof sketch, followed by the statement that these are the only two fundamental
  classes within the anticommuting-TRS classification.

## Scientific and visual checks

The Kramers sketch tracks the conserved transformation, pairing within a selected
sector, and the even number of creation operators in a canonical sector basis.
The split-orthogonal sketch explains the real basis and how the third symmetry
combined with Hermitian conjugation balances annihilation and creation directions.
Its displayed weight retains the factor `(-1)^(N/2)` and the real scalar prefactor.
Both sketches agree with the SM reduced-weight formulas.

An independent reader/physics review checked these bridges and the scope of the
two-class uniqueness statement. Its clarity findings were resolved, and the final
prose review reported no remaining material issues.

The authoritative WSL build refreshed `pdf/main.pdf` (33 pages) and the expanded
main-plus-SM diff `pdf/main-diff.pdf` (34 pages), with baseline `1b207e7`.
Rendered inspection covered the table, caption spacing, proof sketches, and nearby
page flow. PDF text inspection confirmed selectable sans-serif table lettering
and no clipping. The only separate symbol font supplies the inequality sign.
Label consistency, preservation of the deferred SM material, exact diff-source
matching, process-language scanning, and `git diff --check` passed.

The review PDF preserves the native table body because the entire table is new
against the comparison baseline, while marking its caption as added. Only the
new proof sketches use ragged-right alignment in the review PDF to prevent the
underlining from stretching word spaces. The manuscript itself remains justified.

No new compilation warnings remain. Existing notices are REVTeX's default type
size and the nameref label redefinition. Existing minor underfull-box notices
remain in the bibliography (badness 1337) and, in the diff only, unchanged passages
affected by markup (badness 1077 and 1237).
