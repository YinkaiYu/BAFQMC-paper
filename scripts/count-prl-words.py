#!/usr/bin/env python3
"""APS Letter length estimator for this manuscript; run in Linux/WSL.

Rules: https://journals.aps.org/authors/length-guide (verified 2026-09-20).
Only scratch copies in .build/ are changed. No report is generated.
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RULES = 'https://journals.aps.org/authors/length-guide'
LIMIT = 3750
ENV = re.compile(r'\\(begin|end)\{([^}]+)\}')
MATH = {'equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
        'multline', 'multline*', 'displaymath'}
MATRIX = {'matrix', 'pmatrix', 'bmatrix', 'Bmatrix', 'vmatrix', 'Vmatrix',
          'smallmatrix', 'array', 'cases'}


def uncomment(text):
    return re.sub(r'(?<!\\)%[^\n]*', '', text)


def environments(text, names):
    """Yield balanced, outermost matching environments (including nested math)."""
    stack = []
    for match in ENV.finditer(text):
        action, name = match.groups()
        if action == 'begin':
            stack.append((name, match.start(), match.end()))
        else:
            if not stack or stack[-1][0] != name:
                raise ValueError(f'Unbalanced LaTeX environment: {name}')
            _, start, content = stack.pop()
            if name in names and not any(x[0] in names for x in stack):
                yield start, match.end(), name, text[content:match.start()]
    if stack:
        raise ValueError(f'Unclosed LaTeX environment: {stack[-1][0]}')


def remove_environments(text, names):
    spans = list(environments(text, names))
    for start, end, _, _ in reversed(spans):
        text = text[:start] + '\n' + text[end:]
    return text


def math_rows(body):
    """Count equation rows; also report a matrix-internal-row allowance."""
    matrices = list(environments(body, MATRIX))
    allowance = sum(max(0, len(re.findall(r'\\\\', block)))
                    for _, _, _, block in matrices)
    for start, end, _, _ in reversed(matrices):
        body = body[:start] + ' MATRIX ' + body[end:]
    # Ignore a trailing row terminator. Alignment markers do not add rows.
    pieces = re.split(r'\\\\(?:\[[^]]*\])?', body)
    rows = sum(bool(re.sub(r'\\(?:begin|end|label)\{[^}]*\}|[\s&]', '', p))
               for p in pieces)
    return max(rows, 1), allowance


def label(body):
    match = re.search(r'\\label\{([^}]+)\}', body)
    if not match:
        raise ValueError('Every counted equation/figure/table needs a label for auditable counting.')
    return match[1]


def table_fingerprint(body):
    """Ignore the caption; changing the table itself invalidates its reviewed rows."""
    match = re.search(r'\\begin\{(?:tikzpicture|tabular\*?|tabularx)\}', body)
    if not match:
        raise ValueError('Unknown table format; review its rendered line count.')
    return hashlib.sha256(re.sub(r'\s+', '', body[match.start():]).encode()).hexdigest()


def graphics(body, double):
    items = re.findall(r'\\includegraphics(?:\[([^]]*)\])?\{([^}]+)\}', body)
    if len(items) != 1:
        raise ValueError('Each figure must embed one combined PDF; review new layouts.')
    options, name = items[0]
    if options.replace(' ', '') not in ('width=\\linewidth', 'width=\\columnwidth',
                                        'width=\\textwidth'):
        raise ValueError(f'Unsupported figure sizing/cropping: {name}: {options}')
    import fitz
    with fitz.open(ROOT / name) as doc:
        if len(doc) != 1:
            raise ValueError(f'Expected a one-page figure: {name}')
        rect = doc[0].rect
        ratio = rect.width / rect.height
    return (600 if double else 150) / ratio + (40 if double else 20), ratio


def text_copy(source):
    source = source.split(r'\bibliography{', 1)[0]
    source = source.split(r'\end{document}', 1)[0] + '\n\\end{document}\n'
    source = re.sub(r'(\\documentclass\[)([^]]*)(\])',
                    lambda m: m[1] + m[2] + ',nofootinbib' + m[3], source, count=1)
    source = source.replace(r'\maketitle', '')
    # wordcount.tex freezes fonts; these packages conflict with that mechanism.
    for package in ('CJK', 'newtxtext', 'newtxmath', 'microtype'):
        source = source.replace('\\usepackage{' + package + '}', '')
    source = remove_environments(source, MATH | {'abstract', 'tikzpicture', 'acknowledgments',
                                                'tabular', 'tabular*', 'tabularx'})
    source = re.sub(r'\\runinsection(?:\[[^]]*\])?\{Acknowledg(?:e)?ments\}.*?'
                    r'(?=\\runinsection|\\end\{document\})', '', source, flags=re.S)
    source = re.sub(r'\\includegraphics(?:\[[^]]*\])?\{[^}]*\}', '', source)
    return source


def count_text(source, scratch):
    (scratch / 'count.tex').write_text(text_copy(source))
    shutil.copy(ROOT / '.build/main.aux', scratch / 'count.aux')
    run = subprocess.run(['pdflatex', r'wordcount.tex\csname ?\endcsname'],
                         input='count.tex\n', cwd=scratch, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    (scratch / 'console.log').write_text(run.stdout)
    log = (scratch / 'wordcount.log').read_text(errors='replace')
    if run.returncode or any(line.startswith('!') for line in log.splitlines()):
        raise ValueError(f'wordcount.tex failed; inspect {scratch / "wordcount.log"}')
    if 'undefined references' in log or re.search(r'(?:Citation|Reference).*undefined', log):
        raise ValueError('Unresolved references in counting copy; rebuild the manuscript.')
    count = sum(bool(re.search(r'3[.]0863[35]', line)) for line in log.splitlines())
    if count == 0:
        raise ValueError('No wordcount markers found; refusing to report zero words.')
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-build', action='store_true', help='require an already up-to-date build')
    parser.add_argument('--check', action='store_true', help='exit 1 if the conservative total exceeds 3750')
    parser.add_argument('--table-lines', action='append', default=[], metavar='LABEL=N',
                        help='explicit rendered line count for a new/changed table (including header)')
    args = parser.parse_args()
    if platform.system() != 'Linux':
        raise ValueError('Run via scripts/count-prl-words.ps1 on Windows, or directly in Linux/WSL.')
    for tool in ('pdflatex', 'kpsewhich', 'latexmk'):
        if not shutil.which(tool):
            raise ValueError(f'Missing Linux/WSL dependency: {tool}')
    if not subprocess.run(['kpsewhich', 'wordcount.tex'], capture_output=True).stdout.strip():
        raise ValueError('Install the TeX Live wordcount package first.')
    build = ROOT / '.build'
    build.mkdir(exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='prl-wordcount-', dir=build))
    if args.no_build:
        outputs = [build / 'main.pdf', build / 'main.aux', build / 'main.fls']
        if not all(p.exists() for p in outputs):
            raise ValueError('No complete build found; rerun without --no-build.')
        dependencies = set(ROOT.glob('*.bib')) | {ROOT / 'main.tex', ROOT / 'SM.tex', ROOT / '.latexmkrc'}
        for line in (build / 'main.fls').read_text().splitlines():
            if line.startswith('INPUT '):
                path = (ROOT / line[6:]).resolve()
                if path.is_relative_to(ROOT) and not path.is_relative_to(build):
                    dependencies.add(path)
        oldest = min(p.stat().st_mtime for p in outputs[:2])
        if any(not p.exists() or p.stat().st_mtime > oldest for p in dependencies):
            raise ValueError('Manuscript dependencies changed; rerun without --no-build.')
    else:
        run = subprocess.run(['latexmk', 'main.tex'], cwd=ROOT, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=180)
        (scratch / 'build.log').write_text(run.stdout)
        if run.returncode:
            raise ValueError(f'Build failed; inspect {scratch / "build.log"}')
    source = uncomment((ROOT / 'main.tex').read_text())
    if r'\bibliography{' not in source:
        raise ValueError('Expected a bibliography boundary in main.tex.')
    body = source.split(r'\begin{document}', 1)[1].split(r'\bibliography{', 1)[0]
    if re.search(r'\\(?:input|include)\b|\\\[|\$\$|\\begin\{(?:eqnarray|flalign|alignat|widetext|longtable)', body):
        raise ValueError('New included source or unsupported math/table layout; extend the parser before counting.')
    reviewed = json.loads((ROOT / 'scripts/prl-table-lines.json').read_text())
    overrides = {}
    for item in args.table_lines:
        key, value = item.rsplit('=', 1)
        overrides[key] = int(value)
        if overrides[key] < 1:
            raise ValueError('Table lines must be positive.')
    entries, matrix_extra, seen_tables = [], 0, set()
    for _, _, kind, content in environments(body, MATH | {'figure', 'figure*', 'table', 'table*'}):
        if kind in MATH:
            rows, extra = math_rows(content)
            entries.append((f'Math {label(content)}: {rows} row(s)', rows * 16))
            matrix_extra += extra * 16
        elif kind.startswith('figure'):
            words, ratio = graphics(content, kind.endswith('*'))
            entries.append((f'Figure {label(content)}: aspect {ratio:.6f}', words))
        else:
            key = label(content)
            seen_tables.add(key)
            record = reviewed.get(key, {})
            if key in overrides:
                lines = overrides[key]
            elif record.get('sha256') == table_fingerprint(content):
                lines = record['lines']
            else:
                raise ValueError(f'Table {key} changed: inspect the PDF and pass --table-lines {key}=N; '
                                 'count wrapped lines and headers, not just logical rows.')
            words = (26 + 13 * lines) if kind.endswith('*') else (13 + 6.5 * lines)
            entries.append((f'Table {key}: {lines} rendered lines', words))
    if overrides.keys() - seen_tables:
        raise ValueError(f'Unknown table override: {overrides.keys() - seen_tables}')
    words = count_text(source, scratch)
    total = words + sum(value for _, value in entries)
    print(f'APS PRL length estimate (limit {LIMIT}); rules: {RULES}')
    print(f'{"Text (body, headings, captions, notes, code availability)":72} {words:9.2f}')
    for name, value in entries:
        print(f'{name:72} {value:9.2f}')
    print(f'\nTotal:                 {total:.2f} equivalent words')
    print(f'Matrix-row allowance:  {matrix_extra:.2f}')
    print(f'Conservative total:    {total + matrix_extra:.2f}')
    print(f'Difference from limit: {total - LIMIT:+.2f} to {total + matrix_extra - LIMIT:+.2f}')
    print('Excluded: abstract, acknowledgments, title/authors, references, Supplemental Material.')
    print('Equation rows are source layout rows; inspect the PDF after changing formula layout.')
    print('APS provides an estimator, not a uniquely specified production word count.')
    print(f'Scratch logs: {scratch.relative_to(ROOT)} (no report generated)')
    return 1 if args.check and total + matrix_extra > LIMIT else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.TimeoutExpired, ImportError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(2)
