# Bosonic auxiliary-field quantum Monte Carlo

This repository accompanies the BAFQMC manuscript in [main.tex](main.tex).
It provides the number-conserving and paired/Nambu implementations for the
two-flavor Bose–Hubbard model on a frustrated triangular lattice, independent
finite-temperature exact diagonalization (ED), and the data and plotting code
for the combined main-text benchmark and the attractive-density benchmark in
the Supplemental Material.

## Check the PRL length

After editing, run in native Windows PowerShell:

```powershell
.\scripts\count-prl-words.ps1
```

Or directly in Linux/WSL:

```bash
python3 scripts/count-prl-words.py
```

The script incrementally builds the manuscript and prints text, equation,
figure, and table equivalents using the [APS length rules](https://journals.aps.org/authors/length-guide)
and APS-recommended `wordcount.tex`. It reports the difference from 3750 words
and a conservative allowance for matrix rows. It excludes the abstract,
acknowledgments, bibliography, and Supplemental Material. It changes no source
and generates no report; temporary counting copies and logs stay in `.build/`.
Dependencies are Linux/WSL TeX Live (`latexmk`, `pdflatex`, `wordcount`) and
Python with PyMuPDF (`fitz`).

Use `-NoBuild` / `--no-build` only for an already up-to-date build. Use `-Check`
/ `--check` to return exit status 1 when the conservative total exceeds the
limit (normal runs return 0; calculation errors return 2).

The counter supports the manuscript's displayed-math environments and figures
embedded as single combined PDFs. Inspect rendered equation rows after layout
changes. New or changed table bodies require an explicit reviewed line count,
including headers and wrapped lines, for example:

```powershell
.\scripts\count-prl-words.ps1 -TableLines 'tab:trs_periodic=9'
```

The Linux option is `--table-lines tab:trs_periodic=9`. Reviewed table counts
and body fingerprints live in `scripts/prl-table-lines.json`; changing captions
alone does not invalidate them. Unsupported layouts fail explicitly rather
than silently omitting content. APS's public rules are an estimate and do not
fully specify matrix-internal row counting; both totals are shown.

## Reproduce the complete benchmark data

The default command **builds and runs BAFQMC and ED at all 22 paper parameter
points**: 15 in the main text and seven in the Supplemental Material. It then
computes the means and standard errors and generates both benchmark figures:

```bash
python3 reproduce.py
```

Budget **12–24 hours on a recent desktop, 16 GiB RAM, and 8 GiB free disk** for
the complete sequential run. The paired Monte Carlo chains dominate the time.
These estimates are based on actual calibration runs and historical production
timings; see [resource measurements](reproducibility/RESOURCES.md).
`python3 reproduce.py --plan` displays the plan without starting calculations.

Fresh simulations run on Linux or WSL. Install an MPI Fortran compiler,
BLAS/LAPACK, and Python 3.11 or newer. For example, on Ubuntu/Debian:

```bash
sudo apt-get install build-essential gfortran libopenmpi-dev openmpi-bin liblapack-dev libblas-dev
python3 -m pip install -r reproducibility/requirements.txt -r reproducibility/requirements-ed.txt
```

Alternatively, the [Conda environment](reproducibility/environment.yml) provides
the Python packages; the compiler and MPI libraries are installed separately.
QuSpin's [installation documentation](https://quspin.github.io/QuSpin/installation/installation.html)
describes the supported Python installation route.

The default run uses one MPI rank and one numerical-library thread. Cases are
computed sequentially. Set `--threads N` to choose the library thread count or
`--python-ed /path/to/python` to use a separate QuSpin environment. Each point
uses the original 100000 measurement bins and original reference prescription.

A new directory `reproducibility/output/full-TIMESTAMP/` receives:

- `runs/`: newly calculated raw BAFQMC data and ED results;
- `observables.csv`, `block_means.csv`, and `records.json`;
- `figures/benchmark_combined.pdf` and `figures/benchmark_attractive.pdf`,
  with PNG previews;
- `progress.json`, per-stage logs, and an environment record.

The driver runs file-intensive simulation output in Linux scratch space and
copies completed stages to the results directory. All generated raw data are
ignored by Git. Resume an interrupted run with:

```bash
python3 reproduce.py --resume --output reproducibility/output/full-TIMESTAMP
```

Completed stages are verified and skipped. Use `--scope main` for the 15
main-text points or `--scope supplement` for the seven attractive-density
points; the default `--scope all` covers both. `--model number_conserving` or
`--model pairing` additionally selects one implementation. For example,
`--scope main --model number_conserving` runs the eight-point interaction scan.
Keep the same scope and model when resuming. `--mode dqmc`, `--mode ed`, and
`--mode analyze` run separate stages with an explicit shared `--output`.

## Check the installation or redraw stored results

A small BAFQMC -> ED -> analysis check exercises both implementations:

```bash
python3 reproduce.py --mode smoke --output reproducibility/output/smoke-check
```

The repository also includes about 250 kB of processed means, standard errors,
block statistics, ED summaries, and initial inputs. A quick redraw uses:

```bash
python3 reproduce.py --mode plot
```

This optional command needs only `reproducibility/requirements.txt`. The
full raw production sequences are regenerated by the solvers and are not
tracked in Git. No access to the original simulation repositories is needed.

On native Windows PowerShell, use the WSL entry point:

```powershell
.\scripts\reproduce.ps1 -Plan
.\scripts\reproduce.ps1
.\scripts\reproduce.ps1 -Mode plot
```

## Use and extend the algorithms

| Component | Entry point |
|---|---|
| Number-conserving BAFQMC, ED, examples, and regression suite | [software/number_conserving/](software/number_conserving/README.md) |
| Paired/Nambu BAFQMC, ED, examples, and regression suite | [software/pairing/](software/pairing/README.md) |
| Shared standard BLAS/LAPACK interfaces and random generator | [software/common/](software/common/README.md) |
| Paper parameters, data conventions, and provenance | [reproducibility/README.md](reproducibility/README.md) |
| Resource estimates and integration checks | [Resources](reproducibility/RESOURCES.md), [validation](reproducibility/VALIDATION.md) |
| Plot layout and common style | [reproducibility/](reproducibility/) |

Each solver includes readable physical conventions, parameterized input files,
and its own `Makefile`. Start from a supplied run directory or campaign manifest,
change the physical and sampling parameters, and run in a fresh directory.
The model kernels and observable estimators are kept separate from campaign
orchestration and plotting. Both solvers build from this repository without
the original workstation's private numerical library.

The main-text interaction is `U (n_b - n_c)^2`; set `U1=0` and `U2=U` in the
solver inputs. The supplemental model retains both `U1 (n_b + n_c)^2` and
`U2 (n_b - n_c)^2`. The [benchmark conventions](reproducibility/README.md)
connect the manuscript symbols, input parameters, observables, and references.
Exported tables include BAFQMC means, standard errors, ED values, and their
differences. All valid parameter points are included.

## License and manuscript

The computational package (`software/`, `reproducibility/`, `reproduce.py`, and
the reproduction launchers) is released under the [MIT license](LICENSE).
External dependencies retain their own licenses and are installed separately.
This license does not relicense the manuscript text, bibliography, or existing
publication figures. Please cite the accompanying manuscript when using BAFQMC
in research.

To compile the manuscript in Linux/WSL, run `bash scripts/build-manuscript.sh`.
The PDF is written to `pdf/main.pdf`.
