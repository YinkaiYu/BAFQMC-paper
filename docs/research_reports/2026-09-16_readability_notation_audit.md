# Main-text readability and notation audit — 2026-09-16

## Scope and reader-facing purpose

Make the main Letter readable in sequence by a condensed-matter physicist, with
notation defined at first use and physical objects introduced before compressed
terminology. Preserve the established theorem domains, two fundamental TRS classes,
benchmark data, equation numbering, and author-approved regularization discussion.
The cumulative comparison remains `1b207e7`.

## Changes

- Theorem 1 starts with the number-conserving criterion and then states the
  anticommutation relation explicitly. Two displayed rows identify the squares
  of the two or three symmetries and define the sign-set labels.
- Replaced the compressed phrase “Nambu time reversals” with antiunitary
  time-reversal symmetries acting on the defined operator vector. Removed the
  theorem's separate sentence about canonical commutators and Hermitian
  conjugation: these belong to the definition of an operator symmetry. The SM
  retains the explicit operator action and all corresponding matrix conditions.
- Clarified that Table I classifies general quadratic slices, including pairing;
  its single-symmetry entries therefore do not negate the number-conserving result.
- Defined the propagation in the Q=+i subspace before using it, explained the
  antilinearity/anticommutation step, and replaced “canonical sector basis” and
  “creation signs” with their operator meaning. Explained the split orthogonal
  class name through the real matrices that preserve the stated form.
- Replaced the RP “reflected coupling cone” shorthand with its actual block
  condition. Explained the ordering of the flavor operators directly.
- Added first-use meanings for L, N, the fixed-field average, the imaginary-time
  step, and benchmark parameters and observable abbreviations.
- Replaced the conclusion's unexplained contraction/semigroup terminology with
  the physical multiplication property of RP propagators. Its mathematical
  comparison remains in the SM.
- Updated corresponding SM terminology and defined complex conjugation in the
  time-reversal notation. No derivation or regularization condition was removed.

## Terminology check

Nambu space, antiunitary symmetry, Kramers pairing, reflection positivity, and
normal ordering are retained. The issue was unfamiliar combinations and missing
first-use definitions, rather than standard physics vocabulary. Li, Jiang, and
Yao explicitly define their Majorana-time-reversal terminology in their own
framework; it does not supply a definition of “Nambu time reversals” for this
paper. See https://arxiv.org/abs/1601.05780. No bibliography entry was changed.

## Verification

An independent reader reviewed the main text and the final theorem/proof changes.
The review found no substantive change to the physical claims, and confirmed that
the deleted theorem sentence is definitional content retained explicitly in the SM.

Source checks confirm that all equation labels and citation lists are unchanged,
and that the full Gaussian-cutoff regularization section is byte-for-byte identical
after newline normalization. All tracked figures and numerical data are unchanged.
WSL compilation and visual inspection confirm a 34-page manuscript, with Table I on
page 3 and Fig. 2 beside Examples and applications on page 4. Main and cumulative
diff PDFs have no new overfull boxes, undefined references, or citation warnings.
The existing REVTeX default-size and nameref notices and bibliography underfull
line remain; the diff also retains one preexisting underfull line in unchanged text.
