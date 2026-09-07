# Canonical bosonic coordinates, time reversal, and imaginary-time damping

Auxiliary-field quantum Monte Carlo assigns a configuration weight to an ordered product of quadratic propagators. For bosons, the unbounded occupation of each mode makes imaginary-time damping central to this construction. A useful sign-free criterion must keep the weight real and control the evolution that could reach a bosonic pole. Canonical position and momentum coordinates make these two roles transparent.

The canonical algebra also permits more freedom than a unitary change of single-particle orbitals. Creation and annihilation operators can be recombined while preserving their commutators. This freedom reveals an additional bosonic anti-linear transformation and brings the contraction conditions into a form with a direct physical interpretation.

## 1. Creation operators and the choice of coordinates

Let \(\hat a_j,\hat a_j^+\) obey
\[
[\hat a_j,\hat a_k^+]=\delta_{jk},\qquad
[\hat a_j,\hat a_k]=[\hat a_j^+,\hat a_k^+]=0.
\tag{1}
\]
The superscript \(+\) identifies the canonical creation partner. In the usual Fock representation we choose \(\hat a_j^+=\hat a_j^\dagger\). The symbol \(\dagger\) always denotes the Hilbert-space adjoint.

A simple rescaling shows why it is useful to keep the two symbols distinct. Starting with an ordinary Fock pair, take real \(s\) and define
\[
\hat a'=\mathrm e^s\hat a,\qquad
\hat a'{}^+=\mathrm e^{-s}\hat a^+.
\]
Then
\[
[\hat a',\hat a'{}^+]=1,\qquad
(\hat a')^\dagger=\mathrm e^s\hat a^+
=\mathrm e^{2s}\hat a'{}^+.
\tag{2}
\]
The commutator is unchanged, and the adjoint relation has acquired a scale factor. The same rescaling preserves the fermionic anticommutator. Gaussian operator identities can therefore be derived using canonical pairs, with the adjoint relation specified when a physical representation is chosen.

Introduce
\[
\hat x=\frac{\hat a+\hat a^+}{\sqrt2},\qquad
\hat p=\frac{\hat a-\hat a^+}{\mathrm i\sqrt2}.
\tag{3}
\]
They obey \([\hat x_j,\hat p_k]=\mathrm i\delta_{jk}\). When \(\hat a^+=\hat a^\dagger\), they are Hermitian position and momentum operators. After a complex canonical change, they remain canonical coordinates and carry the transformed adjoint relation. Throughout the derivation, \(+\) is retained for creation operators.

## 2. Quadratic evolution in position and momentum

Collect the operators into columns,
\[
\hat\chi=\binom{\hat a}{\hat a^+},\qquad
\hat r=\binom{\hat x}{\hat p}=Q\hat\chi,\qquad
Q=\frac1{\sqrt2}
\begin{pmatrix}I&I\\-\mathrm iI&\mathrm iI\end{pmatrix}.
\tag{4}
\]
In these block matrices, \(I\) is the identity for the \(N\) modes. The commutators are
\[
[\hat r_\mu,\hat r_\nu]=\mathrm i\Omega_{\mu\nu},\qquad
\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix}.
\]
In the Nambu convention \(g=-\Omega\), a quadratic generator has the equivalent forms
\[
\hat h=\frac12\hat\chi^{\mathsf T}gA\hat\chi
=\frac12\hat r^{\mathsf T}H\hat r,\qquad
B=QAQ^\dagger,\qquad H=\mathrm i\Omega B.
\tag{5}
\]
The matrices \(A\) and \(B\) describe one-body propagation in the two bases. The matrix \(H\) contains the coefficients of the quadratic operator. Substitution of \(Q\) gives
\[
gA+A^{\mathsf T}g=0
\quad\Longleftrightarrow\quad
B^{\mathsf T}\Omega+\Omega B=0
\quad\Longleftrightarrow\quad H^{\mathsf T}=H.
\tag{6}
\]
Thus all allowed quadratic coefficients are contained in a complex symmetric \(H\). With Hermitian quadratures, its real part supplies the coefficients of the Hermitian part of \(\hat h\).

