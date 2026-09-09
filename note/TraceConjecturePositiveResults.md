# Strict fermionic trace positivity and restricted bosonic versions

Cone-insertion traces distinguish fermionic and bosonic Gaussian semigroups.
For finitely many fermion modes, Wei's nonnegative trace inequality strengthens
to strict positivity at every interior semigroup element whenever the insertion
product is nonzero. For bosons, the
[oscillator counterexample](TraceConjectureCounterexample.md) rules out this
general statement. Two useful bosonic versions remain: a common-position
insertion theorem for the first standard semigroup, and a positive-operator
theorem applicable in the physical realizations of both standard families.

All cones below use the convention that the Gaussian factor is
\(\mathrm e^{\hat h}\), with contraction generators satisfying
\(\eta A+A^\dagger\eta\leq0\). In the standard physical bosonic realization,
pure cone quadratics are negative operators. This sign matters for odd numbers
of bosonic insertions.

## 1. Fermions: strict positivity follows from Wei's inequality

Let \(S\) be either of Wei's two fermionic contraction semigroups, acting on
the full Fock space of finitely many modes, and let \(C\) denote its invariant
cone of quadratic operators. The same result then applies to the equivalent
Nambu classes. Let

\[
P=\hat h_1\cdots\hat h_s,\qquad \hat h_j\in C,\qquad s\geq1.
\]

**Theorem.** If \(P\ne0\) and \(\hat g_0\in\operatorname{int}S\), then

\[
\boxed{\operatorname{Tr}(P\hat g_0)>0.}
\tag{1}
\]

The interior is relative to the symmetry-constrained Gaussian Lie group, with
the Fock-space lift fixed by the semigroup. Thus it is the strict-contraction
interior in the question. No invertibility or interior assumption is imposed
on the individual insertions.

The input from the literature is

\[
\operatorname{Tr}(\hat c_1\cdots\hat c_m\hat g)\geq0,
\qquad \hat c_j\in C,\quad\hat g\in S,
\tag{2}
\]

