# Reproducing the contraction-semigroup note

This directory contains the calculations used by
`experts/ContractionSemigroupsQMC.tex`.  A single command reconstructs the
classification, solves the generator spaces, enumerates the time-reversal
subgroups, checks the three model slices, and redraws Fig. 1.  It then compares
the results with the committed reference tables and checks the formulas
transcribed into the TeX source.

The default workflow writes only to `build/`, which is ignored by Git.  It does
not overwrite an approved CSV table or the published figure.

## Quick start

Create and activate the tested Conda environment:

```bash
conda env create -f experts/contraction_semigroups_qmc/environment.yml
conda activate bafqmc-contraction
python experts/contraction_semigroups_qmc/reproduce.py check
```

The core calculation takes about 20 seconds on a laptop.  A successful run
includes the following summaries:

```text
Verified 64 bosonic/fermionic five-relation classes.
Verified all A_group and A_cone Pauli directions for 64 representatives.
Verified the 16 generator formulas transcribed into the note.
Verified all 64 time-reversal subgroup constructions and M/K TeX case lists.
Found sign/phase-problem witnesses for 40 proper-subgroup relation classes (20 bosonic, 20 fermionic).
Verified the B05, B13, and F04 model slices.
All generated CSV files match the committed reference results.
Verified the B05, B13, and F04 TeX formulas against verify_model_slices.py.
Verified 64 TeX cases: 24 whole maximal subgroups, 28 Majorana proper subgroups, 8 Kramers proper subgroups, and 4 split-orthogonal proper subgroups.
```

`reproduce.py` pins BLAS/OpenMP subprocesses to one thread.  The matrices in
this package are small, and this cap prevents unnecessary WSL memory pressure.

If Octave is installed in another Conda environment, its launch command can be
given without changing the scripts:

```bash
OCTAVE_COMMAND='conda run -n bafqmc-octave octave' \
python experts/contraction_semigroups_qmc/reproduce.py check
```

The equivalent command-line option is
`--octave-command 'conda run -n bafqmc-octave octave'`.

## What is computed

The calculation has two independent branches.

1. The Octave branch enumerates the five binary relations, identifies the
   contraction-semigroup cases, and solves the complete Pauli-tensor generator
   spaces for a lowest-dimensional representative found with one to three
   Pauli factors.
2. The Python branch searches for physical Nambu representations of the same
   64 relation classes.  It determines whether the complete maximal subgroup
   or a proper subgroup is fixed by the Majorana, Kramers, or bosonic
   split-orthogonal time-reversal class.  The resulting table is the data source
   for Fig. 1.

These branches can choose different matrices (J_1,J_2) in the same relation
class.  The Octave representative minimizes the Pauli-tensor dimension used to
display (A_{\rm group}) and (A_{\rm cone}).  The Python representative must
also preserve the physical Hermitian-conjugation relation between the two
halves of the Nambu column and is optimized for the largest displayed
time-reversal-invariant subgroup.  The verification compares their five signs,
contraction-semigroup status, and contraction metric.  It does not require the
two representatives to be identical.

## Matrix conventions

All scripts use the real Pauli basis

```text
I = I_2,  X = sigma_x,  Y = i sigma_y,  Z = sigma_z.
```

A word denotes a tensor product from left to right.  Its first letter always
acts on the Nambu components.  Later letters act on internal components.  For
example, `XY` means

```text
sigma_x^(Nambu) tensor (i sigma_y)^(flavor).
```

A leading lowercase `i`, as in `iXY`, multiplies the complete Pauli word by the
imaginary unit.

The five signs in a class are ordered as

```text
s1, q1, s2, q2, r
```

and mean

```text
J1^T g J1 = s1 g,    J1^2 = q1 I,
J2^T g J2 = s2 g,    J2^2 = q2 I,
J1 J2 = r J2 J1.
```

The case number used in Fig. 1 is the binary order with `+` before `-`:

