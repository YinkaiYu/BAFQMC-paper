"""Independent finite-Fock and Gaussian-matrix checks for ConvergentBosonicTRS.

Run from the repository root in Linux/WSL:
    python3 note/convergent_bosonic_trs/verify.py
Only NumPy is required. The analytic derivations in the note are the proofs;
these checks compare different representations and increase the Fock cutoff.
"""

import math
import numpy as np


def expm(a):
    """Scaling and squaring with a Taylor series for the small canonical matrices."""
    a = np.asarray(a, dtype=complex)
    scale = max(0, int(math.ceil(math.log2(max(np.linalg.norm(a, 1), 1e-30)))))
    b = a / 2**scale
    value = np.eye(len(a), dtype=complex)
    term = value.copy()
    for k in range(1, 100):
        term = term @ b / k
        value += term
        if np.linalg.norm(term, 1) < 2e-16:
            break
    else:
        raise AssertionError("Matrix exponential failed to converge.")
    for _ in range(scale):
        value = value @ value
    return value


def exp_antihermitian(a):
    assert np.linalg.norm(a + a.conj().T) < 1e-10
    eigenvalues, vectors = np.linalg.eigh(-1j * a)
    return (vectors * np.exp(1j * eigenvalues)) @ vectors.conj().T


def annihilator(cutoff):
    return np.diag(np.sqrt(np.arange(1, cutoff)), 1)


def kernel(m):
    n = len(m) // 2
    a, b, c, d = m[:n, :n], m[:n, n:], m[n:, :n], m[n:, n:]
    dinv = np.linalg.inv(d)
    s = np.block([[b @ dinv, dinv.T], [dinv, -dinv @ c]])
    l0 = np.block([[np.zeros((n, n)), np.eye(n)], [dinv, -dinv @ c]])
    assert np.linalg.norm(s - s.T) < 1e-11
    return s, l0


def trace_from_kernel(s, vacuum, filtering=0.0):
    n = len(s) // 2
    damping = np.diag(np.r_[np.full(n, np.exp(-filtering)), np.ones(n)])
    filtered = damping @ s @ damping
    i = np.eye(n)
    # (z*,z) = f @ (x,p), with z=(x+i p)/sqrt(2).
    f = np.block([[i, -1j * i], [i, 1j * i]]) / np.sqrt(2)
    quadratic = np.eye(2 * n) - f.T @ filtered @ f
    assert np.linalg.eigvalsh(quadratic.real).min() > 0
    determinant = np.linalg.det(quadratic)
    assert abs(determinant.imag) < 1e-9
    assert determinant.real > 0
    return vacuum / np.sqrt(determinant.real)


def evolve_vacuum(generators, steps=600):
    """Integrate the independent pair-state and log-vacuum equations."""
    n = len(generators[0]) // 2
    z = np.zeros((n, n), complex)
    logc = 0j
    max_pair_norm = 0.0
    dt = 1 / steps
    for generator in reversed(generators):
        k = generator[:n, :n]
        p = generator[:n, n:]
        q = -generator[n:, :n]
        scalar = np.trace(k) / 2  # The examples are Weyl-ordered quadratics.

        def derivative(pair):
            return (p + k @ pair + pair @ k.T + pair @ q @ pair,
                    scalar + np.trace(q @ pair) / 2)

        for _ in range(steps):
            d1, c1 = derivative(z)
            d2, c2 = derivative(z + dt * d1 / 2)
            d3, c3 = derivative(z + dt * d2 / 2)
            d4, c4 = derivative(z + dt * d3)
            z += dt * (d1 + 2 * d2 + 2 * d3 + d4) / 6
            logc += dt * (c1 + 2 * c2 + 2 * c3 + c4) / 6
            max_pair_norm = max(max_pair_norm, np.linalg.norm(z, 2))
    assert max_pair_norm < 1
    assert abs(logc.imag) < 1e-11
    return z, float(np.exp(logc.real)), max_pair_norm


def check_plus_example():
    beta, squeezing = 0.9, 0.55
    thermal = np.diag([-beta, beta])
    pair = np.array([[0, -squeezing], [-squeezing, 0]])
    m = expm(thermal) @ expm(pair)
    s, _ = kernel(m)
    exact = 1 / np.sqrt(2 * np.cosh(beta) * np.cosh(squeezing) - 2)
    exact_vacuum = np.exp(-beta / 2) / np.sqrt(np.cosh(squeezing))
    z, vacuum, _ = evolve_vacuum([thermal, pair])
    assert abs(vacuum - exact_vacuum) < 1e-11
    assert abs(z[0, 0] - s[0, 0]) < 1e-11
    assert abs(trace_from_kernel(s, vacuum) - exact) < 1e-11
    errors = []
    for cutoff in (24, 48, 80):
        a = annihilator(cutoff)
        unitary = exp_antihermitian(squeezing * (a @ a - a.T @ a.T) / 2)
        g = np.exp(-beta * (np.arange(cutoff) + 0.5))[:, None] * unitary
        errors.append(abs(np.trace(g) - exact))
        assert abs(g[0, 0] - exact_vacuum) < 1e-7
    assert errors[-1] < 1e-12
    print(f"One-mode trace: {exact:.12f}; Fock errors {errors}")


