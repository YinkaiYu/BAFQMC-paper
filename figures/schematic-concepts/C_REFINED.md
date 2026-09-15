# Focused 3D revision of concept C, version 3

This candidate keeps the original classification and its overlapping half-planes.
Only the upper-left and lower-right quadrants contain physical illustrations.
The production figure `figures/schematic.pdf` is unchanged.

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

The compositor requires NumPy, Matplotlib, Pillow, PyMuPDF and Poppler. The
`PYTHONPATH` above supplies the `packaging` dependency missing from this WSL
installation. On a complete Python installation it can be omitted.

Use `--quality draft` for faster previews and `--only background`, `interaction`,
`field`, `loop`, or `hs` to rerender selected components. `hs` renders both the
before- and after-decoupling scenes.

## Outputs and validation

Outputs remain in the ignored `pdf/schematic-concepts/` directory:

- `C_refined_3d_v3.pdf`: one 86 mm square figure.
- `C_refined_3d_v3.svg`: vector labels with embedded 3D renders.
- `C_refined_3d_v3.png`: 450 dpi preview rendered from the PDF by Poppler.
- `C_refined_v3_assets/`: four PNG renders and their editable `.blend` scenes.
- `C_refined_3d_v3_manifest.json`: dimensions, font sizes and motif resolution.

The previous version's outputs remain available under their original names.

The PDF/SVG combine raster 3D artwork with vector typography; they are not
all-vector illustrations. Inspect both the enlarged preview and the figure at
86 mm width. The exporter checks text bounds, page count and physical dimensions.
The candidate does not change any manuscript source, bibliography or figure
reference, so validation concerns these candidate artifacts.
