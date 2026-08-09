#!/usr/bin/env python3
"""Scan every low-dimensional bosonic Pauli representation for a sign witness.

The scan covers all physical ordered real-Pauli pairs with one to three tensor
factors in the 20 relation classes whose current time-reversal construction
selects a proper ``A_group`` subspace.  Pairs with ``J1 == J2`` are included.

For each representation, random ordered products are drawn from its complete
maximal-group Lie algebra.  The bosonic square-root branch is continued from a
stable number-damping reference along a specified complex detour.  A reported
negative continued branch is independently checked with a finer path and with
detours on both sides of the real interpolation.  This continuation is a
path-recorded diagnostic; it is not identified with a convergent Fock trace at
the endpoint.  Records are written as they are found, so memory use does not
grow with the number of representations.

This finite seeded scan supplies reproducible witnesses in the searched Pauli
family.  It is not a classification of arbitrary bosonic representations.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

from enumerate_time_reversal_subgroups import (
    canonical_matrices,
    class_id,
    five_relations,
    group_basis,
    pauli_matrix,
    pauli_words,
    physical_time_reversal,
    time_reversal_is_physical,
)
from search_sign_problem_witnesses import continued_boson_weight


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSIFICATION = (
    PACKAGE_ROOT / "reference" / "time_reversal_subgroups.csv"
)
DEFAULT_OUTPUT = (
    PACKAGE_ROOT / "build" / "boson_representation_witnesses.csv"
)
DEFAULT_SEED = 20260809
WEIGHT_TOLERANCE = 1.0e-7
EXPECTED_REPRESENTATIONS_BY_FACTOR = {1: 4, 2: 50, 3: 712}

FIELDNAMES = [
    "statistics",
    "class_number",
    "class_id",
    "s1",
    "q1",
    "s2",
    "q2",
    "r",
    "semigroup_status",
    "time_reversal_table_scope",
    "number_of_pauli_factors",
    "nambu_dimension",
    "J1_word",
    "J2_word",
    "A_group_dimension",
    "A_group_basis",
    "base_seed",
    "representation_seed",
    "ordered_pair_index",
    "attempt",
    "slice_count",
    "coefficient_scale",
    "coefficients",
    "stable_basis",
    "stable_coefficient",
    "coarse_steps",
    "coarse_detour",
    "verification_steps",
    "verification_detour",
    "witness_type",
    "weight_real",
    "weight_imag",
    "radicand_real",
    "radicand_imag",
    "identity_residual",
    "refinement_residual",
    "opposite_detour_residual",
    "opposite_radicand_residual",
    "continuation_winding",
    "opposite_continuation_winding",
    "continuation_minimum",
]


def class_number(signs: tuple[int, int, int, int, int]) -> int:
    return 1 + sum(
        (sign == -1) * weight
        for sign, weight in zip(signs, (16, 8, 4, 2, 1))
    )


def read_proper_rows(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["statistics"] == "boson"
            and row["time_reversal_result"]
            == "proper A_group subspace"
        ]
    if len(rows) != 20:
        raise AssertionError(
            f"expected 20 proper-subgroup boson rows, found {len(rows)}"
        )
    result = {int(row["class_number"]): row for row in rows}
    if len(result) != len(rows):
        raise AssertionError("duplicate bosonic relation class")
    return result


def random_slices(
    generators: list[np.ndarray],
    random: np.random.Generator,
    attempt: int,
) -> tuple[list[np.ndarray], np.ndarray, float]:
    slice_counts = (1, 2, 3, 4)
    scales = (0.5, 1.0, 2.0, 3.0, 4.0, 6.0)
    slice_count = slice_counts[(attempt - 1) % len(slice_counts)]
    scale = scales[
        ((attempt - 1) // len(slice_counts)) % len(scales)
    ]
    coefficients = random.normal(
        scale=scale,
        size=(slice_count, len(generators)),
    )
    slices = [
        sum(
            (
                coefficient * generator
                for coefficient, generator in zip(values, generators)
            ),
            start=np.zeros_like(generators[0]),
        )
        for values in coefficients
    ]
    return slices, coefficients, scale


def find_witness(
    row: dict[str, str],
    number_of_factors: int,
    ordered_pair_index: int,
    first_word: str,
    second_word: str,
    signs: tuple[int, int, int, int, int],
    basis: list[tuple[str, np.ndarray]],
    base_seed: int,
    attempts: int,
    coarse_steps: int,
    verification_steps: int,
) -> dict[str, object]:
    basis_names = [name for name, _ in basis]
    generators = [generator for _, generator in basis]
    stable_name = "Z" + "I" * (number_of_factors - 1)
    if stable_name not in basis_names:
        raise AssertionError(
            f"no number-damping direction for {first_word}, {second_word}"
        )
    stable_coefficient = -3.0
    stable_generator = (
        stable_coefficient * generators[basis_names.index(stable_name)]
    )

    representation_seed = (
        base_seed + 100000 * number_of_factors + ordered_pair_index
    )
    random = np.random.default_rng(representation_seed)
    coarse_detour = 0.1
    verification_detour = 0.05

    for attempt in range(1, attempts + 1):
        slices, coefficients, scale = random_slices(
            generators, random, attempt
        )
        try:
            with np.errstate(over="ignore", under="ignore", invalid="ignore"):
                coarse_weight, _, coarse_winding, coarse_minimum = (
                    continued_boson_weight(
                        slices,
                        stable_generator,
                        steps=coarse_steps,
                        detour=coarse_detour,
                    )
                )
        except (FloatingPointError, OverflowError, np.linalg.LinAlgError):
            continue
        if (
            abs(coarse_weight.imag) >= WEIGHT_TOLERANCE
            or coarse_weight.real >= -WEIGHT_TOLERANCE
        ):
            continue

        try:
            with np.errstate(over="ignore", under="ignore", invalid="ignore"):
                weight, radicand, winding, positive_minimum = (
                    continued_boson_weight(
                        slices,
                        stable_generator,
                        steps=verification_steps,
                        detour=verification_detour,
                    )
                )
                opposite_weight, opposite_radicand, opposite_winding, (
                    opposite_minimum
                ) = continued_boson_weight(
                    slices,
                    stable_generator,
                    steps=verification_steps,
                    detour=-verification_detour,
                )
        except (FloatingPointError, OverflowError, np.linalg.LinAlgError):
            continue

        identity_residual = abs(1.0 / (weight * weight) - radicand) / max(
            1.0, abs(radicand)
        )
        refinement_residual = abs(weight - coarse_weight) / max(
            1.0, abs(weight)
        )
        opposite_detour_residual = abs(
            opposite_weight - weight.conjugate()
        ) / max(1.0, abs(weight))
        opposite_radicand_residual = abs(
            opposite_radicand - radicand.conjugate()
        ) / max(1.0, abs(radicand))
        continuation_minimum = min(
            coarse_minimum, positive_minimum, opposite_minimum
        )

        verified = (
            abs(weight.imag) < WEIGHT_TOLERANCE
            and weight.real < -WEIGHT_TOLERANCE
            and winding == coarse_winding
            and abs(winding) % 2 == 1
            and abs(opposite_winding) == abs(winding)
            and identity_residual < 1.0e-9
            and refinement_residual < WEIGHT_TOLERANCE
            and opposite_detour_residual < WEIGHT_TOLERANCE
            and opposite_radicand_residual < 1.0e-9
            and continuation_minimum > 1.0e-12
        )
        if not verified:
            continue

        return {
            "statistics": "boson",
            "class_number": int(row["class_number"]),
            "class_id": class_id(signs),
            "s1": signs[0],
            "q1": signs[1],
            "s2": signs[2],
            "q2": signs[3],
            "r": signs[4],
            "semigroup_status": row["semigroup_status"],
            "time_reversal_table_scope": row["time_reversal_result"],
            "number_of_pauli_factors": number_of_factors,
            "nambu_dimension": 2**number_of_factors,
            "J1_word": first_word,
            "J2_word": second_word,
            "A_group_dimension": len(basis),
            "A_group_basis": ";".join(basis_names),
            "base_seed": base_seed,
            "representation_seed": representation_seed,
            "ordered_pair_index": ordered_pair_index,
            "attempt": attempt,
            "slice_count": len(slices),
            "coefficient_scale": scale,
            "coefficients": json.dumps(
                coefficients.tolist(), separators=(",", ":")
            ),
            "stable_basis": stable_name,
            "stable_coefficient": stable_coefficient,
            "coarse_steps": coarse_steps,
            "coarse_detour": coarse_detour,
            "verification_steps": verification_steps,
            "verification_detour": verification_detour,
            "witness_type": "negative_continued_branch",
            "weight_real": f"{weight.real:.17g}",
            "weight_imag": f"{weight.imag:.17g}",
            "radicand_real": f"{radicand.real:.17g}",
            "radicand_imag": f"{radicand.imag:.17g}",
            "identity_residual": f"{identity_residual:.3e}",
            "refinement_residual": f"{refinement_residual:.3e}",
            "opposite_detour_residual": (
                f"{opposite_detour_residual:.3e}"
            ),
            "opposite_radicand_residual": (
                f"{opposite_radicand_residual:.3e}"
            ),
            "continuation_winding": winding,
            "opposite_continuation_winding": opposite_winding,
            "continuation_minimum": f"{continuation_minimum:.3e}",
        }

    raise RuntimeError(
        "no verified negative bosonic weight for "
        f"n={number_of_factors}, J1={first_word}, J2={second_word} "
        f"after {attempts} attempts"
    )


def scan(
    proper_rows: dict[int, dict[str, str]],
    output: Path,
    seed: int,
    attempts: int,
    coarse_steps: int,
    verification_steps: int,
    large_verification_steps: int,
) -> tuple[int, Counter[int], set[int]]:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = output.with_name(output.name + ".tmp")
    count_by_factor: Counter[int] = Counter()
    represented_classes: set[int] = set()
    total = 0

    with temporary_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=FIELDNAMES, lineterminator="\n"
        )
        writer.writeheader()

        for number_of_factors in (1, 2, 3):
            words = pauli_words(number_of_factors)
            matrices = {word: pauli_matrix(word) for word in words}
            canonical, conjugation = canonical_matrices(
                "boson", number_of_factors
            )
            ordered_pairs = itertools.product(words, repeat=2)
            for ordered_pair_index, (first_word, second_word) in enumerate(
                ordered_pairs
            ):
                first = matrices[first_word]
                second = matrices[second_word]
                signs = five_relations(canonical, first, second)
                number = class_number(signs)
                if number not in proper_rows:
                    continue
                first_u = physical_time_reversal(first, signs[0])
                second_u = physical_time_reversal(second, signs[2])
                if not time_reversal_is_physical(
                    first_u, canonical, conjugation
                ) or not time_reversal_is_physical(
                    second_u, canonical, conjugation
                ):
                    continue
                basis = group_basis(
                    canonical, first, second, matrices
                )
                if not basis:
                    continue

                record = find_witness(
                    proper_rows[number],
                    number_of_factors,
                    ordered_pair_index,
                    first_word,
                    second_word,
                    signs,
                    basis,
                    seed,
                    attempts,
                    coarse_steps,
                    (
                        verification_steps
                        if number_of_factors <= 2
                        else large_verification_steps
                    ),
                )
                writer.writerow(record)
                total += 1
                count_by_factor[number_of_factors] += 1
                represented_classes.add(number)

    expected_classes = set(proper_rows)
    if dict(count_by_factor) != EXPECTED_REPRESENTATIONS_BY_FACTOR:
        raise AssertionError(
            "unexpected representation counts: "
            f"{dict(sorted(count_by_factor.items()))}"
        )
    if represented_classes != expected_classes:
        missing = sorted(expected_classes - represented_classes)
        extra = sorted(represented_classes - expected_classes)
        raise AssertionError(
            f"relation-class coverage mismatch; missing={missing}, extra={extra}"
        )
    if total != 766:
        raise AssertionError(f"expected 766 witnesses, found {total}")

    temporary_output.replace(output)
    return total, count_by_factor, represented_classes


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--classification", type=Path, default=DEFAULT_CLASSIFICATION
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--attempts", type=int, default=250)
    parser.add_argument("--coarse-steps", type=int, default=129)
    parser.add_argument("--verification-steps", type=int, default=513)
    parser.add_argument(
        "--large-verification-steps", type=int, default=257
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.attempts <= 0:
        raise ValueError("attempts must be positive")
    if (
        arguments.coarse_steps < 3
        or arguments.verification_steps < 3
        or arguments.large_verification_steps < 3
    ):
        raise ValueError("continuation paths require at least three steps")
    total, count_by_factor, represented_classes = scan(
        read_proper_rows(arguments.classification),
        arguments.output,
        arguments.seed,
        arguments.attempts,
        arguments.coarse_steps,
        arguments.verification_steps,
        arguments.large_verification_steps,
    )
    print(
        f"Verified negative continued bosonic branches for {total} physical "
        "Pauli realizations in "
        f"{len(represented_classes)} proper-subgroup relation classes."
    )
    print(
        "Representations by Pauli-factor count: "
        + ", ".join(
            f"n={number}: {count_by_factor[number]}"
            for number in sorted(count_by_factor)
        )
    )
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
