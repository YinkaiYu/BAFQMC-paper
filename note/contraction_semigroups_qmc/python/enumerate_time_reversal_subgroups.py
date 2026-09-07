#!/usr/bin/env python3
"""Enumerate time-reversal-positive subspaces in the 64 semigroup classes.

Matrix words use the real Pauli basis

    I = I_2, X = sigma_x, Y = i sigma_y, Z = sigma_z.

A leading ``i`` multiplies the complete word by the imaginary unit.  The
linear part U of every reported time reversal Theta = U K is checked against

    U^T g U = g,      C conjugate(U) C = U,

where C exchanges the annihilation and creation halves of the Nambu column.
The script writes one auditable representative for every one of the 64
bosonic and fermionic five-relation classes.
"""

from __future__ import annotations

import argparse
import csv
import itertools
from pathlib import Path

import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PACKAGE_ROOT / "build" / "time_reversal_subgroups.csv"
TOLERANCE = 1.0e-9

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
I_SIGMA_Y = np.array([[0, 1], [-1, 0]], dtype=complex)
SIGMA_Z = np.diag([1, -1]).astype(complex)
REAL_PAULI = {
    "I": I2,
    "X": SIGMA_X,
    "Y": I_SIGMA_Y,
    "Z": SIGMA_Z,
}


def pauli_words(number_of_factors: int) -> list[str]:
    return [
        "".join(letters)
        for letters in itertools.product("IXYZ", repeat=number_of_factors)
    ]


def pauli_matrix(word: str) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=complex)
    for letter in word:
        matrix = np.kron(matrix, REAL_PAULI[letter])
    return matrix


def signed_relation(left: np.ndarray, right: np.ndarray) -> int:
    if np.linalg.norm(left - right) < TOLERANCE:
        return 1
    if np.linalg.norm(left + right) < TOLERANCE:
        return -1
    raise ValueError("matrices are not related by a sign")


def canonical_matrices(
    statistics: str, number_of_factors: int
) -> tuple[np.ndarray, np.ndarray]:
    internal = np.eye(2 ** (number_of_factors - 1), dtype=complex)
    if statistics == "boson":
        g = np.kron(-I_SIGMA_Y, internal)
    elif statistics == "fermion":
        g = np.kron(SIGMA_X, internal)
    else:
        raise ValueError(statistics)
    conjugation = np.kron(SIGMA_X, internal)
    return g, conjugation


def class_id(signs: tuple[int, int, int, int, int]) -> str:
    marks = ["+" if sign == 1 else "-" for sign in signs]
    return (
        f"s1{marks[0]}_q1{marks[1]}_s2{marks[2]}_"
        f"q2{marks[3]}_r{marks[4]}"
    )


def physical_time_reversal(
    matrix: np.ndarray, action_on_g: int
) -> np.ndarray:
    return matrix if action_on_g == 1 else 1j * matrix


def time_reversal_is_physical(
    linear_part: np.ndarray,
    g: np.ndarray,
    conjugation: np.ndarray,
) -> bool:
    return (
        np.linalg.norm(linear_part.T @ g @ linear_part - g) < TOLERANCE
        and np.linalg.norm(
            conjugation @ linear_part.conj() @ conjugation - linear_part
        )
        < TOLERANCE
    )


def time_reversal_square(linear_part: np.ndarray) -> int:
    identity = np.eye(linear_part.shape[0], dtype=complex)
    return signed_relation(linear_part @ linear_part.conj(), identity)


def time_reversals_anticommute(
    first: np.ndarray, second: np.ndarray
) -> bool:
    return (
        np.linalg.norm(
            first @ second.conj() + second @ first.conj()
        )
        < TOLERANCE
    )


def generator_is_invariant(
    generator: np.ndarray, linear_part: np.ndarray
) -> bool:
    transformed = np.linalg.solve(
        linear_part, generator.conj() @ linear_part
    )
    return np.linalg.norm(transformed - generator) < TOLERANCE


def candidate_time_reversals(
    statistics: str,
    number_of_factors: int,
    matrices: dict[str, np.ndarray],
) -> list[tuple[str, np.ndarray, int]]:
    g, conjugation = canonical_matrices(statistics, number_of_factors)
    candidates: list[tuple[str, np.ndarray, int]] = []
    for word, matrix in matrices.items():
        for phase, name in ((1, word), (1j, f"i{word}")):
            linear_part = phase * matrix
            if time_reversal_is_physical(linear_part, g, conjugation):
                candidates.append(
                    (
                        name,
                        linear_part,
                        time_reversal_square(linear_part),
                    )
                )
    return candidates


