"""Reproduce the paired analytic-continuation counterexample in the author report.

Run in Linux/WSL; requires NumPy. This is a formula check, not a QMC benchmark.
"""
from pathlib import Path
import json

import numpy as np


I = np.eye(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0])
J = 1j * Y
Omega = np.kron(J, I)
C = np.kron(X, I)
checks = 0


def equal(actual, expected, label):
    global checks
    np.testing.assert_allclose(
        actual, expected, atol=1e-12, rtol=1e-12, err_msg=label
    )
    checks += 1


def physical_tr(A, U, square):
    equal(U.T @ Omega @ U, Omega, "Canonical commutators")
    equal(C @ U.conj() @ C, U, "Hermitian conjugation")
    equal(A.conj() @ U, U @ A, "Slice invariance")
    equal(U.conj() @ U, square * np.eye(4), "TR square")


def cutoff_trace(x, kappa, d):
    ann = np.diag(np.sqrt(np.arange(1, d)), 1)
    b = np.kron(ann, np.eye(d))
    c = np.kron(np.eye(d), ann)
    h = -x * (b.T @ b + c.T @ c + np.eye(d * d))
    h += kappa * (b.T @ c.T + b @ c)
    return float(np.exp(np.linalg.eigvalsh(h)).sum())


records = []
for x, kappa in [(1.2, 0.4), (0.2, 0.6)]:
    A = np.block([[-x * I, kappa * X], [-kappa * X, x * I]])
    equal(A.T @ Omega + Omega @ A, np.zeros((4, 4)), "Canonical generator")
    equal(A @ A, (x * x - kappa * kappa) * np.eye(4), "Squared generator")
    plus = np.eye(4)
    minus = -np.kron(Z, Y)
    physical_tr(A, plus, 1)
    physical_tr(A, minus, -1)
    equal(minus.conj() @ plus, -plus.conj() @ minus, "TR anticommutation")
    omega = np.sqrt(complex(x * x - kappa * kappa))
    weight = 1 / (4 * np.sinh(omega / 2) ** 2)
    equal(weight.imag, 0, "Real continued weight")
    M = np.cosh(omega) * np.eye(4) + np.sinh(omega) * A / omega
    equal(
        np.linalg.det(np.eye(4) - M),
        16 * np.sinh(omega / 2) ** 4,
        "Nambu determinant",
    )
    traces = [cutoff_trace(x, kappa, d) for d in (6, 10, 14)]
    records.append(
        {
            "x": x,
            "kappa": kappa,
            "continued_weight": float(weight.real),
            "cutoff_dimensions_per_mode": [6, 10, 14],
            "cutoff_traces": traces,
        }
    )

assert records[0]["continued_weight"] > 0
assert abs(records[0]["cutoff_traces"][-1] / records[0]["continued_weight"] - 1) < 2e-6
assert records[1]["continued_weight"] < 0
assert all(t > 0 for t in records[1]["cutoff_traces"])

# The existing pure-pair example also has a {+,+,-} symmetry triple.
A = -0.4 * Omega
triple = [np.kron(I, X), np.kron(I, Z), np.kron(I, J)]
for U, square in zip(triple, [1, 1, -1]):
    physical_tr(A, U, square)
for a in range(3):
    for b in range(a):
        equal(
            triple[a].conj() @ triple[b],
            -triple[b].conj() @ triple[a],
            "Triple anticommutation",
        )

result = {
    "matrix_checks": checks,
    "result": "Paired negative analytic continuation confirmed",
    "records": records,
}
out = Path(".build/trs-branch-issue-checks.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
