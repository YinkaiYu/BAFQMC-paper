# Benchmarks

The default benchmark is the strict live DQMC-vs-ED suite:

```bash
make benchmark
```

`make benchmark` is an alias for `make benchmark-dqmc`. It runs the manifest in `benchmarks/dqmc_suite.json`, which includes the free-boson analytic case plus all four ED cases preserved in `benchmarks/dqmc_references/`. All cases must pass for `total_NE`, `total_kinetic`, `doubleOcc`, `squareOcc`, `numsquare_up`, and `numsquare_do`.

All live benchmark inputs use `dtau = beta / Ltrot = 0.01`. The interacting cases use `Nbin = 100000`, `Nsweep = 1`, `shiftLoc = 1.5`, and warm-up enabled. On the current WSL workstation with `MPI_NP=1`, the full live suite was observed at `real 604.50` seconds, about 10 minutes 5 seconds; budget at least 15 minutes, and longer if the machine is busy.

The fast benchmark is a real DQMC run for the no-interaction `U1=U2=0` case:

```bash
make benchmark-fast
```

It compares against the analytic reference in `benchmarks/dqmc_references/triangle_3x2_free_beta3_mu-2.5.json`. This is useful for quick executable, Green-function, particle-number, kinetic-normalization, and equal-time scalar observable checks, but it does not exercise the interacting Monte Carlo path.

`make check-fixtures` is a fast comparison-script check over checked-in fixture files. It discovers every `*.json` file under `benchmarks/references/`. Each reference points to a fixture DQMC-style output directory under `benchmarks/fixtures/`. This validates parsing and documented DQMC-to-ED normalization semantics, but it is not physics validation and must not replace `make benchmark` for algorithm changes.

For one-off debugging of a single case, override both `DQMC_BENCHMARK_INPUT_DIR` and `DQMC_BENCHMARK_REFERENCE`. Do not use a single-case override as the final benchmark evidence for substantive algorithm changes.

## Live Pass/Fail Semantics

For an interacting live DQMC observable, `benchmarks/compare.py` first converts each bin to the ED scale. Live benchmark pass/fail covers the `num_up`, `num_do`, `kinetic`, `doubleOcc`, `squareOcc`, `numsquare_up`, and `numsquare_do` conversions documented below. It then groups the 100000 samples into 10 blocks of 10000 samples. The reported `stderr` is the standard error of the Monte Carlo mean:

```text
stderr = std(block_means) / sqrt(number_of_blocks)
z = (DQMC_block_mean - ED_value) / stderr
```

The field `stderr_tolerance` is the allowed number of standard errors of the mean, not the standard deviation of individual Monte Carlo samples. The current references use `stderr_tolerance = 3.0`; a case passes when:

```text
abs(DQMC_block_mean - ED_value) <= max(atol, rtol * abs(ED_value), stderr_tolerance * stderr)
```

The free-boson case is deterministic and uses a tight absolute tolerance instead of block statistics.

## Observable Conversions

For the current DQMC output:

```text
total_NE = last(num_up) + last(num_do)
total_kinetic = last(kinetic) * Lq
doubleOcc = last(doubleOcc)
squareOcc = last(squareOcc)
numsquare_up = last(numsquare_up)
numsquare_do = last(numsquare_do)
```

The ED script accumulates `NE = NE_b + NE_c` and its kinetic operator includes both b and c hopping layers. The DQMC `kinetic` file includes both flavors and is divided by `Lq` in `src/obser_equal.f90`. `doubleOcc` is compared per site. `squareOcc` is compared as the per-site half normal-ordered same-flavor onsite pair, `0.5 * <sum_i,s n_s,i (n_s,i - 1)> / Lq`. `numsquare_up` and `numsquare_do` are compared as total flavor number-square observables.

Interacting real DQMC benchmarks use sample means instead of the last bin:

```text
total_NE = mean(num_up) + mean(num_do)
total_kinetic = mean(kinetic) * Lq
doubleOcc = mean(doubleOcc)
squareOcc = mean(squareOcc)
numsquare_up = mean(numsquare_up)
numsquare_do = mean(numsquare_do)
```

