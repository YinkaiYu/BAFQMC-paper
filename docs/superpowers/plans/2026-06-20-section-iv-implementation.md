# Section IV Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite Sec. IV around the new triangular-lattice BAFQMC benchmarks, keep the main text PRL-like, and move benchmark mechanics into the Supplemental Material.

**Architecture:** The main manuscript gets one compact model-and-benchmark section with two figures. The Supplemental Material gets the HS, pairing-sign convention, observable normalization, and numerical-detail record. References are updated only for the verified earlier Bose-Fermi AFQMC paper needed to state what the Nambu benchmark extends.

**Tech Stack:** REVTeX 4.2, `latexmk main.tex`, BibTeX through `apsrev4-2`, existing `.latexmkrc`, `latexdiff` if available for `pdf/main-diff.pdf`, project skill `.codex/skills/bafqmc-prl-revision`, and subagent review prompts from `.codex/skills/bafqmc-prl-revision/references/review-prompts.md`.

---

## File Map

- Modify `references.bib`: add verified `rubenstein2012pra` entry and expand the `SM` note to include benchmark details after the SM task.
- Modify `main.tex`: replace the current Sec. IV from `\section{Examples and applications}` through the old benchmark figure with the unified model, compact HS/RP/TRS explanation, observable definitions, and the two new figures.
- Modify `SM.tex`: append a new section `Benchmark model, observables, and numerical details` after the current TRS appendix.
- Build artifacts: refresh `pdf/main.pdf`; refresh `pdf/main-diff.pdf` after manuscript edits if a usable diff workflow is available.

---

### Task 1: Add Verified Bose-Fermi AFQMC Reference

**Files:**
- Modify: `references.bib`

- [ ] **Step 1: Confirm the entry is absent**

Run:
```bash
rg -n "Rubenstein|Bose-Fermi|053606|1209\\.0186|rubenstein2012pra" references.bib
```

Expected before this task: no matching entry for Phys. Rev. A 86, 053606.

- [ ] **Step 2: Add the verified BibTeX entry**

Add this entry before `@misc{SM,`:

```bibtex
@article{rubenstein2012pra,
  title = {Finite-temperature auxiliary-field quantum Monte Carlo technique for Bose-Fermi mixtures},
  author = {Rubenstein, Brenda M. and Zhang, Shiwei and Reichman, David R.},
  journal = {Phys. Rev. A},
  volume = {86},
  issue = {5},
  pages = {053606},
  year = {2012},
  month = {Nov},
  publisher = {American Physical Society},
  doi = {10.1103/PhysRevA.86.053606},
  eprint = {1209.0186},
  archivePrefix = {arXiv},
  primaryClass = {cond-mat.quant-gas},
  url = {https://link.aps.org/doi/10.1103/PhysRevA.86.053606}
}
```

Verification sources already checked by the controller:

- Crossref DOI API for `10.1103/PhysRevA.86.053606`.
- DOI content-negotiated BibTeX from `https://doi.org/10.1103/PhysRevA.86.053606`.
- arXiv `1209.0186`, which lists the title, authors, journal reference `Phys. Rev. A 86, 053606 (2012)`, and related DOI.

- [ ] **Step 3: Verify entry formatting**

Run:
```bash
rg -n "rubenstein2012pra|Finite-temperature auxiliary-field|PhysRevA.86.053606|1209.0186" references.bib
```

Expected: the new entry appears once, with DOI and arXiv identifier.

- [ ] **Step 4: Commit**

Run:
```bash
git add references.bib
git commit -m "refs: add Bose-Fermi AFQMC reference"
```

---

### Task 2: Rewrite Main-Text Sec. IV And Update Benchmark Figures

**Files:**
- Modify: `main.tex`

- [ ] **Step 1: Locate the replacement range**

Run:
```bash
rg -n "\\\\section\\{Examples and applications\\}|\\\\section\\{Discussion\\}|To be finished|fig:benchmark|benchmark\\.pdf|benchmark_pairing" main.tex
```

Expected before this task: Sec. IV starts at `\section{Examples and applications}` and the old range ends immediately before `\section{Discussion}`. The old unfinished marker and old `figures/benchmark.pdf` appear in this range.

