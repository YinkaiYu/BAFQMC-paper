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
Verified the B05, B13, and F04 model slices.
All generated CSV files match the committed reference results.
Verified the B05, B13, and F04 TeX formulas against verify_model_slices.py.
Verified 64 TeX cases: 24 whole maximal subgroups, 28 Majorana proper subgroups, 8 Kramers proper subgroups, and 4 split-orthogonal proper subgroups.
```

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
10. The B05, B13, and F04 examples satisfy the canonical, anti-linear, group,
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

## Tested environment

The committed results were reproduced with:

```text
GNU Octave 10.3.0
Python 3.12.12
NumPy 2.3.4
Matplotlib 3.10.7
```

The core Octave scripts use only standard Octave functions.  The Python
enumeration requires NumPy, while Matplotlib is needed only for Fig. 1.
