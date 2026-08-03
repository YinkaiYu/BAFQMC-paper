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


def random_one_sided_product(
    positive: int,
    negative: int,
    rng: np.random.Generator,
    layers: int = 4,
) -> tuple[np.ndarray, np.ndarray, float]:
    dimension = positive + negative
    eta = np.diag([1.0] * positive + [-1.0] * negative)
    product = np.eye(dimension)
    minimum_generator_eigenvalue = np.inf
    for _ in range(layers):
        trial = rng.normal(scale=0.18, size=(dimension, dimension))
        positive_matrix = trial.T @ trial
        antisymmetric = rng.normal(
            scale=0.18, size=(dimension, dimension)
        )
        antisymmetric -= antisymmetric.T
        generator = eta @ (antisymmetric + 0.5 * positive_matrix)
        generator_inequality = (
            generator.T @ eta + eta @ generator
        )
        minimum_generator_eigenvalue = min(
            minimum_generator_eigenvalue,
            float(np.linalg.eigvalsh(generator_inequality).min()),
        )
        product = expm(generator) @ product
    return eta, product, minimum_generator_eigenvalue


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


def one_sided_semigroup_checks() -> list[dict[str, str]]:
    rng = np.random.default_rng(20260804)
    rows: list[dict[str, str]] = []
    for positive in range(4):
        for negative in range(4):
            dimension = positive + negative
            if dimension < 2:
                continue
            minimum_plus = np.inf
            minimum_semigroup_eigenvalue = np.inf
            minimum_generator_eigenvalue = np.inf
            for _ in range(240):
                eta, product, generator_eigenvalue = (
                    random_one_sided_product(positive, negative, rng)
                )
                plus = float(np.linalg.det(np.eye(dimension) + product).real)
                semigroup_difference = product.T @ eta @ product - eta
                minimum_plus = min(minimum_plus, plus)
                minimum_semigroup_eigenvalue = min(
                    minimum_semigroup_eigenvalue,
                    float(np.linalg.eigvalsh(semigroup_difference).min()),
                )
                minimum_generator_eigenvalue = min(
                    minimum_generator_eigenvalue, generator_eigenvalue
                )
            assert minimum_generator_eigenvalue > -TOLERANCE
            assert minimum_semigroup_eigenvalue > -2.0e-8
            assert minimum_plus > -TOLERANCE
            rows.append(
                {
                    "check": f"one_sided_semigroup({positive},{negative})",
                    "samples": "240",
                    "result": "pass",
                    "diagnostic_1": f"minimum_det_I_plus_B={minimum_plus:.12e}",
                    "diagnostic_2": (
                        "minimum_semigroup_eigenvalue="
                        f"{minimum_semigroup_eigenvalue:.12e}"
                    ),
                    "maximum_residual": (
                        f"{max(0.0, -minimum_generator_eigenvalue):.12e}"
                    ),
                }
            )
    return rows


def fermion_fock_operators() -> list[np.ndarray]:
    identity = np.eye(2, dtype=complex)
    sigma_z = np.diag([1, -1]).astype(complex)
    annihilation = np.array([[0, 1], [0, 0]], dtype=complex)
    first = np.kron(annihilation, identity)
    second = np.kron(sigma_z, annihilation)
    return [first, second, first.conj().T, second.conj().T]


def fock_generator(
    fermion_g: np.ndarray,
    generator: np.ndarray,
    operators: list[np.ndarray],
) -> np.ndarray:
    coefficient = fermion_g @ generator
    result = np.zeros_like(operators[0])
    for row, first in enumerate(operators):
        for column, second in enumerate(operators):
            result += (
                0.5
                * coefficient[row, column]
                * first
                @ second
            )
    return result


def pfaffian_4x4(matrix: np.ndarray) -> complex:
    assert matrix.shape == (4, 4)
    assert np.linalg.norm(matrix + matrix.T) < TOLERANCE
    return (
        matrix[0, 1] * matrix[2, 3]
        - matrix[0, 2] * matrix[1, 3]
        + matrix[0, 3] * matrix[1, 2]
    )


