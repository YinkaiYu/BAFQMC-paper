"""Check the bosonic trace counterexample using exact and Fock-space algebra.

Run from Linux/WSL. NumPy is used only for the independent finite-basis check;
the cone identities and closed trace sums use exact rational arithmetic.
"""

from fractions import Fraction as F
import math

import numpy as np


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def transpose(a):
    return tuple(zip(*a))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def multiply(a, b):
    return tuple(
        tuple(sum(x * y for x, y in zip(row, col)) for col in transpose(b))
        for row in a
    )


def determinant(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def trace(a):
    return a[0][0] + a[1][1]


def negative_semidefinite(a, strict=False):
    assert a == transpose(a)
    if strict:
        return a[0][0] < 0 and determinant(a) > 0
    return a[0][0] <= 0 and a[1][1] <= 0 and determinant(a) >= 0


def main():
    identity = matrix(((1, 0), (0, 1)))
    zero = scale(0, identity)
    canonical = matrix(((0, -1), (1, 0)))
    j2 = matrix(((0, 1), (1, 0)))
    eta = matrix(((1, 0), (0, -1)))
    ax = matrix(((-1, -1), (1, 1)))
    ap = matrix(((-1, 1), (-1, 1)))
    eps = F(1, 32)
    a1 = add(ax, scale(eps, ap))
    a2 = add(ap, scale(eps, ax))

    assert multiply(j2, canonical) == eta
    for a in (ax, ap, a1, a2, scale(-1, eta)):
        assert add(multiply(canonical, a), multiply(transpose(a), canonical)) == zero
        assert multiply(multiply(transpose(j2), a), j2) == scale(-1, a)
        assert multiply(multiply(eta, transpose(a)), eta) == a
        assert negative_semidefinite(multiply(eta, a))
    assert multiply(eta, ax) == matrix(((-1, -1), (-1, -1)))
    assert multiply(eta, ap) == matrix(((-1, 1), (1, -1)))
    assert add(ax, ap) == scale(-2, eta)
    for a in (a1, a2):
        contracted = multiply(eta, a)
        assert negative_semidefinite(contracted, strict=True)
        # These exact trace and determinant values fix eigenvalues -2, -2 eps.
        assert trace(contracted) == -2 * (1 + eps)
        assert determinant(contracted) == 4 * eps

    q = F(1, 9)
    sqrt_q = F(1, 3)
    finite_defect = matrix(((q * q - 1, 0), (0, 1 - 1 / (q * q))))
    assert negative_semidefinite(finite_defect, strict=True)
    z = sqrt_q / (1 - q)
    v = (1 + q) / (2 * (1 - q))
    xp_expectation = q / (1 - q) ** 2 - F(1, 4)
    assert xp_expectation == v * v - F(1, 2)
    assert z == F(3, 8)
    assert z * xp_expectation == F(-21, 512)
    strict_expectation = (1 + eps * eps) * xp_expectation + 6 * eps * v * v
    assert z * strict_expectation == F(-7125, 524288)
    vacuum_strict = (-1 + 6 * eps - eps * eps) / 4
    assert vacuum_strict == F(-833, 4096)

    # A polynomial of degree four needs at most four intermediate raising steps.
    # Trace only states 0,...,47 and retain four additional oscillator states.
    traced_states = 48
    dimension = traced_states + 4
    annihilation = np.diag(np.sqrt(np.arange(1, dimension, dtype=float)), 1)
    creation = annihilation.T
    x = (annihilation + creation) / math.sqrt(2)
    p = (annihilation - creation) / (1j * math.sqrt(2))
    x2, p2 = x @ x, p @ p
    hx, hp = -x2, -p2
    h1, h2 = hx + float(eps) * hp, hp + float(eps) * hx

    # Also check the Nambu quadratic convention, including its scalar term.
    nambu = (annihilation, creation)
    for a, target in ((ax, hx), (ap, hp), (a1, h1), (a2, h2)):
        coefficients = multiply(canonical, a)
        operator = sum(
            0.5 * float(coefficients[i][j]) * nambu[i] @ nambu[j]
            for i in range(2)
            for j in range(2)
        )
        np.testing.assert_allclose(operator, target, rtol=1e-13, atol=1e-13)

    occupations = np.arange(traced_states, dtype=float)
    weights = float(sqrt_q) * float(q) ** occupations
    diagonal = np.diag(hx @ hp)[:traced_states]
    expected_diagonal = occupations * (occupations + 1) / 2 - 0.25
    np.testing.assert_allclose(diagonal, expected_diagonal, rtol=1e-12, atol=1e-12)
    strict_diagonal = np.diag(h1 @ h2)[:traced_states]
    expected_fourth = 0.75 * (2 * occupations ** 2 + 2 * occupations + 1)
    np.testing.assert_allclose(
        np.diag(x2 @ x2)[:traced_states], expected_fourth, rtol=1e-12, atol=1e-12
    )
    np.testing.assert_allclose(
        strict_diagonal,
        (1 + float(eps) ** 2) * expected_diagonal
        + 2 * float(eps) * expected_fourth,
        rtol=1e-12,
        atol=1e-12,
    )

    finite_trace = np.dot(diagonal, weights)
    finite_strict_trace = np.dot(strict_diagonal, weights)
    assert abs(finite_trace - float(z * xp_expectation)) < 1e-13
    assert abs(finite_strict_trace - float(z * strict_expectation)) < 1e-13

    # An exact bound on the omitted number-state diagonal sum. For n>=1,
    # |n(n+1)/2 - 1/4| <= (n+1)^2. The perturbed diagonal is bounded by
    # (1 + eps^2 + 3 eps) (n+1)^2. Sum that majorant analytically.
    k = traced_states
    tail_bound = sqrt_q * q ** k * (
        F((k + 1) ** 2, 1) / (1 - q)
        + 2 * (k + 1) * q / (1 - q) ** 2
        + q * (1 + q) / (1 - q) ** 3
    )
    strict_tail_bound = (1 + eps * eps + 3 * eps) * tail_bound
    assert tail_bound < F(1, 10 ** 40)
    assert strict_tail_bound < F(1, 10 ** 40)

    print("Exact cone identities and finite strict-contraction inequality: PASS")
    print(f"Thermal trace: {z}")
    print(f"Two-insertion trace: {z * xp_expectation}")
    print(f"Strict-cone insertion trace: {z * strict_expectation}")
    print(f"Strict-cone product vacuum matrix element: {vacuum_strict}")
    print(f"Independent oscillator-basis trace: {finite_trace.real:.16g}")
    print(f"Independent strict-cone trace: {finite_strict_trace.real:.16g}")
    print(f"Omitted diagonal tails: < {float(strict_tail_bound):.3e}")
    print("All checks passed.")


if __name__ == "__main__":
    main()
