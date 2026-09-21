# Lattice color comparison

## Production choice

The manuscript uses option B from the original, ungraded comparison
`pdf/schematic-color-study/four-palettes-comparison.pdf`: purple bosons
(`#7851A8`), purple halos (`#AC8ACE`), a red arrow (`#C8473B`), and a red label
(`#B43B31`). These are the defaults in the render, composition, and card builders.

## Balanced alternatives

This alternative review offers four gently softened palettes using the same rendered
geometry, highlight shapes, alpha channel, and peripheral fade. Color grading
retains 88 percent of the motif and halo OKLab chroma, and 94 percent of the arrow
and label chroma. Colored midtones receive a small perceptual lightness lift
(at most 0.035 for the motif and 0.015 for the annotations); neutral tones and
near-white highlights receive less lift. This retains clear color while slightly
softening its contrast with the card backgrounds.

| Option | Bosons | Hopping arrow and label |
| --- | --- | --- |
| A | Coral red | Purple |
| B | Purple | Red |
| C | Blue | Purple |
| D | Blue | Blue |

```bash
PYTHONPATH=.build/schematic-exploration/vendor python3 figures/schematic-concepts/compare_lattice_colors.py --balanced
```

These outputs are under `pdf/schematic-color-study/balanced/`, with the same
contact-sheet and PDF filenames as the original study. The original comparison
and manuscript figure are retained. This is a color-grading study of the existing
renders rather than a change to the Blender material parameters.

The earlier strong desaturation can be reproduced with `--muted`, which retains
52 percent motif chroma and 70 percent annotation chroma without a lightness lift.
This treatment was rejected because the spheres and arrows looked gray.
Generated `balanced/` and `muted/` outputs were cleaned after approval; either
command recreates them from the retained render caches.

## Original alternatives

The four alternatives keep the current card backgrounds, geometry, positions,
type, arrows, outlines, material roughness, lighting, and fading fixed. Only the
boson base color, corresponding halo, and hopping annotation colors change.

| Option | Bosons | Hopping arrow and label |
| --- | --- | --- |
| A | Coral red | Purple |
| B, current | Purple | Red |
| C | Deep blue | Purple |
| D | Deep blue | Deep blue |

Coral, purple, and blue bosons are rendered in Blender at the production resolution
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
that ungraded B matches the current production PNG pixel for pixel. It also verifies
that the production figure files remain unchanged; none of these alternatives
is installed automatically.
