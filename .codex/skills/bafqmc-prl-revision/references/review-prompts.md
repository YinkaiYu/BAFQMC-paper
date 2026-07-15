# Independent Review Prompts

Use these prompts after substantive edits. The reviewer should judge the text as a
reader with no access to the author-assistant conversation. Return findings first,
with concrete corrections and file/line references where possible; do not rewrite
the paper wholesale.

## Scientific-Story Review

Review the changed unit against `manuscript-story-evidence-principles.md`:

- What scientific job does each paragraph perform?
- Does the argument advance causally, or does it read as a list of facts, methods,
  papers, or caveats?
- Does each sentence establish importance, explain a mechanism, support a claim,
  create a transition, report evidence, or state a consequence?
- Is any sentence present mainly to display terminology, mention a citation, answer a
  collaborator, or defend against an objection the reader has not encountered?
- Does the ending of each paragraph create the need for the next one?
- Has compression removed a physical explanation or transition that the reader needs?
- Does the prose make the paper's contribution memorable without claiming more than
  the results support?

For frontmatter, also apply `introduction-frontmatter-guidelines.md`. Verify that the
literature supports the approved story instead of becoming the story.

## Evidence Review

For every externally checkable statement in changed prose, ask:

- What evidence type is appropriate: citation, equation, proof, numerical comparison,
  or figure?
- Does each citation support the exact nearby clause?
- Are original methods and discoveries cited where appropriate, rather than only
  textbooks or reviews?
- Are method developments, successful applications, physical understanding,
  limitations, and motivating phases kept conceptually distinct?
- Are broad citation clusters coherent, and are citations attached to individual
  physical examples when needed?
- Has a prestigious, strategic, or newly discovered paper been forced into a sentence
  it does not support?
- Does a missing caveat change the conclusion, or would adding it merely burden the
  wrong precision layer?

For bibliography changes, verify authoritative metadata and exact-key PDF-cache
coverage using `reference-verification.md`.

## Physics And Claims Review

Check:

- Does the text preserve the Fig. 1 classification: BAFQMC sign-free for RP/TRS,
  SSE/WLQMC sign-free for unfrustrated systems, and the frustrated RP/TRS quadrant
  as new computable territory?
- Are TRS/RP assumptions stated accurately at the appropriate precision layer?
- Are paired/Nambu branch and pole statements no stronger than supported?
- Does the pairing term use `-\Delta b^+c^+ - \Delta^*bc` consistently, without
  gauge-transform wording in the manuscript?
- Does benchmark wording stay within the evidence supplied by the reported data?
- Do equations, theorem statements, prose interpretations, examples, captions, and SM
  make the same claim?

## PRL Voice Review

Compare the changed section with `style-analysis.md` and `style-micro-excerpts.md`:

- Is the prose direct, confident, and readable by theoretical physicists outside the
  immediate subfield?
- Are unfamiliar concepts explained before technical labels carry the argument?
- Does it avoid catalogue prose, unnecessary `not ... but ...` constructions,
  adjacent colon sentences, excessive parentheses or dashes, and repeated
  superlatives?
- Is concision achieved by removing detours rather than deleting the physical picture?
- Are theorem-like statements limited to assumptions and conclusions, with intuition,
  examples, and implementation caveats placed around them?
- Does the section sound like a scientific paper rather than a literature report,
  theorem manuscript, software manual, or response letter?

## Reader-Burden Review

Read as a first-time theoretical-physics reader:

- Are operators, indices, fields, matrices, commutators, and specialist terms defined
  before compact formulas use them?
- Are symbols reintroduced after a long gap?
- Does each displayed equation answer a question established in the prose?
- Does the sentence after a formula explain its consequence?
- Are determinant identities, update ratios, conjugacy relations, and stabilization
  formulas derived where the reader needs them rather than hidden behind `similarly`?
- Does the main text contain only the detail needed to understand the result, with
  checkable derivations and implementation details retained in the SM?

## Process-Language Review

Search for wording that reveals the revision process or answers a prompt, including:

- `we add`
- `as requested`
- `this revision`
- `to address`
- `we now clarify`
- `the requested benchmark`
- `the manuscript currently`

Also flag subtler prose whose only purpose is to echo an author instruction. Judge
the sentence from the reader's context alone.

## Figure And Benchmark Review

Check:

- Every figure has one clear reader-facing job and can be understood by readers who
  scan title, abstract, and figures before the body.
- Captions describe what is shown and the intended inference without slogans,
  classification disclaimers, or unreported guarantees.
- Fig. 1 remains the simple classification schematic.
- Fig. 2 matches `figures/benchmark_number_conserving.pdf`.
- Fig. 3 matches `figures/benchmark_pairing_delta.pdf`.
- Reported parameters, observables, uncertainty statements, and comparison data match
  the benchmark records.
- Technical caveats are placed where they affect interpretation, not inserted by
  default into the caption or conclusion.