## 3x3 Observable Campaign

The 3x3 observable campaign is a separate research workflow for the
publication benchmark. It does not replace `make benchmark`, and it must not
change the default 3x2 regression suite.

Tracked campaign files:

- manifest: `benchmarks/campaigns/triangle_3x3_observables.json`
- campaign helper and report writer: `benchmarks/campaign_3x3.py`
- DQMC parser/statistics helper: `benchmarks/campaign_analysis.py`
- paper plotting helper: `benchmarks/plot_style.py` (style rules in `docs/plotting.md`)
- 3x3 QuSpin ED reference: `benchmarks/ed/EDtriangle_quspin_3x3.py`
- Slurm ED wrapper: `scripts/sbatch_ed_3x3.sh`
- tiny DQMC smoke input: `runs/benchmarks/triangle_3x3_smoke/`

Generated research outputs live under ignored `data/`, for example:

```text
data/20260603_bafqmc_ed_3x3_observables/
```

Use the manifest and write the Stage 1 report with:

```bash
python3 benchmarks/campaign_3x3.py write-manifest \
  --output benchmarks/campaigns/triangle_3x3_observables.json

python3 benchmarks/campaign_3x3.py stage1-report \
  --output-dir data/20260603_bafqmc_ed_3x3_observables
```

Create local fixed-file input directories for all starting cases:

```bash
python3 benchmarks/campaign_3x3.py init-local \
  --manifest benchmarks/campaigns/triangle_3x3_observables.json \
  --output-dir data/20260603_bafqmc_ed_3x3_observables/probe_inputs \
  --seed 64464988
```

Each generated case directory contains DQMC fixed filenames
`paramC_sets.txt`, `confin.txt`, and `seeds.txt`, plus an ED `params.json`.
`write_dqmc_case()` removes known append-only DQMC output files before
regenerating inputs, so stale samples do not silently mix with reruns. Unknown
user files in the run directory are left alone.

The starting sweeps are:

```text
U2 sweep: mu=-3.5, beta=4.0, U1=0.0, U2=[0, 0.5, 1.0, 1.5, 2.0]
U1 sweep: mu=-5.0, beta=1.0, U2=1.0, U1=[0, -0.05, -0.1, -0.15, -0.2]
```

For 3x3 and the current hopping convention, `epsilon_min=-3`, so the `U1=0`
grand-canonical sweep must keep `mu < -3`. Negative `U1` is treated as a
low-density finite-window/cutoff comparison. Such ED points can be accepted
only with status `low_density_cutoff_accepted`; they are not labeled fully
converged. The postprocessing trusted gate is intentionally stricter than the
ED script's runtime early-stop policy: negative-`U1` finite-window points must
also have `density_total <= 5e-2` and `completed_shells >= 6` before entering
trusted BAFQMC-vs-ED curves. Shallower checkpoints, such as an `N=2` early stop,
remain diagnostics only.

The 3x3 structure-factor channel uses the common triangular-lattice vectors
`a1=(1,0)`, `a2=(1/2,sqrt(3)/2)` and reciprocal vectors
`b1=2*pi*(1,-1/sqrt(3))`, `b2=2*pi*(0,2/sqrt(3))`. The code-facing K index
is `(2*Lx/3+1, Ly/3+1)`, corresponding on a 3x3 lattice to integer momentum
coordinate `(2,1)` and physical momentum `K=(4*pi/3,0)`. Earlier reports that
used the equivalent `a2'=a2-a1` primitive-cell relabeling need no data rerun
for this convention update.

The campaign DQMC defaults are:

```text
dtau=0.01
Ltrot=beta/dtau
Nwrap=10
Nbin=100000
Nsweep=1
shiftLoc=1.5
is_warm=true
Nwarm=500
shiftWarm1=1.0
shiftWarm2=1.0
iniType=2
iniAmpl=0.1
iniBias1=0.0
iniBias2=0.0
block_size=10000
```

Campaign comparisons use `analysis_defaults` from the manifest unless CLI
options override them:

```text
stderr_tolerance=3.0
atol=0.0
rtol=0.0
min_ipr_number=1e-8
```