```text
number = 1 + 16[s1=-1] + 8[q1=-1] + 4[s2=-1]
           + 2[q2=-1] + [r=-1].
```

Thus `boson,s1+_q1+_s2+_q2+_r-` is B02.

In `generator_spaces.csv`, every term has the form `P:type`.  The four types
state the two conditions on the coefficient matrix (K_P):

| Code | Complex conjugation | Transpose |
|---|---|---|
| `R_S` | \(\overline K_P=K_P\) | \(K_P^T=K_P\) |
| `R_A` | \(\overline K_P=K_P\) | \(K_P^T=-K_P\) |
| `iR_S` | \(\overline K_P=-K_P\) | \(K_P^T=K_P\) |
| `iR_A` | \(\overline K_P=-K_P\) | \(K_P^T=-K_P\) |

## Files and their relation to the note

| File | Role in the note |
|---|---|
| `octave/enumerate_semigroup_classes.m` | Enumerates all 64 cases, proves the numerical `8+24` and `4+4` counts, constructs the metric, and checks (A_{\rm cone}=-\eta). |
| `octave/derive_generator_spaces.m` | Solves the full (A_{\rm group}) and candidate (A_{\rm cone}) Pauli directions used in Sec. V. |
| `python/enumerate_time_reversal_subgroups.py` | Produces the complete/proper subgroup and M/K/S classifications used in Sec. VI and Fig. 1. |
| `python/search_sign_problem_witnesses.py` | Uses seeded random products to find a negative fermion trace or bosonic continued branch in every relation class labelled `proper A_group subspace`. |
| `python/enumerate_abelian_hermitian_representations.py` | Optionally scans for complete fermionic generator spaces whose Fock lifts are commuting and Hermitian. |
| `python/enumerate_boson_commuting_hermitian_representations.py` | Checks the bosonic analogue together with Fock-trace convergence and analytic continuation. |
| `python/scan_boson_representation_witnesses.py` | Streams a seeded negative-branch continuation over every physical one-to-three-factor Pauli realization in the 20 bosonic proper-subgroup classes. |
| `python/verify_model_slices.py` | Checks the B05, B13, and F04 slice formulas and contraction inequalities in Sec. VII. |
| `python/verify_model_tex.py` | Cross-checks the B05, B13, and F04 equations in the note against the numerical model checker. |
| `python/verify_time_reversal_tex.py` | Parses all 64 displayed time-reversal cases and checks their matrices, algebra, class, and retained generator bases. |
| `python/plot_periodic_table.py` | Draws Fig. 1 from the time-reversal CSV. |
| `python/verify_results.py` | Independently reconstructs the algebra, cross-checks both branches, and checks the TeX transcription. |
| `octave/scan_pauli_realizations.m` | Optional full scan over every ordered (J_1,J_2) Pauli-word pair with one to three factors. |
| `reproduce.py` | Runs the complete workflow. |

The committed `reference/` directory contains the approved machine-readable
results:

| Reference table | Contents |
|---|---|
| `semigroup_classes.csv` | 32 bosonic and 32 fermionic classes, their representative matrices, metric, status, and residuals. |
| `generator_spaces.csv` | Complete generator solutions for all 64 representatives.  The note prints the 16 rows with a nonempty contraction cone. |
| `time_reversal_subgroups.csv` | Physical representatives, time-reversal class, complete/proper scope, and retained generator basis for Fig. 1. |
| `sign_problem_witnesses.csv` | Reproducible negative fermion traces and bosonic continued branches showing that the two-J relations alone do not protect each proper-subgroup relation class. |
| `abelian_hermitian_representations.csv` | Six fermionic relation classes with a sign-free complete generator space in at least one searched representation. |
| `boson_commuting_hermitian_representations.csv` | The B05/B17 structural candidates, their positive convergence half-line, and their negative pure-group meromorphic continuation. |
| `boson_representation_witnesses.csv` | One verified negative continued branch for each of the 766 searched bosonic proper-subgroup realizations. |
| `model_slice_checks.csv` | Nine deterministic checks, using three field values for each of B05, B13, and F04. |
| `pauli_realization_scan.csv` | Optional aggregate data for the 8568-realization full scan. |