- [ ] **Step 2: Replace Sec. IV with the new main-text draft**

Replace everything from `\section{Examples and applications}` through the old `\end{figure*}` that precedes `\section{Discussion}` with:

```tex
\section{Examples and applications}
\label{sec:examples}

We now apply the RP/TRS criteria to a frustrated bosonic benchmark. Consider two boson flavors $b$ and $c$ on a triangular lattice,
\begin{equation}
\begin{aligned}
    \hat H ={}&
    t\sum_{\langle ij\rangle,\alpha=b,c}
    \left(\hat a_{\alpha i}^{\hc}\hat a_{\alpha j}+\hc\right)
    + U_1\sum_i\left(\hat n_{b,i}+\hat n_{c,i}\right)^2 \\
    &+ U_2\sum_i\left(\hat n_{b,i}-\hat n_{c,i}\right)^2
    + \Delta\sum_i\left(\hat b_i^{\hc}\hat c_i^{\hc}+\hat b_i\hat c_i\right),
\end{aligned}
\label{eq:benchmark_pairing}
\end{equation}
where $\hat a_{b i}\equiv\hat b_i$, $\hat a_{c i}\equiv\hat c_i$, $t>0$, $U_1\le0$, $U_2\ge0$, and $\Delta\ge0$. The positive hopping on the triangular lattice places the model in the frustrated side of the classification in Fig.~\ref{fig:schematic}. The sign-free structure follows by applying the criteria of Sec.~\ref{sec:positive} after HS decoupling.

For $\Delta=0$, the two interactions are decoupled in density channels. For a time step $\Delta\tau$,
\begin{equation}
    \ee^{-\Delta\tau U_1(\hat n_{b,i}+\hat n_{c,i})^2}
    =
    \int \frac{\dd\phi_{i\ell}}{\sqrt{2\pi}}\,
    \ee^{-\phi_{i\ell}^2/2}
    \ee^{\alpha_1\phi_{i\ell}(\hat n_{b,i}+\hat n_{c,i})},
    \qquad
    \alpha_1=\sqrt{-2\Delta\tau U_1},
    \label{eq:benchmark_hs_total}
\end{equation}
while
\begin{equation}
    \ee^{-\Delta\tau U_2(\hat n_{b,i}-\hat n_{c,i})^2}
    =
    \int \frac{\dd\varphi_{i\ell}}{\sqrt{2\pi}}\,
    \ee^{-\varphi_{i\ell}^2/2}
    \ee^{\ii\alpha_2\varphi_{i\ell}(\hat n_{b,i}-\hat n_{c,i})},
    \qquad
    \alpha_2=\sqrt{2\Delta\tau U_2}.
    \label{eq:benchmark_hs_relative}
\end{equation}
Thus the $b$ and $c$ flavors see conjugate one-body potentials. With the reflection $\theta(\hat b_i)=\hat c_i$ and $\theta(\ii)=-\ii$, each number-conserving slice has the form $\hat q_\ell+\theta(\hat q_\ell)$ and lies in the RP cone of Eq.~\eqref{eq:rp_generator}. Equivalently, in the single-particle basis $(\hat{\bb b},\hat{\bb c})^\trans$, the slice has the block-conjugate structure of Eq.~\eqref{eq:block_TRS}. The density-channel benchmark is therefore sign-free by both RP and TRS.

The paired term probes the more general BAFQMC formulation. For $\Delta\ne0$, particle number is not conserved, and the one-body evolution must be written in Nambu space. The onsite term in Eq.~\eqref{eq:benchmark_pairing} is a reflected anomalous bilinear. After the global gauge transformation $\tilde c_i=-\hat c_i$, which leaves the hopping and density interactions unchanged, the imaginary-time generator has the positive reflected block $F=(\Delta\tau\Delta/2)I_{2N_s}$ in Eq.~\eqref{eq:rp_block_form}. The SM gives the corresponding convention. This finite-$\Delta$ cut exercises the anomalous bosonic Gaussian trace formula, a case not formulated in the earlier finite-temperature Bose-Fermi AFQMC method~\cite{rubenstein2012pra}.

We benchmark Eq.~\eqref{eq:benchmark_pairing} on a $3\times3$ triangular lattice with periodic boundary conditions against finite-temperature exact diagonalization (ED). The simulations are grand-canonical, with the chemical potential specified in each figure caption, while $E=\langle \hat H\rangle$ denotes the physical energy of Eq.~\eqref{eq:benchmark_pairing}. The plotted observables are the density $\rho=\langle N_b+N_c\rangle/N_s$, the energy shown as $-E$, the single-particle structure factor $S_{\rm SF}(K)=N_s^{-2}\sum_{ij,\alpha} \ee^{\ii K\cdot(r_i-r_j)}\langle \hat a_{\alpha i}^{\hc}\hat a_{\alpha j}\rangle$, and the density-wave structure factor $S_{\rm DW}(K)=N_s^{-2}\sum_{ij}\ee^{\ii K\cdot(r_i-r_j)}\langle \hat n_i\hat n_j\rangle$, with $\hat n_i=\hat n_{b,i}+\hat n_{c,i}$ and $K=(4\pi/3,0)$.

Figure~\ref{fig:benchmark_number} shows the number-conserving cut, $\Delta=0$. The upper row scans $U_2$ at fixed $U_1=0$, $\mu=-3.5$, and $\beta=4$; the lower row scans $U_1$ at fixed $U_2=1$, $\mu=-7$, and $\beta=1$. Across density, energy, and both $K$-point structure factors, BAFQMC follows the ED reference within the plotted statistical resolution. This directly tests the frustrated RP/TRS quadrant of Fig.~\ref{fig:schematic}.

\begin{figure*}[bt]
    \centering
    \includegraphics[width=\linewidth]{figures/benchmark_number_conserving.pdf}
    \caption{\textbf{Number-conserving benchmark on a frustrated triangular lattice.} BAFQMC and ED results for Eq.~\eqref{eq:benchmark_pairing} at $\Delta=0$ on a $3\times3$ triangular lattice. The upper row scans $U_2$ at fixed $U_1=0$, $\mu=-3.5$, and $\beta=4$; the lower row scans $U_1$ at fixed $U_2=1$, $\mu=-7$, and $\beta=1$. The four columns show $\rho$, $-E$, $S_{\rm SF}(K)$, and $S_{\rm DW}(K)$, respectively. Red points denote ED or exact free-boson references, and blue open circles denote BAFQMC block means with standard-error bars.}
    \label{fig:benchmark_number}
\end{figure*}

Figure~\ref{fig:benchmark_pairing} turns on the anomalous channel by scanning $\Delta$ from $0$ to $0.30$ at fixed $U_1=0$, $U_2=1$, $\mu=-5$, and $\beta=4$. The same four observables again agree with ED on the scale of the curves. The agreement validates the paired Nambu implementation of BAFQMC in the same frustrated model family.

\begin{figure*}[bt]
    \centering
    \includegraphics[width=0.92\linewidth]{figures/benchmark_pairing_delta.pdf}
    \caption{\textbf{Paired Nambu-basis benchmark.} BAFQMC and ED results for Eq.~\eqref{eq:benchmark_pairing} on the same $3\times3$ triangular lattice with $U_1=0$, $U_2=1$, $\mu=-5$, and $\beta=4$, scanning $\Delta=0,0.05,\ldots,0.30$. The panels show $\rho$, $-E$, $S_{\rm SF}(K)$, and $S_{\rm DW}(K)$. The finite-$\Delta$ data test the anomalous one-body propagation handled by the Nambu-basis BAFQMC formulation.}
    \label{fig:benchmark_pairing}
\end{figure*}
```

