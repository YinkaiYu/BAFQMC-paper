# Two standard forms of bosonic contraction semigroups

The eight bosonic cases with nonzero contraction cones in the Nambu periodic table reduce to two standard forms under complex changes of canonical coordinates. The remaining distinction is whether the anti-linear transformation that constrains each generator squares to \(+I\) or \(-I\). Position and momentum coordinates make this reduction explicit.

A table entry specifies a set of allowed quadratic generators. Their ordered exponentials form the corresponding semigroup. To identify two entries, a single change of coordinates must map all their allowed generators and preserve every ordered product. This establishes equivalence of the complete semigroups.

The reduction proceeds in two steps. The familiar change from \(a,a^+\) to \(x,p\) puts the canonical relations and the quadratic coefficients into a common form. A further canonical change then makes the contraction condition identical in all eight cases. Once this second step is completed, only the square of the first anti-linear transformation remains to distinguish the two families.

## 1. From creation and annihilation operators to \(x,p\)

Let \([\hat a_j,\hat a_k^+]=\delta_{jk}\), with all other commutators zero, and write
\[
\hat a=\frac{\hat x+\mathrm i\hat p}{\sqrt2},\qquad
\hat a^+=\frac{\hat x-\mathrm i\hat p}{\sqrt2}.
\tag{1}
\]
The superscript \(+\) labels the operator paired with \(\hat a\) in the canonical commutator. In the usual Fock representation, \(\hat a^+=\hat a^\dagger\) and \(x,p\) are Hermitian. Complex canonical changes preserve the commutators and transform the adjoint relation along with the operators.

To apply the same change to all \(N\) modes and to their quadratic generators, collect the operators into columns,
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
Here the identity blocks have dimension \(N\). The off-diagonal blocks of \(\Omega\) record \([x_j,p_k]=\mathrm i\delta_{jk}\) and \([p_j,x_k]=-\mathrm i\delta_{jk}\).

Write a quadratic time slice as \(\mathrm e^{\hat h}\), with the time step absorbed into \(\hat h\). In the Nambu convention \(g=-\Omega\),
\[
\hat h=\frac12\hat\chi^{\mathsf T}gA\hat\chi
=\frac12\hat r^{\mathsf T}H\hat r,\qquad
B=QAQ^\dagger,\qquad H=\mathrm i\Omega B.
\tag{3}
\]
The matrices \(A,B\) are the one-body generators in the two bases, with propagation matrices \(\mathrm e^A,\mathrm e^B\). The matrix \(H\) contains the coefficients that multiply the position and momentum operators in \(\hat h\). Thus \(B\) describes one-body propagation, while \(H\) displays the quadratic operator itself. The canonical constraint becomes
\[
gA+A^{\mathsf T}g=0
\quad\Longleftrightarrow\quad
B^{\mathsf T}\Omega+\Omega B=0
\quad\Longleftrightarrow\quad H^{\mathsf T}=H.
\tag{4}
\]
For example, \(H^{\mathsf T}=-\mathrm iB^{\mathsf T}\Omega=\mathrm i\Omega B=H\). In position and momentum coordinates, the allowed quadratic coefficients are therefore contained in a complex symmetric matrix.

## 2. The semigroup conditions in the new coordinates

To compare semigroups, both the symmetry condition and the contraction inequality must be carried into the new coordinates. The Nambu table expresses them through two real orthogonal matrices \(J_1,J_2\). The first imposes
\[
J_1^{\mathsf T}AJ_1=\overline A.
\]
The second determines the Hermitian matrix \(\eta\) in
\[
\eta A+A^\dagger\eta\leq0,\qquad \eta^2=I.
\tag{5}
\]
These conditions select the allowed generators. Their ordered exponentials generate the contraction semigroup.

