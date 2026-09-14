"""Check the two counterexamples in the bosonic Gaussian-weight TRS table.

Run from the repository root through scripts/run-in-wsl.ps1 on Windows:
  python3 docs/research_reports/2026-09-15_trs_gaussian_weights/verify.py
Only NumPy is required. These are formula checks, not QMC benchmarks.
"""

import json

import numpy as np


I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.diag([1, -1]).astype(complex)
checks = 0


def close(actual, expected):
    global checks
    np.testing.assert_allclose(actual, expected, rtol=2e-10, atol=2e-10)
    checks += 1


def physical_trs(A, omega, exchange, matrices, signs):
    size = A.shape[0]
    close(omega @ A + A.T @ omega, np.zeros_like(A))
    for U, sign in zip(matrices, signs):
        close(U.T @ omega @ U, omega)
        close(exchange @ U.conj() @ exchange, U)
        close(np.linalg.solve(U, A.conj() @ U), A)
        close(U.conj() @ U, sign * np.eye(size))
    for a, Ua in enumerate(matrices):
        for Ub in matrices[a + 1:]:
            close(Ub.conj() @ Ua + Ua.conj() @ Ub, np.zeros_like(A))


# One physical mode: two anticommuting positive-square time reversals.
for kappa in (-0.7, 0.7):
    A = kappa * sz
    physical_trs(A, 1j * sy, sx, [I2, 1j * sz], [1, 1])
    M = np.diag(np.exp([kappa, -kappa]))
    W = np.exp(kappa / 2) / (1 - np.exp(kappa))
    close(W, -1 / (2 * np.sinh(kappa / 2)))
    close(W ** -2, -np.linalg.det(I2 - M))
    assert (W > 0) == (kappa < 0)


# Two physical modes: the common set {+,+,-} for all real alpha and x.
I4 = np.eye(4, dtype=complex)
omega = np.kron(1j * sy, I2)
exchange = np.kron(sx, I2)
matrices = [np.kron(I2, sz), np.kron(I2, sx), np.kron(I2, 1j * sy)]
points = []
for alpha, x in [(1.2, 0.4), (0.2, 0.6), (0.0, np.pi)]:
    A = np.block([[-alpha * I2, -x * I2], [x * I2, alpha * I2]])
    physical_trs(A, omega, exchange, matrices, [1, 1, -1])
    z = alpha ** 2 - x ** 2
    close(A @ A, z * I4)
    nu = np.sqrt(complex(z))
    M = np.cosh(nu) * I4 + np.sinh(nu) / nu * A
    close(M.T @ omega @ M, omega)
    W = 1 / (4 * np.sinh(nu / 2) ** 2)
    determinant = np.linalg.det(I4 - M)
    close(W ** -2, determinant)
    close(W.imag, 0)
    assert (W.real > 0) == (alpha > abs(x))
    if alpha > abs(x):
        r = np.arctanh(x / alpha) / 2
        V = np.block([[np.cosh(r) * I2, -np.sinh(r) * I2],
                      [-np.sinh(r) * I2, np.cosh(r) * I2]])
        close(V.T @ omega @ V, omega)
        close(np.linalg.solve(V, A @ V),
              np.diag([-nu, -nu, nu, nu]))
    if alpha == 0:
        close(determinant, 16 * np.sin(x / 2) ** 4)
        close(W, -0.25)
    points.append(dict(alpha=alpha, x=x, weight=float(W.real),
                       determinant=float(determinant.real)))


# Continue the actual square root along a pole-free path in z=alpha^2-x^2.
# The determinant ends positive, while its continuously followed root ends -4.
z_path = np.pi ** 2 * np.exp(1j * np.linspace(0, np.pi, 2001))
nu_path = np.sqrt(z_path)
weight_path = 1 / (4 * np.sinh(nu_path / 2) ** 2)
det_path = 16 * np.sinh(nu_path / 2) ** 4
root_path = np.sqrt(np.abs(det_path)) * np.exp(0.5j * np.unwrap(np.angle(det_path)))
assert np.min(np.abs(det_path)) > 0
close(1 / root_path, weight_path)
close(root_path[-1], -4)
close(weight_path[-1], -0.25)

print(json.dumps(dict(matrix_and_formula_checks=checks, points=points,
                      continued_endpoint_weight=float(weight_path[-1].real),
                      continued_endpoint_root=float(root_path[-1].real)),
                 indent=2))
