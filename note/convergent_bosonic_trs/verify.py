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


def rp_basis(m):
    eye, zero = np.eye(m), np.zeros((m, m))
    return np.block([[eye, zero, eye, zero],
                     [1j * eye, zero, -1j * eye, zero],
                     [zero, eye, zero, eye],
                     [zero, -1j * eye, zero, 1j * eye]]) / np.sqrt(2)


def check_rp_basis():
    """Check RP coefficients, commutators, adjoints, and real propagation."""
    rng = np.random.default_rng(20260916)
    largest_residual = 0.0
    for m in (1, 2, 3):
        eye, zero = np.eye(m), np.zeros((m, m))
        j = np.block([[zero, eye], [-eye, zero]])
        exchange = np.block([[zero, eye], [eye, zero]])
        z2, i2 = np.zeros((2 * m, 2 * m)), np.eye(2 * m)
        jr = np.block([[j, z2], [z2, j]])
        jd = np.block([[z2, i2], [-i2, z2]])
        eta = np.diag(np.tile(np.r_[np.ones(m), -np.ones(m)], 2))
        sigma = np.diag(np.r_[np.ones(2 * m), -np.ones(2 * m)])
        reflection = np.block([[z2, i2], [i2, z2]])
        s = rp_basis(m)
        t = np.block([[i2, i2], [-1j * i2, 1j * i2]]) / np.sqrt(2)
        assert np.linalg.norm(s @ s.conj().T - np.eye(4 * m)) < 1e-12
        assert np.linalg.norm(s @ jr @ s.T - jd) < 1e-12
        assert np.linalg.norm(s @ eta @ s.conj().T - sigma) < 1e-12
        assert np.linalg.norm(s.conj() @ reflection @ s.conj().T
                              - np.eye(4 * m)) < 1e-12
        for _ in range(8):
            d = 0.06 * (rng.normal(size=(2 * m, 2 * m))
                        + 1j * rng.normal(size=(2 * m, 2 * m)))
            d = (d + d.T) / 2
            v = rng.normal(size=(2 * m, 2 * m)) + 1j * rng.normal(size=(2 * m, 2 * m))
            f = 0.02 * v @ v.conj().T
            hrp = np.block([[d, f], [f.T, d.conj()]])
            hd = s.conj() @ hrp @ s.conj().T
            hquad = 2 * t.conj() @ hd @ t.conj().T
            # Add ordinary thermal damping without changing the RP coupling F.
            damping = np.linalg.norm(hquad.real, 2) + 0.3
            d -= damping * exchange / 2
            hrp = np.block([[d, f], [f.T, d.conj()]])
            hd = s.conj() @ hrp @ s.conj().T
            hquad = 2 * t.conj() @ hd @ t.conj().T
            ar = 2 * jr @ hrp
            ad = s @ ar @ s.conj().T
            residual = max(np.linalg.norm(hd.imag), np.linalg.norm(ad.imag),
                           np.linalg.norm(ad - 2 * jd @ hd))
            largest_residual = max(largest_residual, residual)
            assert residual < 1e-12
            assert np.linalg.eigvalsh(hquad.real).max() < -0.29
            mr = expm(ar)
            md = s @ mr @ s.conj().T
            assert np.linalg.eigvalsh(eta - mr.conj().T @ eta @ mr).min() > 0
            assert np.linalg.norm(md.imag) < 1e-11
            assert np.linalg.norm(md - expm(ad)) < 1e-11
    print(f"24 RP basis/metric checks; largest generator residual {largest_residual:.3e}")


