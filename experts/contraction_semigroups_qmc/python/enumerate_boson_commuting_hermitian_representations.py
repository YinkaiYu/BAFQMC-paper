#!/usr/bin/env python3
"""Find bosonic representations with commuting Hermitian group generators.

For bosons the structural analogue of the fermion test requires the quadratic
form ``B = g A`` to define a Hermitian Fock operator and the complete real
``A_group`` basis to commute.  The infinite boson Fock space adds a convergence
condition.  A real group direction contains both signs, so this script reports
the positive convergent domain rather than claiming positivity on the complete
real coefficient line.

The search covers all physical real-Pauli pairs with one to three tensor
factors, including pairs with ``J1 == J2``.
"""

from __future__ import annotations

import argparse
import csv
import itertools
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


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSIFICATION = (
    PACKAGE_ROOT / "reference" / "time_reversal_subgroups.csv"
)
DEFAULT_OUTPUT = (
    PACKAGE_ROOT / "build" / "boson_commuting_hermitian_representations.csv"
)
TOLERANCE = 1.0e-9


def class_number(signs: tuple[int, int, int, int, int]) -> int:
    return 1 + sum(
        (sign == -1) * weight
        for sign, weight in zip(signs, (16, 8, 4, 2, 1))
    )


def boson_hermiticity_residual(
    generator: np.ndarray,
    canonical: np.ndarray,
    conjugation: np.ndarray,
) -> float:
    quadratic_form = canonical @ generator
    return float(
        np.linalg.norm(
            conjugation @ quadratic_form.conj() @ conjugation
            - quadratic_form
        )
    )


def commuting_hermitian_residuals(
    generators: list[np.ndarray],
    canonical: np.ndarray,
    conjugation: np.ndarray,
) -> tuple[float, float]:
    hermiticity_residual = max(
        boson_hermiticity_residual(
            generator, canonical, conjugation
        )
        for generator in generators
    )
    commutator_residual = max(
        np.linalg.norm(first @ second - second @ first)
        for first in generators
        for second in generators
    )
    return float(hermiticity_residual), float(commutator_residual)


def read_scope_rows(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["statistics"] == "boson"
        ]
    if len(rows) != 32:
        raise AssertionError(f"expected 32 bosonic rows, found {len(rows)}")
    return {int(row["class_number"]): row for row in rows}


def stable_trace_residual() -> float:
    maximum_residual = 0.0
    for alpha in (-2.0, -0.7, -0.2, 0.2, 0.7, 2.0):
        propagation = np.diag((np.exp(alpha), np.exp(-alpha)))
        radicand = float(
            -np.linalg.det(np.eye(2) - propagation).real
        )
        expected_radicand = float(4.0 * np.sinh(alpha / 2.0) ** 2)
        maximum_residual = max(
            maximum_residual,
            abs(radicand - expected_radicand)
            / max(1.0, abs(expected_radicand)),
        )
    for alpha in (-0.2, -0.7, -2.0):
        expected = 1.0 / (2.0 * np.sinh(-alpha / 2.0))
        levels = np.arange(1000, dtype=float) + 0.5
        truncated_trace = float(np.exp(alpha * levels).sum())
        radicand = float(4.0 * np.sinh(alpha / 2.0) ** 2)
        determinant_weight = 1.0 / np.sqrt(radicand)
        residual = max(
            abs(truncated_trace - expected),
            abs(determinant_weight - expected),
        ) / max(1.0, abs(expected))
        maximum_residual = max(maximum_residual, residual)
    for alpha in (0.2, 0.7, 2.0):
        continued = np.exp(alpha / 2.0) / (1.0 - np.exp(alpha))
        expected = -1.0 / (2.0 * np.sinh(alpha / 2.0))
        maximum_residual = max(
            maximum_residual,
            abs(continued - expected) / max(1.0, abs(expected)),
            abs(1.0 / continued**2 - 4.0 * np.sinh(alpha / 2.0) ** 2)
            / max(1.0, abs(4.0 * np.sinh(alpha / 2.0) ** 2)),
        )
    if maximum_residual >= 1.0e-12:
        raise AssertionError("bosonic trace and determinant formulas disagree")
    return maximum_residual


