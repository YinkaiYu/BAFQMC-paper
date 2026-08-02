#!/usr/bin/env python3
"""Screen reduced real SO(p,q) subspaces in the 64 J1,J2 classes.

The script verifies three distinct statements:

1. The five defining relations do not force the complete A_group space of
   any class into the reduced-real-SO construction.  At generic coefficient
   multiplicity, the common linear centralizer is a two-dimensional abelian
   algebra, whereas the construction needs two invertible anticommuting
   elements Q and R0 in that centralizer.
2. Every class contains the constrained compact subspace
   A = I_base tensor k, with k a real antisymmetric matrix.
3. The tensor-block tables contain an additional coefficient-only SO(p,q)
   subspace in two previously unclassified bosonic classes and six previously
   unclassified fermionic classes.

Here Y denotes i sigma_y = [[0, 1], [-1, 0]], as in the Octave enumeration.
No random sampling is used.
"""

from __future__ import annotations

import csv
import itertools
import math
from pathlib import Path

import numpy as np


REPORT_DIR = Path(__file__).resolve().parents[1]
TABLE_DIR = REPORT_DIR / "tables"
TENSOR_PATH = TABLE_DIR / "tensor_block_structures.csv"
FULL_PATH = TABLE_DIR / "full_64_class_enumeration.csv"
OUTPUT_PATH = TABLE_DIR / "reduced_so_subspace_screen.csv"

TOLERANCE = 1.0e-10

PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, 1], [-1, 0]], dtype=complex),
    "Z": np.diag([1, -1]).astype(complex),
}

EXPECTED_NEW_SPLIT = {
    "boson": {1, 2},
    "fermion": {2, 3, 5, 9, 14, 17},
}

EXPECTED_EXISTING_SPLIT = {
    "boson": {4, 10},
    "fermion": {4, 10, 12},
}


def pauli_word(text: str) -> np.ndarray:
    matrix = np.array([[1.0]], dtype=complex)
    for label in text:
        matrix = np.kron(matrix, PAULI[label])
    return matrix


def pauli_words(length: int) -> list[str]:
    return ["".join(labels) for labels in itertools.product("IXYZ", repeat=length)]


def maximum_residual(*matrices: np.ndarray) -> float:
    return max((np.linalg.norm(matrix, "fro") for matrix in matrices), default=0.0)


def sign_relative(left: np.ndarray, right: np.ndarray) -> int:
    if np.linalg.norm(left - right, "fro") < TOLERANCE:
        return 1
    if np.linalg.norm(left + right, "fro") < TOLERANCE:
        return -1
    raise AssertionError("Matrices are not related by a sign")


def canonical_matrices(statistics: str, internal_dimension: int) -> tuple[np.ndarray, np.ndarray]:
    if statistics == "boson":
        g = np.kron(-PAULI["Y"], np.eye(internal_dimension))
    elif statistics == "fermion":
        g = np.kron(PAULI["X"], np.eye(internal_dimension))
    else:
        raise ValueError(statistics)
    conjugation = np.kron(PAULI["X"], np.eye(internal_dimension))
    return g, conjugation


def maximal_pauli_factors(row: dict[str, str]) -> list[str]:
    return [entry.split(":", 1)[0] for entry in row["maximal_terms"].split(";")]


def centralizer_basis(row: dict[str, str]) -> tuple[list[str], float]:
    length = int(row["n"])
    factors = [pauli_word(word) for word in maximal_pauli_factors(row)]
    basis: list[str] = []
    for word in pauli_words(length):
        candidate = pauli_word(word)
        if max(
            np.linalg.norm(candidate @ factor - factor @ candidate, "fro")
            for factor in factors
        ) < TOLERANCE:
            basis.append(word)

    abelian_residual = 0.0
    for first in basis:
        for second in basis:
            first_matrix = pauli_word(first)
            second_matrix = pauli_word(second)
            abelian_residual = max(
                abelian_residual,
                np.linalg.norm(
                    first_matrix @ second_matrix - second_matrix @ first_matrix,
                    "fro",
                ),
            )
    return basis, abelian_residual