The sign convention is fixed by one damped mode in the usual Fock representation. For \(\kappa>0\),
\[
H=-\kappa I,\qquad
\hat h=-\frac{\kappa}{2}(\hat x^2+\hat p^2)
=-\kappa(\hat a^+\hat a+\tfrac12),
\qquad
\operatorname{Tr}\mathrm e^{\hat h}
=\frac1{2\sinh(\kappa/2)}>0.
\tag{7}
\]
The exponent suppresses states with large occupation. Its propagation matrix nevertheless has eigenvalues \(\mathrm e^\kappa\) and \(\mathrm e^{-\kappa}\). These reciprocal eigenvalues reflect the canonical relation between creation and annihilation operators. A useful matrix contraction criterion must accommodate both directions.

For several slices, write \(M=\mathrm e^{B_1}\cdots\mathrm e^{B_L}\). The Gaussian weight is
\[
w=\operatorname{Tr}\bigl(\mathrm e^{\hat h_1}\cdots\mathrm e^{\hat h_L}\bigr)
=\bigl[(-1)^N\det(I-M)\bigr]^{-1/2}.
\tag{8}
\]
This expression agrees with the Fock trace where it converges. The ordered operators fix the square-root branch, and \(\det(I-M)=0\) locates its poles. The damped oscillator supplies a positive reference from which that branch can be followed.

## 3. Two kinds of bosonic anti-linear transformation

An anti-linear transformation conjugates numerical coefficients and acts on the canonical operators as
\[
\Theta\hat\chi=U\hat\chi,\qquad
\Theta(c\hat d)=\overline c\,\Theta\hat d.
\]
Preservation of the canonical algebra requires \(U^{\mathsf T}gU=g\). In quadrature coordinates,
\[
R=\overline Q\,UQ^\dagger,\qquad
\Theta\hat r=R\hat r,\qquad
R^{\mathsf T}\Omega R=-\Omega.
\tag{9}
\]
The bar on \(Q\) follows from anti-linearity. The minus sign in the last equation accounts for \(\Theta(\mathrm i)=-\mathrm i\).

To compare the action on annihilation and creation operators, introduce the exchange matrix
\[
C=\begin{pmatrix}0&I\\I&0\end{pmatrix}.
\]
The two possibilities of interest are
\[
\begin{array}{c|c}
\text{First kind}&C\overline U C=U\\
\text{Second kind}&C\overline U C=-U.
\end{array}
\tag{10}
\]
In a usual Fock basis, the first kind preserves the adjoint relation. It can describe a physical antiunitary time reversal. The second kind is an anti-linear transformation of the canonical algebra. In that same Fock basis, the image of \(\hat a^+\) under a second-kind map is minus the adjoint of the image of \(\hat a\). Its use is to constrain quadratic generators algebraically.

Equation (9) makes this distinction concrete,
\[
C\overline U C=U\ \Longleftrightarrow\ \overline R=R,
\qquad
C\overline U C=-U\ \Longleftrightarrow\ \overline R=-R.
\tag{11}
\]
First-kind transformations have real quadrature matrices. Second-kind transformations have \(R=\mathrm iV\), where \(V\) is real and obeys \(V^{\mathsf T}\Omega V=\Omega\). The two types are compatible with the bosonic commutators.

The simplest second-kind example is
\[
U=\mathrm iC,\qquad
\Theta\hat a=\mathrm i\hat a^+,\qquad
\Theta\hat a^+=\mathrm i\hat a,\qquad
R=\mathrm iI.
\tag{12}
\]
Indeed,
\[
[\mathrm i\hat a^+,\mathrm i\hat a]
=-[\hat a^+,\hat a]=1,\qquad
U^{\mathsf T}gU=g.
\]
The exchange of the operators reverses a bosonic commutator, and the two factors of \(\mathrm i\) supply the compensating minus sign.