def enumerate_candidates(
    scope_rows: dict[int, dict[str, str]],
) -> list[dict[str, object]]:
    candidates: dict[int, list[dict[str, object]]] = {
        number: [] for number in range(1, 33)
    }
    for number_of_factors in (1, 2, 3):
        words = pauli_words(number_of_factors)
        matrices = {word: pauli_matrix(word) for word in words}
        canonical, conjugation = canonical_matrices(
            "boson", number_of_factors
        )
        for first_word, second_word in itertools.product(words, repeat=2):
            first = matrices[first_word]
            second = matrices[second_word]
            signs = five_relations(canonical, first, second)
            first_u = physical_time_reversal(first, signs[0])
            second_u = physical_time_reversal(second, signs[2])
            if not time_reversal_is_physical(
                first_u, canonical, conjugation
            ) or not time_reversal_is_physical(
                second_u, canonical, conjugation
            ):
                continue
            basis = group_basis(canonical, first, second, matrices)
            if not basis:
                continue
            hermiticity_residual, commutator_residual = (
                commuting_hermitian_residuals(
                    [generator for _, generator in basis],
                    canonical,
                    conjugation,
                )
            )
            if (
                hermiticity_residual >= TOLERANCE
                or commutator_residual >= TOLERANCE
            ):
                continue
            candidates[class_number(signs)].append(
                {
                    "number_of_pauli_factors": number_of_factors,
                    "nambu_dimension": 2**number_of_factors,
                    "J1_word": first_word,
                    "J2_word": second_word,
                    "A_group_dimension": len(basis),
                    "A_group_basis": ";".join(
                        name for name, _ in basis
                    ),
                    "hermiticity_residual": hermiticity_residual,
                    "commutator_residual": commutator_residual,
                }
            )

    formula_residual = stable_trace_residual()
    records: list[dict[str, object]] = []
    for number, representations in candidates.items():
        if not representations:
            continue
        minimum_factors = min(
            int(row["number_of_pauli_factors"])
            for row in representations
        )
        at_minimum = [
            row
            for row in representations
            if int(row["number_of_pauli_factors"]) == minimum_factors
        ]
        representative = min(
            at_minimum,
            key=lambda row: (
                -int(row["A_group_dimension"]),
                str(row["J1_word"]),
                str(row["J2_word"]),
            ),
        )
        if (
            representative["A_group_basis"] != "Z"
            or representative["A_group_dimension"] != 1
        ):
            raise AssertionError("unexpected bosonic generator algebra")
        scope = scope_rows[number]
        signs = tuple(
            int(scope[field]) for field in ("s1", "q1", "s2", "q2", "r")
        )
        records.append(
            {
                "class_number": f"B{number:02d}",
                "class_id": class_id(signs),
                "semigroup_status": scope["semigroup_status"],
                "time_reversal_table_scope": scope["time_reversal_result"],
                **representative,
                "convergence_domain": "alpha < 0",
                "exact_weight_formula": "1 / (2 sinh(-alpha/2))",
                "determinant_radicand": "4 sinh(alpha/2)^2",
                "continued_domain": "alpha > 0",
                "continued_weight_formula": "-1 / (2 sinh(alpha/2))",
                "complete_real_group_status": (
                    "negative pure-group meromorphic continuation"
                ),
                "formula_residual": formula_residual,
                "search_maximum_number_of_pauli_factors": 3,
                "qualifying_count_one_factor": sum(
                    int(row["number_of_pauli_factors"]) == 1
                    for row in representations
                ),
                "qualifying_count_two_factors": sum(
                    int(row["number_of_pauli_factors"]) == 2
                    for row in representations
                ),
                "qualifying_count_three_factors": sum(
                    int(row["number_of_pauli_factors"]) == 3
                    for row in representations
                ),
                "qualifying_representations_at_minimum_dimension": len(
                    at_minimum
                ),
                "qualifying_representations_through_three_factors": len(
                    representations
                ),
            }
        )
    return records


def validate_records(records: list[dict[str, object]]) -> None:
    expected_classes = {"B05", "B17"}
    actual_classes = {str(row["class_number"]) for row in records}
    if actual_classes != expected_classes:
        raise AssertionError(
            f"unexpected bosonic classes: {sorted(actual_classes)}"
        )
    if any(
        row["semigroup_status"] != "contraction semigroup"
        for row in records
    ):
        raise AssertionError("bosonic candidate lies outside the semigroup classes")
    for row in records:
        counts = (
            row["qualifying_count_one_factor"],
            row["qualifying_count_two_factors"],
            row["qualifying_count_three_factors"],
        )
        if counts != (1, 0, 0):
            raise AssertionError(f"unexpected bosonic dimension counts: {counts}")


def write_csv(records: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(records[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--classification", type=Path, default=DEFAULT_CLASSIFICATION
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    records = enumerate_candidates(read_scope_rows(arguments.classification))
    validate_records(records)
    write_csv(records, arguments.output)
    print(
        "Found commuting-Hermitian bosonic representations with a positive "
        f"convergent half-line in {len(records)} relation classes."
    )
    print("Classes: " + ", ".join(str(row["class_number"]) for row in records))
    print(
        "The pure-group meromorphic continuation is negative on the "
        "opposite half-line."
    )
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