- [ ] **Step 3: Confirm required text properties**

Run:
```bash
rg -n "To be finished|benchmark\\.pdf|n_\\{i,\\+\\}|n_\\{i,-\\}|bipart|not .*but|no-go|Delta_p|\\\\Delta_p" main.tex
```

Expected: no output from the replaced Sec. IV. If this command finds older Introduction or Discussion prose outside Sec. IV, do not edit it in this task; report it as pre-existing.

- [ ] **Step 4: Confirm figure paths and labels**

Run:
```bash
rg -n "benchmark_number_conserving|benchmark_pairing_delta|fig:benchmark_number|fig:benchmark_pairing|eq:benchmark_pairing|rubenstein2012pra" main.tex
```

Expected: the two new figure files and labels appear, `eq:benchmark_pairing` still exists for earlier cross-references, and `rubenstein2012pra` is cited.

- [ ] **Step 5: Commit**

Run:
```bash
git add main.tex
git commit -m "rewrite section iv benchmark narrative"
```

---

### Task 3: Add Supplemental Benchmark Details

**Files:**
- Modify: `SM.tex`
- Modify: `references.bib`

- [ ] **Step 1: Append the benchmark-details section**

Append this section after the current final paragraph of `SM.tex`:

```tex
\section{Benchmark model, observables, and numerical details}
\label{app:benchmark_details}

This section records the conventions used for the benchmark figures in the main text. The simulations use the physical Hamiltonian in Eq.~\eqref{eq:benchmark_pairing}; the grand-canonical sampling weight contains $\hat H-\mu \hat N$, with $\hat N=\sum_i(\hat n_{b,i}+\hat n_{c,i})$. The energy plotted in Figs.~\ref{fig:benchmark_number} and~\ref{fig:benchmark_pairing} is always $E=\langle \hat H\rangle$, not $\langle \hat H-\mu\hat N\rangle$.

\subsection{Density-channel decoupling}
\label{app:benchmark_hs}

For $U_1\le0$ and $U_2\ge0$, the two onsite interactions are decoupled exactly as in Eqs.~\eqref{eq:benchmark_hs_total} and~\eqref{eq:benchmark_hs_relative}. For fixed auxiliary fields on time slice $\ell$, the number-conserving part of the one-body generator is
\begin{equation}
\begin{aligned}
    \hat h_\ell^{(0)}
    ={}& -\Delta\tau\, t\sum_{\langle ij\rangle}
    \left(\hat b_i^{\hc}\hat b_j+\hat c_i^{\hc}\hat c_j+\hc\right)\\
    &+\sum_i\left(\alpha_1\phi_{i\ell}+\ii\alpha_2\varphi_{i\ell}\right)\hat n_{b,i}
    +\sum_i\left(\alpha_1\phi_{i\ell}-\ii\alpha_2\varphi_{i\ell}\right)\hat n_{c,i}.
\end{aligned}
\end{equation}
The two flavor sectors are therefore complex conjugates. This gives the RP form $\hat q_\ell+\theta(\hat q_\ell)$ with $\theta(\hat b_i)=\hat c_i$ and $\theta(\ii)=-\ii$, and also the TRS block form used in the main text.

\subsection{Pairing-sign convention}
\label{app:benchmark_pairing_convention}

The benchmark reports use the physical convention
\begin{equation}
    \hat H_\Delta=\Delta\sum_i\left(\hat b_i^{\hc}\hat c_i^{\hc}+\hat b_i\hat c_i\right),
    \qquad \Delta\ge0.
\end{equation}
Introduce $\tilde c_i=-\hat c_i$. This global gauge transformation leaves the hopping term and the density interactions invariant but sends
\begin{equation}
    \hat H_\Delta
    \mapsto
    -\Delta\sum_i\left(\hat b_i^{\hc}\tilde c_i^{\hc}+\hat b_i\tilde c_i\right).
\end{equation}
In this gauge the Trotter generator contains $+\Delta\tau\Delta\sum_i(\hat b_i^{\hc}\tilde c_i^{\hc}+\hat b_i\tilde c_i)$, which is the positive reflected anomalous block in Eq.~\eqref{eq:rp_block_form}. In the main-text RP ordering $(\hat{\bb b},\hat{\bb b}^{\hc},\hat{\tilde{\bb c}},\hat{\tilde{\bb c}}^{\hc})^\trans$, this corresponds to $F=(\Delta\tau\Delta/2)I_{2N_s}\succeq0$. The gauge transformation is unitary and does not change the trace or the Monte Carlo weight, so the report convention and the RP-positive block convention describe the same sign-free model.

\subsection{Observable and geometry conventions}
\label{app:benchmark_observables}

The triangular lattice has $N_s=9$ sites with periodic boundary conditions. We use primitive vectors
\begin{equation}
    \bb a_1=(1,0),\qquad
    \bb a_2=\left(\frac12,\frac{\sqrt3}{2}\right),
\end{equation}
and the reciprocal convention $\bb b_i\cdot\bb a_j=2\pi\delta_{ij}$. The plotted momentum is the triangular-lattice corner
\begin{equation}
    K=\frac23\bb b_1+\frac13\bb b_2=\left(\frac{4\pi}{3},0\right).
\end{equation}
The four main observables are
\begin{equation}
    \rho=\frac{\langle N_b+N_c\rangle}{N_s},
    \qquad
    E=\langle \hat H\rangle,
\end{equation}
\begin{equation}
    S_{\rm SF}(K)=\frac{1}{N_s^2}
    \sum_{ij,\alpha=b,c}\ee^{\ii K\cdot(r_i-r_j)}
    \left\langle \hat a_{\alpha i}^{\hc}\hat a_{\alpha j}\right\rangle,
\end{equation}
and
\begin{equation}
    S_{\rm DW}(K)=\frac{1}{N_s^2}
    \sum_{ij}\ee^{\ii K\cdot(r_i-r_j)}
    \left\langle \hat n_i\hat n_j\right\rangle,
    \qquad
    \hat n_i=\hat n_{b,i}+\hat n_{c,i}.
\end{equation}
The plotted energy panel uses $-E$ so that all four panels can be displayed on positive vertical scales in the low-density benchmark windows.

\subsection{Numerical parameters}
\label{app:benchmark_numerics}

For Fig.~\ref{fig:benchmark_number}, the number-conserving calculations set $\Delta=0$ and use $\Delta\tau=0.01$. The upper row scans $U_2=0,0.125,0.25,0.375,0.5,0.75,1,1.25,1.5,2$ at $U_1=0$, $\mu=-3.5$, and $\beta=4$. The lower row scans $U_1=-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0$ at $U_2=1$, $\mu=-7$, and $\beta=1$. Each BAFQMC point uses $100000$ production samples grouped into blocks of size $10000$.

For Fig.~\ref{fig:benchmark_pairing}, the paired calculations fix $U_1=0$, $U_2=1$, $\mu=-5$, $\beta=4$, and scan $\Delta=0,0.05,\ldots,0.30$. The production runs use $\Delta\tau=0.01$, $500$ warmup sweeps, and $100000$ samples grouped into blocks of size $10000$. The finite-$\Delta$ ED references use a truncated occupation basis with convergence checked against the low-density weight in the highest retained shells. The small residuals at the largest $\Delta$ values are much smaller than the scale of the curves in Fig.~\ref{fig:benchmark_pairing}; time-step and ED-cutoff floors are the natural systematic checks for future refinements.
```