def group_basis(
    g: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    matrices: dict[str, np.ndarray],
) -> list[tuple[str, np.ndarray]]:
    basis: list[tuple[str, np.ndarray]] = []
    for word, matrix in matrices.items():
        for phase, name in ((1, word), (1j, f"i{word}")):
            generator = phase * matrix
            if np.linalg.norm(g @ generator + generator.T @ g) >= TOLERANCE:
                continue
            if (
                np.linalg.norm(
                    first.T @ generator @ first - generator.conj()
                )
                >= TOLERANCE
            ):
                continue
            if (
                np.linalg.norm(
                    second.T @ generator @ second - generator.conj()
                )
                >= TOLERANCE
            ):
                continue
            basis.append((name, generator))
    return basis


def five_relations(
    g: np.ndarray, first: np.ndarray, second: np.ndarray
) -> tuple[int, int, int, int, int]:
    identity = np.eye(g.shape[0], dtype=complex)
    return (
        signed_relation(first.T @ g @ first, g),
        signed_relation(first @ first, identity),
        signed_relation(second.T @ g @ second, g),
        signed_relation(second @ second, identity),
        signed_relation(first @ second, second @ first),
    )


def whole_group_class(
    signs: tuple[int, int, int, int, int]
) -> str | None:
    action_first, square_first, action_second, square_second, mutual = signs
    relative_sign = mutual * action_first * action_second
    if relative_sign != -1:
        return None
    if sorted((square_first, square_second)) == [-1, 1]:
        return "Majorana"
    if square_first == square_second == -1:
        return "Kramers"
    return None


def selected_subspace_class(
    statistics: str,
    signs: tuple[int, int, int, int, int],
) -> str:
    action_first, square_first, action_second, square_second, mutual = signs
    relative_sign = mutual * action_first * action_second
    if (
        statistics == "boson"
        and square_first == square_second == 1
        and relative_sign == -1
    ):
        return "split-orthogonal"
    if square_first == square_second == -1:
        return "Kramers"
    return "Majorana"


def figure_tag(time_reversal_class: str, proper_subspace: bool) -> str:
    symbol = {
        "Majorana": "M",
        "Kramers": "K",
        "split-orthogonal": "S",
    }[time_reversal_class]
    return f"{symbol}*" if proper_subspace else symbol


def square_set(time_reversal_class: str) -> str:
    return {
        "Majorana": "{+,-}",
        "Kramers": "{-,-}",
        "split-orthogonal": "{+,+,+}",
    }[time_reversal_class]


def completion_with_one_extra_time_reversal(
    statistics: str,
    signs: tuple[int, int, int, int, int],
    first_time_reversal: np.ndarray,
    second_time_reversal: np.ndarray,
    extra_square: int,
    extra: np.ndarray,
) -> tuple[str, str] | None:
    _, square_first, _, square_second, _ = signs
    target = selected_subspace_class(statistics, signs)

    if target == "split-orthogonal":
        if (
            extra_square == 1
            and time_reversals_anticommute(first_time_reversal, extra)
            and time_reversals_anticommute(second_time_reversal, extra)
        ):
            return target, "Theta1 and Theta2"
        return None

    if target == "Kramers":
        if extra_square != -1:
            return None
        if time_reversals_anticommute(first_time_reversal, extra):
            return target, "Theta1"
        if time_reversals_anticommute(second_time_reversal, extra):
            return target, "Theta2"
        return None

    if extra_square == -square_first and time_reversals_anticommute(
        first_time_reversal, extra
    ):
        return target, "Theta1"
    if extra_square == -square_second and time_reversals_anticommute(
        second_time_reversal, extra
    ):
        return target, "Theta2"
    return None


def semigroup_data(
    statistics: str,
    signs: tuple[int, int, int, int, int],
) -> tuple[str, str]:
    action_first, _, action_second, square_second, mutual = signs
    statistics_sign = -1 if statistics == "boson" else 1
    strict = (
        square_second == -statistics_sign
        and mutual == -action_first * action_second
    )
    if not strict:
        return "maximal subgroup only", ""
    metric_is_j2g = statistics_sign * square_second * action_second == 1
    return "contraction semigroup", "J2g" if metric_is_j2g else "iJ2g"


