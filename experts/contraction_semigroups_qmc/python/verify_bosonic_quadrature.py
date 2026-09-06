#!/usr/bin/env python3
"""Check the Nambu/quadrature dictionary and the two complex canonical forms.

Run in Linux/WSL with Python and NumPy.  This checks both sets of representatives
already recorded in the note; it does not replace physical trace convergence by
a determinant test.  No generated file is written.
"""

from pathlib import Path
import csv

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
P = {
    "I": np.eye(2),
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, 1], [-1, 0]]),
    "Z": np.diag([1, -1]),
}
MAX_ERROR = 0.0
CHECKS = 0


def word(s):
    result = np.ones((1, 1))
    for letter in s:
        result = np.kron(result, P[letter])
    return result.astype(complex)


def check(a, b=0):
    global MAX_ERROR, CHECKS
    error = float(np.max(np.abs(np.asarray(a) - b)))
    MAX_ERROR = max(MAX_ERROR, error)
    CHECKS += 1
    assert error < 2e-10, error


def anti_basis(u, square):
    """V with V^dagger U bar(V) = I or the real skew matrix J."""
    n = len(u)
    vectors = []
    if square == 1:
        for e in np.eye(n, dtype=complex):
            for v in (e + u @ e.conj(), 1j * (e - u @ e.conj())):
                for b in vectors:
                    coefficient = np.vdot(b, v)
                    check(coefficient.imag)
                    v = v - b * coefficient.real
                norm = np.linalg.norm(v)
                if norm > 1e-8:
                    vectors.append(v / norm)
                if len(vectors) == n:
                    result = np.column_stack(vectors)
                    check(result.conj().T @ u @ result.conj(), np.eye(n))
                    return result
    else:
        assert n % 2 == 0
        first, second = [], []
        for e in np.eye(n, dtype=complex):
            v = e.copy()
            for b in first + second:
                v -= b * np.vdot(b, v)
            norm = np.linalg.norm(v)
            if norm <= 1e-8:
                continue
            v /= norm
            w = -u @ v.conj()
            first.append(v)
            second.append(w)
            if len(first) * 2 == n:
                result = np.column_stack(first + second)
                check(result.conj().T @ u @ result.conj(), np.kron(P["Y"], np.eye(n // 2)))
                return result
    raise AssertionError("Could not construct anti-linear basis")


def normalizer(eta, r1, omega, square):
    """Construct a complex unitary symplectic change, without assuming reality."""
    n = len(eta) // 2
    values, vectors = np.linalg.eigh(eta)
    assert np.sum(values > 0) == n
    positive = vectors[:, values > 0]
    negative = -omega @ positive.conj()
    v = np.column_stack((positive, negative))
    check(v.conj().T @ v, np.eye(2 * n))
    check(v.T @ omega @ v, omega)
    p1 = v.conj().T
    r = p1.conj() @ r1 @ p1.conj().T
    u = r[:n, :n]
    check(r[n:, n:], -u.conj())
    check(r[:n, n:])
    check(u.T, square * u)
    w = anti_basis(u, square).T
    zero = np.zeros((n, n))
    p2 = np.block([[w, zero], [zero, w.conj()]])
    result = p2 @ p1
    check(result.conj().T @ result, np.eye(2 * n))
    check(result.T @ omega @ result, omega)
    return result


def expm(a):
    """Scaling-and-squaring Taylor exponential for the small test matrices."""
    scale = max(0, int(np.ceil(np.log2(max(np.linalg.norm(a, 1), 1)))))
    x = a / 2**scale
    result = np.eye(len(a), dtype=complex)
    term = result.copy()
    for k in range(1, 70):
        term = term @ x / k
        result += term
        if np.linalg.norm(term, 1) < 1e-17:
            break
    for _ in range(scale):
        result = result @ result
    return result


def test_row(row, physical, rng):
    s1, q1, s2 = (int(row[key]) for key in ("s1", "q1", "s2"))
    j1, j2 = (word(row[key]) for key in ("J1_word", "J2_word"))
    n = len(j1) // 2
    identity = np.eye(2 * n)
    eye = np.eye(n)
    zero = np.zeros((n, n))
    omega = np.block([[zero, eye], [-eye, zero]])
    g = -omega
    c = np.block([[zero, eye], [eye, zero]])
    q = np.block([[eye, eye], [-1j * eye, 1j * eye]]) / np.sqrt(2)
    qinv = q.conj().T
    check(q @ qinv, identity)
    check(q.conj(), q @ c)
    check(qinv.T @ g @ qinv, 1j * omega)
    check(q @ (-g) @ q.T, 1j * omega)

    u1 = (1 if s1 == 1 else 1j) * j1
    u2 = (1 if s2 == 1 else 1j) * j2
    r1 = q.conj() @ u1 @ qinv
    r2 = q.conj() @ u2 @ qinv
    eta = (1j if s2 == 1 else 1) * j2 @ g
    e = q @ eta @ qinv
    for u, r, square in ((u1, r1, q1), (u2, r2, 1)):
        check(u.T @ g @ u, g)
        check(r.conj().T @ r, identity)
        check(r.T @ omega @ r, -omega)
        check(r.T, square * r)
        check(r.conj() @ r, square * identity)
        check(q.T @ r @ q, u)
        if physical:
            check(c @ u.conj() @ c, u)
            check(r.imag)
    check(r1.conj() @ r2 + r2.conj() @ r1)
    check(e, -r2.conj() @ omega)
    check(e.conj().T, e)
    check(e @ e, identity)
    check(e.T @ omega + omega @ e)
    check(np.linalg.solve(r1, e.conj() @ r1), e)

    p = normalizer(e, r1, omega, q1)
    d = np.kron(P["Z"], eye)
    x = np.kron(P["X"], eye)
    internal = eye if q1 == 1 else np.kron(P["Y"], np.eye(n // 2))
    r1_standard = np.kron(P["Z"], internal)
    check(p @ e @ p.conj().T, d)
    check(p.conj() @ r2 @ p.conj().T, x)
    check(p.conj() @ r1 @ p.conj().T, r1_standard)

    products = [identity.astype(complex) for _ in range(3)]
    for _ in range(4):
        a = rng.normal(size=j1.shape) + 1j * rng.normal(size=j1.shape)
        a = (a - np.linalg.solve(g, a.T @ g)) / 2
        a = (a + j1.T @ a.conj() @ j1) / 2
        group = (a + j2.T @ a.conj() @ j2) / 2
        candidate = (a - j2.T @ a.conj() @ j2) / 2
        a = -eta + 0.08 * (group + candidate) / max(1, np.linalg.norm(a, 2))
        check(g @ a + a.T @ g)
        check(j1.T @ a @ j1, a.conj())
        contraction = eta @ a + a.conj().T @ eta
        assert np.linalg.eigvalsh(contraction).max() < -1.8
        b = q @ a @ qinv
        h = 1j * omega @ b
        check(h.T, h)
        check(qinv.T @ g @ a @ qinv, h)
        check(np.linalg.solve(r1, b.conj() @ r1), b)
        check(e @ b + b.conj().T @ e, q @ contraction @ qinv)
        bg = q @ group @ qinv
        bc = q @ candidate @ qinv
        check(np.linalg.solve(r2, bg.conj() @ r2), bg)
        check(np.linalg.solve(r2, bc.conj() @ r2), -bc)
        final = p @ b @ p.conj().T
        check(final.T @ omega + omega @ final)
        check(np.linalg.solve(r1_standard, final.conj() @ r1_standard), final)
        check(d @ final + final.conj().T @ d, p @ q @ contraction @ qinv @ p.conj().T)
        for product, generator in zip(products, (a, b, final)):
            product[:] = product @ expm(0.17 * generator)
    check(products[1], q @ products[0] @ qinv)
    check(products[2], p @ products[1] @ p.conj().T)
    for m in products[1:]:
        check(np.linalg.det(identity - m), np.linalg.det(identity - products[0]))
    assert np.linalg.eigvalsh(products[1].conj().T @ e @ products[1] - e).max() < -0.1


def main():
    rng = np.random.default_rng(20260906)
    counts = []
    for name, physical in (("semigroup_classes.csv", False), ("time_reversal_subgroups.csv", True)):
        with (ROOT / "reference" / name).open(newline="") as stream:
            rows = [r for r in csv.DictReader(stream) if r["statistics"] == "boson"]
        retained = []
        for row in rows:
            strict = row.get("strict_interior") == "1" or row.get("semigroup_status") == "contraction semigroup"
            if strict:
                test_row(row, physical, rng)
                retained.append(row)
        assert len(retained) == 8
        assert sum(int(r["q1"]) == 1 for r in retained) == 4
        counts.append(len(retained))

    # A physical-basis obstruction that survives arbitrary real symplectic changes.
    omega = np.kron(P["Y"], np.eye(2))
    r2 = np.kron(P["Z"], np.eye(2))
    inertias = []
    for signature in (np.eye(2), P["Z"]):
        r1 = np.kron(P["X"], signature)
        form = omega @ r1 @ r2
        eig = np.linalg.eigvalsh(form)
        inertias.append((int(np.sum(eig > 0)), int(np.sum(eig < 0))))
    assert inertias == [(4, 0), (2, 2)]

    print(f"Verified {counts[0]} minimal and {counts[1]} physical bosonic contraction representatives.")
    print("All normalize to the q1=+ or q1=- form under complex unitary symplectic changes.")
    print("Verified quadratic forms, inverse dictionaries, group/cone projections, and ordered products.")
    print(f"Real-canonical obstruction verified: inertias {inertias[0]} and {inertias[1]} differ.")
    print(f"Passed {CHECKS} matrix identities; maximum residual {MAX_ERROR:.3e}.")


if __name__ == "__main__":
    main()
