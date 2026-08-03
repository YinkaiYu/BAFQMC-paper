#!/usr/bin/env python3
"""Numerical checks for the pure-symmetry positivity statements in Part 7."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy.linalg import expm


REPORT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPORT_DIR / "tables" / "symmetry_group_positivity_checks.csv"
TOLERANCE = 2.0e-9


def pauli() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    identity = np.eye(2, dtype=complex)
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.diag([1, -1]).astype(complex)
    return identity, sigma_x, sigma_y, sigma_z


def random_so_product(
    positive: int,
    negative: int,
    rng: np.random.Generator,
    layers: int = 5,
) -> tuple[np.ndarray, np.ndarray]:
    dimension = positive + negative
    eta = np.diag([1.0] * positive + [-1.0] * negative)
    product = np.eye(dimension)
    for _ in range(layers):
        trial = rng.normal(scale=0.32, size=(dimension, dimension))
        generator = trial - eta @ trial.T @ eta
        assert np.linalg.norm(generator.T @ eta + eta @ generator) < TOLERANCE
        product = expm(generator) @ product
    return eta, product


def orthogonal_group_checks() -> list[dict[str, str]]:
    rng = np.random.default_rng(20260803)
    rows: list[dict[str, str]] = []
    for positive in range(5):
        for negative in range(5):
            dimension = positive + negative
            if dimension < 2:
                continue
            minimum_plus = np.inf
            minimum_minus = np.inf
            maximum_group_residual = 0.0
            maximum_odd_minus = 0.0
            for _ in range(400):
                eta, product = random_so_product(positive, negative, rng)
                plus = float(np.linalg.det(np.eye(dimension) + product).real)
                signed_minus = float(
                    ((-1) ** negative)
                    * np.linalg.det(np.eye(dimension) - product).real
                )
                maximum_group_residual = max(
                    maximum_group_residual,
                    float(np.linalg.norm(product.T @ eta @ product - eta)),
                )
                minimum_plus = min(minimum_plus, plus)
                if dimension % 2 == 0:
                    minimum_minus = min(minimum_minus, signed_minus)
                else:
                    maximum_odd_minus = max(
                        maximum_odd_minus, abs(signed_minus)
                    )
            assert maximum_group_residual < 3.0e-9
            assert minimum_plus > -TOLERANCE
            if dimension % 2 == 0:
                assert minimum_minus > -TOLERANCE
                minus_result = f"minimum={minimum_minus:.12e}"
            else:
                assert maximum_odd_minus < 3.0e-8
                minus_result = f"odd_dimension_max_abs={maximum_odd_minus:.12e}"
            rows.append(
                {
                    "check": f"SO0({positive},{negative})",
                    "samples": "400",
                    "result": "pass",
                    "diagnostic_1": f"minimum_det_I_plus_B={minimum_plus:.12e}",
                    "diagnostic_2": minus_result,
                    "maximum_residual": f"{maximum_group_residual:.12e}",
                }
            )
    return rows


def exact_counterexample_checks() -> list[dict[str, str]]:
    identity, sigma_x, sigma_y, sigma_z = pauli()
    rows: list[dict[str, str]] = []

    symplectic_form = np.array([[0, 1], [-1, 0]], dtype=float)
    symplectic_product = np.diag([-2.0, -0.5])
    symplectic_residual = np.linalg.norm(
        symplectic_product.T
        @ symplectic_form
        @ symplectic_product
        - symplectic_form
    )
    symplectic_determinant = np.linalg.det(
        np.eye(2) + symplectic_product
    )
    assert symplectic_residual < TOLERANCE
    assert symplectic_determinant < 0
    rows.append(
        {
            "check": "symplectic_not_positive",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"det_I_plus_B={symplectic_determinant:.12e}",
            "diagnostic_2": "expected_negative",
            "maximum_residual": f"{symplectic_residual:.12e}",
        }
    )

    x = 0.75 * np.pi
    fermion_g = sigma_x
    fermion_c = sigma_x
    fermion_a = -2j * x * sigma_z
    fermion_u = -sigma_y
    fermion_residual = max(
        np.linalg.norm(fermion_a.T @ fermion_g + fermion_g @ fermion_a),
        np.linalg.norm(fermion_u.T @ fermion_g @ fermion_u - fermion_g),
        np.linalg.norm(
            fermion_c @ fermion_u.conj() @ fermion_c - fermion_u
        ),
        np.linalg.norm(
            np.linalg.solve(fermion_u, fermion_a.conj()) @ fermion_u
            - fermion_a
        ),
        np.linalg.norm(
            fermion_u @ fermion_u.conj() + np.eye(2)
        ),
    )
    fermion_weight = 2.0 * np.cos(x)
    assert fermion_residual < TOLERANCE
    assert fermion_weight < 0
    rows.append(
        {
            "check": "fermion_single_negative_TR_not_positive",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"weight={fermion_weight:.12e}",
            "diagnostic_2": "U_inverse_barA_U_equals_A",
            "maximum_residual": f"{fermion_residual:.12e}",
        }
    )

    boson_g = -1j * sigma_y
    boson_c = sigma_x
    boson_a = x * boson_g
    boson_u = np.eye(2, dtype=complex)
    boson_product = expm(boson_a)
    boson_radicand = -np.linalg.det(np.eye(2) - boson_product)
    boson_residual = max(
        np.linalg.norm(boson_a.T @ boson_g + boson_g @ boson_a),
        np.linalg.norm(boson_u.T @ boson_g @ boson_u - boson_g),
        np.linalg.norm(boson_c @ boson_u.conj() @ boson_c - boson_u),
        np.linalg.norm(
            np.linalg.solve(boson_u, boson_a.conj()) @ boson_u
            - boson_a
        ),
        abs(boson_radicand + 4.0 * np.sin(x / 2.0) ** 2),
    )
    assert boson_residual < TOLERANCE
    assert boson_radicand.real < 0
    rows.append(
        {
            "check": "boson_single_positive_TR_not_positive",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"radicand={boson_radicand.real:.12e}",
            "diagnostic_2": "analytic_weight_is_imaginary",
            "maximum_residual": f"{boson_residual:.12e}",
        }
    )

    x = 0.7
    fermion_g = np.kron(sigma_x, identity)
    fermion_c = fermion_g.copy()
    time_reversals = [
        np.eye(4, dtype=complex),
        1j * np.kron(sigma_z, sigma_x),
        1j * np.kron(sigma_z, sigma_z),
    ]
    generators = [
        np.pi * 1j * np.kron(sigma_x, sigma_y),
        x * np.kron(sigma_z, identity),
    ]
    residuals = []
    for generator in generators:
        residuals.append(
            np.linalg.norm(
                generator.T @ fermion_g + fermion_g @ generator
            )
        )
        for unitary in time_reversals:
            residuals.append(
                np.linalg.norm(
                    np.linalg.solve(unitary, generator.conj())
                    @ unitary
                    - generator
                )
            )
    for unitary in time_reversals:
        residuals.extend(
            [
                np.linalg.norm(unitary.T @ fermion_g @ unitary - fermion_g),
                np.linalg.norm(
                    fermion_c @ unitary.conj() @ fermion_c - unitary
                ),
                np.linalg.norm(unitary @ unitary.conj() - np.eye(4)),
            ]
        )
    for first in range(3):
        for second in range(first + 1, 3):
            residuals.append(
                np.linalg.norm(
                    time_reversals[first] @ time_reversals[second].conj()
                    + time_reversals[second]
                    @ time_reversals[first].conj()
                )
            )
    product = expm(generators[1]) @ expm(generators[0])
    expected_weight = 2.0 - np.exp(x) - np.exp(-x)
    radicand_residual = abs(
        np.linalg.det(np.eye(4) + product) - expected_weight**2
    )
    maximum_residual = max(residuals + [radicand_residual])
    assert maximum_residual < 3.0e-9
    assert expected_weight < 0
    rows.append(
        {
            "check": "fermion_three_positive_TR",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"weight={expected_weight:.12e}",
            "diagnostic_2": f"radicand_residual={radicand_residual:.12e}",
            "maximum_residual": f"{maximum_residual:.12e}",
        }
    )
    return rows


def main() -> None:
    rows = orthogonal_group_checks() + exact_counterexample_checks()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Checks passed: {len(rows)}")


if __name__ == "__main__":
    main()
