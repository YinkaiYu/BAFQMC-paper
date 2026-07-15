# Formalism And Algorithm Guidelines

Use this reference for Section II formalism, Supplemental Material derivations, update ratios, branch conventions, numerical stabilization, and benchmark reproducibility details.
Apply the manuscript-wide story, evidence, reader-burden, and precision-layer rules
in `manuscript-story-evidence-principles.md` before using the technical guidance
below.

## Main Text

- Start from the physical AFQMC construction: HS fields decouple interactions into one-body problems, and the Monte Carlo samples spacetime auxiliary-field configurations.
- Introduce notation only when it carries a result. Prefer direct trace and determinant formulas over notation-only displays.
- Use displayed equations for core formulas and results. Put local definitions, matrix conventions, and one-use objects inline when readability allows.
- Before a formula, tell the reader what physical or algorithmic question it answers. After it, explain the consequence rather than immediately introducing another symbol.
- Avoid compact prose that transfers work to the reader: unexplained forward references, abrupt technical openings, dense semicolon chains, or comparisons that do not state the concrete differences.
- Keep early formalism independent of later benchmark details unless the object has already been introduced.
- Compare bosonic and fermionic AFQMC weights through concrete formula differences: the matrix structure and whether the determinant is in the numerator or denominator.
- Introduce Nambu language only after a pairing term or particle-number-nonconserving evolution makes it necessary.
- When shortening the main text, preserve the omitted derivation, caveat, or implementation detail in SM if it supports a formula or claim.

## Supplemental Derivations

- Order derivations from simple to general: HS identities, number-conserving trace, Green functions, local updates, then paired/Nambu formulas.
- For every local update, show the matrix factorization, determinant reduction, and Green/resolvent update. Use Sherman-Morrison or Woodbury explicitly when locality is essential.
- Avoid phrases that hide algebra, such as "the same manipulation gives," when the omitted step is needed to check a formula.
- Use intermediate symbols only when they shorten multiple subsequent equations. Do not introduce one-use variables that hide the evaluated matrix.
- State branch conventions as mathematical choices and physical-regime assumptions. Do not present unreported diagnostics or scans as part of the algorithm.

## Algorithm Fidelity

- A Metropolis ratio is a ratio of the full auxiliary-field measure. Include all changing factors: HS Gaussian weights, determinant or square-root determinant factors, and normal-ordering constants when present.
- In sign-free formulas, write the physical ratio as nonnegative. Do not add absolute values, phases, or code-level repairs unless the manuscript explicitly studies them.
- When an algorithmic simplification depends on a symmetry or conjugacy relation, derive it from the slice generator or matrix product before stating the computational consequence.
- Translate implementation details into physics-algorithm prose. Use code names only when they are necessary for reproducibility.

## Stabilization And Reproducibility

- Define the propagated object, the equal-time cut, and the cyclic product before discussing stabilization.
- Explain the propagation window and its cadence as part of the sweep, not as a detached parameter definition.
- State the product orientation and factorization convention before writing a stabilized solve.
- Explain why the stabilized representation is algebraically the same AFQMC product in exact arithmetic.
- If the exact algebra has extra structure but the implementation uses a generic numerical stabilization, keep those claims separate.
- For benchmark reproducibility, include HS fields, initialization, proposal distribution and width, warmup, stabilization cadence, statistics, and reference-solver truncation checks when available.