def record_sort_key(record: dict[str, object]) -> tuple[object, ...]:
    return (
        int(record["number_of_pauli_factors"]),
        -int(record["time_reversal_subspace_dimension"]),
        int(record["A_group_dimension"]),
        str(record["J1_word"]),
        str(record["J2_word"]),
        str(record["extra_U"]),
    )


def lies_in_real_span(
    matrix: np.ndarray, basis: list[np.ndarray]
) -> bool:
    columns = np.column_stack(
        [
            np.concatenate((candidate.real.ravel(), candidate.imag.ravel()))
            for candidate in basis
        ]
    )
    target = np.concatenate((matrix.real.ravel(), matrix.imag.ravel()))
    coefficients, *_ = np.linalg.lstsq(columns, target, rcond=None)
    return np.linalg.norm(columns @ coefficients - target) < TOLERANCE


def assert_lie_closed(
    names: str, matrices: dict[str, np.ndarray]
) -> None:
    basis = [
        (1j * matrices[name[1:]]) if name.startswith("i") else matrices[name]
        for name in names.split(";")
    ]
    for first in basis:
        for second in basis:
            if not lies_in_real_span(first @ second - second @ first, basis):
                raise AssertionError("reported generator subspace is not Lie closed")


def enumerate_records() -> list[dict[str, object]]:
    best: dict[tuple[str, tuple[int, int, int, int, int]], dict[str, object]] = {}

    for statistics in ("boson", "fermion"):
        for number_of_factors in (1, 2, 3):
            words = pauli_words(number_of_factors)
            matrices = {word: pauli_matrix(word) for word in words}
            g, conjugation = canonical_matrices(statistics, number_of_factors)
            candidates = candidate_time_reversals(
                statistics, number_of_factors, matrices
            )

            for first_word in words:
                for second_word in words:
                    if first_word == second_word:
                        continue
                    first = matrices[first_word]
                    second = matrices[second_word]
                    signs = five_relations(g, first, second)
                    action_first, square_first, action_second, square_second, mutual = signs
                    first_u = physical_time_reversal(first, action_first)
                    second_u = physical_time_reversal(second, action_second)
                    if not time_reversal_is_physical(first_u, g, conjugation):
                        continue
                    if not time_reversal_is_physical(second_u, g, conjugation):
                        continue
                    assert time_reversal_square(first_u) == square_first
                    assert time_reversal_square(second_u) == square_second
                    relative_sign = mutual * action_first * action_second
                    assert time_reversals_anticommute(first_u, second_u) == (
                        relative_sign == -1
                    )

                    basis = group_basis(g, first, second, matrices)
                    if not basis:
                        continue
                    automatic_class = whole_group_class(signs)
                    semigroup_status, metric = semigroup_data(statistics, signs)

                    if automatic_class is not None:
                        record: dict[str, object] = {
                            "statistics": statistics,
                            "class_number": 0,
                            "class_id": class_id(signs),
                            "s1": action_first,
                            "q1": square_first,
                            "s2": action_second,
                            "q2": square_second,
                            "r": mutual,
                            "semigroup_status": semigroup_status,
                            "metric": metric,
                            "time_reversal_result": "whole A_group",
                            "time_reversal_class": automatic_class,
                            "figure_tag": figure_tag(automatic_class, False),
                            "time_reversal_squares": square_set(automatic_class),
                            "number_of_pauli_factors": number_of_factors,
                            "nambu_dimension": 2**number_of_factors,
                            "J1_word": first_word,
                            "J2_word": second_word,
                            "induced_U1": first_word
                            if action_first == 1
                            else f"i{first_word}",
                            "induced_U2": second_word
                            if action_second == 1
                            else f"i{second_word}",
                            "extra_U": "",
                            "extra_square": "",
                            "extra_pairs_with": "",
                            "A_group_dimension": len(basis),
                            "time_reversal_subspace_dimension": len(basis),
                            "time_reversal_subspace_basis": ";".join(
                                name for name, _ in basis
                            ),
                        }
                        key = (statistics, signs)
                        if key not in best or record_sort_key(record) < record_sort_key(best[key]):
                            best[key] = record
                        continue

                    for extra_name, extra_u, extra_square in candidates:
                        completion = completion_with_one_extra_time_reversal(
                            statistics,
                            signs,
                            first_u,
                            second_u,
                            extra_square,
                            extra_u,
                        )
                        if completion is None:
                            continue
                        positive_class, pairs_with = completion
                        selected_basis = [
                            (name, generator)
                            for name, generator in basis
                            if generator_is_invariant(generator, extra_u)
                        ]
                        if not 0 < len(selected_basis) < len(basis):
                            continue
                        record = {
                            "statistics": statistics,
                            "class_number": 0,
                            "class_id": class_id(signs),
                            "s1": action_first,
                            "q1": square_first,
                            "s2": action_second,
                            "q2": square_second,
                            "r": mutual,
                            "semigroup_status": semigroup_status,
                            "metric": metric,
                            "time_reversal_result": "proper A_group subspace",
                            "time_reversal_class": positive_class,
                            "figure_tag": figure_tag(positive_class, True),
                            "time_reversal_squares": square_set(positive_class),
                            "number_of_pauli_factors": number_of_factors,
                            "nambu_dimension": 2**number_of_factors,
                            "J1_word": first_word,
                            "J2_word": second_word,
                            "induced_U1": first_word
                            if action_first == 1
                            else f"i{first_word}",
                            "induced_U2": second_word
                            if action_second == 1
                            else f"i{second_word}",
                            "extra_U": extra_name,
                            "extra_square": extra_square,
                            "extra_pairs_with": pairs_with,
                            "A_group_dimension": len(basis),
                            "time_reversal_subspace_dimension": len(selected_basis),
                            "time_reversal_subspace_basis": ";".join(
                                name for name, _ in selected_basis
                            ),
                        }
                        key = (statistics, signs)
                        if key not in best or record_sort_key(record) < record_sort_key(best[key]):
                            best[key] = record

    records: list[dict[str, object]] = []
    for statistics in ("boson", "fermion"):
        for class_number, signs in enumerate(
            itertools.product((1, -1), repeat=5), start=1
        ):
            key = (statistics, signs)
            if key not in best:
                raise RuntimeError(f"no physical representative for {key}")
            record = best[key]
            record["class_number"] = class_number
            records.append(record)
    return records


