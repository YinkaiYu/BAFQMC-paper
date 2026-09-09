# Cone insertions can have negative bosonic traces

The trace of a Gaussian evolution can be positive for every element of a
contraction semigroup while an ordered correlation function with insertions from
its invariant cone is negative. A single bosonic oscillator in the B05 class of
[ContractionSemigroupsQMC.tex](ContractionSemigroupsQMC.tex) gives an explicit
example. Both the Gaussian trace and the inserted trace converge in the ordinary
Fock representation, so the example also applies to any regularization that
agrees with the trace on trace-class operators.

In particular, the conditions

\[
\hat h_1\cdots\hat h_s\ne0,\qquad
\hat h_j\text{ in the invariant cone},\qquad
\hat g\text{ a strict contraction}
\]

do not imply \(\operatorname{Tr}(\hat h_1\cdots\hat h_s\hat g)>0\).
The failure persists for two insertions that are both in the interior of the
cone. This disproves Eq. (6) of *Trace Conjecture for Sign-problem-free
Semigroups*, dated September 9, 2026, for its stated bosonic scope.

## 1. The oscillator and its invariant cone

Set \(\hbar=1\) and take

\[
[\hat a,\hat a^+]=1,\qquad
\hat x=\frac{\hat a+\hat a^+}{\sqrt2},\qquad
\hat p=\frac{\hat a-\hat a^+}{\mathrm i\sqrt2},\qquad
[\hat x,\hat p]=\mathrm i.
\]

Here \(\hat a^+\) is the physical adjoint of \(\hat a\), and \(\hat x,\hat p\)
are Hermitian. Define the oscillator Hamiltonian

\[
\hat K=\frac{\hat x^2+\hat p^2}{2}
=\hat a^+\hat a+\frac12,
\qquad
\hat g_\beta=\mathrm e^{-\beta\hat K},\qquad \beta>0.
\tag{1}
\]

To check membership directly in the original Nambu convention, write

\[
\hat\chi=\binom{\hat a}{\hat a^+},\qquad
g_{\rm B}=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
\hat h(A)=\frac12\hat\chi^{\mathsf T}g_{\rm B}A\hat\chi.
\tag{2}
\]

The B05 representative has

\[
J_1=I_2,\qquad
J_2=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
\eta=J_2g_{\rm B}=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\tag{3}
\]

Its invariant cone consists of the matrices satisfying

\[
g_{\rm B}A+A^{\mathsf T}g_{\rm B}=0,\qquad
\overline A=A,\qquad
J_2^{\mathsf T}AJ_2=-A,\qquad
\eta A\leq0.
\tag{4}
\]

The last matrix is Hermitian; strict negativity places a generator in the
interior of the cone. These are precisely the cone conditions in the Nambu
note, rather than just the weaker condition for a general semigroup generator.

Consider the two insertions

\[
\hat h_x=-\hat x^2,\qquad \hat h_p=-\hat p^2.
\tag{5}
\]

Their Nambu matrices are

\[
A_x=\begin{pmatrix}-1&-1\\1&1\end{pmatrix},\qquad
A_p=\begin{pmatrix}-1&1\\-1&1\end{pmatrix}.
\tag{6}
\]

Substitution into (2) gives (5), including the scalar terms required by the
canonical commutator. Both matrices obey the first three relations in (4), and

\[
\eta A_x=-\binom{1}{1}\begin{pmatrix}1&1\end{pmatrix}\leq0,
\qquad
\eta A_p=-\binom{1}{-1}\begin{pmatrix}1&-1\end{pmatrix}\leq0.
\tag{7}
\]

Thus both insertions belong to the invariant cone. Equivalently, in the first
standard form of
[BosonicContractionSemigroups.md](BosonicContractionSemigroups.md), their
quadrature coefficient matrices are \(H_x=\operatorname{diag}(-2,0)\) and
\(H_p=\operatorname{diag}(0,-2)\). They have the required time reversal
\(\Theta(\hat x)=\hat x\), \(\Theta(\hat p)=-\hat p\), and negative
semidefinite real coefficients. No complex canonical change is used here.

The generator of \(\hat g_\beta\) is

\[
A_\beta=\frac\beta2(A_x+A_p)=-\beta\eta,
\qquad \eta A_\beta=-\beta I_2<0.
\]

Consequently its propagation matrix satisfies

\[
M_\beta=\mathrm e^{A_\beta}
=\operatorname{diag}(\mathrm e^{-\beta},\mathrm e^\beta),\qquad
M_\beta^\dagger\eta M_\beta-\eta
=\begin{pmatrix}
\mathrm e^{-2\beta}-1&0\\
0&1-\mathrm e^{2\beta}
\end{pmatrix}<0.
\tag{8}
\]