for every positive integer \(m\). This is Eq. (11) of Zhong-Chao Wei,
*Semigroup approach to the sign problem in quantum Monte Carlo simulations*,
Phys. Rev. B **110**, 075146 (2024),
[DOI](https://doi.org/10.1103/PhysRevB.110.075146),
[arXiv:1712.09412v3](https://arxiv.org/abs/1712.09412v3).
The [local PDF](../local_reference_pdfs/manuscript/wei2024prb.pdf) discusses
Majorana reflection positivity for one standard class and proves the other
case using Kramers structure in Appendix C. The following argument supplies
the strictness step in (1).

### A zero at an interior point forces every further cone insertion to vanish

Suppose, toward a contradiction, that \(\operatorname{Tr}(P\hat g_0)=0\).
For any \(\hat c\in C\), the curve
\(\mathrm e^{t\hat c}\hat g_0\) lies in \(S\) for all sufficiently small
positive and negative real \(t\), because \(\hat g_0\) is an interior point.
Equation (2) implies that

\[
f(t)=\operatorname{Tr}(P\mathrm e^{t\hat c}\hat g_0)\geq0,
\qquad f(0)=0.
\]

All operators here are finite matrices, so differentiation is ordinary matrix
differentiation. The minimum at zero gives

\[
f'(0)=\operatorname{Tr}(P\hat c\hat g_0)=0.
\tag{3}
\]

Now apply the same argument with \(P\hat c\) in place of \(P\). It is still
a product of cone elements, so (2) remains available. Induction gives

\[
\operatorname{Tr}(P\hat c_1\cdots\hat c_k\hat g_0)=0
\quad\text{for every } k\geq0\text{ and every }\hat c_j\in C.
\tag{4}
\]

Let \(\mathcal A_C\) be the complex linear span of the identity and all
finite products of cone elements. It is an associative algebra, and (4)
implies

\[
\operatorname{Tr}(P Q\hat g_0)=0
\qquad(Q\in\mathcal A_C).
\tag{5}
\]

To finish, we identify enough of this algebra to test (5) against
\(P^\dagger\hat g_0^{-1}\). The two standard classes require slightly
different checks. The dagger in this argument may be taken in the standard
finite-dimensional CAR representation after the canonical reduction.

### The Majorana reflection class

Use Hermitian Majoranas \(\gamma_1,\ldots,\gamma_N\) and
\(\widetilde\gamma_1,\ldots,\widetilde\gamma_N\), with anticommutators
equal to twice the identity matrix. In the standard representative
\(J_1=\sigma_x\otimes I_N\), \(J_2=\mathrm i\sigma_y\otimes I_N\),
the invariant cone has the form

\[
\hat c(C)=-\frac{\mathrm i}{2}
\sum_{i,j}\gamma_i C_{ij}\widetilde\gamma_j,
\qquad C=C^\dagger\geq0.
\tag{6}
\]

Positive semidefinite Hermitian matrices span all Hermitian matrices over
the reals and hence all matrices over the complex numbers. Consequently
\(\mathcal A_C\) contains every \(\gamma_i\widetilde\gamma_j\). It also
contains the same-half bilinears, because for distinct indices

\[
\begin{aligned}
[\gamma_i\widetilde\gamma_j,\gamma_k\widetilde\gamma_j]
&=-2\gamma_i\gamma_k,\\
[\gamma_i\widetilde\gamma_j,\gamma_i\widetilde\gamma_l]
&=-2\widetilde\gamma_j\widetilde\gamma_l.
\end{aligned}
\tag{7}
\]

All even Majorana monomials are products of bilinears. Thus
\(\mathcal A_C\) is the full even Clifford algebra, including the
one-mode case where the single cross bilinear already generates it.
Both \(P^\dagger\) and \(\hat g_0^{-1}\) belong to this algebra: Gaussian
operators and their inverses preserve parity and are exponentials of even
quadratics. Finite-dimensionality keeps those exponentials in the same
algebra. Choosing \(Q=P^\dagger\hat g_0^{-1}\) in (5) gives

\[
0=\operatorname{Tr}(P P^\dagger),
\]

which contradicts \(P\ne0\).

### The Kramers class, including the two-mode exception

Let there be \(N=2m\) complex fermion modes, collected in \(a\), and set

\[
K=\begin{pmatrix}0&I_m\\-I_m&0\end{pmatrix}.
\]

The standard cone can be written, up to a common positive normalization, as

\[
\hat c(R,S)=a^{\mathsf T}RK a
-(a^+)^{\mathsf T}SK a^+,
\quad R,S\geq0,
\quad R=R^\dagger,\quad S=S^\dagger,
\quad K^{\mathsf T}RK=\overline R,
\quad K^{\mathsf T}SK=\overline S.
\tag{8}
\]

The creation and annihilation coefficients are independent. The real vector
space of the allowed Hermitian matrices is spanned by its positive cone,
since adding a sufficiently large multiple of the identity makes any of them
positive. The map \(R\mapsto W=RK\) identifies this space with the real
subspace of complex skew matrices satisfying
\(K^{\mathsf T}WK=\overline W\). This is a real form of all complex skew
matrices: the antilinear map
\(W\mapsto K^{\mathsf T}\overline W K\) is an involution, and any skew
matrix is the sum of a fixed matrix and \(\mathrm i\) times a fixed matrix.
Therefore the complex span of (8) contains every
\(a_i a_j\) and every \(a_i^+a_j^+\), \(i\ne j\).

For \(N\geq4\), these pair operators generate all number-conserving
quadratics as well. For distinct \(i,j,k\), CAR gives

\[
[a_i^+a_k^+,a_k a_j]=a_i^+a_j,
\qquad
[a_i^+a_j^+,a_j a_i]=n_i+n_j-1.
\tag{9}
\]

Taking linear combinations of three of the second identities isolates
\(n_i-1/2\). These operators, together with the pair operators, generate
the full even Clifford algebra. The same choice
\(Q=P^\dagger\hat g_0^{-1}\) in (5) again proves \(P=0\), a
contradiction.

For \(N=2\), the cone operators annihilate the odd sector
\(\operatorname{span}\{|10\rangle,|01\rangle\}\). On the even sector
\(\operatorname{span}\{|00\rangle,|11\rangle\}\), pair creation and
annihilation are the two off-diagonal matrix units, up to nonzero constants.
Their products give the two diagonal matrix units. Hence \(\mathcal A_C\)
contains every matrix on the even sector with zero odd block. Since
\(s\geq1\), \(P\) also has zero odd block. Gaussian operators preserve
parity and are invertible on both blocks. Choose \(Q\) to have even block
\(P_{\rm e}^\dagger(\hat g_0)_{\rm e}^{-1}\) and zero odd block.
Equation (5) gives
\(\operatorname{Tr}(P_{\rm e}P_{\rm e}^\dagger)=0\), which contradicts
\(P\ne0\). This completes the proof of (1).

Finite-dimensional canonical changes act by algebra isomorphisms implemented
by similarities of the CAR representation. They preserve traces, nonzero
products, and the interior under the stated semigroup equivalences. Thus the
two standard-form proofs cover the corresponding fermionic Nambu classes.

## 2. Bosons: mutual commutativity alone is insufficient

The one-oscillator example with \(-x^2\) and \(-p^2\) has a positive thermal
\(\hat g\), but noncommuting insertions. Conversely, commuting insertions
can fail when the Gaussian evolution is non-Hermitian. This distinction
determines which extra conditions suffice.

Let \(\hat K=(x^2+p^2)/2\), take two identical strict cone insertions
\(\hat h_1=\hat h_2=-\hat K\), and set

\[
\hat D_t=\exp\!\left[\frac t2\bigl((a^+)^2-a^2\bigr)\right],
\qquad \hat g=\hat D_t\mathrm e^{-\beta\hat K},
\qquad\beta>0.
\tag{10}
\]

In B05, \(D_t=\mathrm e^{t\sigma_x}\) is a maximal-subgroup element and
\(\mathrm e^{-\beta\hat K}\) is a strict contraction. Thus their product
is a strict contraction. The operator \(\hat D_t\) is unitary, while
\(\hat g\) is generally non-Hermitian. Its convergent trace, with the
positive thermal branch, is

\[
Z(t,\beta)=\frac1{\sqrt{2(\cosh t\cosh\beta-1)}}.
\tag{11}
\]

Writing \(c=\cosh t\) and \(u=\cosh\beta\), differentiation gives

\[
\operatorname{Tr}(\hat K^2\hat g)
=\partial_\beta^2 Z(t,\beta)
=\frac{c^2u^2+2cu-3c^2}{[2(cu-1)]^{5/2}}.
\tag{12}
\]

For \(c=2\) and \(\beta=\log2\), so that \(u=5/4\),

\[
\boxed{\operatorname{Tr}(\hat h_1\hat h_2\hat g)
=-\frac1{12\sqrt3}<0.}
\tag{13}
\]

The insertions are identical, mutually commuting, and strictly inside the
cone. Thus none of those requirements alone controls traces against a general
non-Hermitian semigroup element.

## 3. A bosonic theorem retaining arbitrary strict evolution in the first family

Use the usual Schrödinger representation on \(L^2(\mathbb R^N)\), with
Hermitian \(x,p\). Consider the first standard family in
[BosonicContractionSemigroups.md](BosonicContractionSemigroups.md), whose
generators have the form

\[
\hat h=-\frac12x^{\mathsf T}A x-\frac12p^{\mathsf T}D p
+\frac{\mathrm i}{2}
\bigl(x^{\mathsf T}B p+p^{\mathsf T}B^{\mathsf T}x\bigr),
\quad A=A^{\mathsf T}\geq0,\quad D=D^{\mathsf T}\geq0,
\quad B\text{ real}.
\tag{14}
\]

Here all factors use the same physical coordinates. Let \(S_+\) be this
Gaussian contraction semigroup in its usual bounded-operator realization.

**Theorem.** Let \(\hat g\in\operatorname{int}S_+\), and choose nonzero
real positive semidefinite matrices \(V_j\). For the cone insertions

\[
\hat h_j=-\frac12x^{\mathsf T}V_jx,\qquad j=1,\ldots,s,
\]

one has

\[
\boxed{(-1)^s\operatorname{Tr}(\hat h_1\cdots\hat h_s\hat g)>0.}
\tag{15}
\]

In particular, an even number of these insertions satisfies the original
strictly positive inequality. The evolution may contain arbitrary allowed
momentum and mixed terms in (14); it need not be Hermitian and need not commute
with the insertions. The restriction is on the common position dependence of
the insertions. These are sufficient conditions, without a claim of minimality.

### Positivity in the position representation

Putting \(p=-\mathrm i\nabla\) in (14) gives

\[
\hat h=\frac12\nabla^{\mathsf T}D\nabla
+(B^{\mathsf T}x)\mathbin{\cdot}\nabla
-\frac12x^{\mathsf T}A x+\frac12\operatorname{tr}B.
\tag{16}
\]

Each Gaussian factor preserves pointwise nonnegative functions. This follows
either from the Feynman--Kac formula for the linear drift, constant diffusion,
and real killing potential in (16), or from the strong Trotter product of
three positivity-preserving factors: multiplication by a positive Gaussian,
convolution with a nonnegative Gaussian measure, and the real dilation
\(f(x)\mapsto \mathrm e^{t\operatorname{tr}B/2}f(\mathrm e^{tB^{\mathsf T}}x)\).
The zero eigenvalues of \(D\) simply give a degenerate Gaussian measure.
Products and their strong limits retain this property. Thus every element of
\(S_+\) preserves nonnegative functions. This statement is about pointwise
positivity, not Hilbert-space positive definiteness of the operator.

### Strict contraction gives a strictly positive diagonal kernel

Let \(\hat K_0=\tfrac12(x^{\mathsf T}x+p^{\mathsf T}p)\) and
\(E_\epsilon=\mathrm e^{-\epsilon\hat K_0}\). The interior condition and
continuity of multiplication in the ambient Gaussian group imply that, for
some sufficiently small \(\epsilon>0\),

\[
\hat g=E_\epsilon\hat g' E_\epsilon,
\qquad \hat g'\in S_+.
\tag{17}
\]

Indeed, the matrix of \(\hat g'\) is obtained by multiplying the matrix of
\(\hat g\) on both sides by the inverse matrix of \(E_\epsilon\). It
approaches the original strict element as \(\epsilon\downarrow0\), so it
stays in the same interior component for sufficiently small \(\epsilon\).
The lift is chosen continuously, which fixes the operator identity in (17).
This use of the inverse takes place in the ambient Gaussian group; the
resulting \(\hat g'\), rather than either inverse heat factor by itself,
belongs to the bounded semigroup.

The heat operator has the Mehler kernel

\[
k_\epsilon(x,y)=\frac1{(2\pi\sinh\epsilon)^{N/2}}
\exp\!\left[-\frac{
(|x|^2+|y|^2)\cosh\epsilon-2x\cdot y}
{2\sinh\epsilon}\right]>0.
\tag{18}
\]

For fixed \(x\), put \(f_x(y)=k_\epsilon(y,x)\). It is a strictly positive
\(L^2\) function. Equations (17)--(18) give the continuous kernel

\[
g(x,y)=\langle f_x,\hat g' f_y\rangle,
\qquad g(x,x)>0.
\tag{19}
\]

To see strictness, \(\hat g' f_x\) is nonnegative by the preceding step and
cannot vanish identically. If a nonzero bounded positivity-preserving
operator \(T\) annihilated a function \(f>0\) almost everywhere, the
inequality \(|Tu|\leq T|u|\leq cTf=0\) would make it vanish on all
functions with \(|u|\leq cf\). Those functions form a dense subspace of
\(L^2\), forcing \(T=0\). Apply this observation to \(T=\hat g'\), which
is nonzero. Pairing \(\hat g' f_x\) with the everywhere positive \(f_x\)
then proves (19).

Finally define the nonnegative polynomial

\[
Q(x)=\prod_{j=1}^s\frac12x^{\mathsf T}V_jx.
\]

It is positive off a set of Lebesgue measure zero, since each \(V_j\) is
positive semidefinite and nonzero. The heat factors in (17) ensure all
polynomial moments are finite. More explicitly,
\(\int Q(x)\|f_x\|^2\,dx<\infty\) by (18), so boundedness of
\(\hat g'\) controls the absolute value of the corresponding integral in
(19). The usual Hilbert--Schmidt kernel product formula therefore gives

\[
(-1)^s\operatorname{Tr}(\hat h_1\cdots\hat h_s\hat g)
=\int_{\mathbb R^N}Q(x)g(x,x)\,dx>0.
\tag{20}
\]

It also justifies this as an ordinary convergent trace. This proves (15).
The proof uses the physical first standard form; it does not assume that a
complex canonical change preserves pointwise kernel positivity, and it does
not extend this kernel argument to the second standard family.

## 4. A bosonic version for both physical standard families

An alternative keeps noncommuting cone insertions and restricts the evolution
and ordering. Work in either physical standard form, so the pure cone
quadratics \(\hat h_j\) are self-adjoint. Let
\(\hat g=\mathrm e^{-\hat K}\), where \(\hat K\) is an elliptic Hermitian
quadratic Hamiltonian with positive definite quadrature coefficients; a real
scalar shift is allowed.
Such \(\hat g\) is trace class and has no kernel. All finite polynomial
insertions have finite thermal moments.

**Theorem.** For \(B=\hat h_m\cdots\hat h_1\ne0\),

\[
\boxed{
\operatorname{Tr}(\hat h_1\cdots\hat h_m\hat h_m\cdots\hat h_1\hat g)
=\operatorname{Tr}(B^\dagger B\hat g)
=\|B\hat g^{1/2}\|_{\rm HS}^2>0.}
\tag{21}
\]

No pairwise commutativity is needed. For the strict inequality, diagonalize
\(\hat g\) in its complete oscillator basis. Every eigenvalue is strictly
positive, and at least one basis vector has a nonzero image under the
nonzero polynomial operator \(B\). Thus the sum of squared norms in (21)
is strictly positive. The oscillator basis is a core for these polynomial
operators, so a polynomial annihilating all its vectors is the zero operator.

Under the same assumption on \(\hat g\), a second sufficient condition is
that the positive operators \(-\hat h_j\) strongly commute. Their product
\(R=\prod_j(-\hat h_j)\) is then positive by their joint spectral calculus.
If \(R\ne0\), faithfulness of the thermal operator gives

\[
(-1)^s\operatorname{Tr}(\hat h_1\cdots\hat h_s\hat g)
=\operatorname{Tr}(R\hat g)>0.
\tag{22}
\]

For even \(s\), this has the original sign. The thermal operator need not
commute with the insertions. Equations (21) and (22) state different sufficient
restrictions: the first uses reverse paired ordering, and the second uses
mutually commuting insertions. The two counterexamples explain why positivity
of the thermal operator alone, or commutativity of the insertions alone with
arbitrary Gaussian evolution, is insufficient.

## Scope and verification

Equation (1) proves the fermionic conjecture under its stated finite-mode,
full-Fock-space, invariant-cone, and interior assumptions, using Wei's
nonnegative inequality as its input. Equations (15), (21), and (22) are
sufficient bosonic replacements. They do not assert a classification of all
bosonic insertions with positive traces or a minimal set of restrictions.

The companion [verification script](trace_conjecture/verify_positive_results.py)
checks finite-dimensional cone-algebra generation in representative mode
numbers, directly evaluates non-Hermitian fermionic Gaussian products, and
checks the commuting bosonic counterexample by integrating the differentiated
Mehler kernel. These are independent algebraic and numerical checks of the
derivations, not substitutes for the all-mode proofs above.

Run in Linux/WSL with

```bash
python3 note/trace_conjecture/verify_positive_results.py
```

or forward the same command with `scripts/run-in-wsl.ps1` from PowerShell.
