#!/usr/bin/env python3
"""Reference arithmetic for lifted bosonic Gaussian operators.

The Nambu convention is chi=(a,a^+)^T and

    chi U = U M chi.

Each ``GaussianLift`` stores the centered Gaussian operator.  Scalar
normal-ordering factors are accumulated separately in ``scalar_log``.
The implementation intentionally accepts only a well-conditioned
Balian--Brezin chart with rho(Z_left X_right) < 1.  In that domain the
matrix logarithm is the analytic branch reached from the identity, so a
product needs no auxiliary-field interpolation path.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import logm


@dataclass(frozen=True)
class GaussianLift:
    matrix: np.ndarray
    vacuum_amplitude: complex
    scalar_log: complex = 0.0j


@dataclass(frozen=True)
class ProductDiagnostics:
    contraction_spectral_radius: float
    minimum_chart_rcond: float
    contraction_rcond: float
    z_factorization_residual: float
    lift_constraint_residual: float
    cocycle: complex


def nambu_blocks(matrix: np.ndarray) -> tuple[np.ndarray, ...]:
    """Return the (u,v,w,z) blocks of an even-dimensional Nambu matrix."""

    matrix = np.asarray(matrix, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("The Nambu matrix must be square.")
    if matrix.shape[0] % 2:
        raise ValueError("The Nambu matrix dimension must be even.")
    modes = matrix.shape[0] // 2
    return (
        matrix[:modes, :modes],
        matrix[:modes, modes:],
        matrix[modes:, :modes],
        matrix[modes:, modes:],
    )


def reciprocal_condition(matrix: np.ndarray) -> float:
    condition = np.linalg.cond(matrix)
    if not np.isfinite(condition) or condition == 0:
        return 0.0
    return float(1.0 / condition)


def lift_constraint_residual(lift: GaussianLift) -> float:
    """Check eta^2 det(z)=1 for the centered metaplectic lift."""

    *_, z_block = nambu_blocks(lift.matrix)
    return float(abs(lift.vacuum_amplitude**2 * np.linalg.det(z_block) - 1.0))


def compose_lifts(
    left: GaussianLift,
    right: GaussianLift,
    *,
    chart_tolerance: float = 1.0e-12,
    contraction_margin: float = 1.0e-10,
) -> tuple[GaussianLift, ProductDiagnostics]:
    """Compose two lifted operators in a common Balian--Brezin chart.

    The returned lift represents ``U_left U_right`` and therefore carries
    the Nambu matrix ``M_left M_right``.  The condition rho(Z_left X_right)
    < 1 makes ``logm(I-Z_left X_right)`` the unambiguous analytic logarithm
    defined by its power series at the identity.
    """

    left_matrix = np.asarray(left.matrix, dtype=complex)
    right_matrix = np.asarray(right.matrix, dtype=complex)
    if left_matrix.shape != right_matrix.shape:
        raise ValueError("The two lifts must act on the same Nambu space.")

    _, _, left_w, left_z = nambu_blocks(left_matrix)
    _, right_v, _, right_z = nambu_blocks(right_matrix)
    left_rcond = reciprocal_condition(left_z)
    right_rcond = reciprocal_condition(right_z)
    if min(left_rcond, right_rcond) <= chart_tolerance:
        raise ValueError("The selected Balian--Brezin z block is singular.")

    left_z_pair = -np.linalg.solve(left_z, left_w)
    right_x_pair = np.linalg.solve(right_z.T, right_v.T).T
    contraction_kernel = left_z_pair @ right_x_pair
    spectral_radius = float(
        np.max(
            np.abs(np.linalg.eigvals(contraction_kernel)),
            initial=0.0,
        )
    )
    if spectral_radius >= 1.0 - contraction_margin:
        raise ValueError(
            "The Gaussian contraction is outside the reference chart: "
            f"rho(Z_left X_right)={spectral_radius:.6g}."
        )

    identity = np.eye(left_z.shape[0], dtype=complex)
    contraction_matrix = identity - contraction_kernel
    contraction_rcond = reciprocal_condition(contraction_matrix)
    if contraction_rcond <= chart_tolerance:
        raise ValueError("The Gaussian contraction matrix is singular.")

    cocycle_log = -0.5 * np.trace(logm(contraction_matrix))
    cocycle = complex(np.exp(cocycle_log))
    product_matrix = left_matrix @ right_matrix
    product = GaussianLift(
        matrix=product_matrix,
        vacuum_amplitude=(
            left.vacuum_amplitude * right.vacuum_amplitude * cocycle
        ),
        scalar_log=left.scalar_log + right.scalar_log,
    )

    *_, product_z = nambu_blocks(product_matrix)
    predicted_z = left_z @ contraction_matrix @ right_z
    z_scale = max(1.0, np.linalg.norm(product_z, ord="fro"))
    diagnostics = ProductDiagnostics(
        contraction_spectral_radius=spectral_radius,
        minimum_chart_rcond=min(left_rcond, right_rcond),
        contraction_rcond=contraction_rcond,
        z_factorization_residual=float(
            np.linalg.norm(product_z - predicted_z, ord="fro") / z_scale
        ),
        lift_constraint_residual=lift_constraint_residual(product),
        cocycle=cocycle,
    )
    return product, diagnostics


def trace_from_lift(
    lift: GaussianLift,
    *,
    trace_chart_sign: int = 1,
    pole_tolerance: float = 1.0e-13,
) -> tuple[complex, dict[str, complex | float]]:
    """Evaluate the trace in one fixed trace chart.

    ``trace_chart_sign`` is fixed once by a simple convergent reference in
    the chosen chart.  It is not updated from Monte Carlo history.  A
    multi-chart production implementation must include the corresponding
    algebraic transition signs.
    """

    if trace_chart_sign not in (-1, 1):
        raise ValueError("trace_chart_sign must be +1 or -1.")
    matrix = np.asarray(lift.matrix, dtype=complex)
    modes = matrix.shape[0] // 2
    *_, z_block = nambu_blocks(matrix)
    determinant_denominator = ((-1) ** modes) * np.linalg.det(
        np.eye(2 * modes, dtype=complex) - matrix
    )
    if abs(determinant_denominator) <= pole_tolerance:
        raise ValueError("The lifted Gaussian trace is at a determinant pole.")

    trace_chart_square = np.linalg.det(z_block) / determinant_denominator
    trace_chart_factor = trace_chart_sign * np.sqrt(complex(trace_chart_square))
    weight = complex(
        np.exp(lift.scalar_log)
        * lift.vacuum_amplitude
        * trace_chart_factor
    )
    expected_weight_square = np.exp(2.0 * lift.scalar_log) / determinant_denominator
    square_residual = abs(weight**2 - expected_weight_square) / max(
        1.0, abs(expected_weight_square)
    )
    return weight, {
        "determinant_denominator": complex(determinant_denominator),
        "trace_chart_square": complex(trace_chart_square),
        "trace_chart_factor": complex(trace_chart_factor),
        "weight_square_residual": float(square_residual),
    }