def metric_from_row(
    row: dict[str, str], second: np.ndarray, g: np.ndarray
) -> np.ndarray:
    phase = 1.0 if row["metric"] == "J2g" else 1.0j
    return phase * second @ g


def physical_commutator_on_half(
    statistics: str,
    half_basis: np.ndarray,
    g: np.ndarray,
    conjugation: np.ndarray,
) -> np.ndarray | None:
    if statistics == "fermion":
        return None
    # The report uses g=-Omega for bosons, while [chi,chi^T]=Omega.
    return -half_basis.T @ g @ conjugation @ half_basis.conj()


def signature(matrix: np.ndarray) -> tuple[int, int]:
    assert np.linalg.norm(matrix - matrix.conj().T, "fro") < TOLERANCE
    eigenvalues = np.linalg.eigvalsh(matrix)
    assert np.min(np.abs(eigenvalues)) > TOLERANCE
    return int(np.sum(eigenvalues > 0)), int(np.sum(eigenvalues < 0))


def count_negative(matrix: np.ndarray | None) -> int | None:
    if matrix is None:
        return None
    assert np.linalg.norm(matrix - matrix.conj().T, "fro") < TOLERANCE
    eigenvalues = np.linalg.eigvalsh(matrix)
    assert np.min(np.abs(eigenvalues)) > TOLERANCE
    return int(np.sum(eigenvalues < 0))