After DQMC and ED outputs are present, write a fail-closed summary with:

```bash
python3 benchmarks/campaign_3x3.py summarize-results \
  --manifest benchmarks/campaigns/triangle_3x3_observables.json \
  --input-dir data/20260603_bafqmc_ed_3x3_observables/production_inputs \
  --output-dir data/20260603_bafqmc_ed_3x3_observables \
  --report-name report_stage_results.html
```

The summary command writes `summary_campaign_results.json`,
`summary_campaign_results.csv`, `figures/*.png`, and an HTML report. It emits
seven observable rows for every case, even when DQMC or ED is missing, so
excluded or unfinished points remain visible in diagnostics. It calls
`ed_reference_reliable()` before any ED point can be trusted, cross-checks that
`results.json` parameters match the manifest case (`Lx`, `Ly`, `beta`, `mu`,
`U1`, `U2`, and `max_total_particles`), and excludes incomplete, dry-run,
stale, or cutoff-unreliable ED JSON from trusted comparisons. For complex
structure factors, the real part is compared to ED and the DQMC imaginary part
must be statistically consistent with zero under the same `stderr_tolerance`,
up to a `1e-14` absolute roundoff floor for double-precision phase sums.
DQMC total density must also remain positive; non-positive block means are
treated as runaway diagnostics rather than trusted physics comparisons.
The CSV and HTML raw index include the run directory, `results.json`,
`paramC_sets.txt`, and the DQMC files used by each observable. If
`submitted_jobs.json` exists in the summary output directory, the JSON and HTML
also index each Slurm job id, job name, queue, case directory, and inferred
`logs/<job_id>.out` / `logs/<job_id>.err` paths.

While production jobs are still queued, write a standalone queue snapshot
report from the summary directory:

```bash
python3 benchmarks/campaign_3x3.py queue-snapshot-report \
  --summary-dir data/20260603_bafqmc_ed_3x3_observables/hpc_summary \
  --output-dir data/20260603_bafqmc_ed_3x3_observables \
  --checked-at 2026-06-03T08:00:32+0800 \
  --hpc-root /path/to/campaign \
  --repo-commit "$(git rev-parse --short HEAD)" \
  --default-state PENDING \
  --default-reason Priority \
  --default-start-time 2026-06-05T20:27:11 \
  --default-time-limit 7-00:00:00
```

This writes `report_stage_4_hpc_queue_snapshot.html`; it is a status report,
not a trusted physics comparison.

The default ED shell cutoff is `max_total_particles=6`, chosen as a practical
starting point for the dense momentum-sector QuSpin implementation. Raise the
cutoff on HPC if the last-shell diagnostics are not small enough. Accepted ED
payloads must have schema version 1, complete finite observable fields,
explicit `completed_shells`, and reliability status consistent with the policy.
Schema-only dry runs are rejected by postprocessing.

The 3x3 QuSpin ED helper writes a checkpoint after every total-particle shell
and, by default, stops once the result is reliable under the policy
(`converged` or `low_density_cutoff_accepted`) after `min_completed_shells`.
The `converged` label itself also requires this minimum-shell gate, so an
early zero-particle checkpoint cannot be reused as a reliable ED reference.
This avoids spending hours on higher shells whose relative contribution is
already below the requested tail tolerance. To force a full run through
`max_total_particles`, pass `--no-stop-when-reliable` or set
`"stop_when_reliable": false` in `convergence_policy`.
The 3x3 ED schema includes both first and second total flavor-number moments:
`num_up`, `num_do`, `numsquare_up`, and `numsquare_do`.

For stable noninteracting 3x3 campaign points with `U1=U2=0` and
`mu < epsilon_min`, postprocessing may use the exact grand-canonical
free-boson reference instead of waiting for a high-cutoff QuSpin ED run. The
analysis still prefers a reliable real ED payload when one is already present,
but replaces missing or unreliable free ED with `ed_status=exact_free_boson`.
For the triangular 3x3 convention used here, `epsilon_min=-3`; the main
`U2=0, mu=-3.5` point is therefore stable and is evaluated exactly from the
single-particle occupations
`n_k = 1 / (exp(beta * (epsilon_k - mu)) - 1)`.
For each flavor, the exact reference reports
`<N^2> = <N>^2 + sum_k n_k * (1 + n_k)`.

