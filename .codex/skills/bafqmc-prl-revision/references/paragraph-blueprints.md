# Paragraph Blueprints

Use these as style patterns for structure only. Do not copy them verbatim into the manuscript. Before using one, rewrite it around the actual section logic, notation, figure references, and nearby prose.

## Discovery/Principle Paragraph

Pattern:

1. Name the obstacle.
2. Say that the paper provides a principle or formulation.
3. State the mathematical object controlled by the principle.
4. State the new class of accessible models.

BAFQMC adaptation:

The sign problem limits unbiased simulations of frustrated bosonic systems. This work formulates finite-temperature BAFQMC and classifies its sign-free domain by RP/TRS of the HS-decoupled Gaussian propagators. The classification gives nonnegative weights throughout the RP/TRS half-plane of Fig. 1 and exposes the frustrated RP/TRS quadrant as a new computable region.

## Formula Paragraph

Pattern:

1. Introduce a fixed auxiliary-field configuration.
2. Give the one-body product.
3. Give the determinant or trace formula.
4. Explain why the sign question reduces to a symmetry question.

BAFQMC adaptation:

For each auxiliary-field configuration, the bosons appear only through Gaussian propagators. In the number-conserving sector, the configuration weight is the inverse determinant of `I-\mc B`. Thus the sign-free problem becomes the problem of constraining the spectrum of the one-body product `\mc B`.

## Criterion Paragraph

Pattern:

1. State the symmetry.
2. State the slice condition.
3. Give the sign consequence.
4. Give one sentence of physical proof.

BAFQMC adaptation:

Kramers TRS pairs nonreal eigenvalues and makes every real eigenvalue even-degenerate. The factors in `\det(I-\mc B)` therefore occur in positive pairs, so the number-conserving BAFQMC weight is nonnegative whenever it is finite.

## Benchmark Paragraph

Pattern:

1. Name the model and why it sits in the target region.
2. State the benchmark reference.
3. Name the measured observables.
4. State the level of agreement and what it validates.

BAFQMC adaptation:

The triangular two-flavor Bose-Hubbard model with positive real hopping lies in the frustrated sector of Fig. 1. The HS-decoupled propagators retain the RP/TRS structure, so BAFQMC samples it without a sign problem. Figures 2 and 3 compare density, energy, and structure factors with finite-temperature ED, validating both the Gaussian weight formulas and the symmetry-protected sampling.

## Concluding Paragraph

Pattern:

1. Restate the principle.
2. State the new territory.
3. State the limitation.
4. State the next direction.

BAFQMC adaptation:

The main result is a symmetry classification of sign-free bosonic AFQMC. It provides a constructive route into the frustrated RP/TRS quadrant of Fig. 1. The finite-temperature method still carries bosonic pole constraints, making dilute and moderate-temperature regimes the natural first domain. A projector formulation is the next target for extending the approach to lower temperatures and stronger coupling.