- [ ] **Step 2: Update the SM bibliography note**

Replace the `@misc{SM, ...}` note in `references.bib` with:

```bibtex
@misc{SM,
  note = {See Supplemental Material at [URL will be inserted by publisher] for technical derivations of the bosonic quadratic algebra, Gaussian trace formulas, equal-time Green's function, local-update ratio, regularized bosonic weight, regularized reflection positivity, time-reversal-symmetry argument, and benchmark model and numerical details.}
}
```

- [ ] **Step 3: Verify labels and process-language scan**

Run:
```bash
rg -n "app:benchmark_details|app:benchmark_hs|app:benchmark_pairing_convention|app:benchmark_observables|app:benchmark_numerics|benchmark model and numerical details" SM.tex references.bib
rg -n "as requested|requested benchmark|this revision|we add|to address|we now clarify|the manuscript currently|this addresses|we have added|we now modify" main.tex SM.tex
```

Expected: labels appear once. The process-language scan returns no new hits from Task 2 or Task 3.

- [ ] **Step 4: Commit**

Run:
```bash
git add SM.tex references.bib
git commit -m "add supplemental benchmark details"
```

---

### Task 4: Build, Review, Diff, And Final Polish

**Files:**
- Modify only if needed after review: `main.tex`, `SM.tex`, `references.bib`
- Generated/ignored: `.build/`, `pdf/main.pdf`, `pdf/main-diff.pdf`

