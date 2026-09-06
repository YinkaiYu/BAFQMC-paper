# Bosonic Nambu and quadrature formulations of contraction semigroups

Research note, 6 September 2026.

The eight bosonic cases with a nonzero contraction cone reduce to **two algebraic families**, distinguished by the square of the first anti-linear map. A complex unitary symplectic change of coordinates puts every representative into one of two explicit standard forms. Requiring all coordinates to remain Hermitian imposes a stronger notion of equivalence: additional representation data can then survive. This distinction is essential when transferring the result to physical Gaussian traces.

This note derives the bosonic counterpart of Appendix B of `TimeReversalSymmetriesQMC.tex`, then applies it to the eight colored bosonic cells of `ContractionSemigroupsQMC.tex`. The classification concerns the strict-contraction cases; it does not identify the 24 group-only cases with these semigroups.

## 1. Nambu operators and Hermitian quadratures

For \(N\) bosonic modes, set

\[
\hat\chi=(\hat a,\hat a^+)^{\mathsf T},\qquad
\hat r=(\hat x,\hat p)^{\mathsf T}=Q\hat\chi,\qquad
Q=\frac1{\sqrt2}\begin{pmatrix}I&I\\-\mathrm iI&\mathrm iI\end{pmatrix}.
\]

Thus \(\hat a=(\hat x+\mathrm i\hat p)/\sqrt2\) and \(\hat a^+=(\hat x-\mathrm i\hat p)/\sqrt2\). Define

\[
\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix},\qquad
g=-\Omega,\qquad C=\begin{pmatrix}0&I\\I&0\end{pmatrix}.
\]

The identities needed below are

\[
Q^{-1}=Q^\dagger,\qquad \overline Q=QC,\qquad
Q^{-\mathsf T}gQ^{-1}=\mathrm i\Omega,\qquad
[\hat r_\mu,\hat r_\nu]=\mathrm i\Omega_{\mu\nu}.
\]

For the quadratic generator and its one-body matrix, write

\[
\hat h=\frac12\hat\chi^{\mathsf T}gA\hat\chi
=\frac12\hat r^{\mathsf T}H\hat r,\qquad
B=QAQ^{-1},\qquad H=\mathrm i\Omega B.
\tag{1}
\]

The exact dictionary is

\[
gA+A^{\mathsf T}g=0
\quad\Longleftrightarrow\quad
B^{\mathsf T}\Omega+\Omega B=0
\quad\Longleftrightarrow\quad H^{\mathsf T}=H.
\tag{2}
\]

The coefficient matrix \(H\) is symmetric, while \(B\) is a complex symplectic Lie-algebra element. They are different objects. Hermiticity of the quadratic operator additionally requires \(H\) real, or equivalently \(\overline B=-B\). Hubbard--Stratonovich generators need not have this property.

For a product, \(M_r=QM Q^{-1}\). In particular,

\[
\det(I-M_r)=\det(I-M),\qquad
p_{\rm B}=\bigl[(-1)^N\det(I-M_r)\bigr]^{-1/2}.
\tag{3}
\]

The ordered Fock-space product selects the square-root branch. Equation (3) preserves its determinant under the coordinate change; it does not select a new branch.

## 2. Physical antiunitary transformations

Use the operator-space convention of the time-reversal note:

\[
\widehat\Theta\hat\chi\widehat\Theta^{-1}=U\hat\chi.
\]

Anti-linearity conjugates the coefficients in \(Q\), so

\[
R=\overline Q\,UQ^{-1},\qquad
\widehat\Theta\hat r\widehat\Theta^{-1}=R\hat r,
\qquad U=(\overline Q)^{-1}RQ.
\tag{4}
\]

The three physical Nambu conditions become

\[
\begin{aligned}
C\overline U C=U
&\quad\Longleftrightarrow\quad \overline R=R,\\
U^{\mathsf T}gU=g
&\quad\Longleftrightarrow\quad R^{\mathsf T}\Omega R=-\Omega,\\
U^{-1}\overline A U=A
&\quad\Longleftrightarrow\quad R^{-1}\overline B R=B.
\end{aligned}
\tag{5}
\]

Thus a physical bosonic time reversal is a **real anti-symplectic transformation** of Hermitian quadratures. The minus sign follows directly from antiunitarity:

\[
[\Theta\hat r_\mu,\Theta\hat r_\nu]
=\Theta(\mathrm i\Omega_{\mu\nu})=-\mathrm i\Omega_{\mu\nu}.
\]

Equivalently, \(R^{\mathsf T}\overline H R=H\). If \(U\) is also unitary as a matrix, as in the periodic-table representatives, \(R\) is orthogonal. General physical bosonic canonical transformations need not satisfy this extra Euclidean orthogonality condition.

