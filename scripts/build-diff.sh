#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'usage: %s BASELINE\n' "$0" >&2
  exit 2
fi

baseline="$1"
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

git rev-parse --verify "${baseline}^{commit}" >/dev/null
rm -rf .build/diff-work
mkdir -p .build/diff-work/old .build/diff-work/new pdf

git show "${baseline}:main.tex" > .build/diff-work/old/main.tex
git show "${baseline}:SM.tex" > .build/diff-work/old/SM.tex
git show "${baseline}:references.bib" > .build/diff-work/old/references.bib
cp main.tex SM.tex references.bib .build/diff-work/new/

(cd .build/diff-work/old && latexpand main.tex > ../old.tex)
(cd .build/diff-work/new && latexpand main.tex > ../new.tex)
latexdiff --math-markup=0 .build/diff-work/old.tex .build/diff-work/new.tex \
  > .build/diff-work/main-diff.tex
latexmk .build/diff-work/main-diff.tex
