#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [[ "$(uname -s)" != "Linux" ]]; then
  printf '%s\n' 'error: run this build in Linux or WSL2' >&2
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  printf '%s\n' 'error: latexmk is not available in the Linux/WSL environment' >&2
  exit 127
fi

exec latexmk main.tex
