#!/usr/bin/env python3
"""Reproduce and verify the computational results used by the note."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parents[1]
BUILD = PACKAGE_ROOT / "build"
REFERENCE = PACKAGE_ROOT / "reference"
PYTHON = PACKAGE_ROOT / "python"
OCTAVE = PACKAGE_ROOT / "octave"

CORE_RESULTS = (
    "semigroup_classes.csv",
    "generator_spaces.csv",
    "time_reversal_subgroups.csv",
    "sign_problem_witnesses.csv",
    "model_slice_checks.csv",
)
FULL_RESULT = "pauli_realization_scan.csv"


def command_text(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def run(command: list[str], *, cwd: Path = REPO_ROOT) -> None:
    print(f"\n$ {command_text(command)}", flush=True)
    environment = os.environ.copy()
    for variable in (
        "OPENBLAS_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        environment[variable] = "1"
    subprocess.run(command, cwd=cwd, check=True, env=environment)


def octave_command(argument: str | None) -> list[str]:
    configured = argument or os.environ.get("OCTAVE_COMMAND")
    if configured:
        return shlex.split(configured)
    executable = shutil.which("octave") or shutil.which("octave-cli")
    if executable:
        return [executable]
    raise SystemExit(
        "Octave was not found. Activate the environment from environment.yml, "
        "or set OCTAVE_COMMAND, for example:\n"
        "  OCTAVE_COMMAND='conda run -n bafqmc-contraction octave'"
    )


def octave_eval(command: list[str], expression: str) -> None:
    run(command + ["--quiet", "--eval", expression])


def reproduce(octave: list[str], *, full: bool) -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    octave_path = OCTAVE.relative_to(REPO_ROOT).as_posix()
    build_path = BUILD.relative_to(REPO_ROOT).as_posix()
    octave_eval(
        octave,
        (
            f"addpath('{octave_path}'); "
            f"enumerate_semigroup_classes('{build_path}/semigroup_classes.csv'); "
            f"derive_generator_spaces('{build_path}/generator_spaces.csv');"
        ),
    )
    run(
        [
            sys.executable,
            str(PYTHON / "enumerate_time_reversal_subgroups.py"),
            "--output",
            str(BUILD / "time_reversal_subgroups.csv"),
        ]
    )
    run(
        [
            sys.executable,
            str(PYTHON / "verify_model_slices.py"),
            "--output",
            str(BUILD / "model_slice_checks.csv"),
        ]
    )
    run(
        [
            sys.executable,
            str(PYTHON / "search_sign_problem_witnesses.py"),
            "--input",
            str(BUILD / "time_reversal_subgroups.csv"),
            "--output",
            str(BUILD / "sign_problem_witnesses.csv"),
        ]
    )
    if full:
        octave_eval(
            octave,
            (
                f"addpath('{octave_path}'); "
                f"scan_pauli_realizations('{build_path}/{FULL_RESULT}');"
            ),
        )
    run(
        [
            sys.executable,
            str(PYTHON / "plot_periodic_table.py"),
            "--input",
            str(BUILD / "time_reversal_subgroups.csv"),
            "--pdf",
            str(BUILD / "periodic_table.pdf"),
            "--png",
            str(BUILD / "periodic_table.png"),
        ]
    )


def verify(*, full: bool, compare_reference: bool) -> None:
    command = [
        sys.executable,
        str(PYTHON / "verify_results.py"),
        "--results",
        str(BUILD),
        "--reference",
        str(REFERENCE),
        "--repo-root",
        str(REPO_ROOT),
    ]
    if full:
        command.append("--full")
    if not compare_reference:
        command.append("--skip-reference-comparison")
    run(command)
    run(
        [
            sys.executable,
            str(PYTHON / "verify_model_tex.py"),
            "--tex",
            str(REPO_ROOT / "note" / "ContractionSemigroupsQMC.tex"),
            "--model-script",
            str(PYTHON / "verify_model_slices.py"),
        ]
    )
    run(
        [
            sys.executable,
            str(PYTHON / "verify_time_reversal_tex.py"),
            "--csv",
            str(BUILD / "time_reversal_subgroups.csv"),
        ]
    )


def publish(*, full: bool) -> None:
    for name in CORE_RESULTS:
        shutil.copy2(BUILD / name, REFERENCE / name)
    if full:
        shutil.copy2(BUILD / FULL_RESULT, REFERENCE / FULL_RESULT)
    shutil.copy2(
        BUILD / "periodic_table.pdf",
        REPO_ROOT / "figures" / "contraction_semigroup_periodic_table.pdf",
    )
    verify(full=full, compare_reference=True)
    print("\nPublished verified CSV snapshots and Fig. 1.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reproduce the enumeration behind ContractionSemigroupsQMC.tex."
    )
    parser.add_argument(
        "action",
        choices=("check", "publish", "note"),
        help=(
            "check recomputes without touching approved results; publish updates "
            "approved CSV files and Fig. 1; note compiles the TeX source"
        ),
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="also scan all 8568 ordered Pauli realizations with one to three factors",
    )
    parser.add_argument(
        "--octave-command",
        help="command used to launch Octave; OCTAVE_COMMAND is the environment equivalent",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.action == "note":
        run(["latexmk", "note/ContractionSemigroupsQMC.tex"])
        return

    octave = octave_command(arguments.octave_command)
    reproduce(octave, full=arguments.full)
    if arguments.action == "check":
        verify(full=arguments.full, compare_reference=True)
    else:
        verify(full=arguments.full, compare_reference=False)
        publish(full=arguments.full)


if __name__ == "__main__":
    main()
