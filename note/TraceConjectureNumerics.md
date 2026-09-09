# Ordered cone insertions in the two bosonic contraction semigroups

The bosonic trace inequality in Eq. (6) of *Trace Conjecture for
Sign-problem-free Semigroups* (September 9, 2026) fails in both standard
families. A single oscillator gives a negative trace with two insertions in
the first family. Two oscillators give a negative trace with four insertions
in the second family. The Gaussian evolution and all inserted generators can
be chosen strictly inside their respective cones. All traces below converge
in the ordinary Fock representation.

The calculation uses the conventions and representative matrices in
[ContractionSemigroupsQMC.tex](ContractionSemigroupsQMC.tex) and the two
standard forms in [BosonicContractionSemigroups.md](BosonicContractionSemigroups.md).
The accompanying [numerical checker](contraction_semigroups_qmc/python/verify_trace_conjecture.py)
evaluates each example through exact rational Wick contractions and an
independent Fock-space calculation. This note concerns the bosonic claim;
the strict-positivity question for fermions is separate.

## 1. A thermal evolution strictly inside the semigroup

Use Hermitian canonical coordinates with
\([x_j,p_k]=\mathrm i\delta_{jk}\), and write

\[
K=\frac12\sum_{j=1}^N(x_j^2+p_j^2)
=\sum_{j=1}^N(a_j^+a_j+\tfrac12),\qquad
\hat g_\beta=\mathrm e^{-\beta K},\qquad \beta>0.
\]

For \(\hat r=(x_1,\ldots,x_N,p_1,\ldots,p_N)^{\mathsf T}\), a quadratic
insertion has the convention

\[
\hat h=\tfrac12\hat r^{\mathsf T}H\hat r,\qquad
B=\mathrm i\Omega H,\qquad
\Omega=\begin{pmatrix}0&I_N\\-I_N&0\end{pmatrix}.
\]

The invariant cone in the damping coordinates consists of real symmetric
\(H\leq0\) satisfying \(R_1^{\mathsf T}HR_1=H\). These are the pure cone
directions, with no group component. Indeed, for \(E=\mathrm i\Omega\),
\(EB=B^\dagger E=H\). In the two cases considered here,

\[
R_1=\operatorname{diag}(1,-1)\quad(N=1),\qquad
R_1=\operatorname{diag}(J,-J),\quad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}\quad(N=2).
\]

They give \(\Theta^2=+1\) and \(\Theta^2=-1\), respectively. The second
transformation exchanges the two oscillators.

The check can also be made directly in the original Nambu basis. Let
\(Z=\operatorname{diag}(1,-1)\),
\(X=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\), and
\(Y=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)\), following
the package's real Pauli convention. The table representatives are

| Family | Case | \(J_1\) | \(J_2\) | \(\eta\) |
|---|---|---|---|---|
| \(\Theta^2=+1\) | B05 | \(I_2\) | \(X\) | \(Z\) |
| \(\Theta^2=-1\) | B13 | \(I_2\otimes Y\) | \(X\otimes I_2\) | \(Z\otimes I_2\) |

The thermal generator is \(A_g=-\beta\eta\), so \(M=\mathrm e^{A_g}\)
satisfies

\[
\eta-M^\dagger\eta M
=\operatorname{diag}(1-\mathrm e^{-2\beta},\mathrm e^{2\beta}-1)
\otimes I_N>0.
\]

Thus \(\hat g_\beta\) is a strict contraction. Its trace and normalized
covariances are

\[
Z_N=\operatorname{Tr}\hat g_\beta
=\left[\frac1{2\sinh(\beta/2)}\right]^N>0,
\qquad v=\langle x_j^2\rangle_\beta=\langle p_j^2\rangle_\beta
=\tfrac12\coth(\beta/2),
\]
\[
\langle x_jp_k\rangle_\beta=\frac{\mathrm i}{2}\delta_{jk},\qquad
\langle p_jx_k\rangle_\beta=-\frac{\mathrm i}{2}\delta_{jk}.
\]

Here brackets denote division by \(Z_N\). We choose \(\beta=\log9\), giving
\(v=5/8\), \(Z_N=(3/8)^N\), and a smallest eigenvalue \(80/81\) of
\(\eta-M^\dagger\eta M\). This evolution is well inside the strict region.

## 2. First family: a single oscillator and two insertions

Take

\[
\hat h_x=-\tfrac12(x^2+\epsilon p^2),\qquad
\hat h_p=-\tfrac12(\epsilon x^2+p^2),\qquad \epsilon\geq0.
\]

