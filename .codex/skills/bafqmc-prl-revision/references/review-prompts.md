# Independent Review Prompts

Use these prompts after each substantive edit round. The reviewer should not rewrite the paper wholesale. Ask for findings and actionable corrections.

## Physics And Claims Review

Review the changed manuscript section for physics consistency. Check:

- Does it preserve the Fig. 1 classification: BAFQMC sign-free for RP/TRS, SSE/WLQMC sign-free for unfrustrated systems, and the upper-left quadrant as new computable territory?
- Are TRS/RP assumptions stated accurately?
- Are paired/Nambu branch and pole statements no stronger than supported?
- Does the pairing term use the current Hermitian convention `-\Delta b^+c^+ - \Delta^*bc` consistently, without gauge-transform wording in the manuscript?
- Does the benchmark wording avoid overclaiming beyond `3x3` proof-of-principle data?

Return findings first, with file and line references when possible.

## PRL Style Review

Compare the changed section against the style-reference notes in `.codex/skills/bafqmc-prl-revision/references/style-analysis.md`. Check:

- Is the prose direct, confident, and readable by theoretical physicists?
- Does it avoid unnecessary "not ... but ..." constructions?
- Does it minimize dashes?
- Does every paragraph have a clear role in the story?
- Are proofs and implementation details kept out of the main text when they interrupt the flow?
- Does each section opening introduce the new question or claim, rather than repeating previous material or jumping to an undefined issue?
- Are theorem-like statements limited to assumptions and conclusions, with intuition, examples, and caveats moved outside the statement?
- Is it attractive enough to keep a theorist reading?

Return concrete edits or concerns, not generic praise.

## Reader-Burden Review

Review the changed text as a first-time theoretical-physics reader. Flag places where the reader must reconstruct missing context. Check:

- Are all operators, indices, fields, matrices, and commutators defined before compact formulas use them?
- Are symbols reintroduced after a long gap before they are used in derivations or algorithms?
- Does the prose avoid one-use variables, scalar factors, diagnostics, or branch parameters that do not help the local result?
- Are determinant identities, update ratios, conjugacy relations, and stabilization formulas derived at the point where the reader needs them, rather than hidden behind phrases such as "similarly" or "the same manipulation"?
- Does an early formal section avoid relying on later benchmark details unless the benchmark object has already been introduced?

## Process-Language Review

Search for sentences that reveal the author-assistant process or explicitly answer a prompt. Flag wording such as:

- "we add"
- "as requested"
- "this revision"
- "to address"
- "we now clarify"
- "the requested benchmark"
- "the manuscript currently"

Also flag prose that sounds like a response to a collaborator rather than a paper sentence.

Use a fresh context for this review. Do not rely on the editing agent's intent; judge only the manuscript prose.

## Figure And Benchmark Review

Check:

- Fig. 1 is treated as the classification schematic.
- Fig. 2 caption matches `figures/benchmark_number_conserving.pdf`.
- Fig. 3 caption matches `figures/benchmark_pairing_delta.pdf`.
- Reported parameters match the benchmark reports.
- Time-step and ED-cutoff caveats are placed appropriately.
