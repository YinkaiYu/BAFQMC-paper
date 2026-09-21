# Lattice color comparison

The four alternatives keep the current card backgrounds, geometry, positions,
type, arrows, outlines, material roughness, lighting, and fading fixed. Only the
boson base color, corresponding halo, and hopping annotation colors change.

| Option | Bosons | Hopping arrow and label |
| --- | --- | --- |
| A, current | Coral red | Purple |
| B | Purple | Red |
| C | Deep blue | Purple |
| D | Deep blue | Deep blue |

Purple and blue bosons are rerendered in Blender at the production resolution
of 2000 x 1545 with 128 Cycles samples. C and D reuse the same blue render.
The arrows and labels remain vector artwork. Exact color values appear in
`compare_lattice_colors.py` and the output `palette-manifest.json`.

Run from the repository root in WSL/Linux:

```bash
PYTHONPATH=.build/schematic-exploration/vendor python3 figures/schematic-concepts/compare_lattice_colors.py --render
```

Use `scripts/run-in-wsl.ps1` from native Windows. Omit `--render` to reuse the
rendered alternatives. The script uses the local Blender runtime under `.build/`.
The PNG contact-sheet headings use Microsoft YaHei from the Windows font directory.

Outputs under the ignored `pdf/schematic-color-study/` directory include:

- `four-palettes-full.png`: 2 x 2 comparison of complete schematics.
- `four-palettes-detail.png`: 2 x 2 comparison of enlarged upper-left regions.
- `four-palettes-comparison.pdf`: complete figures with vector typography.
- Individual PDFs, SVGs, PNGs, transparent renders, and Blender scenes.

The workflow checks that all four figures have identical text positions and
that A matches the current production PNG pixel for pixel. It also verifies
that the production figure files remain unchanged; none of these alternatives
is installed automatically.
