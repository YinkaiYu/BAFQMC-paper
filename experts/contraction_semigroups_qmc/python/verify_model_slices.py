#!/usr/bin/env python3
"""Verify the B05, B13, and F04 fixed-field slices in the note."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PACKAGE_ROOT / "build" / "model_slice_checks.csv"
TOLERANCE = 1.0e-10

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, 1], [-1, 0]], dtype=complex)  # i sigma_y
Z = np.diag([1, -1]).astype(complex)
SIGMA_Y = -1j * Y


def kron(*factors: np.ndarray) -> np.ndarray:
    result = np.ones((1, 1), dtype=complex)
    for factor in factors:
        result = np.kron(result, factor)
    return result


def residual(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def signed_relation(left: np.ndarray, right: np.ndarray) -> int:
    if np.array_equal(left, right):
        return 1
    if np.array_equal(left, -right):
        return -1
    raise AssertionError("matrices are not related by a sign")


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


def invariant_residual(generator: np.ndarray, linear_part: np.ndarray) -> float:
    return residual(
        np.linalg.solve(linear_part, generator.conj() @ linear_part)
        - generator
    )


def check_slice(
    *,
    model: str,
    class_number: str,
    expected_signs: tuple[int, int, int, int, int],
    g: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    eta: np.ndarray,
    group: np.ndarray,
    cone: np.ndarray,
    field_value: float,
    extra_checks: dict[str, float] | None = None,
) -> dict[str, object]:
    total = group + cone
    relation_residual = max(
        residual(first.T @ g @ first - expected_signs[0] * g),
        residual(first @ first - expected_signs[1] * np.eye(g.shape[0])),
        residual(second.T @ g @ second - expected_signs[2] * g),
        residual(second @ second - expected_signs[3] * np.eye(g.shape[0])),
        residual(first @ second - expected_signs[4] * second @ first),
    )
    if five_relations(g, first, second) != expected_signs:
        raise AssertionError(f"{model}: incorrect five relations")

    checks = {
        "relation_residual": relation_residual,
        "lie_residual": residual(g @ total + total.T @ g),
        "reality_residual": residual(first.T @ total @ first - total.conj()),
        "group_J2_residual": residual(
            second.T @ group @ second - group.conj()
        ),
        "cone_J2_residual": residual(
            second.T @ cone @ second + cone.conj()
        ),
        "group_metric_residual": residual(
            eta @ group + group.conj().T @ eta
        ),
        "cone_metric_residual": residual(
            eta @ cone - cone.conj().T @ eta
        ),
    }
    if max(checks.values()) >= TOLERANCE:
        raise AssertionError(f"{model}: algebraic residual {max(checks.values())}")

    contraction = eta @ total + total.conj().T @ eta
    if residual(contraction - contraction.conj().T) >= TOLERANCE:
        raise AssertionError(f"{model}: contraction matrix is not Hermitian")
    maximum_eigenvalue = float(np.linalg.eigvalsh(contraction).max())
    if maximum_eigenvalue >= -TOLERANCE:
        raise AssertionError(f"{model}: slice is not strictly contractive")

    row: dict[str, object] = {
        "model": model,
        "class_number": class_number,
        "field_value": field_value,
        **checks,
        "maximum_contraction_eigenvalue": maximum_eigenvalue,
        "extra_symmetry_residual": "",
        "broken_extra_symmetry_residual": "",
        "minimum_coefficient_margin": "",
    }
    if extra_checks:
        row.update(extra_checks)
    return row


def b05_rows() -> list[dict[str, object]]:
    site_identity = np.eye(2)
    energy = np.diag([2.0, 3.0])
    circulation = np.array([[0.0, 1.0], [-1.0, 0.0]])
    g = kron(-Y, site_identity)
    first = kron(I2, site_identity)
    second = kron(X, site_identity)
    eta = kron(Z, site_identity)
    cone = -kron(Z, energy)
    rows = []
    for field in (-2.0, 0.0, 1.5):
        group = field * kron(I2, circulation)
        extra = 1j * kron(Z, site_identity)
        rows.append(
            check_slice(
                model="B05",
                class_number="B05",
                expected_signs=(1, 1, -1, 1, 1),
                g=g,
                first=first,
                second=second,
                eta=eta,
                group=group,
                cone=cone,
                field_value=field,
                extra_checks={
                    "extra_symmetry_residual": invariant_residual(
                        group + cone, extra
                    )
                },
            )
        )
    return rows


def b13_rows() -> list[dict[str, object]]:
    site_identity = np.eye(2)
    energy = 4.0 * site_identity
    circulation = np.array([[0.0, 1.0], [-1.0, 0.0]])
    pairing = site_identity
    field_matrix = np.diag([1.0, 2.0])
    g = kron(-Y, I2, site_identity)
    first = kron(I2, Y, site_identity)
    second = kron(X, I2, site_identity)
    eta = kron(Z, I2, site_identity)
    cone = -(
        kron(Z, I2, energy)
        + kron(Z, Y, circulation)
        + kron(Y, I2, pairing)
    )
    block = np.block(
        [
            [kron(I2, energy) + kron(Y, circulation), kron(I2, pairing)],
            [kron(I2, pairing), kron(I2, energy) + kron(Y, circulation)],
        ]
    )
    margin = float(np.linalg.eigvalsh(block).min())
    if margin <= TOLERANCE:
        raise AssertionError("B13: coefficient block is not positive definite")

    rows = []
    for field in (-2.0, 0.0, 1.5):
        group = 1j * field * kron(Z, Z, field_matrix)
        extra = kron(I2, X, site_identity)
        extra_without_circulation = invariant_residual(
            group - kron(Z, I2, energy) - kron(Y, I2, pairing), extra
        )
        extra_with_circulation = invariant_residual(group + cone, extra)
        if extra_without_circulation >= TOLERANCE:
            raise AssertionError("B13: extra time reversal should hold at R=0")
        if extra_with_circulation <= TOLERANCE:
            raise AssertionError("B13: circulation should break the extra symmetry")
        rows.append(
            check_slice(
                model="B13",
                class_number="B13",
                expected_signs=(1, -1, -1, 1, 1),
                g=g,
                first=first,
                second=second,
                eta=eta,
                group=group,
                cone=cone,
                field_value=field,
                extra_checks={
                    "extra_symmetry_residual": extra_without_circulation,
                    "broken_extra_symmetry_residual": extra_with_circulation,
                    "minimum_coefficient_margin": margin,
                },
            )
        )
    return rows


def f04_rows() -> list[dict[str, object]]:
    site_identity = np.eye(2)
    hopping = np.diag([1.0, 2.0])
    pairing = 4.0 * site_identity
    conversion = np.diag([1.0, -1.0])
    field_matrix = np.diag([1.0, 2.0])
    g = kron(X, I2, site_identity)
    first = kron(I2, X, site_identity)
    second = kron(I2, Y, site_identity)
    eta = 1j * second @ g
    cone = kron(X, SIGMA_Y, pairing) - kron(Z, X, conversion)
    margin = min(
        float(np.linalg.eigvalsh(pairing + conversion).min()),
        float(np.linalg.eigvalsh(pairing - conversion).min()),
    )
    if margin <= TOLERANCE:
        raise AssertionError("F04: D+T and D-T must be positive definite")

    rows = []
    for field in (-2.0, 0.0, 1.5):
        group = -kron(Z, I2, hopping) + 1j * field * kron(
            Z, Z, field_matrix
        )
        extra = kron(Z, SIGMA_Y, site_identity)
        extra_without_conversion = invariant_residual(
            group + kron(X, SIGMA_Y, pairing), extra
        )
        extra_with_conversion = invariant_residual(group + cone, extra)
        if extra_without_conversion >= TOLERANCE:
            raise AssertionError("F04: extra time reversal should hold at T=0")
        if extra_with_conversion <= TOLERANCE:
            raise AssertionError("F04: flavor conversion should break the extra symmetry")
        rows.append(
            check_slice(
                model="F04",
                class_number="F04",
                expected_signs=(1, 1, 1, -1, -1),
                g=g,
                first=first,
                second=second,
                eta=eta,
                group=group,
                cone=cone,
                field_value=field,
                extra_checks={
                    "extra_symmetry_residual": extra_without_conversion,
                    "broken_extra_symmetry_residual": extra_with_conversion,
                    "minimum_coefficient_margin": margin,
                },
            )
        )
    return rows


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the three interacting model slices in the note."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output CSV (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def stable_output(row: dict[str, object]) -> dict[str, object]:
    """Round diagnostic floats only after every physical assertion has passed."""
    result: dict[str, object] = {}
    for key, value in row.items():
        if isinstance(value, float):
            rounded = round(value, 12)
            result[key] = 0.0 if rounded == 0.0 else rounded
        else:
            result[key] = value
    return result


def main() -> None:
    arguments = parse_arguments()
    rows = [stable_output(row) for row in b05_rows() + b13_rows() + f04_rows()]
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Verified {len(rows)} fixed-field slices for B05, B13, and F04.")
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
