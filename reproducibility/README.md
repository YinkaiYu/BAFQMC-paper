# Benchmark reproduction

The default `python3 reproduce.py` reruns the 15 current BAFQMC/reference
calculations, processes the new measurements, and draws the combined benchmark
figure in `main.tex`. The optional `--mode plot` redraws the stored data.
Seven attractive-density points from an earlier Supplemental Material are
retained as an explicitly selected historical campaign.
See [RESOURCES.md](RESOURCES.md) for the conservative 12–24 hour production
budget, memory, scratch storage, and continuation commands.

## Data and reference conventions

| Figure / row | Varying parameter | Fixed parameters | Reference |
|---|---|---|---|
| Main Fig. 2(a–d) | U1 = 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2 | mu = -3.5, beta = 4 | Particle-shell ED; analytic free-boson reference at U1 = 0 |
| Main Fig. 2(e–h) | Delta = 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3 | U1 = 1, mu = -5, beta = 4 | Dense ED with nmax = 3 and ncut = 4 |
| Historical attractive-density scan | U2 = -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0 | U1 = 1, mu = -7, beta = 1 | Low-density finite-occupation-window reference for U2 < 0 |

The stored input and data keys retain the historical solver convention. The
manuscript uses `U1` for the repulsive relative-density channel. In the archived
two-channel model, `U2` denotes the attractive total-density channel; its
coefficient is zero at every current manuscript point. Solver input names,
stored measurements, error bars, and historical reference selections are preserved.

`--scope main` is the default and selects the 15 points in the main-text figure.
`--scope supplement` selects the seven historical attractive-density points;
`--scope all` includes both sets. The historical scope name is retained for
existing commands and does not refer to the current Supplemental Material.
Scope and solver selection are independent:

| Selection | Points | Scan |
|---|---|---|
| `--scope main` | 15 | U1 and Delta |
| `--scope main --model number_conserving` | 8 | U1 |
| `--scope main --model pairing` | 7 | Delta |
| `--scope supplement` | 7 | Historical U2 |
| `--model number_conserving` | 8 | U1 |
| `--scope all --model number_conserving` | 15 | U1 and historical U2 |

The main-text model satisfies `mu < -3*t - abs(Delta)` at every plotted point.
As proved in the SM benchmark section, its quadratic propagation and unitary
relative-density HS factors give a finite trace throughout the auxiliary-field
domain. This result applies
to both current scans. The historical attractive-density scan retains its
original finite-occupation references and is excluded from the current manuscript.

The pairing implementation writes the real pair term with a positive input
coefficient, whereas the manuscript writes it as `-Delta (b^+ c^+ + b c)`.
The phase convention `c_code = -c_paper` relates these expressions at the same
positive scan value. Density, total physical energy, and the two plotted
structure factors are invariant under this transformation. The solver's
anomalous pair amplitude `pair_equal` changes sign when expressed in manuscript
operators; see [the pairing conventions](../software/pairing/docs/physics.md).

All points have t = 1, a periodic 3 x 3 triangular lattice, Delta tau = 0.01,
100000 measurement bins, and one MPI rank. The error bars are standard errors
from ten consecutive blocks of 10000 bins. Warmup and stabilization settings,
proposal widths, and exact initial seeds are in each `inputs/<case>/` directory.
The paired `seeds.txt` contains a list of rank seeds; the paper uses its first
entry. It is not a multiword state for one random-number stream.

The four measurement files are `density_total`, `energy_density`, `sf_K`, and
`dw_K`. Structure-factor files store real and imaginary components. The plots
use their real parts and show the physical total energy as -E = -9 e, with the
energy standard error multiplied by 9. The chemical-potential term is excluded
from E. No statistical acceptance criterion removes points during reproduction.

The historical negative-U2 reference uses the original low-density occupation
window: six completed particle shells, with a configured maximum of eight.
This is the finite-window comparison encoded by `low_density_cutoff_accepted`
in the ED records. The U1 = 0 reference in the main-text interaction scan is computed
analytically; its original truncated ED JSON is retained for provenance but is
not used for that red point. All other reference values are read from the
archived ED results.