def verify_reduced_so_construction(
    row: dict[str, str],
    generator: np.ndarray,
    q_matrix: np.ndarray,
    u_zero: np.ndarray,
    r_zero: np.ndarray,
    reduced_propagator: np.ndarray,
) -> dict[str, float | int]:
    statistics = row["statistics"]
    base_dimension = 2 ** int(row["n"])
    auxiliary_dimension = generator.shape[0] // base_dimension
    internal_dimension = base_dimension // 2
    total_internal_dimension = internal_dimension * auxiliary_dimension
    total_dimension = 2 * total_internal_dimension
    assert generator.shape == (total_dimension, total_dimension)

    g, conjugation = canonical_matrices(statistics, total_internal_dimension)
    first = np.kron(pauli_word(row["J1_word"]), np.eye(auxiliary_dimension))
    second = np.kron(pauli_word(row["J2_word"]), np.eye(auxiliary_dimension))
    eta_group = metric_from_row(row, second, g)
    identity = np.eye(total_dimension, dtype=complex)

    kappa = -1 if statistics == "boson" else 1
    square_sign = sign_relative(r_zero @ r_zero, identity)
    g_sign = sign_relative(r_zero.T @ g @ r_zero, g)
    assert kappa * g_sign == square_sign

    half_basis = np.eye(total_dimension, dtype=complex)[:, :total_internal_dimension]
    assert np.linalg.norm(q_matrix @ half_basis - 1.0j * half_basis, "fro") < TOLERANCE
    reduced_generator = half_basis.conj().T @ generator @ half_basis
    reduced_metric = half_basis.T @ g @ r_zero @ half_basis
    positive, negative = signature(reduced_metric)
    commutator_form = physical_commutator_on_half(
        statistics, half_basis, g, conjugation
    )
    negative_commutators = count_negative(commutator_form)

    residuals = {
        "lie": np.linalg.norm(g @ generator + generator.T @ g, "fro"),
        "first_reality": np.linalg.norm(
            first.T @ generator @ first - generator.conj(), "fro"
        ),
        "second_reality": np.linalg.norm(
            second.T @ generator @ second - generator.conj(), "fro"
        ),
        "group_metric": np.linalg.norm(
            eta_group @ generator + generator.conj().T @ eta_group, "fro"
        ),
        "q_square": np.linalg.norm(q_matrix @ q_matrix + identity, "fro"),
        "q_canonical": np.linalg.norm(q_matrix.T @ g @ q_matrix - g, "fro"),
        "q_dagger": np.linalg.norm(
            conjugation @ q_matrix.conj() @ conjugation - q_matrix, "fro"
        ),
        "q_symmetry": np.linalg.norm(
            q_matrix @ generator - generator @ q_matrix, "fro"
        ),
        "u_canonical": np.linalg.norm(u_zero.T @ g @ u_zero - g, "fro"),
        "u_dagger": np.linalg.norm(
            conjugation @ u_zero.conj() @ conjugation - u_zero, "fro"
        ),
        "u_square": np.linalg.norm(u_zero @ u_zero.conj() - identity, "fro"),
        "u_symmetry": np.linalg.norm(
            np.linalg.inv(u_zero) @ generator.conj() @ u_zero - generator,
            "fro",
        ),
        "u_preserves_half": np.linalg.norm(
            u_zero @ q_matrix.conj() + q_matrix @ u_zero, "fro"
        ),
        "r_symmetry": np.linalg.norm(
            r_zero @ generator - generator @ r_zero, "fro"
        ),
        "r_exchanges_halves": np.linalg.norm(
            r_zero @ q_matrix + q_matrix @ r_zero, "fro"
        ),
        "r_real": np.linalg.norm(
            u_zero @ r_zero.conj() @ np.linalg.inv(u_zero) - r_zero, "fro"
        ),
        "reduced_real": np.linalg.norm(reduced_generator.imag, "fro"),
        "reduced_metric_real": np.linalg.norm(reduced_metric.imag, "fro"),
        "reduced_metric_symmetric": np.linalg.norm(
            reduced_metric.T - reduced_metric, "fro"
        ),
        "reduced_orthogonal": np.linalg.norm(
            reduced_generator.T @ reduced_metric
            + reduced_metric @ reduced_generator,
            "fro",
        ),
        "reduced_trace": abs(np.trace(reduced_generator)),
        "propagator_metric": np.linalg.norm(
            reduced_propagator.T @ reduced_metric @ reduced_propagator
            - reduced_metric,
            "fro",
        ),
        "propagator_determinant": abs(np.linalg.det(reduced_propagator) - 1.0),
    }
    largest_residual = max(residuals.values())
    assert largest_residual < TOLERANCE, residuals

    determinant_plus = float(
        np.real_if_close(np.linalg.det(np.eye(total_internal_dimension) + reduced_propagator))
    )
    determinant_minus = float(
        np.real_if_close(np.linalg.det(np.eye(total_internal_dimension) - reduced_propagator))
    )
    assert determinant_plus >= -TOLERANCE

    parity_match: int | None = None
    if statistics == "boson":
        assert negative_commutators is not None
        parity_match = int((negative_commutators - negative) % 2 == 0)
        assert total_internal_dimension % 2 == 0
        assert parity_match == 1
        assert determinant_minus > TOLERANCE

    return {
        "total_nambu_dimension": total_dimension,
        "reduced_dimension": total_internal_dimension,
        "signature_p": positive,
        "signature_q": negative,
        "negative_commutators": negative_commutators,
        "parity_match": parity_match,
        "max_residual": largest_residual,
        "determinant_plus": determinant_plus,
        "determinant_minus": determinant_minus,
    }


def universal_compact_check(row: dict[str, str]) -> dict[str, float | int | str]:
    base_dimension = 2 ** int(row["n"])
    internal_dimension = base_dimension // 2
    auxiliary_dimension = 2
    identity_internal = np.eye(internal_dimension)
    identity_auxiliary = np.eye(auxiliary_dimension)

    generator = np.kron(np.eye(base_dimension), PAULI["Y"])
    q_matrix = np.kron(
        np.kron(1.0j * PAULI["Z"], identity_internal), identity_auxiliary
    )
    u_zero = np.eye(base_dimension * auxiliary_dimension, dtype=complex)
    r_sign = -1.0 if row["statistics"] == "boson" else 1.0
    r_zero = r_sign * np.kron(
        np.kron(PAULI["X"], identity_internal), identity_auxiliary
    )

    angle = 0.7
    rotation = np.array(
        [[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]]
    )
    reduced_propagator = np.kron(identity_internal, rotation)
    result = verify_reduced_so_construction(
        row, generator, q_matrix, u_zero, r_zero, reduced_propagator
    )

    # In odd reduced dimension every SO matrix has an eigenvalue +1.  The
    # explicit block-diagonal rotation provides a deterministic check.
    odd_rotation = np.block(
        [
            [rotation, np.zeros((2, 1))],
            [np.zeros((1, 2)), np.ones((1, 1))],
        ]
    )
    assert abs(np.linalg.det(np.eye(3) - odd_rotation)) < TOLERANCE
    return {
        **result,
        "auxiliary_dimension": auxiliary_dimension,
        "q_word": "iZ" + "I" * int(row["n"]),
        "r0_word": ("-" if r_sign < 0 else "")
        + "X"
        + "I" * int(row["n"]),
        "a_word": "I" * int(row["n"]) + "Y",
        "odd_reduced_pole_verified": 1,
    }


