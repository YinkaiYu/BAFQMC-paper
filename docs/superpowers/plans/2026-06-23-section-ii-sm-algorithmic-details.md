# Section II and SM Algorithmic Details Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise Sec. II and the Supplemental Material so the BAFQMC trace formulas, update ratios, branch discussion, and stabilization algorithms are physically readable, implementation-faithful, and reproducible.

**Architecture:** Keep the main text concise and PRL-like, while moving detailed derivations and algorithmic details into the SM. Treat the number-conserving and paired algorithms separately, because the former uses conjugate flavor sectors and an ordinary inverse determinant, while the latter uses Nambu matrices and a square-root determinant branch. Cross-check every implementation-backed statement against the two benchmark code repositories before writing it into the manuscript.

**Tech Stack:** REVTeX 4.2 LaTeX (`main.tex`, `SM.tex`), BibTeX (`references.bib`, existing `rubenstein2012pra` key), `latexmk main.tex`, `latexpand`, `latexdiff`, `rg`, `git`, and read-only subagents for code-repository inspection.

---

## File Structure

- Modify `main.tex:124-132` to shorten the HS-measure sentence and remove the explicit "real continuous fields" aside from the main text.
- Modify `SM.tex:111-141` to rewrite the number-conserving trace derivation in a physics-reader-friendly way, cite the existing `rubenstein2012pra` reference where useful, and remove the unexplained scalar-factor paragraph.
- Modify `SM.tex:175-248` to expand the number-conserving local-update benchmark algorithm: explicit HS-decoupled slice generators, conjugate flavor relation, determinant ratios, Green-function reconstruction, and one-sector implementation consequence.
- Modify `SM.tex:241-248` and likely extend that subsection to explain number-conserving stabilization: cyclic Green propagation, `N_{\rm wrap}`, segment products, UDV/QR decomposition, and stabilized inversion.
- Modify `SM.tex:313-350` to keep the paired trace branch discussion in the trace-formula subsection and remove premature local-update notation, phase diagnostics, phase reweighting, and any algorithmic step not used in the actual calculation.
- Modify `SM.tex:386-495` to use the existing local-update symbol `\Delta_\ell`, define it before discussing branch continuation, remove the artificial `s`-scan language, rewrite the paired local block with explicit sums, and remove finite-precision implementation diagnostics that are not reader-facing physics algorithm.
- Modify `SM.tex:497-500` and likely extend that subsection to explain paired/Nambu stabilization in the same concrete style as the number-conserving case, after inspecting the pairing code.
- Modify `SM.tex:806-824` only if needed to keep benchmark numerical details consistent after the algorithm sections are expanded.
- Modify `.codex/skills/bafqmc-prl-revision/SKILL.md` to add generalized rules learned from this round: derive before stating, do not invent algorithmic steps, do not insert implementation diagnostics unless reader-facing, and explain stabilization as a reproducible physical algorithm.
- Do not modify `references.bib` unless execution finds that `rubenstein2012pra` metadata is wrong. The current key already exists with DOI `10.1103/PhysRevA.86.053606` and arXiv `1209.0186`.

## Task 1: Source Study and Implementation Reconnaissance

