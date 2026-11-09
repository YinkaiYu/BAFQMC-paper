# Sign-problem-free Bosonic Auxiliary Field Quantum Monte Carlo

**Yin-Kai Yu, Zhong-Chao Wei, and Zi-Xiang Li**

[Read the paper](https://arxiv.org/abs/2610.31541) ·
[PDF](https://arxiv.org/pdf/2610.31541) ·
[arXiv v1 source](https://github.com/YinkaiYu/BAFQMC-paper/tree/arxiv-v1) ·
[BAFQMC software](https://github.com/YinkaiYu/BAFQMC)

Geometrical frustration makes many interacting bosonic systems difficult to study
with conventional quantum Monte Carlo. This work develops bosonic auxiliary-field
quantum Monte Carlo (BAFQMC) and establishes time-reversal symmetry and reflection
positivity as sufficient conditions for sign-problem-free simulations. These
principles open a broad class of frustrated bosonic models to unbiased, numerically
exact calculations. Benchmarks on a two-flavor Bose-Hubbard model on the triangular
lattice demonstrate agreement with finite-temperature exact diagonalization.

This repository contains the manuscript and Supplemental Material, figures,
research notes, and the computational package used to reproduce the benchmarks.
For using and extending the algorithm, visit the dedicated
[BAFQMC software repository](https://github.com/YinkaiYu/BAFQMC).

## Read and explore

| Content | Location |
|---|---|
| Main manuscript | [main.tex](main.tex) |
| Supplemental Material, compiled with the manuscript | [SM.tex](SM.tex) |
| Bibliography | [references.bib](references.bib) |
| Publication figures | [figures/](figures/) |
| Benchmark data, inputs, analysis, and plotting | [reproducibility/](reproducibility/README.md) |
| Number-conserving BAFQMC and reference calculations | [software/number_conserving/](software/number_conserving/README.md) |
| Paired/Nambu BAFQMC and reference calculations | [software/pairing/](software/pairing/README.md) |
| Shared numerical routines | [software/common/](software/common/README.md) |
| Research notes and supporting calculations | [note/](note/) |

The [`arxiv-v1`](https://github.com/YinkaiYu/BAFQMC-paper/tree/arxiv-v1)
tag preserves the source corresponding to
[arXiv:2610.31541v1](https://arxiv.org/abs/2610.31541v1).
The `main` branch contains ongoing work, including research notes that develop
beyond the published preprint.

## Build the paper

Builds use Linux or WSL with a TeX Live installation providing `latexmk`,
`pdflatex`, BibTeX, REVTeX 4.2, and the packages used by the manuscript.
A full TeX Live installation is a convenient option.

From the repository root on Linux/WSL:

```bash
bash scripts/build-manuscript.sh
```

From native Windows PowerShell with WSL installed:

```powershell
.\scripts\build-manuscript.ps1
```

The resulting `pdf/main.pdf` contains both the main text and Supplemental Material.
Intermediate files are written to `.build/`.

To generate `pdf/main-diff.pdf` against a Git revision, use the diff script
with that revision. For example, to compare with arXiv v1:

```bash
bash scripts/build-diff.sh arxiv-v1
```

The Windows equivalent is `.\scripts\build-diff.ps1 arxiv-v1`.
Diff generation additionally requires `latexpand` and `latexdiff`.

## Reproduce the benchmarks

The repository includes processed measurements, block statistics, reference
results, and simulation inputs. You can redraw these results or run new BAFQMC
and reference calculations. See the [benchmark guide](reproducibility/README.md)
for physical conventions, parameters, and data provenance.

### Redraw the stored results

With Python 3.11 or newer:

```bash
python3 -m pip install -r reproducibility/requirements.txt
python3 reproduce.py --mode plot
```

This generates the main-text and supplemental benchmark figures under
`reproducibility/output/`. It uses the stored processed data and does not launch
new simulations.

### Run new calculations

Fresh simulations run on Linux/WSL and require an MPI Fortran compiler,
BLAS/LAPACK, and the Python packages for plotting and exact diagonalization.
For Ubuntu/Debian:

```bash
sudo apt-get install build-essential gfortran libopenmpi-dev openmpi-bin liblapack-dev libblas-dev
python3 -m pip install -r reproducibility/requirements.txt -r reproducibility/requirements-ed.txt
```

A [Conda environment](reproducibility/environment.yml) is also provided for the
Python dependencies. The compiler and MPI libraries are installed separately.

Inspect the calculation plan, run a small installation check, or reproduce the
complete campaign:

```bash
python3 reproduce.py --plan
python3 reproduce.py --mode smoke --output reproducibility/output/smoke-check
python3 reproduce.py
```

The full campaign reruns the BAFQMC and reference calculations, processes the
measurements, and generates the figures in a new
`reproducibility/output/full-TIMESTAMP/` directory. Consult the
[resource guide](reproducibility/RESOURCES.md) before starting a production run.

Use `--scope main` or `--scope supplement` to select benchmarks, and
`--model number_conserving` or `--model pairing` to select a solver. Resume an
interrupted run with the same selections and output directory:

```bash
python3 reproduce.py --resume --output reproducibility/output/full-TIMESTAMP
```

Windows PowerShell users can invoke the same workflow through WSL:

```powershell
.\scripts\reproduce.ps1 -Plan
.\scripts\reproduce.ps1 -Mode plot
.\scripts\reproduce.ps1
```

Large raw simulation outputs and local build products are excluded from Git.
The [validation notes](reproducibility/VALIDATION.md) describe the integration
checks; each solver's README explains how to configure and extend it.

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{yu2026bafqmc,
  title         = {Sign-problem-free Bosonic Auxiliary Field Quantum Monte Carlo},
  author        = {Yin-Kai Yu and Zhong-Chao Wei and Zi-Xiang Li},
  year          = {2026},
  eprint        = {2610.31541},
  archivePrefix = {arXiv},
  primaryClass  = {cond-mat.str-el},
  doi           = {10.48550/arXiv.2610.31541},
  url           = {https://arxiv.org/abs/2610.31541}
}
```

## Questions and contributions

Questions, corrections, and suggestions about the manuscript or its reproduction
materials are welcome through this repository's
[issues](https://github.com/YinkaiYu/BAFQMC-paper/issues) and pull requests.
For algorithm development and software contributions, visit
[YinkaiYu/BAFQMC](https://github.com/YinkaiYu/BAFQMC).

## License

The computational package (`software/`, `reproducibility/`, `reproduce.py`, and
the reproduction launchers) is released under the [MIT license](LICENSE).
External dependencies retain their own licenses. This software license does not
relicense the manuscript text, bibliography, or publication figures; see the
[arXiv record](https://arxiv.org/abs/2610.31541) for the preprint's license.