Campaign observables and DQMC file names:

| Observable | DQMC files used | Notes |
| --- | --- | --- |
| `density_total` | `density_total` | per-site total particle density |
| `energy_density` | `energy_density` | physical energy density without `-mu N` |
| `doubleOcc` | `doubleOcc` | per-site cross-flavor onsite density product |
| `num_up` | `num_up` | total `b`-flavor particle number |
| `num_do` | `num_do` | total `c`-flavor particle number |
| `numsquare_up` | `numsquare_up` | total `b`-flavor number-square moment `<N_b^2>` |
| `numsquare_do` | `numsquare_do` | total `c`-flavor number-square moment `<N_c^2>` |
| `IPR` | `density_site_total` | normalized total-density profile `sum_i rho_i^2/(sum_i rho_i)^2`; uniform 3x3 gives `1/9` |
| `S_SF_K` | `sf_K` | complex file, real/imag columns, K point; real part is the plotted structure factor |
| `S_PSF_Gamma` | `psf_Gamma` | complex file, real/imag columns, Gamma point; real part is the plotted structure factor |
| `S_DW_K` | `dw_K` | complex file, real/imag columns, K point; real part is the plotted structure factor |

Optional runtime smoke checks:

```bash
RUN_DQMC_SMOKE=1 python3 -m unittest \
  benchmarks.test_obser_equal.EqualTimeCampaignObservableRuntimeTests -v

RUN_ED_SMOKE=1 python3 -m unittest \
  benchmarks.test_ed_quspin_schema.EDQuSpinSchemaTests.test_tiny_runtime_ed_smoke_when_quspin_is_available -v
```

Use the Python interpreter from your QuSpin environment for ED work. Set
`ED_PYTHON=/path/to/python` to select that interpreter for optional runtime tests.
For paper cases, use `../run_paper.py`; it accepts the exact distributed input
files and ED convergence policy through a portable manifest. The original
campaign helper remains available for preparing broader custom sweeps; its
cluster settings are placeholders and are not needed for local execution.

## Pole Diagnostic Checks

Continuous pole diagnostics are structural and analysis outputs, not ED physics observables. They are not used in live benchmark pass/fail decisions.

For a run with `Nbin` bins and MPI size `ISIZE`, the diagnostic files contain `Nbin * ISIZE` configuration samples. One sample is written per bin per MPI rank, and rank 0 gathers rank-local samples and writes rows in rank order. These samples are not rank averaged.

Validate the diagnostic file structure and consistency with:

```bash
python3 benchmarks/check_pole_diagnostics.py <run_dir>
```

## Adding A Case

Add one JSON file under `benchmarks/references/` and one fixture directory under `benchmarks/fixtures/`. The reference JSON must include:

- `case`: stable case identifier, matching the JSON filename stem
- `dqmc_fixture`: repository-relative path to the fixture output directory
- `parameters`: `Lx`, `Ly`, `t`, `U1`, `U2`, `beta`, `mu`
- `observables`: the scalar observables needed by the case, with explicit operation names such as `last`, `mean`, `sum_mean`, or `mean_times_lq`

The fixture directory must contain scalar output files with DQMC names, currently `num_up`, `num_do`, `kinetic`, `doubleOcc`, `squareOcc`, `numsquare_up`, and `numsquare_do`.

Run the suite after adding a case:

```bash
python3 -m unittest benchmarks/test_compare.py -v
make check-fixtures
```

If the case is meant to exercise the live DQMC executable, add a JSON under `benchmarks/dqmc_references/`, add or reuse an input directory under `runs/benchmarks/`, wire it through `benchmarks/dqmc_suite.json`, and run `make benchmark`.

## Optional ED Recompute

Run:

```bash
make benchmark-ed
```

This runs `benchmarks/ed/EDtriangle_symm_NEblock.py` from inside `benchmarks/ed/`. It requires QuSpin and Numba and can take much longer than the default benchmark.