## Verification performed by `check`

The verification script reconstructs the real Pauli matrices independently of
Octave and checks the core relations by exact elementwise equality.  In
particular, it checks:

1. Each statistics has all 32 distinct sign choices.
2. Exactly eight cases have a contraction cone and 24 have only a maximal
   subgroup.  Four contraction cases use (J_2g) and four use
   \(\mathrm{i}J_2g).
3. Every reported (J_1,J_2) obeys its five relations.  Every contraction
   metric is Hermitian and squares to the identity.
4. In every contraction case, (A_{\rm cone}=-\eta) obeys the canonical,
   (J_1), and (J_2) constraints and gives
   \(\eta A_{\rm cone}+A_{\rm cone}^\dagger\eta=-2I\).
5. For each generator representative, every Pauli word occurs exactly once in
   either (A_{\rm group}) or the candidate (A_{\rm cone}) space.  Its
   coefficient type and dimension formula follow from the matrix equations.
   This proves that the displayed Pauli expansion is the complete solution for
   the chosen representative, including an arbitrary additional site or
   orbital space carried by (K_P).
6. The 16 cases printed in `ContractionSemigroupGenerators.tex` have exactly the
   same (J_1,J_2,\eta), Pauli directions, conjugation conditions, and transpose
   conditions as the generated table.  Duplicate or missing TeX terms fail the
   check.
7. The Octave and Python branches agree on the representation-independent
   classification of every case.
8. Every time reversal preserves the canonical matrix and the physical Nambu
   conjugation.  The reported proper subgroup is precisely the subspace fixed
   by the added time reversal.  The retained generator spaces are Lie closed.
9. The whole-group, proper Majorana, proper Kramers, and bosonic
   split-orthogonal TeX entries agree with the generated classification case by
   case, including their displayed matrices, five-relation algebra, added time
   reversal, class, and retained generator basis.
10. Every proper-subgroup relation class has an explicit seeded random product
    in the complete maximal subgroup.  The fermionic calculation finds a
    negative finite Fock trace and checks `p_F^2 = det(I+M)`.  The bosonic
    calculation records a continuation path from a stable positive reference
    to a negative square-root branch, detouring around intervening poles, and
    checks `p_B^(-2) = (-1)^N det(I-M)`.
11. The B05, B13, and F04 examples satisfy the canonical, anti-linear, group,
    cone, and negative-definite contraction conditions.  Their TeX equations
    are checked term by term against the numerical constructions.  The model
    checker also verifies the extra symmetry at the stated special point and
    its breaking by the stated term.

The model eigenvalue inequalities and figure rendering use floating-point
linear algebra.  Their tolerances and deterministic input matrices are defined
in `verify_model_slices.py`.  The model diagnostics are rounded to twelve
decimal places only after all inequalities have been tested, which keeps the
CSV stable across compatible BLAS implementations.  These floating-point
checks do not enter the exact 64-class screening.

## Full representation scan

The optional scan tests every distinct ordered pair of real Pauli words with
one, two, or three factors:

```bash
python experts/contraction_semigroups_qmc/reproduce.py check --full
```

It covers 8568 ordered realizations.  Of these, 2184 belong to a contraction
class.  The scan verifies (A_{\rm cone}=-\eta) for all 2184 and records how the
dimensions of the allowed generator spaces depend on the representation.

This search establishes the reported lowest dimension within the explicitly
searched one-to-three-factor Pauli-tensor family.  A statement of absolute
minimality over all real orthogonal representations would additionally require
a representation-theory proof.

## Output and publication workflow

The ordinary command is read-only with respect to tracked results:

```bash
python experts/contraction_semigroups_qmc/reproduce.py check
```

It creates

```text
experts/contraction_semigroups_qmc/build/
```