**Files:**
- Read only: `references.bib`
- Read only: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC`
- Read only: `/mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC_paring`
- Read only: PhysRevA 86, 053606 / arXiv:1209.0186

- [ ] **Step 1: Re-read the external bosonic AFQMC reference**

Use the primary source already cited in the manuscript:

```bash
python - <<'PY'
print("Primary source to inspect:")
print("https://arxiv.org/pdf/1209.0186")
print("Focus: Appendix A for the boson determinant trace formula and Appendix B for local updates/stabilization.")
PY
```

Expected: The command prints the source URL and focus areas. In the manuscript rewrite, use the source as a guide for reader-friendly exposition, but do not copy its prose. The key physics points to carry forward are:

```text
Appendix A derives the bosonic determinant trace by expanding the bosonic trace in occupation-number sectors and summing the resulting geometric series in the stable region.
Appendix B explains local Green-function updates and uses the bosonic sign change in the stabilized inversion, with the schematic identity
G_b=[I-UDV]^{-1}=V^{-1}[U^{-1}V^{-1}-D]^{-1}U^{-1}.
```

- [ ] **Step 2: Dispatch the number-conserving code-repo subagent**

Prompt a read-only subagent with this exact task:

```text
Inspect /mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC for the number-conserving BAFQMC benchmark. Do not edit files. Summarize the physics algorithm, not code style: HS fields and coefficients, the exact slice generators for b and c particles after HS decoupling, why b and c one-body matrices are complex conjugates, the determinant ratio used for U1 and U2 local proposals, the Green-function update/reconstruction relation, initialization, local proposal shift, warmup rule, Nwrap, QR/UDV stabilization, and the formula used to recompute G=(I-B)^{-1}. Give file/function references and concrete parameter values from the publication report.
```

Expected: A summary with file/function references and no edits. It must explicitly confirm whether only the `b`-sector matrix algebra is needed in production and how the `c` sector is reconstructed.

- [ ] **Step 3: Dispatch the paired/Nambu code-repo subagent**

Prompt a read-only subagent with this exact task:

```text
Inspect /mnt/c/Users/Newton/Documents/LigroupIOP/2408_bosonSignProblem/code_bosonDQMC_paring for the finite-pairing BAFQMC benchmark. Do not edit files. Summarize the physics algorithm, not code style: Nambu basis, exact density-HS slice matrix, normal-ordering scalar, local determinant-ratio formula, whether the code uses Delta_l or another update notation, initialization, local proposal shift, warmup rule, Nwrap, QR/UDV stabilization, how the Nambu resolvent (I-M)^{-1} is recomputed, whether any structure-preserving symplectic factorization is actually used, and the publication-report parameter values. Give file/function references.
```

Expected: A summary with file/function references and no edits. It must state whether the code truly preserves symplectic structure numerically or instead computes the same exact symplectic product through ordinary stabilized matrix factorizations.

- [ ] **Step 4: Record execution constraints for the edit**

Before editing, run:

```bash
git status --short
rg -n "rubenstein2012pra|PhysRevA.86.053606|1209.0186" references.bib main.tex SM.tex
```

Expected: `git status --short` may show ignored/generated local files, but no tracked dirty files unrelated to this task. The reference scan should show `references.bib` already contains `rubenstein2012pra`, and `main.tex` already cites it.

## Task 2: Main-Text Sec. II HS Measure Cleanup

**Files:**
- Modify: `main.tex:124-132`

- [ ] **Step 1: Replace the two-sentence HS-measure explanation**

Replace the current sentence pair:

```tex
Here $\ell$ labels the spacetime auxiliary-field variables generated by the Trotter and HS decomposition, and $P_{\rm HS}$ is the product of the Gaussian factors introduced by the HS transformation. For the real continuous fields used here, $P_{\rm HS}(\phi)=\prod_\ell(2\pi)^{-1/2}\ee^{-\phi_\ell^2/2}$.
```

with:

```tex
Here $\ell$ labels the spacetime auxiliary-field variables generated by the Trotter and HS decomposition, and $P_{\rm HS}(\phi)=\prod_{\ell}\frac{1}{\sqrt{2\pi}}\ee^{-\frac12\phi_{\ell}^{2}}$ is the product of the Gaussian factors introduced by the HS transformation.
```

- [ ] **Step 2: Verify the main-text wording**

Run:

```bash
rg -n "real continuous fields|P_\\{\\\\rm HS\\} is the product|P_\\{\\\\rm HS\\}\\(\\\\phi\\)=\\\\prod_\\\\ell" main.tex
```

Expected: no match for "real continuous fields" or the old split wording. A match for the new single-sentence `P_{\rm HS}(\phi)=\prod_{\ell}` wording is expected.

## Task 3: Reader-Friendly Number-Conserving Trace Formula

**Files:**
- Modify: `SM.tex:111-141`

- [ ] **Step 1: Rewrite the trace-formula derivation**

Replace the current dense analytic-continuation discussion with a two-layer derivation:

```tex
Consider first the one-mode operator $\hat U(\varepsilon)=\exp(\varepsilon \hat a^+\hat a)$. In the occupation-number basis,
\begin{equation}
    \Tr\,\hat U(\varepsilon)
    =
    \sum_{n=0}^{\infty}\ee^{n\varepsilon}
    =
    \frac{1}{1-\ee^{\varepsilon}},
    \qquad |\ee^{\varepsilon}|<1.
\end{equation}
For $N$ independent modes this gives $\prod_m(1-\ee^{\varepsilon_m})^{-1}$. This is the physical content of the bosonic determinant formula: each single-particle eigenmode contributes a geometric occupation-number sum. The same result was used in the finite-temperature bosonic AFQMC construction of Ref.~\cite{rubenstein2012pra}.

