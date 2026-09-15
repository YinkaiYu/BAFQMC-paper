# Card refinement, version 7

Current output: `pdf/schematic-concepts/C_refined_cards_v7` (PDF, SVG, PNG,
manifest and source ZIP). Reproduce with `build_cards_v7.py` using the same
WSL command and dependencies as version 6 below.

The transition arrow is shorter and narrower, with a clear gap before the
post-HS motif. Its widening perspective is retained. The silhouette halo uses
broader diffusion and additional transparent padding to avoid clipped edges.
The entire flat background is deepened to #d9dfe5; the uncovered lower-left
region gains definition without adding another category color or raised panel.
The physics, wording, card colors and opacity are unchanged. Version 6 remains
available for comparison. The production manuscript figure is unchanged.

---

# Selected card design, version 6

The current candidate is `C_refined_cards_v6`. It preserves the two physical
motifs and classification of version 5 while refining the selected card style.
The manuscript production figure remains unchanged.

- Blue card: #39a8f5 at 48 percent opacity; gold card: #ffc342 at 64 percent.
  The lower card remains visible through the upper card. Uniform flat gray base,
  equal layer overhangs and restrained shadows are retained.
- Row labels: Within symmetry criteria / Outside symmetry criteria.
  These refer to the manuscript's existing sufficient criteria; the schematic
  does not enlarge their scope or assert a necessary condition.
- The small interacting triangle is in the upper left. A curved ribbon widens
  toward the larger foreground auxiliary-field scene on its lower right.
- A softly padded cyan-white halo follows the field and particle silhouettes.
  The effect is illustrative, not numerical or physical emission data.

Reproduce in WSL:

```powershell
.\scripts\run-in-wsl.ps1 'PYTHONPATH=.build/schematic-exploration/vendor python3 -W error figures/schematic-concepts/build_cards_v6.py'
```

Outputs are `pdf/schematic-concepts/C_refined_cards_v6` with PDF, SVG, PNG and
manifest extensions, plus `C_refined_cards_v6_sources.zip`. The compositor uses
unchanged physical renders in `C_refined_v5_assets`. GNU FreeSans is required.
Labels are checked against the page and card interiors. Older outputs and the
version-5 builder are preserved.

---

# Focused 3D revision of concept C, version 5

This candidate keeps the original classification and its overlapping half-planes.
Only the upper-left and lower-right quadrants contain physical illustrations.
The production figure `figures/schematic.pdf` is unchanged.

## Apple Design reference

Visual reference inspected on 2026-09-15: https://developer.apple.com/design/.
The hero artwork motivates rounded liquid-glass silhouettes, narrow bright
refractive rims, pale tints, diffuse suspension shadows and restrained dark type.
The artwork is original Blender geometry; no Apple assets or proprietary fonts
are embedded. Version 5 retains the approved physics and equal projected margins.
Both coverage labels are single lines in blue and gold, with WLQMC/SSE written
explicitly. Glass uses uniform tint with no selective lighting or spotlight.
The whole glass material has IOR 1.85; shadow rays receive 82 percent
transparent mixing to restrain cast shadows. A faint cyan halo follows only
the post-HS mesh and particle silhouettes; it is decorative, not physical data. The reference is aesthetic, not scientific.

The alternate `--background cards` output uses vector cards with no thickness
or refraction, retaining the same 28-unit layer offsets and restrained shadows.
Both variants share the exact typography and physics composition. HS and phi
labels are omitted; one curved arrow carries the transformation. The post-HS
scene is enlarged relative to the preceding version.

## Visual meaning

- **Upper left:** continuous wavy strokes join interacting particles.
  The smaller, distant interacting configuration leads through one HS arrow to
  the larger foreground view of particles coupled individually to a fluctuating,
  open two-dimensional auxiliary-field net. There are no particle-particle
  connections after the arrow. The net has no opaque filled surface.