Some entries use a \(J_j\) that preserves \(g\), while others use one that reverses its sign. Multiplication by \(\mathrm i\) compensates for the latter sign, since
\[
(\mathrm iJ_j)^{\mathsf T}g(\mathrm iJ_j)
=-J_j^{\mathsf T}gJ_j.
\]
The transformations of the canonical operators can therefore be written uniformly by choosing
\[
U_j=
\begin{cases}
J_j,&J_j^{\mathsf T}gJ_j=g,\\
\mathrm iJ_j,&J_j^{\mathsf T}gJ_j=-g.
\end{cases}
\tag{6}
\]
Both choices give \(U_j^{\mathsf T}gU_j=g\). The anti-linear transformation \(\Theta_j\hat\chi=U_j\hat\chi\) conjugates numerical coefficients. Applying it to \(\hat r=Q\hat\chi\) gives
\[
\Theta_j\hat r
=\overline Q\,\Theta_j\hat\chi
=\overline Q\,U_jQ^\dagger\hat r.
\]
Its matrix in the \(x,p\) coordinates is consequently
\[
R_j=\overline Q\,U_jQ^\dagger,\qquad
\Theta_j\hat r=R_j\hat r,\qquad
R_j^{\mathsf T}\Omega R_j=-\Omega.
\tag{7}
\]
The bar on \(Q\) follows from conjugating its numerical entries. The minus sign multiplying \(\Omega\) has the same origin, since the transformation sends \([x_j,p_k]=\mathrm i\delta_{jk}\) to a commutator with right-hand side \(-\mathrm i\delta_{jk}\).

Applying the transformation twice also conjugates the first matrix, so
\(\Theta_j^2\hat\chi=\overline U_jU_j\hat\chi\).
The phase in (6) leaves this square unchanged. In particular,
\((-\mathrm iJ_j)(\mathrm iJ_j)=J_j^2\).
In all eight contraction cases, \(J_2^2=I\), and the induced anti-linear transformations anticommute. These common properties of the table become
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
The first transformation constrains \(B\), while the second determines the matrix \(E\) in the inequality. The identity \(E=-\overline R_2\Omega\) is the useful link between them. A coordinate choice that fixes \(E\) also fixes \(R_2\), allowing both to be standardized in the same step.

## 3. Why only two standard forms remain