For a general matrix $C$, the coherent-state calculation gives the basis-independent form of the same result. Let $\|z\rangle=\exp(\hat{\bb a}^+z)|0\rangle$ be the unnormalized coherent state. The resolution of identity and overlap are
\begin{equation}
    I=\int\frac{\dd^{2N}z}{\pi^N}\,\ee^{-z^\hc z}\,\|z\rangle\langle z\|,\qquad
    \langle z\|w\rangle=\ee^{z^\hc w}.
\end{equation}
Since $\ee^{\hat{\bb a}^+C\hat{\bb a}}\hat{\bb a}^+\ee^{-\hat{\bb a}^+C\hat{\bb a}}=\hat{\bb a}^+\ee^C$, one has $\hat U(C)\|z\rangle=\|\ee^C z\rangle$. Hence, in the convergent region,
\begin{equation}
    \Tr\,\hat U(C)
    =
    \int\frac{\dd^{2N}z}{\pi^N}
    \exp[-z^\hc(I_N-\ee^C)z]
    =
    \det(I_N-\ee^C)^{-1}.
    \label{eq:number_trace_appendix}
\end{equation}
Convergence means that the Gaussian suppresses large coherent-state amplitudes; a sufficient condition is that the Hermitian part of $I_N-\ee^C$ is positive. Equivalently, in a diagonal stable case all single-particle factors obey $|\ee^{\varepsilon_m}|<1$, so every occupation-number geometric series converges.

Outside this stable region the determinant remains the algebraic continuation of the same geometric sums, but the ordinary Hilbert-space trace need not converge configuration by configuration. The pole occurs when an eigenvalue of $\ee^C$ reaches one. In the AFQMC integral this issue is handled by the Gaussian-cutoff finite-part construction in Sec.~\ref{app:regularization}; the present subsection only derives the trace formula in the convergent region where it is an ordinary trace.
```

This replacement keeps the coherent-state derivation but moves mathematical terminology such as "holomorphic function of the entries" out of the reader's path.

- [ ] **Step 2: Remove the scalar-factor aside**

Replace:

```tex
This is Eq.~\eqref{eq:trace_formula_number}. If scalar factors are kept outside the one-body matrix product, the right-hand side is multiplied by their product. In the main-text convention those factors are included in the auxiliary-field measure unless they arise from the Nambu normal-ordering constant discussed below.
```

with:

```tex
This is Eq.~\eqref{eq:trace_formula_number}.
```

- [ ] **Step 3: Verify trace-section style**

Run:

```bash
rg -n "holomorphic|meromorphic|scalar factors|outside the one-body matrix product|identity theorem" SM.tex
```

Expected: no matches in Sec.~\ref{app:trace_number}. If "meromorphic" remains elsewhere in regularization or semigroup sections, inspect context before changing it.

## Task 4: Number-Conserving Benchmark Update Algorithm

**Files:**
- Modify: `SM.tex:175-240`

- [ ] **Step 1: Adjust the generic Metropolis sentence**

Replace:

```tex
For a symmetric proposal $\phi_{i\ell}\to\phi_{i\ell}'$ in a sign-free number-conserving simulation, the acceptance probability is
```

with:

```tex
For a symmetric proposal $\phi_{i\ell}\to\phi_{i\ell}'$ in our sign-problem-free simulation, the acceptance probability is
```

- [ ] **Step 2: Replace the incorrect "density-channel Hamiltonian" paragraph with an explicit slice generator**

Replace the paragraph beginning:

```tex
For the density-channel Hamiltonian in Eq.~\eqref{eq:benchmark_pairing} at $\Delta=0$, the algorithm can be made more explicit.
```

with a derivation in this form. Use $K$ for the common real hopping and chemical-potential matrix in the benchmark Trotter convention; if Task 1 shows the code separates hopping and chemical potential into two matrices, write their sum as $K$ before the displayed equation:

```tex
For the benchmark Hamiltonian in Eq.~\eqref{eq:benchmark_pairing} at $\Delta=0$, the HS transformations in Eqs.~\eqref{eq:benchmark_hs_total} and~\eqref{eq:benchmark_hs_relative} give a number-conserving slice
\begin{equation}
\begin{aligned}
    \hat h_\ell
    ={}& \sum_{ij}\hat b_i^+K_{ij}\hat b_j
    +\sum_i v_{b,i\ell}\hat n_{b,i} \\
    &+\sum_{ij}\hat c_i^+K_{ij}\hat c_j
    +\sum_i v_{c,i\ell}\hat n_{c,i},