def pfaffian_small(matrix: np.ndarray) -> complex:
    """Recursive Pfaffian for the small exact checks below."""
    dimension = matrix.shape[0]
    assert matrix.shape == (dimension, dimension)
    assert dimension % 2 == 0
    assert np.linalg.norm(matrix + matrix.T) < TOLERANCE
    if dimension == 0:
        return 1.0 + 0.0j
    value = 0.0 + 0.0j
    for column in range(1, dimension):
        reduced = np.delete(
            np.delete(matrix, [0, column], axis=0),
            [0, column],
            axis=1,
        )
        value += (
            (-1) ** (column + 1)
            * matrix[0, column]
            * pfaffian_small(reduced)
        )
    return value


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

    majorana_change = np.array(
        [[1.0, 1.0], [-1.0j, 1.0j]], dtype=complex
    )
    majorana_generator = (
        majorana_change
        @ fermion_a
        @ np.linalg.inv(majorana_change)
    )
    majorana_product = expm(majorana_generator)
    majorana_residual = max(
        np.linalg.norm(majorana_generator.imag),
        np.linalg.norm(
            majorana_product.T @ majorana_product - np.eye(2)
        ),
        abs(
            np.linalg.det(np.eye(2) + majorana_product)
            - fermion_weight**2
        ),
    )
    assert majorana_residual < TOLERANCE
    assert fermion_weight < 0
    rows.append(
        {
            "check": "full_nambu_SO2_does_not_fix_lift_sign",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": (
                "det_I_plus_M="
                f"{np.linalg.det(np.eye(2) + majorana_product).real:.12e}"
            ),
            "diagnostic_2": f"fock_trace={fermion_weight:.12e}",
            "maximum_residual": f"{majorana_residual:.12e}",
        }
    )

    closed_angle = np.pi
    closed_generator = np.array(
        [[0.0, 2.0 * closed_angle], [-2.0 * closed_angle, 0.0]]
    )
    closed_rotation = expm(closed_generator)
    split_product = np.block(
        [
            [closed_rotation, np.zeros((2, 2))],
            [np.zeros((2, 2)), np.eye(2)],
        ]
    )
    split_eta = np.diag([1.0, 1.0, -1.0, -1.0])
    split_fock_trace = 4.0 * np.cos(closed_angle)
    split_radicand = np.linalg.det(np.eye(4) + split_product)
    split_residual = max(
        np.linalg.norm(split_product - np.eye(4)),
        np.linalg.norm(
            split_product.T @ split_eta @ split_product - split_eta
        ),
        abs(split_radicand - split_fock_trace**2),
    )
    assert split_residual < 2.0e-8
    assert split_fock_trace < 0
    rows.append(
        {
            "check": "full_nambu_SO22_same_M_opposite_lift",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": (
                f"det_I_plus_M={split_radicand:.12e};M_equals_I"
            ),
            "diagnostic_2": f"fock_trace={split_fock_trace:.12e}",
            "maximum_residual": f"{split_residual:.12e}",
        }
    )

    first_angle = 1.0
    second_angle = 1.2

    def rotation(angle: float) -> np.ndarray:
        return np.array(
            [
                [np.cos(2.0 * angle), np.sin(2.0 * angle)],
                [-np.sin(2.0 * angle), np.cos(2.0 * angle)],
            ]
        )

    first_rotation = rotation(first_angle)
    second_rotation = rotation(second_angle)
    first_green = (
        2.0 * np.linalg.inv(np.eye(2) + first_rotation) - np.eye(2)
    )
    second_green = (
        2.0 * np.linalg.inv(np.eye(2) + second_rotation) - np.eye(2)
    )
    product_pfaffian = pfaffian_4x4(
        np.block(
            [
                [first_green, -np.eye(2)],
                [np.eye(2), second_green],
            ]
        )
    )
    lifted_product_trace = (
        -2.0
        * np.cos(first_angle)
        * np.cos(second_angle)
        * product_pfaffian
    )
    expected_product_trace = 2.0 * np.cos(
        first_angle + second_angle
    )
    product_residual = max(
        abs(lifted_product_trace - expected_product_trace),
        abs(
            expected_product_trace**2
            - np.linalg.det(
                np.eye(2) + first_rotation @ second_rotation
            )
        ),
    )
    assert product_residual < TOLERANCE
    assert expected_product_trace < 0
    rows.append(
        {
            "check": "fermion_lifted_pfaffian_product_sign",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": (
                f"pfaffian_trace={lifted_product_trace.real:.12e}"
            ),
            "diagnostic_2": (
                f"direct_fock_trace={expected_product_trace:.12e}"
            ),
            "maximum_residual": f"{product_residual:.12e}",
        }
    )

    slice_angles = [np.pi / 4.0] * 4
    slice_count = len(slice_angles)
    spacetime_matrix = np.zeros(
        (2 * slice_count, 2 * slice_count), dtype=float
    )
    slice_trace_product = 1.0
    majorana_form = np.array([[0.0, -1.0], [1.0, 0.0]])
    for row, angle in enumerate(slice_angles):
        row_slice = slice(2 * row, 2 * row + 2)
        spacetime_matrix[row_slice, row_slice] = (
            np.tan(angle) * majorana_form
        )
        slice_trace_product *= np.cos(angle)
        for column in range(row + 1, slice_count):
            column_slice = slice(2 * column, 2 * column + 2)
            block = ((-1) ** (column - row)) * np.eye(2)
            spacetime_matrix[row_slice, column_slice] = block
            spacetime_matrix[column_slice, row_slice] = -block
    spacetime_trace = (
        (-1) ** (slice_count // 2)
        * 2.0
        * slice_trace_product
        * pfaffian_small(spacetime_matrix)
    )
    expected_closed_loop_trace = -2.0
    spacetime_residual = max(
        np.linalg.norm(spacetime_matrix + spacetime_matrix.T),
        abs(spacetime_trace - expected_closed_loop_trace),
    )
    assert spacetime_residual < TOLERANCE
    rows.append(
        {
            "check": "fermion_spacetime_pfaffian_closed_loop",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"pfaffian_trace={spacetime_trace.real:.12e}",
            "diagnostic_2": "four_positive_slices_total_lift_negative",
            "maximum_residual": f"{spacetime_residual:.12e}",
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

    real_y = 1j * sigma_y
    spatial_identity = np.eye(2, dtype=complex)
    spatial_symmetric = np.array([[1.7, 0.3], [0.3, 2.1]])
    spatial_antisymmetric = np.array([[0.0, 1.0], [-1.0, 0.0]])

    def kron3(
        first: np.ndarray, second: np.ndarray, third: np.ndarray
    ) -> np.ndarray:
        return np.kron(np.kron(first, second), third)

    boson_model_g = kron3(-1j * sigma_y, identity, spatial_identity)
    boson_model_c = kron3(sigma_x, identity, spatial_identity)
    boson_r2 = kron3(sigma_z, sigma_x, spatial_identity)
    boson_r3 = kron3(sigma_z, sigma_z, spatial_identity)
    boson_model_time_reversals = [
        np.eye(8, dtype=complex),
        1j * boson_r2,
        1j * boson_r3,
    ]
    boson_model_generators = [
        kron3(sigma_z, identity, spatial_symmetric),
        kron3(real_y, real_y, spatial_antisymmetric),
        kron3(identity, identity, spatial_antisymmetric),
        kron3(sigma_x, real_y, spatial_antisymmetric),
    ]
    boson_model_residuals: list[float] = []
    for generator in boson_model_generators:
        boson_model_residuals.extend(
            [
                np.linalg.norm(generator.imag),
                np.linalg.norm(
                    boson_model_g @ generator
                    + generator.T @ boson_model_g
                ),
                np.linalg.norm(generator @ boson_r2 - boson_r2 @ generator),
                np.linalg.norm(generator @ boson_r3 - boson_r3 @ generator),
            ]
        )
        for unitary in boson_model_time_reversals:
            boson_model_residuals.append(
                np.linalg.norm(
                    np.linalg.solve(unitary, generator.conj()) @ unitary
                    - generator
                )
            )
    for unitary in boson_model_time_reversals:
        boson_model_residuals.extend(
            [
                np.linalg.norm(
                    unitary.T @ boson_model_g @ unitary - boson_model_g
                ),
                np.linalg.norm(
                    boson_model_c @ unitary.conj() @ boson_model_c
                    - unitary
                ),
                np.linalg.norm(unitary @ unitary.conj() - np.eye(8)),
            ]
        )
    for first in range(3):
        for second in range(first + 1, 3):
            boson_model_residuals.append(
                np.linalg.norm(
                    boson_model_time_reversals[first]
                    @ boson_model_time_reversals[second].conj()
                    + boson_model_time_reversals[second]
                    @ boson_model_time_reversals[first].conj()
                )
            )

    boson_eta = boson_model_g @ boson_r3
    boson_s = boson_model_c @ boson_r3
    boson_q = -1j * boson_r2
    boson_model_residuals.extend(
        [
            np.linalg.norm(boson_q.T @ boson_eta @ boson_q + boson_eta),
            np.linalg.norm(boson_s @ boson_q - boson_q @ boson_s),
            np.linalg.norm(boson_s.T @ boson_eta @ boson_s + boson_eta),
            np.linalg.norm(
                boson_s.T
                @ (-boson_model_g @ boson_model_c)
                @ boson_s
                - boson_model_g
                @ boson_model_c
            ),
        ]
    )

    negative_unitary = boson_r2 @ boson_r3
    boson_model_residuals.extend(
        [
            np.linalg.norm(
                negative_unitary @ negative_unitary.conj() + np.eye(8)
            ),
            np.linalg.norm(
                negative_unitary.T
                @ boson_model_g
                @ negative_unitary
                - boson_model_g
            ),
            np.linalg.norm(
                boson_model_c
                @ negative_unitary.conj()
                @ boson_model_c
                - negative_unitary
            ),
        ]
    )
    for generator in boson_model_generators:
        boson_model_residuals.append(
            np.linalg.norm(
                np.linalg.solve(negative_unitary, generator.conj())
                @ negative_unitary
                - generator
            )
        )
    for unitary in boson_model_time_reversals:
        boson_model_residuals.append(
            np.linalg.norm(
                negative_unitary @ unitary.conj()
                - unitary @ negative_unitary.conj()
            )
        )

    base_generators = [
        np.kron(sigma_z, identity),
        np.kron(real_y, real_y),
        np.kron(sigma_x, real_y),
    ]
    commutator_columns = []
    for row in range(4):
        for column in range(4):
            matrix_unit = np.zeros((4, 4), dtype=complex)
            matrix_unit[row, column] = 1.0
            commutator_columns.append(
                np.concatenate(
                    [
                        (matrix_unit @ generator - generator @ matrix_unit)
                        .reshape(-1)
                        for generator in base_generators
                    ]
                )
            )
    commutator_map = np.stack(commutator_columns, axis=1)
    centralizer_dimension = 16 - np.linalg.matrix_rank(
        commutator_map, tol=TOLERANCE
    )
    assert centralizer_dimension == 4

    coefficients = np.array([0.2, -0.3, 0.4, 0.5])
    a_coefficient, b_coefficient, c_coefficient, d_coefficient = coefficients
    general_unitary = (
        a_coefficient * np.eye(8)
        + 1j * b_coefficient * boson_r2
        + 1j * c_coefficient * boson_r3
        + d_coefficient * negative_unitary
    )
    expected_square = (
        a_coefficient**2
        + b_coefficient**2
        + c_coefficient**2
        - d_coefficient**2
    ) * np.eye(8) + 2.0 * d_coefficient * (
        -1j * c_coefficient * boson_r2
        + 1j * b_coefficient * boson_r3
        + a_coefficient * negative_unitary
    )
    boson_model_residuals.append(
        np.linalg.norm(
            general_unitary @ general_unitary.conj() - expected_square
        )
    )

    boson_model_maximum_residual = max(boson_model_residuals)
    assert boson_model_maximum_residual < TOLERANCE
    rows.append(
        {
            "check": "boson_three_positive_odd_parity_pair_model",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": (
                "four_generator_families_preserve_three_positive_TR;"
                f"centralizer_dimension={centralizer_dimension}"
            ),
            "diagnostic_2": "single_negative_TR_commutes_with_positive_TRs",
            "maximum_residual": f"{boson_model_maximum_residual:.12e}",
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
    fock_operators = fermion_fock_operators()
    fock_generators = [
        fock_generator(fermion_g, generator, fock_operators)
        for generator in generators
    ]
    fock_weight = np.trace(
        expm(fock_generators[0]) @ expm(fock_generators[1])
    )
    expected_first_exponential = np.diag([-1, 1, 1, -1])
    expected_second_exponential = np.diag(
        [np.exp(-x), 1, 1, np.exp(x)]
    )
    fock_residual = max(
        abs(fock_weight - expected_weight),
        np.linalg.norm(
            expm(fock_generators[0]) - expected_first_exponential
        ),
        np.linalg.norm(
            expm(fock_generators[1]) - expected_second_exponential
        ),
    )
    maximum_residual = max(
        residuals + [radicand_residual, float(fock_residual)]
    )
    assert maximum_residual < 3.0e-9
    assert expected_weight < 0
    rows.append(
        {
            "check": "fermion_three_positive_TR",
            "samples": "exact",
            "result": "pass",
            "diagnostic_1": f"weight={expected_weight:.12e}",
            "diagnostic_2": (
                f"fock_trace={fock_weight.real:.12e};"
                f"radicand_residual={radicand_residual:.12e}"
            ),
            "maximum_residual": f"{maximum_residual:.12e}",
        }
    )
    return rows


def main() -> None:
    rows = (
        orthogonal_group_checks()
        + one_sided_semigroup_checks()
        + exact_counterexample_checks()
    )
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