Squares and mutual anticommutation are preserved:

\[
\overline U U=\epsilon I
\Longleftrightarrow\overline R R=\epsilon I,
\qquad
\overline U_bU_a+\overline U_aU_b=0
\Longleftrightarrow
\overline R_bR_a+\overline R_aR_b=0.
\tag{6}
\]

For physical real matrices these reduce to \(R^2=\epsilon I\) and ordinary matrix anticommutation. Under the additional orthogonality assumption, \(R^{\mathsf T}=\epsilon R\).

The fermionic analogue has a symmetric canonical form that becomes \(I\) in the Majorana basis. The bosonic alternating form remains \(\Omega\); an invertible change of basis cannot turn an alternating form into a symmetric one. This is the structural difference between the two dictionaries.

## 3. The eight contraction cases in a common language

Write the table's five signs as

\[
J_j^{\mathsf T}gJ_j=s_jg,\qquad J_j^2=q_jI,\qquad
J_1J_2=rJ_2J_1.
\]

All \(J_j\) are real orthogonal. The existing cone criterion is

\[
q_2=+1,\qquad r=-s_1s_2.
\tag{7}
\]

Introduce the canonically preserving anti-linear matrices

\[
U_j=\begin{cases}J_j,&s_j=+1,\\ \mathrm iJ_j,&s_j=-1,\end{cases}
\qquad R_j=\overline Q\,U_jQ^{-1}.
\tag{8}
\]

These matrices are unitary, and \(U_j^{\mathsf T}gU_j=g\). For an arbitrary table representative, physical adjoint compatibility is a separate condition. Specifically,

\[
C\overline U_jC=U_j
\quad\Longleftrightarrow\quad CJ_jC=s_jJ_j.
\tag{9}
\]

The minimal generator representatives and the physical time-reversal representatives in the repository are different choices in some cells. Equation (9) must therefore be checked rather than inferred from the five signs. Without it, \(R_j\) can be complex even though the initial \(x,p\) operators are Hermitian.

Let \(E=Q\eta Q^\dagger\). Substitution of the table metric gives, for both signs of \(s_2\),

\[
\boxed{E=-\overline R_2\Omega},\qquad
E=E^\dagger,\quad E^2=I,\quad
E^{\mathsf T}\Omega+\Omega E=0.
\tag{10}
\]

For example, \(\overline R_2=Q\overline\alpha_2J_2Q^{\mathsf T}\), where \(\alpha_2=1\) or \(\mathrm i\). Combining this with \(Q^{-\mathsf T}gQ^{-1}=\mathrm i\Omega\) yields (10) for either \(\eta=\mathrm iJ_2g\) or \(\eta=J_2g\). For a physical \(R_2\), the bar in (10) can be omitted.

All eight cases now satisfy the same equations:

\[
\begin{gathered}
B^{\mathsf T}\Omega+\Omega B=0,\qquad
R_1^{-1}\overline B R_1=B,\qquad EB+B^\dagger E\leq0,\\
R_j^\dagger R_j=I,\qquad R_j^{\mathsf T}\Omega R_j=-\Omega,\\
R_1^{\mathsf T}=q_1R_1,\qquad R_2^{\mathsf T}=R_2,\qquad
\overline R_2R_1+\overline R_1R_2=0.
\end{gathered}
\tag{11}
\]

Only \(q_1\) remains as a binary algebraic choice. The transformation also preserves the full group/cone decomposition:

\[
\begin{aligned}
B_{\rm group}&=\tfrac12(B+R_2^{-1}\overline B R_2),\\
B_{\rm cone}&=\tfrac12(B-R_2^{-1}\overline B R_2),\\
EB+B^\dagger E&=2EB_{\rm cone}.
\end{aligned}
\tag{12}
\]

The first anti-linear map is a symmetry of the complete generator. The second fixes the group directions and reverses the cone directions. It is consequently not a second time-reversal symmetry of a general semigroup element.

| Family | Bosonic cells | Anti-linear squares on the maximal subgroup |
|---|---|---|
| \(q_1=+1\) | B02, B05, B17, B22 | \(\{+,+\}\) |
| \(q_1=-1\) | B10, B13, B25, B30 | \(\{-,+\}\) |

The fermionic construction instead requires \(q_2=-1\), giving \(\{+,-\}\) and \(\{-,-\}\). These are the two fermionic semigroup families in [Wei, *Physical Review B* **110**, 075146 (2024), Sec. IV](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.110.075146/fulltext). The paper also explicitly allows complex canonical Majorana coordinates; its algebraic scope is useful when comparing the two statistics.

## 4. Proof that there are two complex canonical standard forms

The allowed coordinate changes in this section are

