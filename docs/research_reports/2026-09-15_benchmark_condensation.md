# Benchmark presentation and uniform trace convergence

Date: 2026-09-15. Author-specified comparison baseline: `1b207e7`.

## Scientific purpose and scope

The main-text benchmark validates the number-conserving and paired BAFQMC
constructions with one compact figure. The reader has already encountered TRS
and RP; the example connects the imaginary relative-density HS field to both
criteria at zero pairing and to RP at finite pairing. Observable definitions,
simulation parameters, and the separate attractive-density scan belong in the SM.
The new convergence proof establishes that the complete auxiliary-field domain of
both main-text scans has finite operator traces and contains no determinant poles.

## Manuscript and figure changes

- Main Eq. (9) uses `U` for the repulsive relative-density interaction and omits
  the attractive total-density term. Hopping occupies the first line; the pairing
  term precedes the `U` term on the second line.
- Main Fig. 2 is a two-row, four-column figure. The upper row scans `U` at
  `Delta=0`, `mu=-3.5`, `beta=4`; the lower row scans `Delta` at `U=1`, `mu=-5`,
  `beta=4`. Both use the original periodic 3-by-3 lattice with `t=1`.
- The original attractive scan is Fig. S1. Its model retains both `U1` and `U2`,
  with `U2=1`, `mu=-7`, and `beta=1`. Its original `U1` horizontal axis remains.
- `reproducibility/plot_manuscript.py` composes these figures from the archived
  records. Original reference points, BAFQMC means, SEM, and observable
  normalizations are preserved. The energy is displayed as `-E=-9e` and its
  standard error is multiplied by 9. The original logarithmic `U` axes and linear
  `Delta` and `U1` axes are retained.
- The existing simulation code and all archived inputs/data are unchanged. The
  older figure assets remain available for provenance. No new simulations were
  performed, and no bibliography entry was added or changed.

## Uniform convergence proof

SM Sec. VIII B proves the sufficient condition

\[
\mu<-3t-|\Delta|,\qquad U\ge0.
\]

The triangular-lattice identity
`epsilon_k=t|1+exp(ik.a1)+exp(ik.a2)|^2-3t` bounds the dispersion below by `-3t`.
The bound is attained on the benchmark cluster. Thus every quadratic mode has
`xi_k=epsilon_k-mu>|Delta|` and positive Bogoliubov energy
`omega_k=sqrt(xi_k^2-|Delta|^2)`. Including the Bogoliubov vacuum constant and
both flavors gives

\[
Z_0=\prod_k\frac{e^{\beta(\xi_k-\omega_k)}}{(1-e^{-\beta\omega_k})^2}<\infty.
\]

The actual discretized propagation has the form `product_l T V_l`, with the full
kinetic-plus-pairing exponential `T=exp(-Delta tau K0)` and unitary relative-density
HS factors `V_l`. Schatten Hölder gives the field-independent bound

\[
\left\|\prod_{\ell=1}^{L_\tau}TV_\ell\right\|_1
\le\prod_\ell\|TV_\ell\|_{L_\tau}
=\|T\|_{L_\tau}^{L_\tau}=Z_0.
\]

Every configuration is trace class, `|W(phi)|<=Z0`, and the normalized Gaussian
HS integral converges absolutely. The bound holds for every finite `U>=0` and
every finite number of slices at fixed beta.

The relative-density generator has zero one-body trace, so the Nambu scalar is
field independent: `sum_l xi_l=beta sum_k xi_k`. The Gaussian trace formula then
gives, on the connected nonsingular region containing zero fields,

\[
|\det(I_{2N}-\mathcal M(\phi))|
\ge\frac{e^{2\beta\sum_k\xi_k}}{Z_0^2}
=\prod_k[2\sinh(\beta\omega_k/2)]^4>0.
\]

Continuous variation of the real auxiliary fields cannot reach a first
determinant zero. This closes the no-pole argument for the whole integration
domain. The minimum `xi_k-|Delta|` is 0.5 for the `U` scan and at least 1.7 for
the pairing scan. The proof is confined to the repulsive main-text model; the
attractive-channel interpretation and the existing finite-part discussion are
preserved for the separate author discussion.

An independent read-only physics review checked the Bogoliubov constant,
Schatten inequality, normal-ordering scalar, determinant bound, and both parameter
sets. Its final inspection confirmed correspondence with the full matrix
exponential in `software/pairing/src/non_interact.f90` and the unitary HS factors,
with no remaining material issues.

## Numerical wording audit

The original blanket claim of agreement within statistical error bars was too
strong. In the paired scan, 19 of 28 observable comparisons exceed one SEM and
11 exceed three SEM. At `Delta=0.30`, the density-wave structure factor differs
by 9.966 SEM and the energy by about 9.790 SEM. The largest relative discrepancy
over the pairing scan is 0.551%; the corresponding maxima for the `U` and `U1`
scans are 3.58% and 0.241%. At the deterministic free point, SEM-scale ratios
are not informative: the density's relative discrepancy is only about
`2.1e-13`, while the recorded SEM is nearly zero.

The manuscript now describes quantitative agreement and identifies the plotted
bars as statistical SEM. No points or uncertainties were adjusted. The cause of
the residual discrepancies is not inferred from this presentation audit.

## Validation and delivery artifacts

- WSL plotting verified all 115 archived input/data checksums and reproduced all
  22 selected cases without launching a new Monte Carlo calculation.
- Inspection of the actual Matplotlib axes verified all 88 reference values,
  BAFQMC means, and SEM pairs, including row selection and the energy conversion.
- All five existing `reproducibility.tests.test_reproduction` tests passed in WSL.
- Source checks preserved the TRS/RP discussion, odd-parity application, deferred
  finite-part discussion, bibliography, and simulation code. Cross-references,
  process-language scanning, and `git diff --check` passed.
- The authoritative WSL build refreshed `pdf/main.pdf` (34 pages) and
  `pdf/main-diff.pdf` (36 pages), comparing expanded main text and SM with
  `1b207e7`. Rendered inspection covered Fig. 2, Eq. (9), the convergence proof,
  Fig. S1, numerical details, and their marked counterparts.
- Diff-only formatting gives the heavily marked example prose ragged-right
  alignment, reserves space for blue figure frames, and displays retired figure
  references using their baseline numbers. The manuscript retains its normal
  justified text and native figure sizes.
- No new compilation warnings remain. Existing notices are REVTeX's default
  type size and nameref's label redefinition, plus the bibliography's underfull
  box (badness 1337) and one unchanged diff passage (badness 1237). There are no
  undefined references/citations or overfull boxes in either final build.