def check_minus_example():
    beta, theta, zeta = 0.9, 0.37, 0.35 + 0.2j
    j = np.array([[0, 1], [-1, 0]])
    u = j
    k = 1j * theta * np.array([[0, 1], [1, 0]])
    p = np.diag([zeta, zeta.conjugate()])
    q = -p.conjugate()
    zero = np.zeros((2, 2))
    thermal = np.diag([-beta, -beta, beta, beta])
    mixing = np.block([[k, zero], [zero, -k.T]])
    pairing = np.block([[zero, p], [-q, zero]])
    nambu_u = np.block([[u, zero], [zero, u.conjugate()]])
    generators = [thermal, mixing, pairing]
    for generator in generators:
        assert np.linalg.norm(nambu_u.conj().T @ generator.conj() @ nambu_u
                              - generator) < 1e-12
    m = expm(thermal) @ expm(mixing) @ expm(pairing)
    s, _ = kernel(m)
    z, vacuum, largest_pair = evolve_vacuum(generators)
    assert np.linalg.norm(z - s[:2, :2]) < 1e-11
    assert np.linalg.norm(z - u.conj().T @ z.conj() @ u.conj()) < 1e-11
    exact = trace_from_kernel(s, vacuum)
    assert exact > 0
    errors = []
    for cutoff in (8, 12, 18):
        a = annihilator(cutoff)
        eye = np.eye(cutoff)
        b, c = np.kron(a, eye), np.kron(eye, a)
        h1 = 1j * theta * (b.T @ c + c.T @ b)
        h2 = (zeta * (b.T @ b.T) - zeta.conjugate() * (b @ b)
              + zeta.conjugate() * (c.T @ c.T) - zeta * (c @ c)) / 2
        occupations = np.add.outer(np.arange(cutoff), np.arange(cutoff)).ravel()
        g = (np.exp(-beta * (occupations + 1))[:, None]
             * (exp_antihermitian(h1) @ exp_antihermitian(h2)))
        trace = np.trace(g)
        assert abs(trace.imag) < 1e-12
        errors.append(abs(trace.real - exact))
    assert errors[-1] < 3e-7
    assert errors[-1] < errors[0] / 1000
    assert abs(trace_from_kernel(s, vacuum, filtering=24) - vacuum) < 1e-10
    print(f"Two-mode trace: {exact:.12f}; Fock errors {errors}")
    print(f"Two-mode positive vacuum: {vacuum:.12f}; largest pair norm {largest_pair:.6f}")


def check_general_matrices():
    rng = np.random.default_rng(20260915)
    largest_residual = 0.0
    total = 0
    for sign, n in ((1, 1), (1, 3), (-1, 2), (-1, 4)):
        eye, zero = np.eye(n), np.zeros((n, n))
        omega = np.block([[zero, eye], [-eye, zero]])
        sigma = np.diag(np.r_[np.ones(n), -np.ones(n)])
        t = np.block([[eye, eye], [-1j * eye, 1j * eye]]) / np.sqrt(2)
        if sign == 1:
            u = eye
        else:
            half = np.eye(n // 2)
            u = np.block([[np.zeros_like(half), half],
                          [-half, np.zeros_like(half)]])
        r = np.block([[u, zero], [zero, -u]])
        for _ in range(12):
            m = np.eye(2 * n, dtype=complex)
            for _ in range(3):
                real = rng.normal(size=(2 * n, 2 * n))
                imag = rng.normal(size=(2 * n, 2 * n))
                h = -0.1 * (real.T @ real + np.eye(2 * n))
                h = h + 0.08j * (imag + imag.T)
                h = (h + r.T @ h.conj() @ r) / 2
                assert np.linalg.eigvalsh(h.real).max() < 0
                a = t.conj().T @ (1j * omega @ h) @ t
                m = m @ expm(a)
            s, l0 = kernel(m)
            defect = sigma - m.conj().T @ sigma @ m
            assert np.linalg.eigvalsh(defect).min() > 0
            assert np.linalg.norm(s, 2) < 1
            identity = np.eye(2 * n) - s.conj().T @ s
            residual = np.linalg.norm(l0.conj().T @ defect @ l0 - identity)
            largest_residual = max(largest_residual, residual)
            assert residual < 3e-11
            # For Weyl ordering, c^2 det D=1; the real positive c is fixed
            # independently by the state evolution proved in the note.
            ddet = np.linalg.det(m[n:, n:])
            assert abs(ddet.imag) < 1e-8
            assert ddet.real > 0
            vacuum = 1 / np.sqrt(ddet.real)
            assert trace_from_kernel(s, vacuum) > 0
            total += 1
    print(f"{total} noncommuting Gaussian products; largest contraction/kernel residual {largest_residual:.3e}")


if __name__ == "__main__":
    check_plus_example()
    check_minus_example()
    check_general_matrices()
    print("All checks passed.")
