# Revision Workflow

Use this workflow for each substantive manuscript-edit round.

## Before Editing

1. Identify the manuscript unit: Section II, Section III, Section IV, Introduction, or Concluding Remarks.
2. State the physics claim that unit must carry.
3. Check whether the unit should cite new literature. If yes, follow `reference-verification.md`.
4. Decide what belongs in main text and what belongs in SM.

## During Editing

- Keep edits local to the target section unless cross references or notation require small coordinated changes.
- Preserve notation and equation labels where possible.
- Keep Fig. 1 classification visible in the conceptual logic.
- Do not introduce process-facing prose or user-prompt language into the manuscript.
- Use the current Section IV pairing convention: `-\Delta b^+c^+ - \Delta^*bc`. Do not describe it as a gauge transform in the manuscript.
- Use real positive triangular hopping in the main example unless the author asks for the complex hopping generalization.

## After Drafting

1. Run `opencode` prose review for important prose:

```bash
opencode run -m deepseek/deepseek-v4-pro "<prompt>"
```

2. Ask a fresh independent-context agent to review with `review-prompts.md`. Require findings first, concrete corrections, and file/line references where possible.
3. Compile:

```bash
latexmk main.tex
```

4. Refresh `pdf/main.pdf`.
5. Refresh `pdf/main-diff.pdf` against the previous substantive content-edit commit, unless the author specifies another baseline.
   When using `latexpand`, run it from the old/new source directories, not from the repository root, so `\input{SM.tex}` expands the matching old/new Supplemental Material rather than the current working-tree file.
6. Run a process-language scan on changed manuscript files:

```bash
rg -n "we add|as requested|this revision|to address|we now clarify|requested benchmark|the manuscript currently|this addresses|we have added|we now modify" main.tex SM.tex
```

7. Report warnings that are relevant to changed text, figures, labels, or citations.
8. Commit after a coherent edit round.

## Review Gates

A round is not complete until:

- The manuscript compiles.
- The changed section has no unfinished markers.
- Figure references and captions match the actual figure files.
- Any new references have verified metadata.
- A fresh independent review has checked reader-friendliness, style fit, physics claims, and process-facing language.