- [ ] **Step 1: Build the manuscript**

Run:
```bash
latexmk main.tex
```

Expected: successful build and refreshed `pdf/main.pdf`.

- [ ] **Step 2: Inspect relevant warnings**

Run:
```bash
rg -n "Warning|Citation|Reference|undefined|multiply defined|Rerun" .build/main.log
```

Expected: no unresolved citations or labels introduced by the Sec. IV edit. Existing warnings not related to changed text should be reported, not silently fixed.

- [ ] **Step 3: Run local prose/process scans**

Run:
```bash
rg -n "not .*but|no-go|bipart|To be finished|benchmark\\.pdf|Delta_p|\\\\Delta_p" main.tex SM.tex
rg -n "as requested|requested benchmark|this revision|we add|to address|we now clarify|the manuscript currently|this addresses|we have added|we now modify" main.tex SM.tex
```

Expected: no hits introduced by the Sec. IV rewrite. Pre-existing hits in Abstract, Introduction, or Discussion should be reported separately unless they break the new Sec. IV.

- [ ] **Step 4: Run external prose review**

Run:
```bash
opencode run -m deepseek/deepseek-v4-pro "Review only Sec. IV of main.tex and the new benchmark-details section of SM.tex for APS/PRL style. Return findings first. Check that the prose is direct, reader-friendly for theoretical physicists, does not contain process-facing language, avoids unnecessary 'not ... but ...' framing, minimizes dashes, and preserves the Fig. 1 classification. Do not rewrite wholesale; give concrete line-level corrections."
```