Their real coefficient matrices are
\(H_x=-\operatorname{diag}(1,\epsilon)\) and
\(H_p=-\operatorname{diag}(\epsilon,1)\). In the Nambu representation,

\[
A_x=-\frac{1+\epsilon}{2}Z-\frac{1-\epsilon}{2}Y,\qquad
A_p=-\frac{1+\epsilon}{2}Z+\frac{1-\epsilon}{2}Y.
\]

Both obey the canonical and cone identities

\[
g_{\rm B}A+A^{\mathsf T}g_{\rm B}=0,\quad
J_1^{\mathsf T}AJ_1=\overline A,\quad
J_2^{\mathsf T}AJ_2=-\overline A,\quad
\eta A=A^\dagger\eta\leq0,
\qquad g_{\rm B}=-\Omega.
\]

The eigenvalues of \(\eta A\) are \(-1,-\epsilon\); choosing
\(\epsilon>0\) makes each insertion strict.

The ordered Wick contraction gives

\[
\langle x^2p^2\rangle_\beta
=\langle x^2\rangle_\beta\langle p^2\rangle_\beta
+2\langle xp\rangle_\beta^2=v^2-\tfrac12.
\]

The negative contribution comes from the canonical commutator. Using also
\(\langle x^4\rangle=\langle p^4\rangle=3v^2\), we obtain

\[
\boxed{\frac{\operatorname{Tr}(\hat h_x\hat h_p\hat g_\beta)}{Z_1}
=\frac14\left[(1+6\epsilon+\epsilon^2)v^2
-\frac{1+\epsilon^2}{2}\right].}
\]

At \(\epsilon=0\) this is negative whenever
\(\beta>2\log(1+\sqrt2)\). At our fixed temperature, even strict insertions
with \(\epsilon=1/100\) give

\[
\frac{\operatorname{Tr}(\hat h_x\hat h_p\hat g_{\log9})}{Z_1}
=-\frac{55007}{2560000}=-0.021487109375,
\qquad
\operatorname{Tr}(\hat h_x\hat h_p\hat g_{\log9})
=-\frac{165021}{20480000}<0.
\]

This already disproves the unrestricted bosonic assertion. The two-insertion
product is nonzero, for example because its highest-degree polynomial symbol
is a nonzero product of two definite quadratic forms.

## 3. Second family: two oscillators and four insertions

To preserve the exchange of the two modes, define

\[
X_2=x_1^2+x_2^2,\qquad P_2=p_1^2+p_2^2,\qquad
\hat h_x=-\tfrac12(X_2+\epsilon P_2),\qquad
\hat h_p=-\tfrac12(\epsilon X_2+P_2).
\]

The Nambu generators are the preceding \(A_x,A_p\), tensored with \(I_2\).
They obey the B13 conditions, including invariance under \(J_1=I_2\otimes Y\).
Their cone eigenvalues are \(-1,-\epsilon\), each repeated twice.
For \(\epsilon>0\), all four generators in the ordered product
\(\hat h_x\hat h_x\hat h_p\hat h_p\) therefore belong to the strict cone.

At \(\epsilon=0\), the essential moments can be obtained from the ordered
generating function

\[
\left\langle\mathrm e^{tX_2}\mathrm e^{uP_2}\right\rangle_\beta
=\frac1{(1-2vt)(1-2vu)+tu},
\]

understood in a neighborhood of \(t=u=0\). This follows by pairing the
Gaussian coordinates using the covariances above. Differentiating twice with
respect to each source gives

\[
\langle X_2^2P_2^2\rangle_\beta=64v^4-64v^2+4,
\qquad
\frac{\operatorname{Tr}(\hat h_x^2\hat h_p^2\hat g_\beta)}{Z_2}
=4v^4-4v^2+\tfrac14.
\]

At \(\beta=\log9\), the last expression is \(-719/1024\). The exact
ordered Wick sum with the strict perturbation \(\epsilon=1/100\) gives

\[
\frac{\operatorname{Tr}(\hat h_x^2\hat h_p^2\hat g_{\log9})}{Z_2}
=-\frac{72052905719}{102400000000}
=-0.703641657412109375,
\]
\[
\operatorname{Tr}(\hat h_x^2\hat h_p^2\hat g_{\log9})
=-\frac{648476151471}{6553600000000}<0.
\]

The product is nonzero for the same polynomial-symbol reason as in the
single-mode example. Negative values therefore occur in both standard
families at even insertion order, including strict cone generators.

## 4. Independent numerical checks

