# Paragraph Blueprints

Use these as optional structural patterns, not fill-in templates. First identify the
paragraph's scientific job and the reader's starting point. Rewrite every pattern
around the actual logic, notation, evidence, and nearby prose. A paragraph may omit,
merge, or reorder steps when that improves the causal story.

## General Paragraph Arc

Most effective physics paragraphs perform one main move:

1. Establish the question or situation inherited from the previous paragraph.
2. Introduce one new mechanism, result, obstacle, or comparison.
3. Explain its physical meaning.
4. End with the consequence that prepares the next paragraph.

Do not spend the final sentence summarizing what the reader has just read when it can
instead create forward motion.

## Discovery Or Principle Paragraph

Pattern:

1. Name the obstacle at the level relevant to the audience.
2. State the paper's principle or formulation directly.
3. Explain the physical or mathematical mechanism at the minimum useful depth.
4. State what becomes possible.

BAFQMC adaptation:

The sign problem limits unbiased simulations of frustrated bosonic systems. This
work formulates finite-temperature BAFQMC and identifies TRS and RP as sufficient
conditions for nonnegative weights. The resulting classification opens the
frustrated TRS/RP region in Fig. 1 to numerically exact simulation.

## Formula Paragraph

Pattern:

1. Tell the reader what question the formula answers.
2. Define the minimum objects needed to read it.
3. Give the formula.
4. Interpret the formula and connect it to the next result.

BAFQMC adaptation:

For each auxiliary-field configuration, the bosons appear only through Gaussian
propagators. In the number-conserving sector, the configuration weight is the inverse
determinant of `I-\mc B`. Thus the sign question becomes a spectral property of the
one-body product `\mc B`.

## Criterion Paragraph

Pattern:

1. State the symmetry or structural condition.
2. State where it acts.
3. Give the mathematical consequence.
4. Explain the proof mechanism or physical meaning in one sentence.

BAFQMC adaptation:

Kramers TRS pairs nonreal eigenvalues and makes every real eigenvalue
even-degenerate. The factors in `\det(I-\mc B)` therefore occur in positive pairs,
so the number-conserving BAFQMC weight is nonnegative whenever it is finite.

## Obstacle-To-Mechanism Paragraph

Pattern:

1. State why the established route fails or becomes costly.
2. Identify the assumption responsible for that failure.
3. Introduce the alternative representation or mechanism.
4. State why it changes the problem.

Use this for conceptual reversals. Delay the qualifying assumption until the reader
understands the prevailing picture; introducing it too early can erase the reversal.

## Benchmark Paragraph

Pattern:

1. State what part of the method the benchmark tests.
2. Name the model and why it is diagnostic.
3. State the independent comparison and relevant observables.
4. Report the agreement and the conclusion it supports, without extending beyond
   the tested regime.

BAFQMC adaptation:

The triangular two-flavor Bose-Hubbard model tests BAFQMC in the frustrated region
targeted by Fig. 1. Its HS-decoupled propagators retain the required symmetry, while
finite-temperature exact diagonalization provides an independent reference for the
density, energy, and structure factors. Agreement between the two calculations
validates the Gaussian weights and symmetry-protected sampling in the tested regime.

## Concluding Paragraph

Pattern:

1. Restate the paper's result at a higher conceptual level.
2. State the immediate scientific territory it opens.
3. State a limitation only if it changes how the main result should be interpreted.
4. End with the strongest well-motivated consequence or next direction.

BAFQMC adaptation:

The main result is a symmetry classification of sign-free bosonic AFQMC. It provides
a constructive route into the frustrated TRS/RP quadrant of Fig. 1 and establishes a
starting point for numerically exact studies of interacting bosons beyond the reach
of conventional world-line formulations.
