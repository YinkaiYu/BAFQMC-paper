# Two standard forms of bosonic contraction semigroups

The eight bosonic cases with nonzero contraction cones in the Nambu periodic table reduce to two standard forms under complex changes of canonical coordinates. The remaining distinction is whether the anti-linear transformation that constrains each generator squares to \(+I\) or \(-I\). Position and momentum coordinates make this reduction explicit.

## 1. From creation and annihilation operators to \(x,p\)

Let \([\hat a_j,\hat a_k^+]=\delta_{jk}\), with all other commutators zero, and write
\[
\hat a=\frac{\hat x+\mathrm i\hat p}{\sqrt2},\qquad
\hat a^+=\frac{\hat x-\mathrm i\hat p}{\sqrt2}.
\tag{1}
\]
The superscript \(+\) labels the operator paired with \(\hat a\) in the canonical commutator. In the usual Fock representation, \(\hat a^+=\hat a^\dagger\) and \(x,p\) are Hermitian. Complex canonical changes preserve the commutators and transform the adjoint relation along with the operators.

Collect the \(N\) modes into columns,
\[
\hat\chi=\binom{\hat a}{\hat a^+},\qquad
\hat r=\binom{\hat x}{\hat p}=Q\hat\chi,\qquad
Q=\frac1{\sqrt2}
\begin{pmatrix}I&I\\-\mathrm iI&\mathrm iI\end{pmatrix}.
\tag{2}
\]
Then
\[
[\hat r_\mu,\hat r_\nu]=\mathrm i\Omega_{\mu\nu},\qquad
\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix}.
\]
Here the identity blocks have dimension \(N\).

Write a quadratic time slice as \(\mathrm e^{\hat h}\), with the time step absorbed into \(\hat h\). In the Nambu convention \(g=-\Omega\),
\[
\hat h=\frac12\hat\chi^{\mathsf T}gA\hat\chi
=\frac12\hat r^{\mathsf T}H\hat r,\qquad
B=QAQ^\dagger,\qquad H=\mathrm i\Omega B.
\tag{3}
\]
The matrices \(A,B\) are the one-body generators in the two bases. The matrix \(H\) contains the quadratic coefficients of the exponent. Direct substitution gives
\[
gA+A^{\mathsf T}g=0
\quad\Longleftrightarrow\quad
B^{\mathsf T}\Omega+\Omega B=0
\quad\Longleftrightarrow\quad H^{\mathsf T}=H.
\tag{4}
\]

## 2. The semigroup conditions in the new coordinates

The Nambu table uses two real orthogonal matrices \(J_1,J_2\). The first imposes
\[
J_1^{\mathsf T}AJ_1=\overline A.
\]
The second determines the Hermitian matrix \(\eta\) in
\[
\eta A+A^\dagger\eta\leq0,\qquad \eta^2=I.
\tag{5}
\]
These conditions select the allowed generators. Their ordered exponentials generate the contraction semigroup.

To express \(J_1,J_2\) as transformations of the canonical operators, choose the phases
\[
U_j=
\begin{cases}
J_j,&J_j^{\mathsf T}gJ_j=g,\\
\mathrm iJ_j,&J_j^{\mathsf T}gJ_j=-g.
\end{cases}
\tag{6}
\]
Both choices give \(U_j^{\mathsf T}gU_j=g\). The anti-linear transformation \(\Theta_j\hat\chi=U_j\hat\chi\) conjugates numerical coefficients. Its matrix in the \(x,p\) coordinates is therefore
\[
R_j=\overline Q\,U_jQ^\dagger,\qquad
\Theta_j\hat r=R_j\hat r,\qquad
R_j^{\mathsf T}\Omega R_j=-\Omega.
\tag{7}
\]
The bar on \(Q\) and the minus sign multiplying \(\Omega\) both follow from anti-linearity.

The phase in (6) leaves the square unchanged, \(\overline U_jU_j=J_j^2\). In all eight contraction cases, \(J_2^2=I\), and the induced anti-linear transformations anticommute. Thus
\[
\overline R_2R_2=I,\qquad
\overline R_2R_1+\overline R_1R_2=0.
\tag{8}
\]
For these \(J_2^2=I\) cases, the table uses
\(\eta=\mathrm iJ_2g\) when \(J_2^{\mathsf T}gJ_2=g\), and
\(\eta=J_2g\) when \(J_2^{\mathsf T}gJ_2=-g\).
Substituting these expressions and transforming (5) gives
\[
\begin{aligned}
R_1^{-1}\overline B R_1&=B,\\
EB+B^\dagger E&\leq0,\qquad
E=Q\eta Q^\dagger=-\overline R_2\Omega.
\end{aligned}
\tag{9}
\]
The first transformation constrains \(B\), while the second determines the matrix \(E\) in the inequality.

## 3. Why only two standard forms remain

