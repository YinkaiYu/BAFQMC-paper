# Style Micro-Excerpts And Sentence Patterns

This file stores short style cues from the arXiv reference papers plus paraphrased sentence patterns. Use it for voice and rhythm only.

## Micro-Excerpts

Keep these as short cues, not as text to paste verbatim into the manuscript.

- arXiv:1408.2269: "we discover a new quantum Monte Carlo"
- arXiv:1408.2269: "fermion sign free in simulating a class"
- arXiv:1506.05349: "We present a guiding principle"
- arXiv:1506.05349: "provide a guideline for sign-free simulations"
- arXiv:1601.01994: "Two sufficient conditions are proven"
- arXiv:1601.01994: "treated on equal footing"
- arXiv:1601.05780: "provide a unifying principle"
- arXiv:1601.05780: "systematically classifying"

## Pattern Library

Use these as adaptable patterns:

- "We formulate [method] and identify [symmetry/classification] conditions under which [weight/sign] is [nonnegative/sign-free]."
- "The resulting criterion applies directly to [model class], including [specific difficult sector]."
- "The important point is that [formal condition] can be checked after [decoupling/representation change]."
- "Figure [n] summarizes the classification: [half-plane/sector] is accessible to [method], while [other sector] is covered by [comparison method]."
- "To demonstrate the construction, we benchmark [method] against [reference] on [minimal frustrated model]."
- "The agreement validates the implementation against the reference calculation."

## BAFQMC-Specific Voice Targets

- Use the mentor revision in commit `66c6cd4` as a historical rhythm example. Reuse
  its moves---broad stakes, concrete obstruction, paradigm shift, rigorous result,
  benchmark, and opportunity---rather than its exact strings.
- Use assertive, precise claims such as "BAFQMC covers the RP/TRS half-plane" instead of hedged claims such as "BAFQMC may help with some cases".
- Connect the broad problem, physical stakes, and classification clearly.
- Let citations sit behind the story. Do not turn a sentence into a taxonomy merely because the research report found many relevant terms or methods.
- Exclude process language: never write "we now modify", "as requested", "this addresses", or "we have added".
- Avoid reader-correction framing: do not begin by negating what the reader supposedly thinks.
- Prefer short conceptual turns and ordinary physics language over invented labels.

## Mentor-Calibrated Pattern Library

- Stakes: "[Problem] poses a fundamental barrier to [scientific capability], limiting access to [physical territory]."
- Paradigm boundary: "This familiar identification is rooted in [specific computational construction]."
- Mechanism turn: "After [transformation], [local object] is replaced by [global object], so [old obstruction] no longer determines [target property]."
- Precedent to gap: "In [neighboring setting], [structure] protects [property]; no unifying criterion has been available for [target setting]."
- Direct delivery: "We establish [principles/criteria] and demonstrate them in [diagnostic model or benchmark]."
- Conceptual conclusion: "The result shifts the organizing principle from [old criterion] to [new structure]."
- Concrete outlook: "The same criteria guide [specific algorithmic extension], while [specific formulation] offers a route around [separate numerical difficulty]."

Do not stack these patterns mechanically. Choose the one rhetorical move needed at
the current point in the reader's journey.