The checker reuses the Pauli matrices and matrix exponential from
`verify_bosonic_quadrature.py`, and loads the B05/B13 representatives directly
from the committed classification table. It checks every canonical,
anti-linear, pure-cone, and contraction condition. The largest equality
residual in this run was below \(10^{-14}\). For the strict examples,
the largest eigenvalue of \(\eta A+A^\dagger\eta\) is \(-0.02\).

For the first trace evaluation, all Wick contractions use rational
arithmetic at \(v=5/8\). Operator order is retained. For the independent
evaluation, the code multiplies oscillator matrices directly and sums their
diagonal entries with Boltzmann weights. Independence of the two thermal
modes allows factorization of this second calculation into single-mode
matrix traces; no Wick factorization is used in this evaluation.

The occupation sum retains \(n=0,\ldots,L-1\) in each mode. Matrix
multiplication uses an additional \(2s\) states so that every possible
intermediate ladder operation is represented exactly. Increasing \(L\)
then tests the omitted Boltzmann tail without imposing an artificial
commutator at the top of the traced sector. The code checks
\(L=4,8,12,16,24,32\); at both \(L=24\) and \(32\), all four traces agree
with the exact values to an absolute tolerance of \(3\times10^{-13}\).

| Family | Modes | Insertions | \(\epsilon\) | Exact normalized trace |
|---|---:|---:|---:|---:|
| B05 | 1 | 2 | 0 | -0.02734375 |
| B05 | 1 | 2 | 0.01 | -0.021487109375 |
| B13 | 2 | 4 | 0 | -0.7021484375 |
| B13 | 2 | 4 | 0.01 | -0.703641657412109375 |

An additional seeded search samples each insertion as
\(-\tfrac12(aX_N+bP_N)\), with independent positive coefficients
\(\log_{10}a,\log_{10}b\) uniform on \([-2,0]\), at the same thermal
evolution. Seed `20260909` and 1,000 samples per family give 15 negative
two-insertion traces for B05 and 142 negative four-insertion traces for B13,
using a threshold of \(-10^{-10}\). The strongest sampled negative value
in each family is independently checked with Fock matrices. This search
covers only the stated diagonal subfamily; its frequencies are not estimates
over the entire semigroup.

## 5. Interpretation and scope

Every inserted product is a finite polynomial in creation and annihilation
operators. Multiplying it by \(\hat g_\beta\) produces a trace-class
operator: the polynomial growth of its finitely many occupation-space bands
is dominated by the exponential Boltzmann decay. Consequently the negative
values apply to any bosonic regularization that agrees with the ordinary
trace on this convergence domain. Square-root branches and poles play no
role in these examples.

Semigroup trace positivity constrains exponentials of cone generators.
Ordered polynomial insertions are mixed derivatives of such traces, whose
signs require additional structure. In particular, the negative quantum
contractions above survive even insertion order. An overall sign reversal
of every insertion, multiplication by \((-1)^s\), requiring strict
insertions, or replacing \(>0\) by \(\geq0\) leaves these counterexamples.
The separate sign of an odd number of negative cone insertions is therefore
not the only obstruction.

Wei's fermionic inequality is Eq. (11) of *Semigroup approach to the sign
problem in quantum Monte Carlo simulations*, Phys. Rev. B **110**, 075146
(2024), [arXiv:1712.09412v3](https://arxiv.org/abs/1712.09412v3),
[DOI](https://doi.org/10.1103/PhysRevB.110.075146). It concerns fermionic
quadratic operators and states nonnegativity. The bosonic counterexamples
do not contradict that result or decide its strict-positivity strengthening.

There is also a normalization issue in Eq. (5) of the conjecture document:
with the conventional hafnian, the ordered bosonic Wick expansion has no
extra factor \(1/(2n)!!\). Already for two operators, the hafnian contains
one contraction. The code uses the explicit sum over pairings and checks it
against direct operator products. A positive prefactor would not change the
negative signs found here.

## Reproduction

From native PowerShell, use the repository's Linux launcher:

```powershell
.\scripts\run-in-wsl.ps1 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 note/contraction_semigroups_qmc/python/verify_trace_conjecture.py'
```

From Linux or WSL:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 note/contraction_semigroups_qmc/python/verify_trace_conjecture.py
```

The default output is `note/contraction_semigroups_qmc/build/trace_conjecture.json`
(ignored by Git), containing the exact fractions, contraction diagnostics,
cutoff sequences, random-search parameters, and strongest sampled witnesses.
The recorded run used Linux/WSL, Python 3.12.3, and NumPy 2.3.4. The existing
quadrature checker also passed all 1,822 identities with maximum residual
\(1.332\times10^{-15}\). No manuscript source, bibliography database, or
approved classification table is changed by this calculation.