This verifies the strict contraction condition explicitly for every
\(\beta>0\). The Fock-space lift is fixed by the positive thermal operator in
(1). Its trace is

\[
Z_\beta=\operatorname{Tr}\hat g_\beta
=\frac{\mathrm e^{-\beta/2}}{1-\mathrm e^{-\beta}}
=\frac1{2\sinh(\beta/2)}>0.
\tag{9}
\]

## 2. Exact evaluation of the inserted trace

The sign can be computed directly from oscillator number states, without a
Pfaffian or hafnian convention. Let \(\hat n=\hat a^+\hat a\),
\(D=2\hat n+1\), and \(S=\hat a^2+(\hat a^+)^2\). Then

\[
\hat x^2=\frac{D+S}{2},\qquad
\hat p^2=\frac{D-S}{2}.
\]

The terms \(SD\) and \(DS\) change occupation by two and have zero diagonal
matrix element. Only \(\hat a^2(\hat a^+)^2\) and
\((\hat a^+)^2\hat a^2\) contribute to the diagonal of \(S^2\). Therefore

\[
\begin{aligned}
\langle n|\hat x^2\hat p^2|n\rangle
&=\frac14\bigl[(2n+1)^2-(n+1)(n+2)-n(n-1)\bigr]\\
&=\frac12n(n+1)-\frac14.
\end{aligned}
\tag{10}
\]

In particular, the product of insertions is nonzero, since its vacuum matrix
element is \(-1/4\).

Put \(q=\mathrm e^{-\beta}\in(0,1)\). The elementary sums

\[
\sum_{n=0}^\infty q^n=\frac1{1-q},\qquad
\sum_{n=0}^\infty n(n+1)q^n=\frac{2q}{(1-q)^3}
\]

give the exact result

\[
\begin{aligned}
\operatorname{Tr}(\hat h_x\hat h_p\hat g_\beta)
&=\sqrt q\sum_{n=0}^\infty q^n
\left[\frac12n(n+1)-\frac14\right]\\
&=Z_\beta\left[\frac{q}{(1-q)^2}-\frac14\right]\\
&=Z_\beta\left[\frac14\coth^2\frac\beta2-\frac12\right].
\end{aligned}
\tag{11}
\]

All these sums converge absolutely. More strongly, every polynomial \(P\) of
degree at most four in \(\hat a,\hat a^+\) obeys
\(\|P|n\rangle\|\leq C(n+1)^2\). The rank-one expansion

\[
P\hat g_\beta=\sum_{n=0}^\infty
\mathrm e^{-\beta(n+1/2)}P|n\rangle\langle n|
\]

converges in trace norm because the sum of the rank-one trace norms is bounded
by \(C\sum_n(n+1)^2\mathrm e^{-\beta(n+1/2)}<\infty\).
Thus the inserted operator really is trace class, not merely an operator with
a formally summable diagonal.

Equation (11) is negative exactly when

\[
q<3-2\sqrt2,
\qquad\text{or equivalently}\qquad
\beta>2\log(1+\sqrt2).
\tag{12}
\]

For a rational-valued example, choose \(\beta=\log9\). Then

\[
q=\frac19,\qquad Z_\beta=\frac38,\qquad
\boxed{\operatorname{Tr}(\hat h_x\hat h_p\hat g_{\log9})
=-\frac{21}{512}<0.}
\tag{13}
\]

At the finite temperature \(\beta=2\log(1+\sqrt2)\), the same nonzero
insertion product instead has trace zero, while \(\hat g_\beta\) is still a
strict contraction. At higher temperature its trace is positive. Hence strict
contraction does not fix the sign of this correlation function.

## 3. The insertions can also be strict cone elements

The negative result is stable under a perturbation into the cone interior.
For \(\epsilon>0\), take

\[
\hat h_{1,\epsilon}=-(\hat x^2+\epsilon\hat p^2),\qquad
\hat h_{2,\epsilon}=-(\hat p^2+\epsilon\hat x^2).
\tag{14}
\]

Their matrices are \(A_x+\epsilon A_p\) and
\(A_p+\epsilon A_x\). Both \(\eta A\) matrices have eigenvalues
\(-2\) and \(-2\epsilon\), so both insertions lie strictly inside the
invariant cone. Their quadratic operators are also strictly negative in the
usual Hilbert-space sense.