The Hilbert-space meaning follows from the chosen adjoint relation. For example, start with Hermitian position and momentum and form the canonical pair
\[
\hat a'=\hat x,\qquad \hat a'{}^+=-\mathrm i\hat p,\qquad
[\hat a',\hat a'{}^+]=1.
\]
A physical antiunitary that exchanges \(\hat x\) and \(\hat p\) acts as
\(\Theta\hat a'=\mathrm i\hat a'{}^+\) and
\(\Theta\hat a'{}^+=\mathrm i\hat a'\).
It is therefore of the second kind in this basis. The actual adjoints are
\((\hat a')^\dagger=\hat a'\) and
\((\hat a'{}^+)^\dagger=-\hat a'{}^+\).
This example shows how a physical antiunitary can acquire the second-kind form when expressed through canonical partners with a different adjoint relation.

For fermions, the canonical matrix is \(g_{\rm F}=C\). The same proposed second-kind condition gives
\[
\overline U=-CUC,\qquad
U^{\mathsf T}CU=C
\quad\Longrightarrow\quad
U^\dagger U=-CU^{\mathsf T}CU=-I.
\tag{13}
\]
A numerical matrix \(U^\dagger U\) is positive semidefinite, so these conditions are incompatible. This argument does not require a separate assumption that \(U\) is unitary. For one mode the obstruction is already visible in
\(\{\mathrm i\hat a^+,\mathrm i\hat a\}=-1\).
The second kind is therefore a specifically bosonic possibility.

The square of an anti-linear map is determined separately by \(\overline U U\). For example, (12) has \(\Theta^2=+I\). The distinction in (10) records its behavior under creation-annihilation conjugation and should be kept separate from the sign of its square.

## 4. The second kind separates damping from reversible evolution

The transformation \(R_2=\mathrm iI\) has a direct use in imaginary-time evolution. Under a canonical anti-linear transformation, the quadratic coefficient changes as
\[
H\ \longmapsto\ R_2^{\mathsf T}\overline H R_2=-\overline H.
\tag{14}
\]
It fixes the imaginary part of \(H\) and reverses its real part. With Hermitian quadratures, these are precisely the two familiar pieces of a quadratic generator,
\[
\hat h=
\frac12\hat r^{\mathsf T}(\operatorname{Re}H)\hat r
+\frac{\mathrm i}{2}\hat r^{\mathsf T}(\operatorname{Im}H)\hat r.
\tag{15}
\]
The second term generates unitary evolution. A negative real part supplies damping.

The matrix relation \(H=\mathrm i\Omega B\) identifies the contraction matrix \(E=\mathrm i\Omega\). It is Hermitian and satisfies \(E^2=I\). Its contraction inequality becomes
\[
\boxed{
EB+B^\dagger E
=H+H^\dagger
=2\operatorname{Re}H\leq0.
}
\tag{16}
\]
Thus the matrix condition is simply a negative-semidefinite real quadratic form. Strict negativity confines all quadrature directions, as in (7).

This also explains the group and cone terminology. The imaginary part of \(H\) can have either sign and gives reversible evolution. The allowed real part is restricted to the negative cone. Reversing it would amplify the same oscillator states. In terms of propagation matrices,
\[
B_{\rm group}=\frac{B+\overline B}{2},\qquad
B_{\rm cone}=\frac{B-\overline B}{2}.
\tag{17}
\]
The map \(R_2=\mathrm iI\) is a symmetry of the group part and changes the sign of the cone part. For the oscillator in (7), it sends \(\hat h\) to \(-\hat h\).

The inequality survives multiplication of slices. For a single slice,
\[
\frac{\mathrm d}{\mathrm dt}
\left(\mathrm e^{tB^\dagger}E\mathrm e^{tB}\right)
=\mathrm e^{tB^\dagger}(H+H^\dagger)\mathrm e^{tB}\leq0.
\]
Hence \(\mathrm e^{B^\dagger}E\mathrm e^B\leq E\), and inserting successive slices preserves this inequality. With strict contraction in one slice, the complete product has no eigenvalue \(+1\), so the Gaussian weight encounters no pole. A symmetry that keeps the weight real then lets its positive reference sign extend throughout a connected contracting domain.

## 5. Two choices for the symmetry of the complete evolution

Let \(R_1\) impose the symmetry of every slice,
\[
R_1^{-1}\overline B R_1=B
\quad\Longleftrightarrow\quad
R_1^{\mathsf T}\overline H R_1=H.
\tag{18}
\]
The contraction construction uses two anticommuting anti-linear maps. Once \(R_2=\mathrm iI\), their anticommutation gives
\[
\overline R_2R_1+\overline R_1R_2
=-\mathrm iR_1+\mathrm i\overline R_1=0.
\]
Consequently \(R_1\) is real and belongs to the first kind. In the orthogonal representatives used below, its square can be \(+I\) or \(-I\).

### A symmetry that squares to \(+I\)

The familiar choice is complex conjugation in the occupation basis,
\[
\Theta_1\hat a=\hat a,\qquad
\Theta_1\hat x=\hat x,\qquad
\Theta_1\hat p=-\hat p,\qquad
R_1=\begin{pmatrix}I&0\\0&-I\end{pmatrix}.
\tag{19}
\]
Equation (18) makes the \(xx\) and \(pp\) coefficients real and the \(xp\) coefficients imaginary. One mode illustrates the complete construction,
\[
\hat h=
-\frac{\kappa_x}{2}\hat x^2
-\frac{\kappa_p}{2}\hat p^2
+\frac{\mathrm i\lambda}{2}(\hat x\hat p+\hat p\hat x),
\qquad
\kappa_x,\kappa_p>0,\quad \lambda\in\mathbb R.
\tag{20}
\]
The first two terms suppress large position and momentum fluctuations. The last term generates a unitary squeezing operation and can have either sign. Under \(\Theta_1\), both \(\mathrm i\) and \(\hat p\) reverse sign, leaving this term invariant. Every slice therefore combines damping with the same reality symmetry.

For many modes, the positive coefficients in (20) become real positive-definite matrices, and the \(xp\) mixing is an arbitrary real matrix with the required transposed partner. The physical interpretation is unchanged.

### A symmetry that squares to \(-I\)

For an even number of modes, organize them into doublets \((\hat b_j,\hat c_j)\) and take
\[
\Theta_1\hat b_j=\hat c_j,\qquad
\Theta_1\hat c_j=-\hat b_j.
\tag{21}
\]
The creation operators transform in the same way. Applying the map twice gives a minus sign, as for a Kramers pair. In quadrature coordinates,
\[
R_1=\begin{pmatrix}\mathcal J&0\\0&-\mathcal J\end{pmatrix},
\qquad
\mathcal J=\begin{pmatrix}0&I\\-I&0\end{pmatrix}.
\tag{22}
\]
Here the identities in \(\mathcal J\) act on the doublet labels. The lower-block sign again comes from the factor of \(\mathrm i\) in momentum.

A simple doublet shows how complex contributions are paired,
\[
\hat h=-\kappa(\hat b^+\hat b+\hat c^+\hat c+1)
+\mathrm i\lambda(\hat b^+\hat b-\hat c^+\hat c),
\qquad \kappa>0,\quad \lambda\in\mathbb R.
\tag{23}
\]
The imaginary phases of the two modes have opposite signs, while their damping is identical. The trace is
\[
w=\frac{1}
{4\left|\sinh[(\kappa-\mathrm i\lambda)/2]\right|^2}>0.
\tag{24}
\]
General pairing terms and noncommuting slices are included by imposing (18) together with (16). The contraction condition remains part of the criterion.

Both families contain the positive reference \(H=-\kappa I\). Interpolating every slice toward this reference preserves the symmetry and the nonpositive real part. An originally strict slice stays strict. The Gaussian branch remains real and encounters no pole, so its sign stays positive. The two families differ in whether the reality symmetry acts on individual canonical modes or on Kramers doublets.

## 6. How the eight Nambu cases acquire these forms

The Nambu enumeration uses real orthogonal matrices \(J_1,J_2\). The first imposes \(J_1^{\mathsf T}AJ_1=\overline A\), and the second constructs the Hermitian matrix \(\eta\) in the contraction condition \(\eta A+A^\dagger\eta\leq0\). The corresponding canonical anti-linear matrices are
\[
U_j=
\begin{cases}
J_j,&J_j^{\mathsf T}gJ_j=g,\\
\mathrm iJ_j,&J_j^{\mathsf T}gJ_j=-g.
\end{cases}
\tag{25}
\]
The phase preserves \(U_j^{\mathsf T}gU_j=g\). It also keeps the square \(\overline U_jU_j=J_j^2\). The eight cases with a nonzero contraction cone all have \(J_2^2=I\), and their two induced anti-linear maps anticommute.

Under (4), the contraction matrix and anti-linear matrices obey
\[
E=Q\eta Q^\dagger=-\overline R_2\Omega,\qquad
R_j=\overline Q\,U_jQ^\dagger.
\tag{26}
\]
The first-kind or second-kind property can be checked directly through \(C\overline U_jC=\pm U_j\). For example, the one-mode representative \(J_1=I,\ J_2=C\) has \(U_1=I,\ U_2=\mathrm iC\). It combines the reality symmetry and damping illustrated in (19)-(20).

A canonical change of coordinates brings the general contraction matrix in (26) to \(E=\mathrm i\Omega\). Equation (26) then fixes \(R_2=\mathrm iI\), and the anticommutation calculation below (18) makes \(R_1\) real. A final choice of canonical pairs reduces \(R_1\) to (19) or (22). An explicit coordinate construction is given in the Appendix.

The eight cases group as follows, with cell labels taken from the [companion contraction-semigroup table](../pdf/ContractionSemigroupsQMC.pdf).

| Square of the first map | Nambu cells | Standard reality symmetry |
|---|---|---|
| \(J_1^2=+I\) | B02, B05, B17, B22 | Equation (19) |
| \(J_1^2=-I\) | B10, B13, B25, B30 | Equation (22) |

Both use the second-kind map \(R_2=\mathrm iI\) to define damping. The two kinds in (10) and the two rows of this table answer different classification questions. The former describe a map's action on creation-annihilation conjugation. The latter describe the square of the symmetry that fixes the complete evolution.

The coordinate changes used for this grouping can be complex. They preserve the canonical algebra, the contraction inequality, and the ordered matrix products. The transformed \(+\) operators retain the adjoint relation inherited from the original operators, as in (2). If the displayed standard forms are realized directly with Hermitian \(x,p\), inequality (16) has the literal damping interpretation used in Secs. 4 and 5. For a transformed operator basis, the same Gaussian operator and its original adjoint relation are carried along.

This separation of roles clarifies the bosonic extension of the [fermionic semigroup construction](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.110.075146/fulltext). The first map makes the configuration weight real. The second-kind bosonic map separates reversible quadratic evolution from imaginary-time damping, and the contraction inequality preserves the positive Gaussian branch. The resulting two families include paired evolution and connect the algebraic classification directly to the suppression of large bosonic occupations.

## Appendix. Choosing coordinates adapted to the contraction condition

The purpose of the coordinate choice is to turn \(EB+B^\dagger E\leq0\) into the energy-coefficient condition (16). A matrix \(P\) preserves the quadrature commutators when \(P^{\mathsf T}\Omega P=\Omega\). We can also choose \(P^\dagger P=I\), so that
\[
B'=PBP^\dagger,\qquad E'=PEP^\dagger,\qquad
R_j'=\overline P R_jP^\dagger
\tag{27}
\]
preserve the contraction inequality by ordinary unitary conjugation.

For the eight contraction cases, \(E\) is Hermitian and satisfies
\[
E^2=I,\qquad E^{\mathsf T}\Omega+\Omega E=0.
\]
Its positive and negative eigenvectors occur in canonical pairs. If \(Ev=v\), then
\[
E(-\Omega\overline v)=-(-\Omega\overline v).
\]
Choose orthonormal positive eigenvectors as the columns of \(V_+\). Their partners form the remaining columns of
\[
V=(V_+,-\Omega\overline V_+),\qquad
V^\dagger V=I,\qquad V^{\mathsf T}\Omega V=\Omega.
\tag{28}
\]
The canonical relation between the two sets follows from
\(V_+^{\mathsf T}\Omega V_+=0\).
Thus \(V^\dagger\) preserves the commutators and sends \(E\) to
\[
D=\begin{pmatrix}I&0\\0&-I\end{pmatrix}.
\]
One final fixed change gives the desired damping matrix,
\[
P_0=\frac1{\sqrt2}
\begin{pmatrix}I&-\mathrm iI\\-\mathrm iI&I\end{pmatrix},
\qquad
P_0DP_0^\dagger=\mathrm i\Omega,\qquad
P=P_0V^\dagger.
\tag{29}
\]
Equations (26)-(27) then give \(R_2'=\mathrm iI\).

The remaining map \(R_1'\) is real and orthogonal, with
\(R_1'{}^{\mathsf T}\Omega R_1'=-\Omega\).
For square \(+I\), choose its \(+1\) eigenvectors as position directions. Their canonical partners have eigenvalue \(-1\), giving (19). For square \(-I\), a vector and its image under \(R_1'\) form a pair. Taking their momentum partners produces a four-dimensional block with the action in (22). Repeating this construction exhausts the modes. These final changes are real, orthogonal, and canonical, so they preserve \(E=\mathrm i\Omega\) and \(R_2=\mathrm iI\).

The complete change preserves \(\det(I-M)\) and the same ordered Gaussian branch. It need not preserve the original identification of every canonical coordinate as a Hermitian observable. Keeping the inherited adjoint relation makes the operator interpretation consistent throughout.