- **Lower right:** four identical particles with the same continuous wavy
  interaction notation on an unfrustrated square. There is no occupation contrast
  or hopping-direction arrow.
- **Background:** a flat, uniform gray plane has no thickness or cast shadow.
  The two suspended colored glass half-planes are more transparent. The blue
  pane is higher; gray, amber and blue have successively larger projected outer
  extents with equal 28-unit steps (2.408 mm in the 86 mm figure). The gray
  plane ends inside the amber pane's right and bottom edges. No categorical
  color is painted on the background and there are no
  black coordinate-axis lines. “Sign-free for …” labels identify the coverage,
  with identically colored TRS/RP and Non-TRS/RP row labels. Sign-free for both
  and Sign-problematic are centered in their respective visible regions.

The particle symbols represent bosons. The interaction sketch illustrates HS
decoupling in general; its pairwise strokes are not a diagram of the onsite
interaction used in the manuscript's benchmark. The auxiliary-field net is a
schematic field configuration, not lattice bonds or numerical data. Its height
variation only makes field fluctuations visible. The square shows the
unfrustrated interaction geometry, not a sampled hopping trajectory.

The HS transformation is contained in the region qualified by the manuscript's
TRS/RP criteria. HS decoupling removes direct particle-particle interactions in
the fixed-field representation, not geometrical frustration. HS alone is not a
sign-positivity criterion. Sign-problematic labels the regime in the schematic's
scope; it is not a universal impossibility theorem for every conceivable method.

## Reproduce

Run Blender in Linux/WSL, with OpenImageDenoise available for clean glass edges.
The verified renderer is the official Blender 4.3.2 Linux distribution. Its
archive was checked against the official SHA-256 manifest and extracted locally
under the ignored `.build/tools/` directory.

From PowerShell:

```powershell
.\scripts\run-in-wsl.ps1 '.build/tools/blender-4.3.2-linux-x64/blender -b --threads 8 --python figures/schematic-concepts/render_c_refined.py -- --quality final --only all'
.\scripts\run-in-wsl.ps1 'PYTHONPATH=.build/schematic-exploration/vendor python3 -W error figures/schematic-concepts/build_c_refined.py'
```

The compositor requires NumPy, Matplotlib, Pillow, PyMuPDF, Poppler and
GNU FreeSans (registered from `/usr/share/fonts/truetype/freefont/FreeSans.ttf`). The
`PYTHONPATH` above supplies the `packaging` dependency missing from this WSL
installation. On a complete Python installation it can be omitted.

Use `--quality draft` for faster previews and `--only background`, `interaction`,
`field`, `loop`, or `hs` to rerender selected components. `hs` renders both the
before- and after-decoupling scenes.

## Outputs and validation

Outputs remain in the ignored `pdf/schematic-concepts/` directory:

- `C_refined_3d_v5.pdf`: one 86 mm square figure.
- `C_refined_3d_v5.svg`: vector labels with embedded 3D renders.
- `C_refined_3d_v5.png`: 450 dpi preview rendered from the PDF by Poppler.
- `C_refined_v5_assets/`: four PNG renders and their editable `.blend` scenes.
- `C_refined_3d_v5_manifest.json`: dimensions, font sizes and motif resolution.
- `C_refined_cards_v5.pdf`, `.svg`, `.png` and `_manifest.json`: card alternative.
- `C_refined_v5_comparison.png`: side-by-side review preview.
- `C_refined_v5_sources.zip`: both versions and reproducible source bundle.

For the card alternative, append `--background cards` to the compositor command.
The minimum text size is 7.6 pt. Both coverage headings are checked against the
interior bounds of their panes, in addition to the page-bound checks.

The previous version's outputs remain available under their original names.

The PDF/SVG combine raster 3D artwork with vector typography; they are not
all-vector illustrations. Inspect both the enlarged preview and the figure at
86 mm width. The exporter checks text bounds, page count and physical dimensions.
The candidate does not change any manuscript source, bibliography or figure
reference, so validation concerns these candidate artifacts.