def split_check(row: dict[str, str]) -> dict[str, float | int | str]:
    base_dimension = 2 ** int(row["n"])
    internal_dimension = base_dimension // 2
    auxiliary_dimension = 2
    identity_internal = np.eye(internal_dimension)
    identity_auxiliary = np.eye(auxiliary_dimension)

    generator = np.kron(
        np.kron(PAULI["Z"], identity_internal), PAULI["X"]
    )
    q_matrix = np.kron(
        np.kron(1.0j * PAULI["Z"], identity_internal), identity_auxiliary
    )
    u_zero = np.eye(base_dimension * auxiliary_dimension, dtype=complex)
    r_sign = -1.0 if row["statistics"] == "boson" else 1.0
    r_zero = r_sign * np.kron(
        np.kron(PAULI["X"], identity_internal), PAULI["Z"]
    )

    rapidity = 0.7
    boost = np.array(
        [[math.cosh(rapidity), math.sinh(rapidity)],
         [math.sinh(rapidity), math.cosh(rapidity)]]
    )
    reduced_propagator = np.kron(identity_internal, boost)
    result = verify_reduced_so_construction(
        row, generator, q_matrix, u_zero, r_zero, reduced_propagator
    )
    return {
        **result,
        "auxiliary_dimension": auxiliary_dimension,
        "q_word": "iZ" + "I" * int(row["n"]),
        "r0_word": ("-" if r_sign < 0 else "")
        + "X"
        + "I" * (int(row["n"]) - 1)
        + "Z",
        "a_word": "Z" + "I" * (int(row["n"]) - 1) + "X",
    }


def is_double_time_reversal_positive(row: dict[str, str]) -> bool:
    relative_sign = int(row["r"]) * int(row["s1"]) * int(row["s2"])
    squares = (int(row["q1"]), int(row["q2"]))
    return relative_sign == -1 and (
        sorted(squares) == [-1, 1] or squares == (-1, -1)
    )


def blank_split_result() -> dict[str, str]:
    return {
        "auxiliary_dimension": "",
        "total_nambu_dimension": "",
        "reduced_dimension": "",
        "signature_p": "",
        "signature_q": "",
        "negative_commutators": "",
        "parity_match": "",
        "max_residual": "",
        "determinant_plus": "",
        "determinant_minus": "",
        "q_word": "",
        "r0_word": "",
        "a_word": "",
    }


def formatted(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.16g}"
    if value is None:
        return ""
    return value


