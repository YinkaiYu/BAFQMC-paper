# Finalized Figure 1

The confirmed manuscript schematic is `figures/schematic.pdf`, with an editable,
self-contained `figures/schematic.svg` and an ignored `figures/schematic.png`
preview. The final design uses overlapping blue and yellow cards, an enlarged
upper-left sign-free region, and one triangular lattice with purple bosons and
a red hopping arrow. Its palette is the original color-study option B, without
the later color grading. `build_cards_v14.py` is the production builder.

The figure maps frustration against satisfaction of the TRS/RP criteria and
highlights the frustrated region accessible to BAFQMC. The single arrow depicts
an example nearest-neighbor hop in
`H_t = +t sum_<ij> (b_i^+ b_j + b_j^+ b_i)`, with `t > 0`. It does not denote a
directed-only Hamiltonian, a circulating current, or numerical occupation data.

## Production files and regeneration

The builder reads only the tracked `triangle-lattice.png` and
`triangle-annotation.json` in `figures/schematic-assets/`. It does not require
Blender or any ignored study output to rebuild the confirmed schematic.

From native PowerShell:

```powershell
.\scripts\run-in-wsl.ps1 'PYTHONPATH=.build/schematic-exploration/vendor python3 -W error figures/schematic-concepts/build_cards_v14.py --publish'
.\scripts\build-manuscript.ps1
```

Run the corresponding Python command and `bash scripts/build-manuscript.sh`
directly in Linux/WSL. Dependencies are NumPy, Pillow, Matplotlib, PyMuPDF, Poppler
(`pdftoppm`), and the FreeSans fonts. The local vendor directory supplies the
Python dependencies missing from the system installation.

Publishing updates the PDF, SVG, and PNG together. The builder checks label
bounds within the cropped 86 x 79.12 mm page, and exports its layout manifest under
`pdf/schematic-concepts/`. The manuscript caption is next to `fig:schematic` in
`main.tex`. Figure revisions do not refresh `pdf/main-diff.pdf`, following the
author's preference.

For further changes:

- [Final card layout and materials](C_REFINED.md).
- [Blender lattice source and regeneration](TRIANGLE_FOCUS.md).
- [Palette values and optional comparisons](COLOR_STUDY.md).
- [Tracked motif assets](../schematic-assets/README.md).

## Historical studies and temporary outputs

The other builders and comparators are retained as historical source material;
they do not define the current manuscript figure. Initial A/B/C concept labels
and later card-layout labels are separate from the final palette choice B.
[Early concepts](archive/EARLY_CONCEPTS.md), their [review](REVIEW.md), and the
[design history](archive/DESIGN_HISTORY.md) record those earlier rounds.

Redundant generated drafts, color-grading variants, temporary checks, and logs
were removed after approval. The original four-palette comparison, final
standalone lattice, and reusable render caches remain under `pdf/`. Historical
generated previews mentioned in the archive may need to be regenerated. Runtime
dependencies and reference images are retained.
