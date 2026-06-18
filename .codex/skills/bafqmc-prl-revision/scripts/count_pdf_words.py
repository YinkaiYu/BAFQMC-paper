#!/usr/bin/env python3
"""Approximate word counts for reference PDFs.

This is only for style calibration. It is not an APS production word count.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz


MARKERS = [
    "Acknowledgement:",
    "Acknowledgments",
    "Acknowledgements",
    "Appendix",
    "APPENDIX",
]


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z0-9'\-]*|\d+(?:\.\d+)?", text))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: count_pdf_words.py PDF [PDF ...]", file=sys.stderr)
        return 2
    for arg in sys.argv[1:]:
        path = Path(arg)
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        candidates = [(text.find(marker), marker) for marker in MARKERS if text.find(marker) >= 0]
        cut, marker = min(candidates) if candidates else (len(text), "none")
        print(
            f"{path.name}\tpages={doc.page_count}\tmarker={marker}"
            f"\twords_to_marker={count_words(text[:cut])}\tfull_words={count_words(text)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