\end{aligned}
\end{equation}
where $K$ contains the hopping and chemical-potential contribution in the chosen Trotter convention, and
\begin{equation}
    v_{b,i\ell}=\alpha_1\phi_{i\ell}+\ii\alpha_2\varphi_{i\ell},
    \qquad
    v_{c,i\ell}=\alpha_1\phi_{i\ell}-\ii\alpha_2\varphi_{i\ell}.
\end{equation}
Thus the $b$ and $c$ onsite fields are complex conjugates. Since the same real hopping and chemical-potential matrix $K$ appears in both sectors, the complete one-body slice matrices satisfy
\begin{equation}
    B_{c,\ell}=\overline{B_{b,\ell}}.
\end{equation}
Consequently the cyclic products and Green functions obey
\begin{equation}
    \mc B_{c,\ell}=\overline{\mc B_{b,\ell}},
    \qquad
    G_{c,\ell}=(I_N-\mc B_{c,\ell})^{-1}
    =\overline{(I_N-\mc B_{b,\ell})^{-1}}
    =\overline{G_{b,\ell}}.
\end{equation}
```

The final text must not say "Since the hopping and chemical-potential terms are real" as the reason for the full relation; it must identify the conjugate HS onsite potentials and then note that the common kinetic/chemical matrix is real in this benchmark convention.

- [ ] **Step 3: Add the one-sector implementation consequence**

After the conjugate Green-function equation, add:

```tex
Therefore the production calculation only needs to carry the $b$-sector stabilized matrix product and Green function explicitly. The $c$-sector determinant ratio, Green function, and local update are obtained by complex conjugation. This reduces the matrix work by a factor of about two without changing the sampled two-flavor weight.
```

- [ ] **Step 4: Expand the local ratio and Green update**

Use the code-repo summary from Task 1 to write the final formula. The intended mathematical structure is:

```tex
A local proposal at site $i$ changes the $b$-sector slice by a diagonal factor $1+\delta_b$ at that site. The single-flavor determinant ratio is
\begin{equation}
    r_b=
    \left[1+\delta_b(1-G_{b,\ell;ii})\right]^{-1}.