## Layout

```text
data/index.json                  selected cases, parameters, plotted values, provenance
data/checksums.json              SHA-256 for every archived data/input file
data/observables.csv             compact processed means, SEM, and ED values
data/block_means.csv             ten block means per case and observable
data/<model>/manifest.json       current and historical campaign inputs
data/<model>/inputs/<case>/      exact initial input files and ED parameters
data/<model>/ed/<case>.json      original ED results
data/<model>/raw/<case>.tar.gz   optional local raw archives, ignored by Git
analysis.py                     raw-data statistics, references, tables, plot dispatch
plot_manuscript.py               main U1/Delta grid and historical U2 scan
plot_number.py                  original 2 x 4 number-conserving layout
plot_pairing.py                 original 1 x 4 paired layout
plot_style.py                   shared original figure style
```

The tracked data package is approximately 250 kB. Large raw measurement files
are generated by BAFQMC and excluded from Git. The small ED JSON files contain
reference expectation values and cutoff metadata. Stored block means permit
independent reconstruction of the plotted mean and standard error without
shipping the full Monte Carlo chains. `--mode check` verifies the processed
files and statistics without making figures. `--mode raw` additionally checks
the optional original raw archives when they are present locally.

The default output is `figures/benchmark_combined.pdf` (two rows), with a PNG
preview alongside it. Explicit selection of the historical scan also produces
`figures/benchmark_attractive.pdf` (one row) and its PNG preview.
Only the figures and rows covered by the selected scope and solver are drawn.
An individual main-text row is written as
`figures/benchmark_combined_number_conserving.pdf` or
`figures/benchmark_combined_pairing.pdf`, preserving panel labels (a–d) or
(e–h), respectively.
The original layout modules and historical figure PDFs remain available for
provenance and comparisons to earlier manuscript versions.

Generated tables include `benchmark`, `section`, `figure`, `figure_row`, and
`panels` to locate each point in the current or historical figure. `scan_parameter`
is the plotted symbol, `solver_parameter` is its input key, and `U` gives the
scanned interaction coefficient. The JSON records collect these fields under
`manuscript`. Existing case IDs and the archived `row` field retain their
historical meaning; use `figure_row` for the selected figure arrangement.

## Fresh calculations

`--mode full` (the default) builds each selected solver, executes the selected
campaign, runs ED, reblocks the new measurements, and draws the selected figures.
With the default scope, this is the 15-point current manuscript campaign.
The original data stay fixed in `data/`. Output goes to the directory selected
by `--output` and includes the numerical differences from ED.

Fresh Monte Carlo trajectories can differ with compiler and numerical library:
the published data remain the exact source for regenerating the original curves.
PDF metadata and font-library versions can also change PDF byte hashes even
when the plotted data and layout are identical.

For separate stages, `--mode dqmc` and `--mode ed` write into `output/runs/`.
After both stages, `--mode analyze` reblocks their outputs and draws the figures.
Use the same `--scope` and `--model` for each stage and for `--resume`.
Each solver's `run_paper.py --help` also exposes case selection or campaign
configuration and an analysis entry point. Do not overwrite archived input files
when creating a new model campaign; copy them into your own configuration directory.

## Source provenance

The number-conserving implementation was imported from `code_bosonDQMC` at
`68b82365ab817fd4a96e357358c31181f7acb3f3`; the paired implementation from
`code_bosonDQMC_paring` at `e4c1d04e6b756eb6bd6d0cf5b9a778c6b54a920c`.
Their Fortran model kernels were imported without changes. The integration
provides portable build files, local campaign runners, and standard numerical
interfaces; see `software/common/README.md`.

Historical campaigns were stored outside Git tracking. These commit IDs identify
the imported source snapshots, not a proven historical production executable.
The original summary, plotting-script, style, and PDF hashes are recorded in
`data/index.json`. The two original PDF hashes match the historical
`benchmark_number_conserving.pdf` and `benchmark_pairing_delta.pdf` retained in
this repository. `tools/import_original.py` is a maintainer import tool;
it is not used by readers and the normal workflow needs no sibling repositories.
