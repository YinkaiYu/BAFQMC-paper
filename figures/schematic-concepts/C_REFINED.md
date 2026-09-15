# Uniform quadrant typography

All four quadrant status labels now use 7.6 pt FreeSans in every panel A-F.
The axis labels retain their separate hierarchy. Positions, improved motif-caption
clearance and corrected mint overlap colors are preserved.

Current individual output stems:
- `C_refined_cards_v8_type`
- `C_refined_cards_v9_raised_type`
- `C_refined_cards_v10_raised_type`
- `C_refined_cards_v11_mint_raised_type`
- `C_refined_cards_v12_mint_raised_type`
- `C_refined_cards_v13_mint_raised_type`

Current comparison: `C_cards_comparison_v8-v13_uniform_type.pdf` and `.png`.
Build all six current card builders then `compare_cards_v8_v13.py`.
The production manuscript figure is unchanged.

---

# Increased clearance above the BAFQMC caption

Panels B-F now move the complete upper-left transformation group upward by
25 design units (2.15 mm at 86 mm width). The small triangle, tapered arrow,
field and halo keep their relative placement and size. The field box ends at
y=441 while the caption stays at y=493, doubling the nominal clearance from
27 to 52 units. Panel A and all lower-right motifs are unchanged.

Updated individual outputs append `_raised` to the previous name. The refreshed
contact sheet is `C_cards_comparison_v8-v13_mint_raised.pdf` and `.png`.
The production manuscript figure is unchanged.

---

# Mint intersection correction for panels D, E and F

The version 11, 12 and 13 builders now export `_mint` suffixed outputs.
Only their overlap is color-corrected to #a3e3cd and clipped to the intersecting
card shapes; this is an intentional compositing adjustment, not raw alpha
mixing. Surrounding translucency, full gray gradients, directional blue/gold
gradients, physics motifs and typography are preserved. Original outputs remain.

The refreshed six-panel comparison is `C_cards_comparison_v8-v13_mint.pdf`
and `.png`. Panels A-C are unchanged. Build with `compare_cards_v8_v13.py`
after running the three updated builders. The production figure is unchanged.

---

# Gradient cards and aligned labels, versions 12 and 13

Version 12 (`build_cards_v12.py`) adds real translucent color gradients: blue
runs from light cyan at left to deeper blue at right; gold runs from pale yellow
at bottom to deeper gold at top. Full neutral gradient and all prior composition
remain. Version 13 (`build_cards_v13.py`) aligns each row's two status labels
at y=493 and y=869, with consistent 7.6 pt type. Physics and color are identical.

`compare_cards_v8_v13.py` generates the six-panel comparison PDF and PNG under
`pdf/schematic-concepts/C_cards_comparison_v8-v13`. Panels E and F isolate the
gradient-card and aligned-label changes. Earlier comparisons remain available.
The manuscript production figure is unchanged.

---

# Full gradient and translucency, version 11

Current alternative: `C_refined_cards_v11`, built with `build_cards_v11.py`.
The full gray base again extends beneath both translucent cards. It varies from
#c8d0d9 at lower left to paper white toward upper right, using a smooth ramp
that reaches white early to soften the upper and right base boundaries.
Blue (#3aaff8, 48 percent) and gold (#ffcb45, 64 percent) now use actual alpha
compositing; the intersection is not assigned an independent hue. All motif
placements and labels match version 10. The production figure is unchanged.

`compare_cards_v8_v11.py` exports a single-page PDF and PNG contact sheet with
four equally sized panels: version 8 (labels above), version 9 (labels below),
version 10 (local gradient), and version 11 (full gradient and transparency).
Output: `pdf/schematic-concepts/C_cards_comparison_v8-v11`.

---

# Diagonal neutral gradient, version 10

Current candidate: `pdf/schematic-concepts/C_refined_cards_v10` (PDF, SVG, PNG,
manifest and source ZIP). Reproduce with `build_cards_v10.py` and the same WSL
compositor command documented below.

The visible lower-left background changes smoothly from #c8d0d9 at the lower
left to #eff2f6 at the upper right. The diagonal blend uses a smooth cubic ramp.
It remains confined to the exposed neutral area, preserving the independently
assigned blue, gold and mint colors and avoiding hidden base edges. Motifs and
below-motif labels match version 9. All previous candidates are preserved.
The production manuscript figure is unchanged.

---

# Below-motif labels, version 9

Current candidate: `pdf/schematic-concepts/C_refined_cards_v9` (PDF, SVG, PNG,
manifest and source ZIP). Reproduce using `build_cards_v9.py` with the WSL
compositor command documented below.

Both colored sign-free labels are below their corresponding physical motifs.
The upper-left transformation group and lower-right square are shifted upward
to preserve internal margins. Version 8 retains the labels-above layout for
comparison. Independent card colors, hidden-base-edge removal, physics content,
small widening arrow and expanded halo are preserved. The production manuscript
figure is unchanged.

---

# Independently colored cards, version 8

Current candidate: `pdf/schematic-concepts/C_refined_cards_v8` (PDF, SVG, PNG,
manifest and source ZIP). Run `build_cards_v8.py` with the WSL compositor
command documented below. All earlier candidates are preserved.

Gray is drawn only in the exposed lower-left region. Blue (#99d1f5), gold
(#f8d479), and the mint intersection (#a2dccd) are independently assigned opaque
colors, so the neutral background neither desaturates them nor reveals hidden
edges. The intersection is clipped to both card silhouettes. Outer offsets,
restrained shadows and exterior rims convey the layer order. The physical
motifs, arrow, glow, labels and production manuscript figure are unchanged.

---

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
