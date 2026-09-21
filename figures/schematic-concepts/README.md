# Figure 1 concept studies

These are alternative compositions for author review. The manuscript still uses
`figures/schematic.pdf`; no candidate is selected automatically.

The selected direction now has [an enlarged frustrated region](C_REFINED.md):
one triangular-lattice illustration, a recessed `New sign-free regime` plaque,
and overlapping colored cards. The A/B/C studies below retain the initial
exploration.

The scientific job is to make the change in the sampled object visible: a negative
closed hopping path assembled from local matrix elements versus an auxiliary-field
configuration whose full bosonic trace has a nonnegative weight under the paper's
TRS or RP criterion. The reader is assumed to know a lattice and particles but not
the determinant formula. The figures introduce the mechanism and then show its
consequence in the existing frustration/criterion classification.

## Render

From native PowerShell, use the repository's Linux launcher:

```powershell
.\scripts\run-in-wsl.ps1 'python3 figures/schematic-concepts/build_schematics.py'
```

The generator uses NumPy, Matplotlib (including its `packaging` dependency) and PyMuPDF. Editable SVGs and vector PDFs,
PNG previews, an author comparison sheet, and a manifest are written to the ignored
`pdf/schematic-concepts/` directory. PDF widths are 86 mm (A), 178 mm (B), and
128 mm (C). B explores a two-column composition; C uses an intermediate width
for comparison and would need a layout decision before manuscript adoption.

In the current WSL environment, Matplotlib is installed but its pure-Python
`packaging` dependency was absent. A copy from the bundled Codex Python runtime
is available in the ignored `.build/schematic-exploration/vendor/` directory.
The verified command in this checkout is:

```powershell
.\scripts\run-in-wsl.ps1 'PYTHONPATH=.build/schematic-exploration/vendor python3 figures/schematic-concepts/build_schematics.py'
```

## Compositions

- **A — local loop and global field:** a compact physical contrast above a reduced
  classification map. The field is flat and the artwork remains legible at 86 mm.
- **B — auxiliary-field landscape:** a local frustrated cycle, HS decoupling and
  a stack of field slices, followed by the smaller classification. The whole stack
  is grouped above the global weight. All depth is vector geometry.
- **C — illustrated classification:** physical objects inhabit the four regions.
  The HS arrow stays within the TRS/RP row and therefore cannot imply that
  decoupling creates a symmetry absent from the model.

## Physical conventions

- The red triangle is a closed three-hop path for positive hopping in the
  Hamiltonian. Each off-diagonal factor in the expansion of `exp(-beta H)` is
  negative; positive scalar factors are omitted in the sketch.
- HS decoupling replaces the direct interaction by coupling to an auxiliary field.
  The field surface is a schematic background, not a physical membrane or a
  specific sampled numerical configuration. Lattice bonds remain present.
- The positive object is the complete fixed-field trace `W(phi)`, conditional on
  the manuscript's TRS or RP criterion. A field sheet or HS arrow alone does not
  assert positivity. No individual path or one-body matrix element is recolored
  as positive by the transformation.
- The classification retains the original orientation: frustrated on the left,
  unfrustrated on the right, the TRS/RP criterion above and neither criterion
  below. The blank lower-left cell makes no universal impossibility claim.
- The figures summarize sign positivity, not convergence or variance behavior.
  Detailed theorem assumptions and pole conventions remain in the manuscript.

## Review

Check both the large previews and the 86 mm PDF: arrows should make a closed path,
the HS diagram must distinguish a direct interaction from a field coupling, and
the criterion must visibly qualify the nonnegative global weight. Labels are kept
short; the caption will carry the remaining explanation after a design is chosen.
