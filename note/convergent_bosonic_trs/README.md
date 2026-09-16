# Contraction, time reversal, and positive bosonic traces

The standalone lecture is [ConvergentBosonicTRS.tex](../ConvergentBosonicTRS.tex).
The English lecture now derives positivity primarily from contraction,
a common physical time reversal, and a continuous connection to the known
positive partition function of independent harmonic oscillators.
It includes the two standard forms, the explicit reflection-positive
mode transformation and physical metric, and a stable paired
auxiliary-field example.

The extension to amplifying slices and its Gaussian-state proof are in
Appendix C. Final trace-class convergence is distinguished from damping
of each original slice. The reflected-pair proof states the
matrix-element limiting condition for unbounded RP constructions.

The [Chinese edition](../ConvergentBosonicTRS_zh.tex) currently presents
the September 15 state-evolution proof and contraction correspondence.
It has not yet incorporated the September 16 English reorganization and
new RP section; equation numbering differs.

## Build

From the repository root on Linux or WSL:

~~~sh
latexmk -pdf note/ConvergentBosonicTRS.tex
~~~

The repository configuration puts temporary output in .build/ and copies
the finished document to pdf/ConvergentBosonicTRS.pdf.
From native Windows PowerShell:

~~~powershell
.\scripts\run-in-wsl.ps1 'latexmk -pdf note/ConvergentBosonicTRS.tex'
~~~

Build the Chinese edition with XeLaTeX (the bundled Fandol Chinese fonts
are used):

~~~sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error note/ConvergentBosonicTRS_zh.tex
~~~

Or from native Windows PowerShell:

~~~powershell
.\scripts\run-in-wsl.ps1 'latexmk -xelatex -interaction=nonstopmode -halt-on-error note/ConvergentBosonicTRS_zh.tex'
~~~

Its finished PDF is copied to pdf/ConvergentBosonicTRS_zh.pdf. Both editions
use the same verification code below.

## Verification

~~~sh
python3 note/convergent_bosonic_trs/verify.py
~~~

Or from native PowerShell:

~~~powershell
.\scripts\run-in-wsl.ps1 'python3 note/convergent_bosonic_trs/verify.py'
~~~

Only NumPy is required. The checks compare independent descriptions:

- The one-mode damped squeezing trace and vacuum amplitude against
  increasing finite-Fock cutoffs.
- The coupled two-mode example with time-reversal square -I, using
  finite-Fock products, the Gaussian coherent-state integral, and the
  differential equations for the pair matrix and vacuum amplitude.
- The thermal filter's limit to the vacuum amplitude.
- Forty-eight noncommuting Gaussian products in the two symmetry forms,
  testing physical contraction against convergence of the kernel and the
  explicit matrix identity in Appendix B.
- Twenty-four RP block generators, checking the explicit change of modes,
  canonical commutators, physical adjoints, transformed real coefficients,
  and contraction in both bases.
- Eighty-two points on continuous paths from independent oscillators to
  products with unitary factors, for both squares of time reversal.
- A noncommuting two-mode RP product with intra-flavor and inter-flavor
  pairing and relative-density fields, comparing the Gaussian trace with
  increasing finite-Fock cutoffs.

The finite-Fock cutoffs test convergence of the examples. They are not used
as proofs of the general theorem.

## Reference records

The lecture has its own short bibliography and does not change the
manuscript's references.bib. Metadata were checked on September 15, 2026.

- *hilgert1989*: Joachim Hilgert, *A note on Howe's oscillator semigroup*,
  Annales de l'Institut Fourier **39** (3), 663–688 (1989),
  DOI 10.5802/aif.1182. Verified against the
  [publisher record](https://aif.centre-mersenne.org/articles/10.5802/aif.1182/).
- *derezinski2017*: Jan Dereziński and Maciej Karczmarczyk,
  *Quantization of Gaussians*, arXiv:1701.07297 (2017).
  The lecture cites this arXiv version, whose author list, title, dates, and
  identifier were checked against the
  [arXiv record](https://arxiv.org/abs/1701.07297).

These citations identify background on Gaussian operators and contraction.
The sign argument and the kernel calculation needed by the lecture are
derived in the lecture itself. Exact-key source PDFs were downloaded,
identified from their title pages, and recorded in the ignored candidate
cache:

- [Hilgert PDF](../../local_reference_pdfs/candidates/hilgert1989.pdf)
- [Dereziński and Karczmarczyk PDF](../../local_reference_pdfs/candidates/derezinski2017.pdf)

These background PDFs are optional reading and are not needed to build the lecture.
