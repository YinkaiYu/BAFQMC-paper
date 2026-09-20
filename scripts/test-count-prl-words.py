"""Small regression checks for counting omissions and nested math handling."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('counter', Path(__file__).with_name('count-prl-words.py'))
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)


class CountingTests(unittest.TestCase):
    def test_matrix_is_not_an_equation_break(self):
        self.assertEqual(counter.math_rows(r'A=\begin{pmatrix}a&b\\c&d\end{pmatrix}'), (1, 1))
        self.assertEqual(counter.math_rows(r'\begin{aligned}a&=b\\c&=d\end{aligned}'), (2, 0))

    def test_exclusions_preserve_caption_and_code(self):
        source = r'''\documentclass[prl]{revtex4-2}
\begin{document}\begin{abstract}ABSTRACT\end{abstract}\maketitle
BODY \begin{equation}DISPLAY\end{equation}
\begin{table}\caption{CAPTION}\begin{tabular}{cc}CELLS\end{tabular}\end{table}
\runinsection{Acknowledgments}THANKS
\runinsection{Code availability}CODE
\bibliography{references}\input{SM.tex}\end{document}'''
        clean = counter.text_copy(source)
        for word in ('BODY', 'CAPTION', 'CODE'):
            self.assertIn(word, clean)
        for word in ('ABSTRACT', 'DISPLAY', 'CELLS', 'THANKS', 'SM.tex'):
            self.assertNotIn(word, clean)

    def test_changed_table_invalidates_review_but_caption_does_not(self):
        table = r'\caption{Old}\begin{tikzpicture}\node{A};\end{tikzpicture}'
        self.assertEqual(counter.table_fingerprint(table), counter.table_fingerprint(table.replace('Old', 'New')))
        self.assertNotEqual(counter.table_fingerprint(table), counter.table_fingerprint(table.replace('{A}', '{B}')))

    def test_unbalanced_environment_is_rejected(self):
        with self.assertRaises(ValueError):
            list(counter.environments(r'\begin{equation}x\end{align}', counter.MATH))


if __name__ == '__main__':
    unittest.main()