Expected: actionable prose findings or a clear statement that no changes are needed. Apply only corrections that preserve the approved physics design.

- [ ] **Step 5: Run independent-agent manuscript review**

Dispatch a fresh subagent reviewer with the review prompts from `.codex/skills/bafqmc-prl-revision/references/review-prompts.md`, asking it to inspect changed lines in `main.tex`, `SM.tex`, and `references.bib`. Require findings first and line references.

Expected: no critical physics or style findings remain. Apply fixes for accepted findings and rebuild.

- [ ] **Step 6: Refresh `pdf/main-diff.pdf`**

Use baseline commit `53a5de9`, the previous commit that touched `main.tex`, `SM.tex`, or `references.bib` before the current Sec. IV work.

First inspect available tools:
```bash
which latexdiff || true
which latexpand || true
which latexmk || true
```

There is no tracked repo-specific script for this artifact. Use the available `latexpand`/`latexdiff` fallback workflow:
```bash
mkdir -p .build/diff-work/old .build/diff-work/new pdf
git show 53a5de9:main.tex > .build/diff-work/old/main.tex
git show 53a5de9:SM.tex > .build/diff-work/old/SM.tex
git show 53a5de9:references.bib > .build/diff-work/old/references.bib
cp main.tex SM.tex references.bib .build/diff-work/new/
latexpand .build/diff-work/old/main.tex > .build/diff-work/old.tex
latexpand .build/diff-work/new/main.tex > .build/diff-work/new.tex
latexdiff .build/diff-work/old.tex .build/diff-work/new.tex > .build/diff-work/main-diff.tex
latexmk .build/diff-work/main-diff.tex
```

Expected: `.latexmkrc` copies the resulting PDF to `pdf/main-diff.pdf`. If `latexdiff` or `latexpand` is unavailable, install the missing TeX utility or report the exact blocker before finishing.

- [ ] **Step 7: Final build after any review fixes**

Run:
```bash
latexmk main.tex
git status --short
```

Expected: manuscript builds, `pdf/main.pdf` and `pdf/main-diff.pdf` are refreshed ignored artifacts, and tracked changes are limited to manuscript/source files required by this plan.

- [ ] **Step 8: Commit final review/build fixes**

If Task 4 changed tracked files, run:
```bash
git add main.tex SM.tex references.bib
git commit -m "polish section iv benchmark rewrite"
```

If Task 4 changed only ignored build artifacts, do not create an empty commit.