def check_thermal_paths():
    """Follow both symmetry forms from the known thermal trace to unitary boundaries."""
    rng = np.random.default_rng(20260917)
    delta, n = 0.4, 2
    eye, zero = np.eye(n), np.zeros((n, n))
    omega = np.block([[zero, eye], [-eye, zero]])
    sigma = np.diag([1, 1, -1, -1])
    t = np.block([[eye, eye], [-1j * eye, 1j * eye]]) / np.sqrt(2)
    smallest_defect = np.inf
    largest_jump = 0.0
    for sign in (1, -1):
        u = eye if sign == 1 else np.array([[0, 1], [-1, 0]])
        r = np.block([[u, zero], [zero, -u]])
        generators = []
        for index in range(3):
            b = rng.normal(size=(4, 4))
            h = 0.12j * (b + b.T)
            if index == 0:
                a = rng.normal(size=(4, 4))
                h -= 0.08 * a.T @ a + 0.35 * np.eye(4)
            h = (h + r.T @ h.conj() @ r) / 2
            generators.append(t.conj().T @ (1j * omega @ h) @ t)
        previous = None
        for position in np.linspace(0, 1, 41):
            m = np.eye(4, dtype=complex)
            for a in generators:
                deformed = position * a - (1 - position) * delta * sigma
                m = m @ expm(deformed)
            s, _ = kernel(m)
            defect = np.linalg.eigvalsh(sigma - m.conj().T @ sigma @ m).min()
            smallest_defect = min(smallest_defect, defect)
            assert defect > 0
            ddet = np.linalg.det(m[n:, n:])
            assert abs(ddet.imag) < 1e-11 and ddet.real > 0
            trace = trace_from_kernel(s, 1 / np.sqrt(ddet.real))
            assert trace > 0
            if previous is None:
                expected = (2 * np.sinh(len(generators) * delta / 2))**(-n)
                assert abs(trace - expected) < 1e-12
            else:
                largest_jump = max(largest_jump, abs(trace - previous))
            previous = trace
        # Endpoint normalization from independent state evolution.
        _, vacuum, _ = evolve_vacuum(generators)
        assert abs(trace_from_kernel(s, vacuum) - trace) < 1e-11
    print(f"82 points on TRS thermal paths; minimum contraction defect {smallest_defect:.6f}; "
          f"largest neighboring trace change {largest_jump:.6f}")


def check_rp_fock():
    """Noncommuting RP damping and phase fields, checked in physical Fock space."""
    epsilon, pairing, same_pairing, step = 1.8, 0.35, 0.24, 0.65
    phases = (0.4, -0.27)
    k = -step * epsilon * np.eye(2)
    p = step * np.array([[same_pairing, pairing], [pairing, same_pairing]])
    thermal = np.block([[k, p], [-p, -k.T]])
    generators = []
    for phase in phases:
        generators.extend([thermal, 1j * phase * np.diag([1, -1, -1, 1])])
    m = np.eye(4, dtype=complex)
    for a in generators:
        m = m @ expm(a)
    s, _ = kernel(m)
    _, vacuum, _ = evolve_vacuum(generators)
    exact = trace_from_kernel(s, vacuum)
    # Convert standard (b,c,b+,c+) order to the reflected-sector order first.
    permutation = np.eye(4)[[0, 2, 1, 3]]
    rotation = rp_basis(1) @ permutation
    transformed = [rotation @ a @ rotation.conj().T for a in generators]
    assert all(np.linalg.norm(a.imag) < 1e-12 for a in transformed)
    assert np.linalg.norm(transformed[0] @ transformed[1]
                          - transformed[1] @ transformed[0]) > 0.1
    errors = []
    for cutoff in (8, 12, 18):
        a, eye = annihilator(cutoff), np.eye(cutoff)
        b, c = np.kron(a, eye), np.kron(eye, a)
        occupations = np.add.outer(np.arange(cutoff), np.arange(cutoff)).ravel()
        difference = np.subtract.outer(np.arange(cutoff), np.arange(cutoff)).ravel()
        hamiltonian = (epsilon * np.diag(occupations + 1)
                       - pairing * (b.T @ c.T + b @ c)
                       - same_pairing * (b.T @ b.T + b @ b + c.T @ c.T + c @ c) / 2)
        eigenvalues, vectors = np.linalg.eigh(hamiltonian)
        thermal_fock = (vectors * np.exp(-step * eigenvalues)) @ vectors.T
        g = np.eye(cutoff**2, dtype=complex)
        for phase in phases:
            g = (g @ thermal_fock) * np.exp(1j * phase * difference)[None, :]
        trace = np.trace(g)
        assert abs(trace.imag) < 1e-12 and trace.real > 0
        errors.append(abs(trace.real - exact))
    assert errors[-1] < 2e-9
    assert errors[-1] < errors[0] / 1000
    print(f"RP noncommuting two-mode trace: {exact:.12f}; Fock errors {errors}")


if __name__ == "__main__":
    check_plus_example()
    check_minus_example()
    check_general_matrices()
    check_rp_basis()
    check_thermal_paths()
    check_rp_fock()
    print("All checks passed.")