def validate_records(records: list[dict[str, object]]) -> None:
    assert len(records) == 64
    for statistics in ("boson", "fermion"):
        rows = [row for row in records if row["statistics"] == statistics]
        assert len(rows) == 32
        assert sum(row["time_reversal_result"] == "whole A_group" for row in rows) == 12
        assert sum(row["time_reversal_result"] == "proper A_group subspace" for row in rows) == 20
        assert sum(row["semigroup_status"] == "contraction semigroup" for row in rows) == 8
        overlap = sum(
            row["semigroup_status"] == "contraction semigroup"
            and row["time_reversal_result"] == "whole A_group"
            for row in rows
        )
        assert overlap == (4 if statistics == "boson" else 8)

    bosonic = [row for row in records if row["statistics"] == "boson"]
    fermionic = [row for row in records if row["statistics"] == "fermion"]
    bosonic_tags = [row["figure_tag"] for row in bosonic]
    fermionic_tags = [row["figure_tag"] for row in fermionic]
    assert {tag: bosonic_tags.count(tag) for tag in set(bosonic_tags)} == {
        "M": 8,
        "K": 4,
        "M*": 12,
        "K*": 4,
        "S*": 4,
    }
    assert {tag: fermionic_tags.count(tag) for tag in set(fermionic_tags)} == {
        "M": 8,
        "K": 4,
        "M*": 16,
        "K*": 4,
    }
    assert sum(
        row["time_reversal_class"] == "split-orthogonal"
        for row in bosonic
    ) == 4

    for row in records:
        number_of_factors = int(row["number_of_pauli_factors"])
        matrices = {
            word: pauli_matrix(word)
            for word in pauli_words(number_of_factors)
        }
        assert_lie_closed(str(row["time_reversal_subspace_basis"]), matrices)
    assert sum(
        row["time_reversal_class"] == "Kramers"
        and row["time_reversal_result"].startswith("proper")
        for row in bosonic
    ) == 4
    assert sum(
        row["time_reversal_class"] == "Kramers"
        and row["time_reversal_result"].startswith("proper")
        for row in fermionic
    ) == 4


def write_csv(records: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(records[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Enumerate physical time-reversal subgroups for all 64 "
            "five-relation cases."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output CSV (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    records = enumerate_records()
    validate_records(records)
    write_csv(records, arguments.output)
    print("Convention: Y = i sigma_y; a leading i multiplies the full word.")
    print(f"Verified {len(records)} physical representatives.")
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