The \(Q\) transformation has expressed every entry in \(x,p\) coordinates. Their matrices \(E,R_1,R_2\) can still differ. To remove this remaining dependence on the entry, make a further change \(\hat r'=P\hat r\). It preserves the commutators when \(P^{\mathsf T}\Omega P=\Omega\). For the reduction below, \(P\) can also be chosen unitary. Then
\[
B'=PBP^\dagger,\qquad
E'=PEP^\dagger,\qquad
R_j'=\overline P R_jP^\dagger.
\tag{10}
\]
The same \(P\) will be used for every allowed generator in a given entry. Its matrix unitarity preserves the inequality,
\[
E'B'+B'^\dagger E'
=P(EB+B^\dagger E)P^\dagger\leq0.
\]
Products transform in the same way,
\[
\mathrm e^{B_1'}\mathrm e^{B_2'}\cdots
=P\bigl(\mathrm e^{B_1}\mathrm e^{B_2}\cdots\bigr)P^\dagger,
\]
so the generator constraints and the multiplication law are both preserved. This is the required correspondence between complete semigroups.

For the eight cases, \(E\) satisfies
\[
E^\dagger=E,\qquad E^2=I,\qquad
E^{\mathsf T}\Omega+\Omega E=0.
\]
The first two relations give orthonormal eigenvectors with eigenvalues \(+1\) and \(-1\). The last relation pairs the two sets. If \(Ev=v\), then \(-\Omega\overline v\) has eigenvalue \(-1\). These pairs provide a canonical basis in which \(E\) is \(\operatorname{diag}(I,-I)\). A fixed additional canonical change, constructed in the Appendix, then gives the same matrix in every case,
\[
E'=\mathrm i\Omega,\qquad R_2'=\mathrm iI.
\tag{11}
\]
The second equality follows directly from \(E'=-\overline R_2'\Omega\). All eight entries now share the same contraction matrix and the same second anti-linear transformation.

It remains to classify the first transformation. Its anticommutation with the now fixed \(R_2'=\mathrm iI\) forces its matrix to be real,
\[
0=\overline R_2'R_1'+\overline R_1'R_2'
=-\mathrm iR_1'+\mathrm i\overline R_1'
\quad\Longrightarrow\quad
\overline R_1'=R_1'.
\tag{12}
\]
Its square is still \(J_1^2=\pm I\). For each sign, the remaining freedom to choose real canonical coordinates brings \(R_1'\) to a single standard form. The basis construction at the end of the Appendix shows why these two forms exhaust the possibilities. We omit primes in these standard coordinates.

For \(J_1^2=+I\),
\[
R_1=\begin{pmatrix}I_N&0\\0&-I_N\end{pmatrix}.
\tag{13}
\]
This is the familiar action of complex conjugation in the occupation basis, \(\Theta_1\hat x=\hat x\), \(\Theta_1\hat p=-\hat p\). Its \(+1\) directions can be chosen as positions, and their canonical momentum partners are the \(-1\) directions.

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
The minus sign after two applications acts on these single-mode operators. Each pair of mode directions requires its two momentum partners, giving four real canonical directions. This is why the number of bosonic modes is even.

The two choices of \(R_1\) can now be inserted into a common set of conditions on the quadratic coefficients,
\[
\boxed{
H^{\mathsf T}=H,\qquad
R_1^{\mathsf T}\overline H R_1=H,\qquad
\operatorname{Re}H\leq0.
}
\tag{15}
\]
The three conditions respectively express the canonical quadratic form, the first anti-linear symmetry, and the contraction inequality. For the last equality, \(E=\mathrm i\Omega\) and \(H=\mathrm i\Omega B\) give
\[
EB+B^\dagger E=H+H^\dagger=2\operatorname{Re}H,
\]
where the final step uses \(H^{\mathsf T}=H\).
The corresponding semigroup consists of ordered products of
\(\mathrm e^B\), with \(B=\mathrm i\Omega H\).

The first standard form also makes the coefficient constraints easy to read. In the \(xx,xp,pp\) blocks of \(H\), its symmetry requires the \(xx\) and \(pp\) coefficients to be real and the \(xp\) coefficients to be purely imaginary. The second standard form imposes the paired action of (14) through the same equation (15).

The [Nambu table](../pdf/ContractionSemigroupsQMC.pdf) therefore groups as follows.

| Square of the first transformation | Bosonic cells | Standard form |
|---|---|---|
| \(J_1^2=+I\) | B02, B05, B17, B22 | Equation (13) |
| \(J_1^2=-I\) | B10, B13, B25, B30 | Equation (14) |

The square of an anti-linear transformation is preserved by a change of coordinates. It distinguishes the two rows, while the other signs used in the Nambu enumeration have been absorbed into the coordinate choice.

The sign of the square can also be distinguished from the first-kind and second-kind labels for anti-linear transformations. These labels refer to the action on creation-annihilation exchange. With
\[
C=\begin{pmatrix}0&I\\I&0\end{pmatrix},
\qquad
C\overline U C=\pm U
\quad\Longleftrightarrow\quad
\overline R=\pm R,
\tag{16}
\]
the first-kind map has real \(R\), and the second-kind map has purely imaginary \(R\). Both standard forms use a first-kind \(R_1\) and the second-kind \(R_2=\mathrm iI\), whose Nambu matrix is \(U_2=\mathrm iC\). The two semigroup families are distinguished by \(R_1^2\). For fermions, a second-kind map together with \(U^{\mathsf T}CU=C\) would imply \(U^\dagger U=-I\), so it cannot preserve the fermionic canonical relations.

The reduction uses complex canonical changes. Their matrix unitarity preserves the contraction inequality, while their canonical property preserves the commutators. The adjoints of the new coordinates are obtained separately from \(\hat r'=P\hat r\) and the original adjoints. Starting from Hermitian \(x,p\), requiring the new coordinates to stay Hermitian restricts \(P\) to real matrices. The two-form reduction established here allows complex \(P\) and carries the actual adjoint relation along with it.

## Appendix. The coordinate change

The coordinate choice is built from the contraction matrix \(E\), so it applies to all generators in that entry. Choose orthonormal eigenvectors of \(E\) with eigenvalue \(+1\) as the columns of \(V_+\). The relations above (11) imply
\[
E(-\Omega\overline V_+)=-(-\Omega\overline V_+),\qquad
V_+^{\mathsf T}\Omega V_+=0.
\]
The first identity supplies the \(-1\) partners. The second ensures the correct commutators within each set. Placing the two sets side by side gives
\[
V=(V_+,-\Omega\overline V_+),\qquad
V^\dagger V=I,\qquad V^{\mathsf T}\Omega V=\Omega.
\tag{17}
\]
The change \(V^\dagger\) therefore preserves the commutators and sends \(E\) to
\(D=\operatorname{diag}(I,-I)\). The following fixed change turns this diagonal matrix into the common form \(\mathrm i\Omega\),
\[
P_0=\frac1{\sqrt2}
\begin{pmatrix}I&-\mathrm iI\\-\mathrm iI&I\end{pmatrix},
\qquad
P_0DP_0^\dagger=\mathrm i\Omega,\qquad
P=P_0V^\dagger.
\tag{18}
\]
This proves (11). It also displays explicitly why complex coordinates enter the construction. For one mode, \(P_0\) gives
\[
\hat x'=\frac{\hat x-\mathrm i\hat p}{\sqrt2},\qquad
\hat p'=\frac{\hat p-\mathrm i\hat x}{\sqrt2}.
\]
These operators still obey \([\hat x',\hat p']=\mathrm i\). Starting with Hermitian \(x,p\), their adjoints are obtained by conjugating the displayed coefficients.

After this change, \(R_1'\) is real and orthogonal, with
\(R_1'{}^{\mathsf T}\Omega R_1'=-\Omega\).
For square \(+I\), take an orthonormal basis of its \(+1\) eigenvectors as position directions. Since \(R_1'\Omega=-\Omega R_1'\), their canonical momentum partners have eigenvalue \(-1\), giving (13).

For square \(-I\), a real unit vector and its image under \(R_1'\) form an orthogonal pair. Their momentum partners complete a four-dimensional block. Orthogonality follows from the antisymmetry of \(R_1'\), \(\Omega\), and \(\Omega R_1'\). Choosing the signs of the paired basis vectors gives the action in (14). Repeating the construction in the orthogonal complement exhausts the modes. These final changes are real, orthogonal, and canonical, and preserve \(E=\mathrm i\Omega\) and \(R_2=\mathrm iI\).

## 4. Conclusions. Two direct criteria for quadratic generators

The two bosonic contraction semigroups can be specified directly by their quadratic coefficients. Take \(N\) canonical pairs satisfying
\[
[\hat x_j,\hat p_k]=\mathrm i\delta_{jk},\qquad
[\hat x_j,\hat x_k]=[\hat p_j,\hat p_k]=0,
\]
and write
\[
\hat h=\frac12\hat r^{\mathsf T}H\hat r,\qquad
H^{\mathsf T}=H.
\tag{19}
\]
The sign and size of the time step are included in \(\hat h\), so the quadratic factor is \(\mathrm e^{\hat h}\). All factors use the same canonical coordinates. Below, \(\operatorname{Re}H\) means the entrywise real part, and \(\operatorname{Re}H\leq0\) means that all its eigenvalues are nonpositive.

To state the contraction property, define \(\Omega\) by
\([\hat r_\mu,\hat r_\nu]=\mathrm i\Omega_{\mu\nu}\).
In the ordering \(\hat r=(\hat x,\hat p)^{\mathsf T}\),
\(\Omega=\left(\begin{smallmatrix}0&I_N\\-I_N&0\end{smallmatrix}\right)\).
The propagation matrix associated with a factor is
\[
\mathrm e^{-t\hat h}\hat r\,\mathrm e^{t\hat h}=M(t)\hat r,
\qquad M(t)=\mathrm e^{\,\mathrm i t\Omega H},\qquad t\geq0.
\tag{20}
\]
The contraction inequality is \(M^\dagger(\mathrm i\Omega)M\leq\mathrm i\Omega\). The Hermitian matrix \(\mathrm i\Omega\) has \(N\) positive and \(N\) negative eigenvalues, so this inequality compares a fixed indefinite quadratic form. Each theorem below gives conditions that preserve this inequality under arbitrary ordered products.

### Theorem 1. Conjugation with square \(+I\)

In the ordering \(\hat r=(\hat x,\hat p)^{\mathsf T}\), suppose
\[
H=\begin{pmatrix}
H_{xx}&H_{xp}\\
H_{xp}^{\mathsf T}&H_{pp}
\end{pmatrix},\qquad
\boxed{
H_{xx},H_{pp}\ \text{real},\quad
H_{xp}\ \text{purely imaginary},\quad
H_{xx}\leq0,\quad H_{pp}\leq0.
}
\tag{21}
\]
Then the propagation matrices generated by these quadratic factors belong to the first bosonic contraction semigroup. Every factor has the anti-linear symmetry
\[
\Theta\,\mathrm i=-\mathrm i,\qquad
\Theta\hat x=\hat x,\qquad
\Theta\hat p=-\hat p,
\qquad \Theta^2\hat r=\hat r.
\tag{22}
\]

This is the familiar conjugation that leaves position unchanged and reverses momentum. It explains the coefficient pattern directly. The \(xx\) and \(pp\) terms are even under momentum reversal and have real coefficients. The \(xp\) terms change sign and have imaginary coefficients, whose conjugation supplies the second sign. The nonpositive \(xx\) and \(pp\) blocks give \(\operatorname{Re}H\leq0\).

### Theorem 2. Conjugation between paired modes with square \(-I\)

Take \(N=2m\) modes in two fixed groups \(b,c\), and order the coordinates as
\[
\hat r=\binom{\hat r_b}{\hat r_c},\qquad
\hat r_b=\binom{\hat x_b}{\hat p_b},\qquad
\hat r_c=\binom{\hat x_c}{\hat p_c},\qquad
\Sigma=\begin{pmatrix}I_m&0\\0&-I_m\end{pmatrix}.
\tag{23}
\]
Here \(\Sigma\) reverses the momenta within either group. In this ordering, \(\Omega\) is block diagonal, with one canonical commutator matrix for each group. Suppose
\[
H=\begin{pmatrix}
H_{bb}&H_{bc}\\
H_{bc}^{\mathsf T}&H_{cc}
\end{pmatrix},\qquad
\boxed{
\begin{gathered}
H_{cc}=\Sigma\overline{H_{bb}}\Sigma,\qquad
H_{bc}=-\Sigma H_{bc}^{\dagger}\Sigma,\\
\operatorname{Re}H\leq0.
\end{gathered}
}
\tag{24}
\]
Then the propagation matrices generated by these quadratic factors belong to the second bosonic contraction semigroup. Every factor has the anti-linear symmetry
\[
\Theta\,\mathrm i=-\mathrm i,\qquad
\Theta\hat r_b=\Sigma\hat r_c,\qquad
\Theta\hat r_c=-\Sigma\hat r_b,
\qquad \Theta^2\hat r=-\hat r.
\tag{25}
\]

The modes now come in partners. The transformation exchanges their positions with a relative minus sign and reverses their momenta at the same time. Applying it twice reverses every canonical operator. The first relation in (24) pairs the coefficients within the two groups, while the second fixes the allowed couplings between them. These couplings can have real parts, so the nonpositivity test uses the full matrix \(\operatorname{Re}H\), including its off-diagonal blocks.

Both families share the same physical meaning of the inequality. When the canonical coordinates are Hermitian, the Hermitian part of \(\hat h\) is
\(\frac12\hat r^{\mathsf T}(\operatorname{Re}H)\hat r\).
For \(\operatorname{Re}H\leq0\), this is a sum of negative squares of Hermitian linear combinations of positions and momenta. The exponential of this Hermitian part suppresses high-energy states of the corresponding nonnegative quadratic Hamiltonian, as in imaginary-time evolution. The imaginary coefficients give the anti-Hermitian part of \(\hat h\), which generates unitary evolution. The two families differ in how conjugation organizes these coefficients, through momentum reversal or through an exchange of paired modes. The matrix criteria themselves require only the canonical commutators, so they also apply when the coordinates carry a transformed adjoint relation.

### Direct proof of both theorems

First apply the stated anti-linear transformation to \(\hat h\). In Theorem 1, coefficient conjugation and momentum reversal give exactly the real and imaginary block conditions in (21). In Theorem 2, substitution of (25) changes the diagonal blocks to
\(\Sigma\overline{H_{cc}}\Sigma\) and
\(\Sigma\overline{H_{bb}}\Sigma\), and the upper off-diagonal block to
\(-\Sigma H_{bc}^{\dagger}\Sigma\).
Thus (24) gives \(\Theta\hat h=\hat h\). The same transformation leaves every ordered product of the quadratic factors invariant.

Next derive the propagation and contraction directly from the commutators. Symmetry of \(H\) gives
\[
[\hat h,\hat r_\mu]
=\frac{\mathrm i}{2}\sum_{\nu,\lambda}H_{\nu\lambda}
\bigl(\hat r_\nu\Omega_{\lambda\mu}
+\Omega_{\nu\mu}\hat r_\lambda\bigr)
=-\mathrm i(\Omega H\hat r)_\mu.
\tag{26}
\]
Exponentiating this linear equation yields (20). Since
\((\mathrm i\Omega H)^{\mathsf T}\Omega+\Omega(\mathrm i\Omega H)=0\),
the propagation preserves \(M(t)^{\mathsf T}\Omega M(t)=\Omega\), as required by the canonical commutators. Its contraction follows from
\[
\begin{aligned}
\frac{\mathrm d}{\mathrm dt}
\bigl[M(t)^\dagger(\mathrm i\Omega)M(t)\bigr]
&=M(t)^\dagger(H+H^\dagger)M(t)\\
&=2M(t)^\dagger(\operatorname{Re}H)M(t)\leq0.
\end{aligned}
\tag{27}
\]
Integration from \(M(0)=I\) proves \(M(t)^\dagger(\mathrm i\Omega)M(t)\leq\mathrm i\Omega\).

Finally, if two propagation matrices satisfy this inequality, then
\[
\begin{aligned}
&(M_1M_2)^\dagger(\mathrm i\Omega)(M_1M_2)-\mathrm i\Omega\\
&\quad=M_2^\dagger
\bigl[M_1^\dagger(\mathrm i\Omega)M_1-\mathrm i\Omega\bigr]M_2
+M_2^\dagger(\mathrm i\Omega)M_2-\mathrm i\Omega
\leq0.
\end{aligned}
\tag{28}
\]
The canonical relations and the common anti-linear symmetry are also preserved by multiplication. This proves the semigroup property for each family, including factors whose generators do not commute. If \(\operatorname{Re}H<0\), (27) gives strict contraction for every \(t>0\). The choice \(H=-I\) satisfies both theorems and supplies a strict contraction in either family.
