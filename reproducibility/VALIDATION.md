# Integration validation

Validation was performed in Linux/WSL during the repository integration on
2026-09-15. The Fortran tests used Intel `mpiifx` 2025.2.1 and MKL. Python ED
used QuSpin 1.0.1, NumPy 2.4.4, SciPy 1.17.1, and Numba 0.65.1. Figure checks
used NumPy 2.3.4 and Matplotlib 3.10.7.

- All 35 imported Fortran model/propagation/measurement sources match their
  source-repository snapshots byte for byte. The shared numerical interfaces
  are the new portable code described in `software/common/README.md`.
- Matrix reconstruction, Hermitian eigensystems, inversion, and the random
  sequence passed independent invariant checks. The modular random recurrence
  also matched 150000 transitions of the historical integer-wrap convention.
- The number-conserving live regression completed its analytic free case and
  four interacting 100000-bin cases. Its Python, parameter-routing, and ED
  memory checks passed.
- Paired live checks covered finite Delta and Delta=0. Independent small ED
  formulations agreed on 25 observables and energy derivatives.
- Small complete DQMC -> ED -> analysis runs passed for both solvers. Production
  orchestration checks cover per-case copying, hashes, continuation, and
  restarting an interrupted chain from its original input.
- A full paper-size paired ED calculation (7297 basis states at Delta=0.2)
  reproduced the archived four reference values within 5.3e-18 absolute.
- All 22 archived cases were reblocked from their original 100000-sample
  measurement sequences before retaining the compact processed tables. The
  stored means and standard errors agree with that independent reconstruction.
  The compact package also passed without any raw archives present.
- Both regenerated figure PDFs, rasterized to 1800 pixels wide with the same
  renderer, matched the manuscript figures pixel for pixel. PDF byte identity
  is not required because metadata can differ.

The 22-point production campaign has not been rerun in its entirety during this
integration. The default command performs that computation. Its time and memory
budget is based on the measurements in [RESOURCES.md](RESOURCES.md).

GNU Fortran/BLAS build settings and a GitHub Actions workflow are supplied.
That compiler was not installed on the validation workstation, so local runtime
results above refer to the Intel/MKL build. CI exercises the GNU setup when run.
