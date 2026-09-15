# Convergent bosonic traces and time reversal

The standalone lecture is [ConvergentBosonicTRS.tex](../ConvergentBosonicTRS.tex).
It derives a sufficient positive-trace theorem from a normalizable Gaussian
vacuum evolution and explains the two physical contraction-semigroup forms.
It explicitly proves the required state condition for Hermitian,
anti-Hermitian, and dissipative slices. It does not replace that condition
by finiteness of an arbitrary non-Hermitian endpoint matrix.

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