\end{equation}
For a $U_1$-field proposal $\phi_{i\ell}\to\phi_{i\ell}'$,
\begin{equation}
    \delta_b=\ee^{\alpha_1(\phi_{i\ell}'-\phi_{i\ell})}-1,
\end{equation}
whereas for a $U_2$-field proposal $\varphi_{i\ell}\to\varphi_{i\ell}'$,
\begin{equation}
    \delta_b=\ee^{\ii\alpha_2(\varphi_{i\ell}'-\varphi_{i\ell})}-1.
\end{equation}
The $c$-sector ratio is $r_c=\overline{r_b}$, so the determinant part of the two-flavor ratio is $|r_b|^2$.
```

Then add the Green update only after verifying the left/right convention against the code. If the code uses the left-update convention already present in `SM.tex`, use:

```tex
\begin{equation}
    G_{b,\ell}'=
    G_{b,\ell}
    -\frac{\delta_b}{1+\delta_b(1-G_{b,\ell;ii})}
    G_{b,\ell}\ket{i}\bra{i}(I_N-G_{b,\ell}),
\end{equation}
```

If the code uses the transpose/right-update convention, use the code-consistent orientation and state the convention in prose.

- [ ] **Step 5: Verify number-conserving update scans**

Run:

```bash
rg -n "density-channel Hamiltonian|Since the hopping and chemical-potential terms are real|only needs to carry the \\$b\\$-sector|G_\\{b,\\\\ell\\}'" SM.tex
```

Expected: no match for the two old phrases. Expected matches for the one-sector implementation consequence and the Green-update formula.

## Task 5: Number-Conserving Stabilization Subsection

**Files:**
- Modify: `SM.tex:241-248`

- [ ] **Step 1: Replace the current short stabilization paragraph**

Replace the existing short subsection with a concrete algorithmic explanation organized as four paragraphs:

```tex
The local-update formulas above are exact algebraic identities, but long imaginary-time products cannot be formed by naive multiplication. At time slice $\ell$ the algorithm works with the cyclic product
\begin{equation}
    \mc B_{b,\ell}=B_{b,\ell}B_{b,\ell+1}\cdots B_{b,L}B_{b,1}\cdots B_{b,\ell-1}
\end{equation}
and the Green function $G_{b,\ell}=(I_N-\mc B_{b,\ell})^{-1}$. During a sweep, accepted local updates are applied by the rank-one formula above. Moving the equal-time cut from slice $\ell$ to $\ell+1$ only cyclically permutes the product, so in exact arithmetic
\begin{equation}
    G_{b,\ell+1}=B_{b,\ell}^{-1}G_{b,\ell}B_{b,\ell}.
\end{equation}
This propagation is used only for short intervals, because roundoff errors grow with repeated multiplication.

The parameter $N_{\rm wrap}$ is the number of time slices between full stabilized recomputations of the Green function. In the reported production runs $N_{\rm wrap}=10$. After every $N_{\rm wrap}$ slices the locally propagated Green function is discarded and recomputed from the stabilized representation of the full cyclic product.

To build that representation, the product is divided into blocks of $N_{\rm wrap}$ slices. Each block product $X$ is factorized by a column-pivoted QR decomposition with separated scales,
\begin{equation}
    XP=UDV,
\end{equation}
where $P$ is a permutation, $U$ is well conditioned, $D$ contains the column scales, and $V$ is the remaining triangular factor. Multiplying blocks in this scaled form keeps exponentially large and small singular directions separate instead of losing them to roundoff.

Once the full cyclic product is represented as $\mc B_{b,\ell}=UDV$, the Green function is computed by solving the equivalent stabilized linear system rather than explicitly forming $UDV$. Following the bosonic version of the standard AFQMC stabilization in Ref.~\cite{rubenstein2012pra},
\begin{equation}
    G_{b,\ell}
    =
    (I_N-UDV)^{-1}
    =
    V^{-1}\left(U^{-1}V^{-1}-D\right)^{-1}U^{-1}.
\end{equation}
The factorization changes only the numerical representation of the same matrix product; it does not alter the AFQMC weight or Green function. The $c$-sector Green function is then reconstructed as $G_{c,\ell}=\overline{G_{b,\ell}}$.
```

Adjust symbols only if Task 1 shows the code uses a different left/right convention. Do not omit the physical meaning of `N_{\rm wrap}`.

- [ ] **Step 2: Verify stabilization scans**

Run:

```bash
rg -n "N_\\{\\\\rm wrap\\}|G_\\{b,\\\\ell\\+1\\}|XP=UDV|I_N-UDV|U\\^{-1\\}V\\^{-1\\}-D" SM.tex
```

Expected: matches for all listed stabilization elements in the number-conserving subsection.

## Task 6: Paired Trace Branch and Update Ratio Cleanup

**Files:**
- Modify: `SM.tex:313-350`
- Modify: `SM.tex:386-495`

- [ ] **Step 1: Remove premature local-update branch language from Sec. III B**

Delete the current paragraph beginning:

```tex
For local Monte Carlo updates, the branch is fixed at the level of the ratio between two nearby configurations.
```

Replace it with a trace-formula branch paragraph that does not introduce `\Gamma_\ell`, `\Delta_\ell`, local ratios, artificial interpolation scans, phase diagnostics, or phase reweighting:

```tex
In the finite-$\Delta$ reflection-positive benchmark, the low-density sampling window stays away from the pole surface $\det(I_{2N}-\mc M)=0$. The square-root branch is therefore the continuation of the stable diagonal branch in Eq.~\eqref{eq:diag_trace_paired} throughout the sampled region. The practical update formula below uses local proposals small enough that the determinant ratio remains on this same branch.
```

- [ ] **Step 2: Restore `\Delta_\ell` as the local update matrix in Sec. III C**

Replace every paired-update occurrence of `\Gamma_\ell` with `\Delta_\ell`, keeping the definition:

```tex
\begin{equation}
    \ee^{A_\ell'}=(I_{2N}+\Delta_\ell)\ee^{A_\ell},\qquad
    \delta\xi_\ell=\xi_\ell'-\xi_\ell.
\end{equation}
```

Then ensure the branch discussion appears only after this definition and after Eq.~\eqref{eq:update_ratio_main}. Use:

```tex
The square root in Eq.~\eqref{eq:update_ratio_main} is the branch connected to the identity update $\Delta_\ell=0$, where the determinant is one and the ratio is one. In the benchmark runs the chemical potential is low enough that sampled configurations remain far from the pole surface, and the local field shifts are small enough that accepted proposals do not cross a square-root branch cut.
```

Do not say the algorithm introduces or scans a continuous parameter `s`.

- [ ] **Step 3: Remove finite-precision phase diagnostics paragraph**

Delete this sentence pair from Sec. III C:

```tex
In finite precision the local square-root ratio is represented as a complex number, so the implementation records its phase as a branch diagnostic and uses the nonnegative representative of the monitored sign-free ratio. In the reported low-density window the recorded phases stay at roundoff scale, so this numerical procedure is equivalent to sampling the nonnegative branch in Eq.~\eqref{eq:paired_metropolis_ratio}.
```

Do not replace it with another implementation-facing diagnostic. The physical branch statement in Step 2 is sufficient.

- [ ] **Step 4: Rewrite the paired local block with an explicit sum**

Replace the local block formula with:

```tex
\begin{equation}
    P_{\rho\sigma}
    =
    \delta_{\rho\sigma}
    +
    \sum_{\tau\in\{b,c,b^+,c^+\}}
    D_{\rho\tau}
    \left[
    \delta_{\tau\sigma}
    -
    \left((I_{2N}-\mc M_\ell)^{-1}\right)_{i\tau,i\sigma}
    \right],
    \label{eq:paired_local_block}
\end{equation}
```

Then define the diagonal matrix `D` immediately below:

```tex
For a local $U_1$ update $\phi_{i\ell}\to\phi_{i\ell}'$ with $\delta\lambda_1=\alpha_1(\phi_{i\ell}'-\phi_{i\ell})$,
\begin{equation}
    D=\diag(\ee^{\delta\lambda_1}-1,\ee^{\delta\lambda_1}-1,\ee^{-\delta\lambda_1}-1,\ee^{-\delta\lambda_1}-1),
\end{equation}
while for a local $U_2$ update $\varphi_{i\ell}\to\varphi_{i\ell}'$ with $\delta\lambda_2=\ii\alpha_2(\varphi_{i\ell}'-\varphi_{i\ell})$,
\begin{equation}
    D=\diag(\ee^{\delta\lambda_2}-1,\ee^{-\delta\lambda_2}-1,\ee^{-\delta\lambda_2}-1,\ee^{\delta\lambda_2}-1).
\end{equation}
```

This avoids an implicit Einstein-summation reading and keeps the local block explicit.

- [ ] **Step 5: Verify paired branch/update scans**

Run:

```bash
rg -n "Gamma_\\ell|s\\\\Gamma|s\\\\Delta|phase diagnostic|phase reweighting|finite precision|records its phase|D=\\\\diag|sum_\\{\\\\tau" SM.tex
```

Expected: no matches for `Gamma_\ell`, `s\Gamma`, `s\Delta`, `phase diagnostic`, `phase reweighting`, `finite precision`, or `records its phase`. Expected matches for `D=\diag` and `\sum_{\tau`.

## Task 7: Paired/Nambu Stabilization Subsection

**Files:**
- Modify: `SM.tex:497-500`

- [ ] **Step 1: Replace the current paired stabilization paragraph**

Write the paired stabilization subsection only after reading the paired code summary from Task 1. If the code uses ordinary pivoted QR/scaled products rather than a structure-preserving symplectic factorization, write this truthfully:

```tex
The paired calculation stabilizes the full Nambu product in the same spirit as the number-conserving calculation, but the matrices now act on the $(\hat{\bb b},\hat{\bb c},\hat{\bb b}^+,\hat{\bb c}^+)^\trans$ space. For a cut at time slice $\ell$ the relevant cyclic product is
\begin{equation}
    \mc M_\ell=M_\ell M_{\ell+1}\cdots M_LM_1\cdots M_{\ell-1},
\end{equation}
where $M_\ell=\ee^{A_\ell}$. The local-update formula requires the resolvent $(I_{2N}-\mc M_\ell)^{-1}$, not the raw product alone.

Between stabilized recomputations, accepted local updates are applied to the Green/resolvent by the low-rank formula implied by Eq.~\eqref{eq:update_ratio_main}, and the equal-time cut is propagated by cyclic permutation of the Nambu slice matrices. As in the number-conserving case, this propagation is exact in algebra but accumulates roundoff error.

The production runs therefore recompute the Nambu resolvent every $N_{\rm wrap}=10$ slices. The product is divided into $N_{\rm wrap}$-slice blocks, and each block product is stored in a pivoted-QR form with separated scales. These factorizations do not change the underlying symplectic one-body evolution; they are numerically equivalent representations of the same product used to solve the linear system for $(I_{2N}-\mc M_\ell)^{-1}$ without forming an ill-conditioned product explicitly.
```

If Task 1 confirms a genuinely structure-preserving symplectic factorization, replace the last paragraph with the exact factorization used in the code and state how it preserves the symplectic constraint. Do not claim symplectic preservation by QR unless the code actually enforces it.

- [ ] **Step 2: Verify paired stabilization scans**

Run:

```bash
rg -n "full Nambu product|M_\\ell=\\\\ee\\^\\{A_\\ell\\}|N_\\{\\\\rm wrap\\}=10|symplectic|pivoted-QR" SM.tex
```

Expected: matches in the paired stabilization subsection. Inspect every `symplectic` occurrence to ensure it does not overclaim the numerical factorization.

## Task 8: Benchmark Numerical Details Consistency

**Files:**
- Modify: `SM.tex:803-826`

- [ ] **Step 1: Keep benchmark details aligned with expanded algorithms**

After Tasks 4, 5, 6, and 7, inspect `SM.tex:803-826` and ensure it still states:

```tex
All BAFQMC benchmarks are grand-canonical simulations of $\hat H-\mu\hat N$ on the $3\times3$ triangular lattice with periodic boundary conditions and $t=1$.
```

Keep the current values unless code-repo inspection contradicts them:

```text
Delta tau = 0.01
L_tau = 400 for beta = 4
L_tau = 100 for beta = 1
production bins = 100000
one sweep per bin
warmup sweeps = 500
block size = 10000
N_wrap = 10
initial fields = 0.1 * Gaussian random variable with zero bias
number-conserving proposal s = 1.5
finite-Delta proposal s = 1.0
number-conserving upper row: U1=0, mu=-3.5, beta=4, scan U2
number-conserving lower row: U2=1, mu=-7, beta=1, scan U1
finite-Delta scan: U1=0, U2=1, mu=-5, beta=4, Delta=0,0.05,...,0.30
```

- [ ] **Step 2: Remove implementation-facing phase diagnostics from benchmark details**

Delete any sentence in `SM.tex:803-826` that says the implementation records the phase, monitors the argument of every proposed local ratio, or reports near-branch-cut events. Replace it only with a physics-facing sentence if needed:

```tex
The finite-$\Delta$ scan is in the same low-density pole-free regime assumed in Sec.~\ref{app:green_paired}.
```

- [ ] **Step 3: Verify benchmark detail scans**

Run:

```bash
rg -n "records the phase|argument of every proposed|near-branch-cut|low-density pole-free|N_\\{\\\\rm wrap\\}=10" SM.tex
```

Expected: no matches for implementation-facing phase diagnostics. Expected matches for the low-density pole-free sentence if it was added and for `N_{\rm wrap}=10`.

## Task 9: Skill Update

**Files:**
- Modify: `.codex/skills/bafqmc-prl-revision/SKILL.md`

- [ ] **Step 1: Add generalized manuscript-editing rules**

Add or revise bullets in the skill so future rounds follow these generalized rules:

```markdown
- Before stating an algorithmic relation, derive the slice generator or matrix identity that makes it true. Do not replace a derivation with a plausible shortcut such as "the terms are real" when HS fields are complex.
- Do not invent algorithmic procedures to explain a branch choice. If the production calculation relies on a low-density, pole-free regime and small proposal shifts, say that directly and do not describe an unimplemented scan or continuation parameter as part of the algorithm.
- Keep implementation diagnostics out of manuscript prose unless they are necessary for reproducibility or for a reader to assess a numerical claim. Phase logging, branch diagnostics, and code-internal checks should not appear as standalone explanations.
- Explain stabilization as a reproducible algorithm: define the propagated Green/resolvent, the meaning of `N_{\rm wrap}`, the matrix product being factorized, the stabilized solve, and why the factorization preserves the physical result.
- When using code repositories as evidence, translate code behavior into physics-algorithm language and include enough equations for a reader to reproduce the method without reading the code.
```

Do not add a bullet that records the user's exact complaint wording.

- [ ] **Step 2: Verify skill update scans**

Run:

```bash
rg -n "invent algorithmic|N_\\{\\\\rm wrap\\}|implementation diagnostics|derive the slice generator|code behavior into physics-algorithm" .codex/skills/bafqmc-prl-revision/SKILL.md
```

Expected: matches for all generalized rules.

## Task 10: Independent Review and Verification

**Files:**
- Read only: `main.tex`
- Read only: `SM.tex`
- Read only: `.codex/skills/bafqmc-prl-revision/SKILL.md`

- [ ] **Step 1: Request an independent review**

Spawn a fresh read-only review agent with this exact prompt:

```text
Review the current working tree in /mnt/c/users/newton/documents/ligroupiop/2408_bosonsignproblem/paper_bafqmc after the Section II + SM algorithmic-detail edits. Do not edit files. Focus on physics/formula errors, false implementation claims, invented algorithmic steps, unexplained symbols, leftover phase-diagnostic or phase-reweighting prose, insufficient derivations in number-conserving and paired update ratios, stabilization clarity, and compliance with AGENTS.md. Return findings first with file/line references and concrete suggested corrections.
```

Expected: findings first. Fix any real issue before proceeding.

- [ ] **Step 2: Run process-language and old-phrase scans**

Run:

```bash
rg -n "we add|as requested|this revision|to address|we now clarify|requested benchmark|the manuscript currently|this addresses|we have added|we now modify" main.tex SM.tex .codex/skills/bafqmc-prl-revision/SKILL.md || true
rg -n "density-channel Hamiltonian|Since the hopping and chemical-potential terms are real|Gamma_\\ell|phase reweighting|phase diagnostic|finite precision|records its phase|real continuous fields|scalar factors are kept outside" main.tex SM.tex .codex/skills/bafqmc-prl-revision/SKILL.md || true
rg -n -F '\\left|R\\right|' main.tex SM.tex || true
rg -n -F '|R|' main.tex SM.tex || true
```

Expected: no matches except legitimate `|r_b|^2` in the number-conserving benchmark determinant ratio.

- [ ] **Step 3: Compile the manuscript**

Run:

```bash
latexmk main.tex
```

Expected: command exits 0 and `.latexmkrc` refreshes `pdf/main.pdf`.

- [ ] **Step 4: Inspect main build warnings**

Run:

```bash
rg -n "Warning|undefined|Rerun|Overfull|Underfull|Citation|Label" .build/main.log || true
```

Expected: no undefined references, no citation warnings, no overfull warnings introduced by the edited formulas. Existing REVTeX class and `nameref` warnings may remain.

- [ ] **Step 5: Refresh the diff PDF**

Use the previous substantive manuscript-content commit as baseline. If this plan is executed immediately after commit `899a3d2`, use `899a3d2`:

```bash
set -e
BASE=899a3d2
rm -rf .build/diff-work
mkdir -p .build/diff-work/old .build/diff-work/new pdf
git show ${BASE}:main.tex > .build/diff-work/old/main.tex
git show ${BASE}:SM.tex > .build/diff-work/old/SM.tex
git show ${BASE}:references.bib > .build/diff-work/old/references.bib
cp main.tex SM.tex references.bib .build/diff-work/new/
(cd .build/diff-work/old && latexpand main.tex > ../old.tex)
(cd .build/diff-work/new && latexpand main.tex > ../new.tex)
latexdiff --math-markup=0 .build/diff-work/old.tex .build/diff-work/new.tex > .build/diff-work/main-diff.tex
latexmk .build/diff-work/main-diff.tex
```

Expected: command exits 0 and `.latexmkrc` refreshes `pdf/main-diff.pdf`.

- [ ] **Step 6: Inspect diff build warnings**

Run:

```bash
rg -n "Warning|undefined|Rerun|Overfull|Underfull|Citation|Label" .build/main-diff.log || true
```

Expected: no undefined references or citation warnings after reruns. Underfull warnings from `latexdiff` markup are acceptable if they occur only in the diff artifact.

- [ ] **Step 7: Check source diff hygiene**

Run:

```bash
git diff --check
git status --short
```

Expected: `git diff --check` exits 0. `git status --short` shows only intended tracked changes to `main.tex`, `SM.tex`, and `.codex/skills/bafqmc-prl-revision/SKILL.md`; generated `pdf/` and `.build/` files remain ignored.

- [ ] **Step 8: Commit the manuscript edit round**

Run:

```bash
git add main.tex SM.tex .codex/skills/bafqmc-prl-revision/SKILL.md
git commit -m "Clarify BAFQMC update algorithms and stabilization"
git status --short
```

Expected: commit succeeds and the final status has no tracked dirty files.

## Self-Review

**Spec coverage:** The plan covers the main-text HS-measure sentence, the Sec. II A trace derivation, removal of scalar-factor prose, number-conserving benchmark slice/update/stabilization details, paired branch/update cleanup, paired stabilization, benchmark numerical consistency, and the project skill update.

**Placeholder scan:** The plan contains no placeholder markers and no step that says only "write tests" without commands. The only conditional branch is the paired stabilization truth condition, which is resolved by the mandated code-repo inspection before writing.

**Type and notation consistency:** The plan uses `\Delta_\ell` for both number-conserving and paired local update matrices, keeps physical pairing as `\Delta`, uses `\mc B` for number-conserving products, `\mc M` for Nambu products, and keeps `N_{\rm wrap}` as the stabilization cadence.