\[
\hat r'=P\hat r,\qquad P^\dagger P=I,\qquad
P^{\mathsf T}\Omega P=\Omega.
\tag{13}
\]

The matrix \(P\) may be complex. Such a change preserves the canonical algebra and the contraction inequality, but need not preserve the Hermiticity of individual coordinates. The transformed data are

\[
B'=PBP^\dagger,\qquad E'=PEP^\dagger,\qquad
R_j'=\overline P R_jP^\dagger.
\tag{14}
\]

In particular, \(E'B'+B'^\dagger E'=P(EB+B^\dagger E)P^\dagger\).

### Normalize the contraction metric

Because \(E\) is Hermitian, symplectic-infinitesimal, and an involution, an eigenvector \(v\) with eigenvalue \(+1\) is paired with \(-\Omega\overline v\), which has eigenvalue \(-1\). The two eigenspaces therefore have equal dimension \(N\). Choose an orthonormal basis \(V_+\) of the positive eigenspace and set

\[
V=(V_+,-\Omega\overline V_+).
\]

The symplectic Lie-algebra relation implies \(V_+^{\mathsf T}\Omega V_+=0\), hence

\[
V^\dagger V=I,\qquad V^{\mathsf T}\Omega V=\Omega.
\]

The change \(P=V^\dagger\) gives

\[
E'=D\equiv\begin{pmatrix}I&0\\0&-I\end{pmatrix},\qquad
R_2'=X\equiv\begin{pmatrix}0&I\\I&0\end{pmatrix}.
\tag{15}
\]

The second identity follows from (10), which is preserved by (14).

### Normalize the remaining anti-linear map

The cone-compatibility condition gives \(R_1^{-1}\overline E R_1=E\). With \(E'=D\), it forces \(R_1'\) to be block diagonal. Its anti-symplectic and unitary properties then imply

\[
R_1'=\begin{pmatrix}U&0\\0&-\overline U\end{pmatrix},\qquad
U^\dagger U=I,\qquad U^{\mathsf T}=q_1U.
\tag{16}
\]

Changes \(P=\operatorname{diag}(W,\overline W)\), with \(W\) unitary, preserve both matrices in (15) and send \(U\mapsto\overline W U W^\dagger\).

For \(q_1=+1\), the anti-linear map \(z\mapsto U\overline z\) is an isometric involution. An orthonormal basis of its real fixed subspace gives \(U=VV^{\mathsf T}\). Taking \(W=V^{\mathsf T}\) reduces \(U\) to \(I\).

For \(q_1=-1\), \(N=2m\) is even. Choose a normalized vector \(v\) and its orthogonal partner \(-U\overline v\), then repeat in the orthogonal complement. This constructs a unitary \(V\) with \(U=V\mathcal J V^{\mathsf T}\), where

\[
\mathcal J=\begin{pmatrix}0&I_m\\-I_m&0\end{pmatrix}.
\]

Again \(W=V^{\mathsf T}\) gives the standard form. The two results are

\[
\boxed{\begin{array}{c|c|c|c}
q_1&E&R_2&R_1\\ \hline
+1&D&X&D\\[2pt]
-1&D&X&\operatorname{diag}(\mathcal J,-\mathcal J)
\end{array}}
\tag{17}
\]

These transformations map the entire generator set, its contraction cone, and all ordered matrix products bijectively. They prove equivalence of the algebraic semigroups, rather than merely a relabeling of their signs. Both standard forms have a strict direction \(B=-D\), for which \(DB+B^\dagger D=-2I\).

As a further distinction, the connected maximal subgroup has Lie algebra \(\mathfrak{gl}(N,\mathbb R)\) in the positive-square family and \(\mathfrak{sp}(2m,\mathbb C)\), regarded as a real Lie algebra, in the negative-square family. Here \(\operatorname{Sp}(2m,\mathbb C)\) denotes matrices of size \(2m\). To see this, split the complexified space into eigenspaces of \(R_1R_2\) in the standard forms (17). For \(q_1=+1\), they are paired Lagrangian sectors, each preserved by the anti-linear map \(z\mapsto R_2\overline z\); an arbitrary real block on one sector determines the other. For \(q_1=-1\), they are symplectic sectors exchanged by that anti-linear map; an arbitrary complex symplectic block determines its partner. For adjoint-compatible representatives, the latter family realizes the bosonic Majorana mechanism on its maximal subgroup.

## 5. What changes when the coordinates must remain Hermitian

A physical change between two Hermitian quadrature bases has \(P\) real and symplectic. The standardization in (13) allows complex matrices and therefore need not satisfy the Hermiticity requirement. Even allowing nonorthogonal real symplectic changes leaves the obstruction below intact.

For real orthogonal anti-symplectic matrices, choose a real orthogonal symplectic basis with