A further change \(\hat r'=P\hat r\) preserves the commutators when \(P^{\mathsf T}\Omega P=\Omega\). For the reduction below, \(P\) can also be chosen unitary. Then
\[
B'=PBP^\dagger,\qquad
E'=PEP^\dagger,\qquad
R_j'=\overline P R_jP^\dagger.
\tag{10}
\]
The contraction inequality is preserved by unitary conjugation. Products transform in the same way,
\[
\mathrm e^{B_1'}\mathrm e^{B_2'}\cdots
=P\bigl(\mathrm e^{B_1}\mathrm e^{B_2}\cdots\bigr)P^\dagger,
\]
so this change maps the complete semigroup.

For the eight cases, \(E\) satisfies
\[
E^\dagger=E,\qquad E^2=I,\qquad
E^{\mathsf T}\Omega+\Omega E=0.
\]
The last relation pairs its eigenvectors with eigenvalues \(+1\) and \(-1\). Choosing these pairs as coordinates allows the same standard matrix in every case,
\[
E'=\mathrm i\Omega,\qquad R_2'=\mathrm iI.
\tag{11}
\]
The second equality follows directly from \(E'=-\overline R_2'\Omega\). The Appendix gives the coordinate change explicitly.

Anticommutation now makes the first matrix real,
\[
0=\overline R_2'R_1'+\overline R_1'R_2'
=-\mathrm iR_1'+\mathrm i\overline R_1'
\quad\Longrightarrow\quad
\overline R_1'=R_1'.
\tag{12}
\]
Its square is still \(J_1^2=\pm I\). A final real canonical change puts it into one of the following forms. We omit primes in these standard coordinates.

For \(J_1^2=+I\),
\[
R_1=\begin{pmatrix}I_N&0\\0&-I_N\end{pmatrix}.
\tag{13}
\]
This is the familiar action of complex conjugation in the occupation basis, \(\Theta_1\hat x=\hat x\), \(\Theta_1\hat p=-\hat p\).

For \(J_1^2=-I\), the number of modes is even and
\[
R_1=\begin{pmatrix}\mathcal J&0\\0&-\mathcal J\end{pmatrix},
\qquad
\mathcal J=\begin{pmatrix}0&I_{N/2}\\-I_{N/2}&0\end{pmatrix}.
\tag{14}
\]
Here the modes occur in pairs \((\hat b_j,\hat c_j)\), with
\(\Theta_1\hat b_j=\hat c_j\) and
\(\Theta_1\hat c_j=-\hat b_j\).
The minus sign after two applications acts on these single-mode operators.

In both forms, the allowed quadratic coefficients obey
\[
\boxed{
H^{\mathsf T}=H,\qquad
R_1^{\mathsf T}\overline H R_1=H,\qquad
\operatorname{Re}H\leq0.
}
\tag{15}
\]
Indeed, \(E=\mathrm i\Omega\) turns the contraction inequality into
\(EB+B^\dagger E=H+H^\dagger=2\operatorname{Re}H\leq0\).
The corresponding semigroup consists of ordered products of
\(\mathrm e^B\), with \(B=\mathrm i\Omega H\).

The [Nambu table](../pdf/ContractionSemigroupsQMC.pdf) therefore groups as follows.

| Square of the first transformation | Bosonic cells | Standard form |
|---|---|---|
| \(J_1^2=+I\) | B02, B05, B17, B22 | Equation (13) |
| \(J_1^2=-I\) | B10, B13, B25, B30 | Equation (14) |

The square of an anti-linear transformation is preserved by a change of coordinates. It distinguishes the two rows, while the other signs used in the Nambu enumeration have been absorbed into the coordinate choice.

The same result also locates the two kinds of bosonic anti-linear transformation. With
\[
C=\begin{pmatrix}0&I\\I&0\end{pmatrix},
\qquad
C\overline U C=\pm U
\quad\Longleftrightarrow\quad
\overline R=\pm R,
\tag{16}
\]
the first-kind map has real \(R\), and the second-kind map has purely imaginary \(R\). Both standard forms use a first-kind \(R_1\) and the second-kind \(R_2=\mathrm iI\), whose Nambu matrix is \(U_2=\mathrm iC\). The two semigroup families are distinguished by \(R_1^2\). For fermions, a second-kind map together with \(U^{\mathsf T}CU=C\) would imply \(U^\dagger U=-I\), so it cannot preserve the fermionic canonical relations.

The reduction uses complex canonical changes. The adjoints of the new coordinates follow from \(\hat r'=P\hat r\) and the original adjoints. Starting from Hermitian \(x,p\), requiring the new coordinates to stay Hermitian would restrict \(P\) to real matrices and impose a stronger notion of equivalence.

## Appendix. The coordinate change

Choose orthonormal eigenvectors of \(E\) with eigenvalue \(+1\) as the columns of \(V_+\). The relations above (11) imply
\[
E(-\Omega\overline V_+)=-(-\Omega\overline V_+),\qquad
V_+^{\mathsf T}\Omega V_+=0.
\]
Consequently,
\[
V=(V_+,-\Omega\overline V_+),\qquad
V^\dagger V=I,\qquad V^{\mathsf T}\Omega V=\Omega.
\tag{17}
\]
The change \(V^\dagger\) preserves the commutators and sends \(E\) to
\(D=\operatorname{diag}(I,-I)\). A fixed additional change gives
\[
P_0=\frac1{\sqrt2}
\begin{pmatrix}I&-\mathrm iI\\-\mathrm iI&I\end{pmatrix},
\qquad
P_0DP_0^\dagger=\mathrm i\Omega,\qquad
P=P_0V^\dagger.
\tag{18}
\]
This proves (11).

After this change, \(R_1'\) is real and orthogonal, with
\(R_1'{}^{\mathsf T}\Omega R_1'=-\Omega\).
For square \(+I\), take its \(+1\) eigenvectors as position directions. Their canonical momentum partners have eigenvalue \(-1\), giving (13).
For square \(-I\), a vector and its image under \(R_1'\) form a pair. Their momentum partners complete a four-dimensional block with the action in (14). Repeating the construction exhausts the modes. These final changes are real, orthogonal, and canonical, and preserve \(E=\mathrm i\Omega\) and \(R_2=\mathrm iI\).