and compares every generated CSV byte for byte with `reference/`.  The generated
PDF is not compared byte for byte because PDF creation timestamps depend on the
Matplotlib run.  The underlying CSV, layout code, and PNG rendering are
deterministic in the recorded environment.

When a scientifically reviewed change intentionally updates the results, first
inspect the generated differences:

```bash
diff -u experts/contraction_semigroups_qmc/reference/semigroup_classes.csv \
        experts/contraction_semigroups_qmc/build/semigroup_classes.csv
diff -u experts/contraction_semigroups_qmc/reference/generator_spaces.csv \
        experts/contraction_semigroups_qmc/build/generator_spaces.csv
```

Then publish the verified tables and Fig. 1 explicitly:

```bash
python experts/contraction_semigroups_qmc/reproduce.py publish
```

`publish` first runs every algebraic and TeX-transcription check without
accepting the old snapshots as an assumption.  It then updates `reference/*.csv`
and `figures/contraction_semigroup_periodic_table.pdf` and reruns the snapshot
comparison.  Use `publish --full` when the full-scan reference is also intended
to change.

Compile the note with

```bash
python experts/contraction_semigroups_qmc/reproduce.py note
```

or directly with

```bash
latexmk experts/ContractionSemigroupsQMC.tex
```

## Evidence boundary for the cone

`generator_spaces.csv` lists the complete linear space satisfying the equality
constraints for a candidate (A_{\rm cone}).  A physical cone generator must
also satisfy the matrix inequality

```text
eta A_cone + A_cone^dagger eta < 0.
```

The scripts prove that this region is nonempty by checking the universal point
(A_{\rm cone}=-\eta).  They do not reduce the full negative-definite matrix
inequality to separate scalar bounds for an arbitrary simultaneous choice of
all coefficient matrices.  The note therefore prints the complete matrix
inequality for each class.

## Evidence boundary for proper subgroups

The `proper A_group subspace` label originally established only that an added
time reversal protects the displayed nonzero proper subspace.  By itself, that
calculation did **not** show that the complete maximal subgroup allowed by the
two original matrices `(J1,J2)` contains a sign problem.  The separate witness
search answers only the one-sided existence question.  For every five-relation
class it constructs at least one realization with a negative fermion trace or
a negative bosonic continued branch.  This disproves positivity derived from
the five signs alone, while leaving every other representation in that class
as a separate question.

For all 20 bosonic proper-subgroup cases and 16 of the 20 fermionic cases, the
committed witness lies in the exact physical representation displayed in the
time-reversal table.  For F01, F06, F18, and F21, the fixed search did not find
a witness in the minimal displayed representative.  The witness search alone
therefore leaves those four representations unresolved.  The recorded witness
instead appends a two-dimensional spectator factor,
`J1 -> J1 tensor I2` and `J2 -> J2 tensor I2`.  This preserves all five signs
and gives a negative weight in the enlarged representation.  Thus the
witnesses rule out a universal positivity conclusion based only on the five
`(J1,J2)` relations; they do not claim that every representation in the same
relation class has a sign problem.  In particular, failure to find a witness
is never treated as evidence of positivity.  Proving positivity for even one
specific representation would instead indicate an additional sign-free
mechanism worth analyzing on its own.

The separate Abelian-Hermitian calculation resolves the four displayed
representations just mentioned.  All four are sign free on their complete
generator spaces.  The same scan finds lower-dimensional sign-free
representations of F05 and F17.  These existence results leave the one-sided
witness claim unchanged and are summarized in Appendix A of
`experts/ContractionSemigroupsQMC.tex`.

The search is deterministic for the committed seed and records the full basis,
slice coefficients, representation, weight, determinant identity residual,
and bosonic continuation winding in `sign_problem_witnesses.csv`.  It is
constructive numerical evidence rather than a proof of minimal slice count or
coefficient magnitude.  For F02, the witness uses the displayed four-component
representation itself: four slices give
`p_F = -1.51748371663e6`, while `det(I+M) = 2.30275683024e12` and the relative
square-identity residual is `6.303e-12`.