\[
R_2=D,\qquad R_1=\begin{pmatrix}0&K\\K&0\end{pmatrix},\qquad
K^{\mathsf T}K=I,\qquad K^2=q_1I.
\tag{18}
\]

This follows by choosing an orthonormal basis in the \(+1\) eigenspace of \(R_2\), completing it with its symplectic partners, and using the anticommutation of \(R_1,R_2\). The anti-symplectic condition identifies the two off-diagonal blocks in \(R_1\).

For \(q_1=-1\), \(K\) is a real orthogonal complex structure; an orthogonal change reduces it to \(\mathcal J\). For \(q_1=+1\), it is a symmetric involution,

\[
K=S=\operatorname{diag}(I_p,-I_q),\qquad p+q=N.
\]

The real symmetric form

\[
F=\Omega R_1R_2=\operatorname{diag}(S,S)
\tag{19}
\]

has inertia \((2p,2q)\). Under any real symplectic change it transforms by congruence,

\[
F'=P^{-\mathsf T}FP^{-1},
\]

so its inertia cannot change. The replacement \(R_1\mapsto-R_1\) leaves the generator constraints unchanged and interchanges \(p,q\); the physically relevant signature label is therefore unordered.

For a concrete counterexample, take two modes, \(R_2=D\), and compare \(K=I_2\) with \(K=\operatorname{diag}(1,-1)\). Their forms \(F\) have inertias \((4,0)\) and \((2,2)\). They share \(q_1=q_2=+1\) and the same anticommutation algebra, but their marked symmetry structures cannot be related by a real canonical change. Both signatures can already occur in physical realizations of the B05 relation case. Thus the five signs do not classify all physical representations up to real canonical equivalence.

The displayed physical representatives of B02, B05, B17, and B22 all have balanced inertia \((2,2)\). The signature issue concerns the allowed representations beyond that particular choice; it does not introduce a third binary contraction criterion.

## 6. Gaussian weights and the interpretation of the reduction

For every change (13), \(M' = PM P^{-1}\), so the determinant and its poles are unchanged. The same ordered Gaussian lift retains its branch. However, if \(P\) is complex, interpreting \(P\hat r\) as a fresh set of Hermitian operators changes the adjoint structure. Trace convergence in that different physical realization need not be preserved.

The one-mode B05 representative makes this explicit. Its minimal matrices are \(J_1=I\), \(J_2=\sigma_x\), and \(\eta=\sigma_z\). The strict generator \(A=-t\sigma_z\), \(t>0\), represents

\[
\hat h=-t(\hat n+\tfrac12),\qquad
p=\frac1{2\sinh(t/2)}>0.
\]

The standardization above sends the matrix to \(B'=-tD\). Its quadratic coefficient is

\[
H'=\mathrm i\Omega B'=\mathrm itX.
\]

If the new coordinates are incorrectly treated as Hermitian, this becomes an anti-Hermitian squeezing generator, whose exponential is unitary and is not trace class. Under the actual complex coordinate change it remains the same damped oscillator, because the new coordinates carry a transformed adjoint relation. This example separates matrix-semigroup equivalence from equivalence of physical trace domains.

Consequently:

1. **Two algebraic contraction families:** yes, with the explicit standard forms (17).
2. **Two patterns in physical quadrature language:** yes, for adjoint-compatible representatives, with real anti-symplectic matrices and squares \(\{+,+\}\) or \(\{-,+\}\) on the maximal subgroup.
3. **Exactly two inequivalent physical realizations under real canonical changes:** this stronger statement does not follow; the signature example (19) supplies an obstruction.

The bosonic time-reversal-only class \(\{+,+,+\}\) is a separate sufficient criterion. It need not collapse because the strict-contraction cases have two families: a cone inequality can protect evolution that breaks the second subgroup time reversal. In every physical application the positive reference, the branch, and the convergence domain must still be specified as in the original semigroup note.

## Verification

The companion `contraction_semigroups_qmc/python/verify_bosonic_quadrature.py` checks all eight minimal representatives and all eight physical representatives recorded in the existing CSV tables. It constructs the complex unitary symplectic standardization independently for each representation and checks the inverse dictionaries, quadratic coefficients, anti-linear constraints, group/cone projections, strict inequalities, and four-slice products. It also verifies the real-canonical inertia obstruction.

Run from the repository root in Linux/WSL:

```text
python3 experts/contraction_semigroups_qmc/python/verify_bosonic_quadrature.py
```

The 6 September 2026 run passed 1,333 matrix identities with maximum residual \(1.78\times10^{-15}\). These finite-dimensional checks support the analytic derivation; they do not test Fock-space trace convergence numerically. The existing manuscript sources and bibliography are unchanged.
