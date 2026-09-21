# Standalone triangular-lattice draft

This study focuses on one equilateral plaquette, with a wide-angle perspective,
glossy coral-red metallic bosons, matte graphite nearest-neighbour bonds,
and a fading surrounding lattice. The central triangle dominates, with its three
neighbouring triangles visible at lower contrast. Soft contact
shadows and offset bond shadows give the motif depth on a clean white background.
Only one broad light casts shadows; the rim and fill lights do not. Caustics are
disabled to keep the floor quiet.
Every lattice site has a sphere, including those that fade toward the perimeter.
Warm coral halos follow their projected sizes and fade with the lattice.
It is not included in the manuscript schematic.

One tall, tapered, single-headed charcoal arrow illustrates an example hop, with
the label above its crest. The lattice is rotated 60 degrees clockwise to bring
the hopping bond toward the camera. The curve connects the exact site centres
and is trimmed to the projected sphere edges. The label `t > 0`
uses the manuscript convention
`H_t = +t sum_<ij> (b_i^+ b_j + b_j^+ b_i)`, which is frustrated on this lattice.
The arrow does not indicate a circulating current or remove the reverse hopping
term. All spheres have the same physical radius; their apparent sizes follow the
perspective projection. Every bond uses the same opaque material and radius;
all spheres share one opaque metallic material with bright, broad highlights.
They have filled centres and a soft halo. These are qualitative images
of bosons, not calculated wavefunctions, occupations, or phase patterns.
The surrounding lattice is faded
during compositing, according to distance from the central triangle in the lattice
plane.

Visual references:

- Science (2011), DOI `10.1126/science.1207239`: small central triangle, sphere and
  bond rendering, and peripheral lattice fading.
- Nature Communications (2023), DOI `10.1038/s41467-023-43204-3`, Fig. 1c:
  arching arrows with variable thickness and a coefficient above the curve.

The geometry and rendering are newly constructed; no reference image is embedded.

## Reproduce

Run from the repository root in Linux/WSL with Blender 4.3 and a Python environment
containing NumPy, Pillow, and Matplotlib:

```bash
blender -b --threads 8 --python figures/schematic-concepts/render_triangle_focus.py -- --final
python3 figures/schematic-concepts/compose_triangle_focus.py
```

From native Windows, pass those commands through `scripts/run-in-wsl.ps1`.
The local bundled Blender executable is
`.build/tools/blender-4.3.2-linux-x64/blender`; local Python dependencies can be
selected with `PYTHONPATH=.build/schematic-exploration/vendor`.

Outputs are under the ignored `pdf/triangle-focus-draft/` directory:

- `triangle-focus-draft.png`: white-background preview.
- `triangle-focus-draft.pdf`: rendered lattice with vector arrow and label.
- `triangle-focus.blend`: editable scene.
- `lattice-render.png`: transparent lattice render before compositing.
- `projection.json`: projected geometry and annotation positions.

Omit `--final` for a quicker preview. The compositor preserves the camera's
projection, adds the single hopping arrow, and fades the lattice at the perimeter.
Neither script edits the production schematic or builds the manuscript.