## Representation-specific positivity scan

For a fermionic representation, let `H_j` be the Fock lifts of a complete real
basis of `A_group`.  Pairwise commuting Hermitian `H_j` make all time slices
commute and give

```text
p_F = Tr exp(sum_l h_l) > 0.
```

The optional script exhausts physical real-Pauli pairs with one to three
tensor factors, including pairs with `J1 == J2`.  It finds this mechanism in
exactly six relation classes within that family:

```text
F01, F05, F06, F17, F18, F21.
```

The script also reconstructs the complete ambient real-linear space of
Nambu-adjoint, group-invariant antiunitary matrices.  Every matrix in that
space is symmetric for the six reported representations.  The canonical
physical members are therefore unitary and square to `+I`, which excludes a
hidden Majorana or Kramers pair as the source of positivity.

Run the optional scan and compare its output with the reviewed snapshot using

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python experts/contraction_semigroups_qmc/python/enumerate_abelian_hermitian_representations.py

diff -u \
  experts/contraction_semigroups_qmc/reference/abelian_hermitian_representations.csv \
  experts/contraction_semigroups_qmc/build/abelian_hermitian_representations.csv
```

This optional scan is separate from the default note-reproduction workflow.
It records an additional representation-specific sufficient mechanism and
does not alter the classification in `ContractionSemigroupsQMC.tex`.

The corresponding bosonic scan is

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python experts/contraction_semigroups_qmc/python/enumerate_boson_commuting_hermitian_representations.py

diff -u \
  experts/contraction_semigroups_qmc/reference/boson_commuting_hermitian_representations.csv \
  experts/contraction_semigroups_qmc/build/boson_commuting_hermitian_representations.csv
```

Only B05 and B17 pass the commuting-Hermitian structural test.  Their ordinary
Fock trace is positive for `alpha < 0`.  The meromorphic continuation along the
same pure one-parameter group is negative for `alpha > 0`, where the
occupation-number trace diverges.  This is the known one-mode bosonic
`{+,+}` counterexample.  A contraction-cone path fixes a different stable
branch, so the pure-group continuation does not signal a negative convergent
configuration inside that semigroup.  The commuting-Hermitian condition alone
does not fix a positive full group character.  No bosonic relation class in the
searched family realizes the full fermionic mechanism.

A stronger seeded stress test examines every ordered physical Pauli realization
in the 20 bosonic proper-subgroup classes through three factors.  Along the
recorded interpolation from a number-damping reference, it finds a negative
continued branch for all 766 realizations: 4 with one factor, 50 with two
factors, and 712 with three factors.  These counts are not quotiented by unitary
equivalence.  Each record contains the complete generator basis, slice
coefficients, stable reference, branch winding, opposite-detour check,
determinant identity residual, and path clearance.  Run this optional scan
under an explicit WSL memory cap with

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  prlimit --as=2147483648 -- \
  python experts/contraction_semigroups_qmc/python/scan_boson_representation_witnesses.py

diff -u \
  experts/contraction_semigroups_qmc/reference/boson_representation_witnesses.csv \
  experts/contraction_semigroups_qmc/build/boson_representation_witnesses.csv
```

The implementation writes one row at a time and keeps no collection of path
samples in memory.  The reviewed run used about 57 MiB peak RSS and produced
a 0.84 MB CSV.  The witnesses are constructive numerical evidence within the
finite Pauli family.  They do not classify arbitrary-dimensional bosonic
representations or exclude a different positivity mechanism.

## Tested environment

The committed results were reproduced with:

```text
GNU Octave 10.3.0
Python 3.12.12
NumPy 2.3.4
SciPy 1.18.0
Matplotlib 3.10.7
```

The core Octave scripts use only standard Octave functions.  The Python
enumeration requires NumPy, while Matplotlib is needed only for Fig. 1.
