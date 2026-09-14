# Focused 3D revision of concept C

This candidate keeps the original classification and its overlapping half-planes.
Only the upper-left and lower-right quadrants contain physical illustrations.
The production figure `figures/schematic.pdf` is unchanged.

## Visual meaning

- **Upper left:** fine, interrupted wavy strokes join interacting particles.
  One HS arrow leads to particles coupled individually to a fluctuating,
  open two-dimensional auxiliary-field net. There are no particle-particle
  connections after the arrow. The net has no opaque filled surface.
- **Lower right:** one closed hopping path on an unfrustrated square, with one
  occupied-site symbol and one direction marker.
- **Background:** blue and gold refractive glass half-planes overlap in green.
  Explicit “Sign-free for …” labels identify the applicability regions. The
  vertical labels spell out time-reversal symmetry and reflection positivity.
  A soft pool of light and a brighter cyan glass edge emphasize the newly
  accessible upper-left region without an additional annotation.

The particle symbols represent bosons. The interaction sketch illustrates HS
decoupling in general; its pairwise strokes are not a diagram of the onsite
interaction used in the manuscript's benchmark. The auxiliary-field net is a
schematic field configuration, not lattice bonds or numerical data. Its height
variation only makes field fluctuations visible. The square is a schematic
closed hopping sequence, not a full world-line configuration.

The HS transformation is contained in the region qualified by the manuscript's
TRS/RP criteria. HS decoupling alone is not a sign-positivity criterion. The empty
lower-left region makes no claim of a universal impossibility result.

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

- `C_refined_3d.pdf`: one 86 mm square figure.
- `C_refined_3d.svg`: editable vector labels and axes with embedded 3D renders.
- `C_refined_3d.png`: 450 dpi preview rendered from the PDF by Poppler.
- `C_refined_assets/`: four PNG renders and their editable `.blend` scenes.
- `C_refined_3d_manifest.json`: dimensions, font sizes and motif resolution.

The PDF/SVG combine raster 3D artwork with vector typography; they are not
all-vector illustrations. Inspect both the enlarged preview and the figure at
86 mm width. The exporter checks text bounds, page count and physical dimensions.
The candidate does not change any manuscript source, bibliography or figure
reference, so validation concerns these candidate artifacts.
