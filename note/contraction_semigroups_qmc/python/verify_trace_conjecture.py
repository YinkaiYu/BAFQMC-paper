#!/usr/bin/env python3
"""Check bosonic counterexamples to TraceConjecture.pdf, Eq. (6).

Uses the package's Nambu/quadrature conventions and matrix exponential. Exact
rational Wick contractions are checked against independently multiplied Fock
matrices with a padded occupation cutoff. No determinant square-root choice,
finite difference, or bosonic analytic continuation enters the trace evaluation.
Run with Python/NumPy in Linux/WSL; outputs are local inspection artifacts.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import platform

import numpy as np

from verify_bosonic_quadrature import expm, word


ROOT = Path(__file__).resolve().parents[1]
F = Fraction
Q_THERMAL = F(1, 9)
VARIANCE = F(5, 8)
BETA = float(np.log(9))


def require_close(a, b, tolerance=2e-11):
    error = float(np.max(np.abs(np.asarray(a) - b)))
    if error > tolerance:
        raise AssertionError((error, tolerance))
    return error


def coefficients(modes, epsilon, order):
    """Coefficients of r_mu^2 in h_x^(s/2) h_p^(s/2), including 1/2."""
    hx = [-F(1, 2)] * modes + [-epsilon / 2] * modes
    hp = [-epsilon / 2] * modes + [-F(1, 2)] * modes
    return [hx] * (order // 2) + [hp] * (order // 2)


def exact_moments(modes, order, variance):
    """Ordered moments of squared coordinates, computed over rational numbers.

    Use (x, i p) internally so every contraction is real rational:
    <xx>=v, <(ip)(ip)>=-v, <x(ip)>=-1/2, <(ip)x>=1/2.
    Each p^2 contributes an additional minus sign on return.
    """
    @lru_cache(None)
    def wick(indices):
        if not indices:
            return F(1)
        i = indices[0]
        result = F(0)
        for k in range(1, len(indices)):
            j = indices[k]
            if i == j:
                contraction = variance if i < modes else -variance
            elif j == i + modes:
                contraction = -F(1, 2)
            elif i == j + modes:
                contraction = F(1, 2)
            else:
                continue
            result += contraction * wick(indices[1:k] + indices[k + 1:])
        return result

    return {
        indices: (-1) ** sum(i >= modes for i in indices)
        * wick(tuple(j for i in indices for j in (i, i)))
        for indices in product(range(2 * modes), repeat=order)
    }


def contract(rows, moments):
    result = 0
    for indices, moment in moments.items():
        coefficient = 1
        for row, i in zip(rows, indices):
            coefficient *= row[i]
        result += coefficient * moment
    return result


def fock_trace(rows, modes, cutoff, q=float(Q_THERMAL)):
    """Direct Fock products, factorizing independent thermal modes only.

    A quadratic insertion changes occupancy by at most two. Padding by 2s
    ensures exact matrix elements for every retained initial state, including
    paths that leave and return to the retained subspace. Only the initial
    thermal sum is truncated. Its missing tail is tested by increasing cutoff.
    """
    order = len(rows)
    dimension = cutoff + 2 * order
    a = np.diag(np.sqrt(np.arange(1, dimension)), 1).astype(complex)
    x = (a + a.conj().T) / np.sqrt(2)
    p = (a - a.conj().T) / (1j * np.sqrt(2))
    squares = (x @ x, p @ p)
    weights = q ** (np.arange(cutoff) + 0.5)
    z1 = float(weights.sum())

    @lru_cache(None)
    def local_trace(sequence):
        operator = np.eye(dimension, dtype=complex)
        for kind in sequence:
            operator = operator @ squares[kind]
        return complex(np.dot(weights, np.diag(operator)[:cutoff]))

    result = 0j
    for indices in product(range(2 * modes), repeat=order):
        coefficient = np.prod([float(row[i]) for row, i in zip(rows, indices)])
        moment = 1 + 0j
        for mode in range(modes):
            sequence = tuple(i // modes for i in indices if i % modes == mode)
            moment *= local_trace(sequence)
        result += coefficient * moment
    require_close(result.imag, 0)
    return result.real, result.real / z1**modes, z1**modes


def check_cone(modes, epsilon):
    """Check each condition in the actual B05/B13 table representatives."""
    label, j1_word, j2_word = (
        ("B05", "I", "X") if modes == 1 else ("B13", "IY", "XI")
    )
    with (ROOT / "reference/semigroup_classes.csv").open(newline="") as handle:
        entries = [r for r in csv.DictReader(handle) if r["statistics"] == "boson"]
    entry = entries[int(label[1:]) - 1]
    assert (entry["J1_word"], entry["J2_word"], entry["status"]) == (
        j1_word, j2_word, "strict"
    )
    j1, j2 = word(j1_word), word(j2_word)
    eye, zero = np.eye(modes), np.zeros((modes, modes))
    omega = np.block([[zero, eye], [-eye, zero]])
    canonical = -omega
    q = np.block([[eye, eye], [-1j * eye, 1j * eye]]) / np.sqrt(2)
    qinv = q.conj().T
    eta = j2 @ canonical
    r1 = q.conj() @ j1 @ q.conj().T
    maximum_error = require_close(q @ eta @ q.conj().T, 1j * omega)
    cone_maxima = []
    for row in coefficients(modes, epsilon, 2):
        h = np.diag([2 * float(c) for c in row])
        b = 1j * omega @ h
        a = q.conj().T @ b @ q
        for left, right in (
            (canonical @ a + a.T @ canonical, 0),
            (j1.T @ a @ j1, a.conj()),
            (j2.T @ a @ j2, -a.conj()),
            (eta @ a, a.conj().T @ eta),
            (r1.T @ h.conj() @ r1, h),
            (q.conj().T @ h @ q, eta @ a),
            (qinv.T @ canonical @ a @ qinv, h),
        ):
            maximum_error = max(maximum_error, require_close(left, right))
        eigenvalues = np.linalg.eigvalsh(eta @ a + a.conj().T @ eta)
        maximum = float(eigenvalues[-1])
        assert maximum <= 2e-12
        if epsilon > 0:
            assert maximum < -float(epsilon)
        cone_maxima.append(maximum)

    # g = exp[-beta sum_j(n_j + 1/2)], so A_g = -beta eta in Nambu form.
    m = expm(-BETA * eta)
    contraction = eta - m.conj().T @ eta @ m
    minimum = float(np.linalg.eigvalsh(contraction)[0])
    require_close(minimum, 80 / 81)
    maximum_error = max(maximum_error, require_close(m.T @ canonical @ m, canonical))
    z = float(F(3, 8) ** modes)
    require_close(z ** -2, ((-1) ** modes * np.linalg.det(np.eye(2 * modes) - m)).real)
    return {
        "class": label,
        "J1_word": j1_word,
        "J2_word": j2_word,
        "maximum_equality_residual": maximum_error,
        "insertion_contraction_max_eigenvalues": cone_maxima,
        "g_contraction_min_eigenvalue": minimum,
    }


def scan(seed, samples):
    """A scoped search of strict diagonal cones at the same thermal g.

    Each insertion is -1/2(a X + b P), a,b>0, with X=sum x_j^2 and
    P=sum p_j^2. The two-mode coefficients respect the Kramers exchange.
    This samples a subfamily only; it is not a test of all Gaussian products.
    """
    rng = np.random.default_rng(seed)
    summaries = []
    for modes, order in ((1, 2), (2, 4)):
        moments = {k: float(v) for k, v in exact_moments(modes, order, VARIANCE).items()}
        negative = 0
        minimum = np.inf
        best = None
        for _ in range(samples):
            ab = 10 ** rng.uniform(-2, 0, size=(order, 2))
            rows = [[-a / 2] * modes + [-b / 2] * modes for a, b in ab]
            value = float(contract(rows, moments))
            negative += value < -1e-10
            if value < minimum:
                minimum, best = value, rows
        assert minimum < -1e-10
        # Independent confirmation of the strongest sampled negative value.
        _, fock_value, _ = fock_trace(best, modes, 24)
        require_close(fock_value, minimum)
        summaries.append({
            "modes": modes, "order": order, "samples": samples,
            "negative_count_below_minus_1e-10": int(negative),
            "minimum_normalized_trace": minimum,
            "minimum_coefficients_of_coordinate_squares": best,
            "minimum_fock_check": fock_value,
        })
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/trace_conjecture.json")
    parser.add_argument("--seed", type=int, default=20260909)
    parser.add_argument("--samples", type=int, default=1000)
    args = parser.parse_args()
    if args.samples < 100:
        parser.error("use at least 100 samples for the scoped random scan")
    expected = {
        (1, F(0)): F(-7, 256),
        (1, F(1, 100)): F(-55007, 2560000),
        (2, F(0)): F(-719, 1024),
        (2, F(1, 100)): F(-72052905719, 102400000000),
    }
    cases = []
    for modes, order in ((1, 2), (2, 4)):
        moments = exact_moments(modes, order, VARIANCE)
        # Check the displayed temperature formulas at several rational v.
        for v in (F(1, 2), F(5, 8), F(3, 4), F(1), F(3, 2)):
            boundary = contract(coefficients(modes, F(0), order), exact_moments(modes, order, v))
            formula = (v*v - F(1, 2))/4 if modes == 1 else 4*v**4 - 4*v*v + F(1, 4)
            assert boundary == formula
        for epsilon in (F(0), F(1, 100)):
            rows = coefficients(modes, epsilon, order)
            exact = contract(rows, moments)
            assert exact == expected[modes, epsilon] < 0
            z = F(3, 8) ** modes
            diagnostics = check_cone(modes, epsilon)
            convergence = []
            for cutoff in (4, 8, 12, 16, 24, 32):
                trace, normalized, partition = fock_trace(rows, modes, cutoff)
                convergence.append({
                    "cutoff": cutoff,
                    "trace": trace,
                    "normalized_trace": normalized,
                    "partition": partition,
                    "normalized_absolute_error": abs(normalized - float(exact)),
                })
            for result in convergence[-2:]:
                require_close(result["normalized_trace"], float(exact), 3e-13)
                require_close(result["trace"], float(exact * z), 3e-13)
            case = {
                "modes": modes, "order": order, "epsilon": str(epsilon),
                "normalized_trace_exact": str(exact), "trace_exact": str(exact * z),
                "partition_exact": str(z), "normalized_trace": float(exact),
                "matrix_checks": diagnostics, "fock_convergence": convergence,
            }
            cases.append(case)
            print(f'{diagnostics["class"]} s={order} epsilon={epsilon}: '
                  f'Tr(product g)/Tr(g) = {exact} = {float(exact):.15g}', flush=True)
    scans = scan(args.seed, args.samples)
    for item in scans:
        print(f'Random strict-cone subfamily N={item["modes"]}, s={item["order"]}: '
              f'{item["negative_count_below_minus_1e-10"]}/{args.samples} negative', flush=True)
    result = {
        "schema_version": 1,
        "python": platform.python_version(), "numpy": np.__version__,
        "platform": platform.platform(),
        "thermal_q": str(Q_THERMAL), "beta": "log(9)",
        "seed": args.seed, "cases": cases, "scoped_random_scans": scans,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"All cone, strict-contraction, exact-Wick, and Fock convergence checks passed.\n{args.output}")


if __name__ == "__main__":
    main()