def main() -> None:
    with TENSOR_PATH.open(newline="", encoding="utf-8") as handle:
        tensor_rows = list(csv.DictReader(handle))
    with FULL_PATH.open(newline="", encoding="utf-8") as handle:
        full_rows = list(csv.DictReader(handle))
    assert len(tensor_rows) == len(full_rows) == 64

    full_by_key = {
        (row["statistics"], row["class_id"]): row for row in full_rows
    }
    class_numbers = {"boson": 0, "fermion": 0}
    output_rows: list[dict[str, object]] = []
    new_split_found = {"boson": set(), "fermion": set()}
    existing_split_found = {"boson": set(), "fermion": set()}

    for row in tensor_rows:
        statistics = row["statistics"]
        class_numbers[statistics] += 1
        class_number = class_numbers[statistics]
        full = full_by_key[(statistics, row["class_id"])]
        assert int(row["n"]) == int(full["min_qubits"])
        assert row["J1_word"] == full["J1_word"]
        assert row["J2_word"] == full["J2_word"]

        identity_term = "I" * int(row["n"]) + ":R_A"
        assert identity_term in row["maximal_terms"].split(";")
        centralizer, abelian_residual = centralizer_basis(row)
        assert len(centralizer) == 2
        assert abelian_residual < TOLERANCE

        universal = universal_compact_check(row)

        split_symmetric_term = (
            "Z" + "I" * (int(row["n"]) - 1) + ":R_S"
        )
        split_available = split_symmetric_term in row["maximal_terms"].split(";")
        if split_available:
            split = split_check(row)
            if is_double_time_reversal_positive(full):
                split_status = "already_double_time_reversal_positive"
                existing_split_found[statistics].add(class_number)
            else:
                split_status = "new_constrained_split_so"
                new_split_found[statistics].add(class_number)
        else:
            split = blank_split_result()
            split_status = "not_available_in_coefficient_only_form"

        output = {
            "statistics": statistics,
            "class_number": class_number,
            "class_id": row["class_id"],
            "base_nambu_dimension": 2 ** int(row["n"]),
            "J1_word": row["J1_word"],
            "J2_word": row["J2_word"],
            "whole_centralizer_dimension": len(centralizer),
            "whole_centralizer_basis": ";".join(centralizer),
            "whole_centralizer_abelian_residual": abelian_residual,
            "whole_reduced_so_automatic": 0,
            "whole_obstruction_verified": 1,
            "universal_compact_verified": 1,
            "universal_auxiliary_dimension": universal["auxiliary_dimension"],
            "universal_total_nambu_dimension": universal["total_nambu_dimension"],
            "universal_reduced_dimension": universal["reduced_dimension"],
            "universal_Q_word": universal["q_word"],
            "universal_R0_word": universal["r0_word"],
            "universal_A_word": universal["a_word"],
            "universal_signature_p": universal["signature_p"],
            "universal_signature_q": universal["signature_q"],
            "universal_negative_commutators": universal["negative_commutators"],
            "universal_parity_match": universal["parity_match"],
            "universal_odd_reduced_pole_verified": universal[
                "odd_reduced_pole_verified"
            ],
            "universal_max_residual": universal["max_residual"],
            "universal_test_det_plus": universal["determinant_plus"],
            "universal_test_det_minus": universal["determinant_minus"],
            "split_status": split_status,
            "split_auxiliary_dimension": split["auxiliary_dimension"],
            "split_total_nambu_dimension": split["total_nambu_dimension"],
            "split_reduced_dimension": split["reduced_dimension"],
            "split_Q_word": split["q_word"],
            "split_R0_word": split["r0_word"],
            "split_A_word": split["a_word"],
            "split_signature_p": split["signature_p"],
            "split_signature_q": split["signature_q"],
            "split_negative_commutators": split["negative_commutators"],
            "split_parity_match": split["parity_match"],
            "split_max_residual": split["max_residual"],
            "split_test_det_plus": split["determinant_plus"],
            "split_test_det_minus": split["determinant_minus"],
        }
        output_rows.append({key: formatted(value) for key, value in output.items()})

    assert class_numbers == {"boson": 32, "fermion": 32}
    assert new_split_found == EXPECTED_NEW_SPLIT
    assert existing_split_found == EXPECTED_EXISTING_SPLIT
    assert all(int(row["whole_obstruction_verified"]) for row in output_rows)
    assert all(int(row["universal_compact_verified"]) for row in output_rows)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(output_rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print("Whole A_group: 64/64 classes have the abelian-centralizer obstruction.")
    print("Universal compact SO subspace: 64/64 classes verified.")
    print(
        "New coefficient-only split SO subspaces: "
        f"boson {sorted(new_split_found['boson'])}; "
        f"fermion {sorted(new_split_found['fermion'])}."
    )
    print(
        "Split SO subspaces already covered by double time reversal: "
        f"boson {sorted(existing_split_found['boson'])}; "
        f"fermion {sorted(existing_split_found['fermion'])}."
    )
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
