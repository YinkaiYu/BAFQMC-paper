#!/usr/bin/env python3
"""Numerical checks for the endpoint-only bosonic Gaussian lift product."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from boson_gaussian_lift import (
    GaussianLift,
    compose_lifts,
    lift_constraint_residual,
    nambu_blocks,
    trace_from_lift,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "tables" / "boson_gaussian_lift_check.csv"


def two_mode_operators(cutoff: int) -> tuple[np.ndarray, ...]:
    local_dimension = cutoff + 1
    annihilation = np.diag(np.sqrt(np.arange(1, local_dimension)), 1)
    identity = np.eye(local_dimension)
    first = np.kron(annihilation, identity)
    second = np.kron(identity, annihilation)
    return first, second, np.eye(local_dimension**2)


def rotation_checks() -> list[dict[str, object]]:
    modes = 2
    damping = 1.3
    pairing = 0.22
    cutoff = 12
    exchange = np.array([[0.0, 1.0], [1.0, 0.0]])
    zero = np.zeros((modes, modes))

    damping_generator = np.block(
        [[-damping * np.eye(modes), zero], [zero, damping * np.eye(modes)]]
    )
    pairing_generator = np.block(
        [[zero, pairing * exchange], [pairing * exchange, zero]]
    )
    damping_lift = GaussianLift(
        expm(damping_generator), np.exp(-damping)
    )
    pairing_lift = GaussianLift(
        expm(pairing_generator), 1.0 / np.cosh(pairing)
    )
    base_lift, base_diagnostics = compose_lifts(damping_lift, pairing_lift)

    annihilation_1, annihilation_2, fock_identity = two_mode_operators(cutoff)
    number_1 = annihilation_1.conj().T @ annihilation_1
    number_2 = annihilation_2.conj().T @ annihilation_2
    damping_fock = -damping * (number_1 + number_2 + fock_identity)
    pairing_fock = pairing * (
        annihilation_1.conj().T @ annihilation_2.conj().T
        - annihilation_1 @ annihilation_2
    )
    base_fock = expm(damping_fock) @ expm(pairing_fock)

    rows: list[dict[str, object]] = []
    reference_matrix = None
    for turns in range(3):
        angle = 2.0 * np.pi * turns
        rotation_generator = np.diag(
            [-1.0j * angle, 0.0, 1.0j * angle, 0.0]
        )
        rotation_lift = GaussianLift(
            expm(rotation_generator), np.exp(-0.5j * angle)
        )
        complete_lift, rotation_diagnostics = compose_lifts(
            base_lift, rotation_lift
        )
        lifted_trace, trace_diagnostics = trace_from_lift(complete_lift)

        rotation_fock = -1.0j * angle * (number_1 + 0.5 * fock_identity)
        truncated_trace = np.trace(base_fock @ expm(rotation_fock))
        if reference_matrix is None:
            reference_matrix = complete_lift.matrix.copy()
        matrix_residual = np.linalg.norm(
            complete_lift.matrix - reference_matrix, ord="fro"
        )
        trace_error = abs(lifted_trace - truncated_trace)

        assert trace_error < 2.0e-8
        assert matrix_residual < 2.0e-14
        assert rotation_diagnostics.lift_constraint_residual < 2.0e-14
        assert trace_diagnostics["weight_square_residual"] < 2.0e-14
        assert np.sign(lifted_trace.real) == (1 if turns % 2 == 0 else -1)

        rows.append(
            {
                "case": "rotation",
                "parameter": turns,
                "contraction_spectral_radius": (
                    rotation_diagnostics.contraction_spectral_radius
                ),
                "cocycle_real": rotation_diagnostics.cocycle.real,
                "cocycle_imag": rotation_diagnostics.cocycle.imag,
                "eta_real": complete_lift.vacuum_amplitude.real,
                "eta_imag": complete_lift.vacuum_amplitude.imag,
                "reference_eta_real": np.nan,
                "reference_eta_imag": np.nan,
                "eta_error": np.nan,
                "lifted_trace_real": lifted_trace.real,
                "lifted_trace_imag": lifted_trace.imag,
                "reference_trace_real": truncated_trace.real,
                "reference_trace_imag": truncated_trace.imag,
                "trace_error": trace_error,
                "matrix_residual": matrix_residual,
                "lift_constraint_residual": lift_constraint_residual(
                    complete_lift
                ),
                "z_factorization_residual": max(
                    base_diagnostics.z_factorization_residual,
                    rotation_diagnostics.z_factorization_residual,
                ),
            }
        )
    return rows


def squeeze_composition_check() -> dict[str, object]:
    modes = 2
    first_parameter = 0.17
    second_parameter = 0.31
    exchange = np.array([[0.0, 1.0], [1.0, 0.0]])
    zero = np.zeros((modes, modes))

    def squeeze_generator(parameter: float) -> np.ndarray:
        return np.block(
            [[zero, parameter * exchange], [parameter * exchange, zero]]
        )

    first_lift = GaussianLift(
        expm(squeeze_generator(first_parameter)),
        1.0 / np.cosh(first_parameter),
    )
    second_lift = GaussianLift(
        expm(squeeze_generator(second_parameter)),
        1.0 / np.cosh(second_parameter),
    )
    product, diagnostics = compose_lifts(first_lift, second_lift)
    total_parameter = first_parameter + second_parameter
    reference_matrix = expm(squeeze_generator(total_parameter))
    reference_eta = 1.0 / np.cosh(total_parameter)
    eta_error = abs(product.vacuum_amplitude - reference_eta)
    matrix_residual = np.linalg.norm(product.matrix - reference_matrix, ord="fro")

    assert diagnostics.contraction_spectral_radius < 1.0
    assert abs(diagnostics.cocycle - 1.0) > 1.0e-4
    assert eta_error < 2.0e-14
    assert matrix_residual < 2.0e-14

    return {
        "case": "squeeze_composition",
        "parameter": total_parameter,
        "contraction_spectral_radius": diagnostics.contraction_spectral_radius,
        "cocycle_real": diagnostics.cocycle.real,
        "cocycle_imag": diagnostics.cocycle.imag,
        "eta_real": product.vacuum_amplitude.real,
        "eta_imag": product.vacuum_amplitude.imag,
        "reference_eta_real": reference_eta,
        "reference_eta_imag": 0.0,
        "eta_error": eta_error,
        "lifted_trace_real": np.nan,
        "lifted_trace_imag": np.nan,
        "reference_trace_real": np.nan,
        "reference_trace_imag": np.nan,
        "trace_error": np.nan,
        "matrix_residual": matrix_residual,
        "lift_constraint_residual": diagnostics.lift_constraint_residual,
        "z_factorization_residual": diagnostics.z_factorization_residual,
    }


def normal_ordering_scalar_check() -> dict[str, object]:
    exponent = -0.7
    matrix = np.diag([np.exp(exponent), np.exp(-exponent)])
    centered_lift = GaussianLift(
        matrix=matrix,
        vacuum_amplitude=np.exp(exponent / 2.0),
        scalar_log=-exponent / 2.0,
    )
    lifted_trace, diagnostics = trace_from_lift(centered_lift)
    reference_trace = 1.0 / (1.0 - np.exp(exponent))
    trace_error = abs(lifted_trace - reference_trace)

    assert trace_error < 2.0e-14
    assert diagnostics["weight_square_residual"] < 2.0e-14

    return {
        "case": "normal_ordered_number",
        "parameter": exponent,
        "contraction_spectral_radius": 0.0,
        "cocycle_real": 1.0,
        "cocycle_imag": 0.0,
        "eta_real": centered_lift.vacuum_amplitude.real,
        "eta_imag": centered_lift.vacuum_amplitude.imag,
        "reference_eta_real": centered_lift.vacuum_amplitude.real,
        "reference_eta_imag": 0.0,
        "eta_error": 0.0,
        "lifted_trace_real": lifted_trace.real,
        "lifted_trace_imag": lifted_trace.imag,
        "reference_trace_real": reference_trace,
        "reference_trace_imag": 0.0,
        "trace_error": trace_error,
        "matrix_residual": 0.0,
        "lift_constraint_residual": lift_constraint_residual(centered_lift),
        "z_factorization_residual": 0.0,
    }


def lifted_local_ratio_check() -> dict[str, object]:
    modes = 2
    damping = 1.1
    pairing = 0.19
    relative_squeeze = 0.13
    cutoff = 16
    exchange = np.array([[0.0, 1.0], [1.0, 0.0]])
    zero = np.zeros((modes, modes))

    def pairing_generator(parameter: float) -> np.ndarray:
        return np.block(
            [[zero, parameter * exchange], [parameter * exchange, zero]]
        )

    damping_generator = np.block(
        [[-damping * np.eye(modes), zero], [zero, damping * np.eye(modes)]]
    )
    damping_lift = GaussianLift(
        expm(damping_generator), np.exp(-damping)
    )
    pairing_lift = GaussianLift(
        expm(pairing_generator(pairing)), 1.0 / np.cosh(pairing)
    )
    current_lift, _ = compose_lifts(damping_lift, pairing_lift)
    relative_lift = GaussianLift(
        expm(pairing_generator(relative_squeeze)),
        1.0 / np.cosh(relative_squeeze),
    )
    proposed_lift, product_diagnostics = compose_lifts(
        relative_lift, current_lift
    )
    current_weight, _ = trace_from_lift(current_lift)
    proposed_weight, _ = trace_from_lift(proposed_lift)
    root_ratio = proposed_weight / current_weight

    _, current_v, _, current_z = nambu_blocks(current_lift.matrix)
    _, _, relative_w, relative_z = nambu_blocks(relative_lift.matrix)
    current_x = np.linalg.solve(current_z.T, current_v.T).T
    q_matrix = relative_z + relative_w @ current_x
    identity = np.eye(2 * modes)
    determinant_p = np.linalg.det(
        identity - relative_lift.matrix @ current_lift.matrix
    ) / np.linalg.det(identity - current_lift.matrix)
    chart_ratio = np.sqrt(np.linalg.det(q_matrix) / determinant_p)
    endpoint_formula_ratio = (
        relative_lift.vacuum_amplitude
        * product_diagnostics.cocycle
        * chart_ratio
    )
    ratio_error = abs(endpoint_formula_ratio - root_ratio)
    squared_ratio_error = abs(
        endpoint_formula_ratio**2 - 1.0 / determinant_p
    )

    annihilation_1, annihilation_2, fock_identity = two_mode_operators(cutoff)
    number_1 = annihilation_1.conj().T @ annihilation_1
    number_2 = annihilation_2.conj().T @ annihilation_2
    damping_fock = -damping * (number_1 + number_2 + fock_identity)
    pairing_unit_fock = (
        annihilation_1.conj().T @ annihilation_2.conj().T
        - annihilation_1 @ annihilation_2
    )
    current_fock = expm(damping_fock) @ expm(pairing * pairing_unit_fock)
    proposed_fock = expm(relative_squeeze * pairing_unit_fock) @ current_fock
    truncated_ratio = np.trace(proposed_fock) / np.trace(current_fock)
    fock_ratio_error = abs(endpoint_formula_ratio - truncated_ratio)

    assert abs(product_diagnostics.cocycle - 1.0) > 1.0e-4
    assert ratio_error < 2.0e-14
    assert squared_ratio_error < 2.0e-14
    assert fock_ratio_error < 2.0e-8

    return {
        "case": "lifted_local_ratio",
        "parameter": relative_squeeze,
        "contraction_spectral_radius": (
            product_diagnostics.contraction_spectral_radius
        ),
        "cocycle_real": product_diagnostics.cocycle.real,
        "cocycle_imag": product_diagnostics.cocycle.imag,
        "eta_real": proposed_lift.vacuum_amplitude.real,
        "eta_imag": proposed_lift.vacuum_amplitude.imag,
        "reference_eta_real": np.nan,
        "reference_eta_imag": np.nan,
        "eta_error": np.nan,
        "lifted_trace_real": endpoint_formula_ratio.real,
        "lifted_trace_imag": endpoint_formula_ratio.imag,
        "reference_trace_real": truncated_ratio.real,
        "reference_trace_imag": truncated_ratio.imag,
        "trace_error": fock_ratio_error,
        "matrix_residual": ratio_error,
        "lift_constraint_residual": (
            product_diagnostics.lift_constraint_residual
        ),
        "z_factorization_residual": (
            product_diagnostics.z_factorization_residual
        ),
    }


def main() -> None:
    rows = rotation_checks()
    rows.append(squeeze_composition_check())
    rows.append(normal_ordering_scalar_check())
    rows.append(lifted_local_ratio_check())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(
            output_file, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT}")
    for row in rows:
        print(
            f"{row['case']:>23}  parameter={row['parameter']!s:<5} "
            f"eta_error={float(row['eta_error']):.3e} "
            f"trace_error={float(row['trace_error']):.3e}"
        )


if __name__ == "__main__":
    main()