Let \(v=\tfrac12\coth(\beta/2)\). Summing number-state diagonals gives
\(\langle\hat x^4\rangle_\beta=\langle\hat p^4\rangle_\beta=3v^2\);
the diagonal for either fourth power is
\(\tfrac34(2n^2+2n+1)\). Equation (10) and its adjoint give
\(\langle\hat x^2\hat p^2\rangle_\beta
=\langle\hat p^2\hat x^2\rangle_\beta=v^2-\tfrac12\).
Expansion of the ordered product in (14) therefore yields

\[
\frac{\operatorname{Tr}(\hat h_{1,\epsilon}\hat h_{2,\epsilon}
\hat g_\beta)}{Z_\beta}
=(1+\epsilon^2)\left(v^2-\frac12\right)+6\epsilon v^2.
\tag{15}
\]

At \(\beta=\log9\), this is

\[
\frac{-7+150\epsilon-7\epsilon^2}{64}.
\]

Taking \(\epsilon=1/32\) gives a counterexample with strict insertions,

\[
\boxed{\operatorname{Tr}
(\hat h_{1,1/32}\hat h_{2,1/32}\hat g_{\log9})
=-\frac{7125}{524288}<0.}
\tag{16}
\]

The insertion product is nonzero: its vacuum expectation is
\((-1+6\epsilon-\epsilon^2)/4=-833/4096\) at this value of
\(\epsilon\). The trace-class argument following (11) applies unchanged.

## 4. Consequences for a trace-positivity theorem

With the convention \(\mathrm e^{\hat h}\) and the contraction inequality
\(\eta A\leq0\), even a single insertion already contradicts the proposed
positive sign. The strict cone element \(\hat h=-\hat K\) gives

\[
\operatorname{Tr}(-\hat K\mathrm e^{-\beta\hat K})
=\frac{\mathrm dZ_\beta}{\mathrm d\beta}
=-\frac{\cosh(\beta/2)}{4\sinh^2(\beta/2)}<0.
\tag{17}
\]

The two-insertion example proves more: changing the overall sign convention
for every insertion, inserting a factor \((-1)^s\), restricting to even
\(s\), replacing strict positivity by nonnegativity, or requiring each
insertion to be a strict cone element does not repair the universal claim.

The physical obstruction is the ordering of noncommuting observables. At low
temperature the trace is dominated by
\(\langle0|\hat x^2\hat p^2|0\rangle=-1/4\). Although each factor
\(\hat x^2\) and \(\hat p^2\) is a positive operator, their ordered product
has no positivity property that would force its expectation in the oscillator
thermal state to be nonnegative. The same negative expectation occurs for the
symmetrized product \(\tfrac12\{\hat x^2,\hat p^2\}\), since the two
orders have equal thermal traces.

Semigroup trace positivity only states that
\(\operatorname{Tr}(\mathrm e^{t_1\hat h_1}
\mathrm e^{t_2\hat h_2}\hat g)>0\) in its finite-trace domain for
\(t_1,t_2\geq0\). It places no general sign restriction on the mixed
derivative at \(t_1=t_2=0\), which is the inserted trace.

The fermionic inequality in Zhong-Chao Wei,
*Semigroup approach to the sign problem in quantum Monte Carlo simulations*,
Phys. Rev. B **110**, 075146 (2024),
[DOI: 10.1103/PhysRevB.110.075146](https://doi.org/10.1103/PhysRevB.110.075146),
[arXiv:1712.09412v3](https://arxiv.org/abs/1712.09412v3), concerns a different
operator algebra. Equation (11) of the local
[PDF](../local_reference_pdfs/manuscript/wei2024prb.pdf) states a nonnegative
fermionic trace; Appendix C uses fermionic Wick contractions and Kramers
structure. The oscillator counterexample is compatible with that fermionic
result and rules out its proposed unrestricted bosonic extension. The separate
fermionic strict-positivity theorem and several sufficient bosonic restrictions
are proved in [TraceConjecturePositiveResults.md](TraceConjecturePositiveResults.md).

## Verification

The companion
[verification script](trace_conjecture/verify_counterexample.py) checks the
cone identities with exact rational arithmetic, evaluates the exact trace
sums, verifies the strict perturbation, and independently evaluates the
insertions in a finite oscillator basis with unused states above the traced
sector. The latter avoids altering the intermediate ladder operations at the
occupation cutoff. Exact identities and the convergent sums above constitute
the proof; the finite-basis calculation is a cross-check.

From Linux or WSL, run

```bash
python3 note/trace_conjecture/verify_counterexample.py
```

From native PowerShell, run

```powershell
.\scripts\run-in-wsl.ps1 'python3 note/trace_conjecture/verify_counterexample.py'
```
