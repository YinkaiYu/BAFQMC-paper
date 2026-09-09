"""Independent finite-mode checks of the trace-positivity derivations.

Run in Linux/WSL with NumPy. The proofs for arbitrary mode number are in
../TraceConjecturePositiveResults.md. This script writes no output files.
"""

import math

import numpy as np


def close(a, b, tolerance=2e-11):
    error = np.max(np.abs(np.asarray(a) - b))
    assert error < tolerance, error


def expm(a):
    """Small dense matrix exponential by a scaled, convergent Taylor series."""
    size = len(a)
    scale = max(0, math.ceil(math.log2(max(1.0, np.linalg.norm(a, np.inf) * 4))))
    x = a / 2 ** scale
    result = np.eye(size, dtype=complex)
    term = result.copy()
    for k in range(1, 100):
        term = term @ x / k
        result += term
        if np.linalg.norm(term, np.inf) < 1e-17:
            break
    else:
        raise AssertionError("Taylor exponential did not converge")
    for _ in range(scale):
        result = result @ result
    return result


def annihilators(modes):
    dimension = 2 ** modes
    result = []
    for j in range(modes):
        a = np.zeros((dimension, dimension), complex)
        for state in range(dimension):
            if state & (1 << j):
                sign = (-1) ** (state & ((1 << j) - 1)).bit_count()
                a[state ^ (1 << j), state] = sign
        result.append(a)
    for i, ai in enumerate(result):
        for j, aj in enumerate(result):
            close(ai @ aj + aj @ ai, 0)
            close(ai @ aj.conj().T + aj.conj().T @ ai, np.eye(dimension) * (i == j))
    return result


def psd_spanning_set(n):
    """Rank-one positive matrices whose real span is every Hermitian matrix."""
    vectors = list(np.eye(n, dtype=complex))
    for i in range(n):
        for j in range(i + 1, n):
            vectors.extend((np.eye(n)[i] + np.eye(n)[j], np.eye(n)[i] + 1j * np.eye(n)[j]))
    return [np.outer(v, v.conj()) for v in vectors]


def independent_matrices(matrices):
    basis = []
    for matrix in matrices:
        vector = matrix.ravel().astype(complex).copy()
        for _ in range(2):
            for b in basis:
                vector -= np.vdot(b, vector) * b
        norm = np.linalg.norm(vector)
        if norm > 1e-10:
            basis.append(vector / norm)
    shape = matrices[0].shape
    return [b.reshape(shape) for b in basis]


def generated_algebra_dimension(generators):
    generators = independent_matrices(generators)
    dimension = len(generators[0])
    basis = [np.eye(dimension, dtype=complex).ravel() / math.sqrt(dimension)]
    index = 0
    while index < len(basis):
        current = basis[index].reshape(dimension, dimension)
        for generator in generators:
            vector = (generator @ current).ravel().copy()
            for _ in range(2):
                for b in basis:
                    vector -= np.vdot(b, vector) * b
            norm = np.linalg.norm(vector)
            if norm > 1e-10:
                basis.append(vector / norm)
        index += 1
    return len(basis)


def majorana_setup(modes):
    a = annihilators(modes)
    gammas = [x + x.conj().T for x in a] + [-1j * (x - x.conj().T) for x in a]

    def quadratic(matrix):
        return sum(
            matrix[i, j] * gammas[i] @ gammas[j] / 4
            for i in range(2 * modes) for j in range(2 * modes)
        )

    zero = np.zeros((modes, modes), complex)
    eye = np.eye(modes)
    j1 = np.block([[zero, eye], [eye, zero]])
    j2 = np.block([[zero, eye], [-eye, zero]])
    eta = 1j * j2

    def cone(c):
        matrix = np.block([[zero, -1j * c], [1j * c.T, zero]])
        close(matrix.T, -matrix)
        close(j1.T @ matrix @ j1, matrix.conj())
        close(j2.T @ matrix @ j2, -matrix.conj())
        close(eta @ matrix, -np.block([[c.T, zero], [zero, c]]))
        return matrix, quadratic(matrix)

    return cone, quadratic, gammas, eta


def kramers_setup(modes):
    assert modes % 2 == 0
    a = annihilators(modes)
    creation = [x.conj().T for x in a]
    m = modes // 2
    k = np.block([[np.zeros((m, m)), np.eye(m)], [-np.eye(m), np.zeros((m, m))]])
    zero = np.zeros((modes, modes), complex)
    eta = np.block([[zero, k], [-k, zero]])
    canonical = np.block([[zero, np.eye(modes)], [np.eye(modes), zero]])
    j1 = np.block([[k, zero], [zero, k]])
    j2 = np.block([[k, zero], [zero, -k]])

    def quaternion(x):
        return (x + k.T @ x.conj() @ k) / 2

    def cone(r, s):
        matrix = np.block([[zero, -2 * s @ k], [2 * r @ k, zero]])
        operator = sum(
            (r @ k)[i, j] * a[i] @ a[j]
            - (s @ k)[i, j] * creation[i] @ creation[j]
            for i in range(modes) for j in range(modes)
        )
        close(canonical @ matrix + matrix.T @ canonical, 0)
        close(j1.T @ matrix @ j1, matrix.conj())
        close(j2.T @ matrix @ j2, -matrix.conj())
        close(eta @ matrix, -2 * np.block([[r.conj(), zero], [zero, s.conj()]]))
        return matrix, operator

    def group(m):
        matrix = np.block([[2 * m, zero], [zero, -2 * m.T]])
        operator = sum(2 * m[i, j] * creation[i] @ a[j] for i in range(modes) for j in range(modes))
        operator -= np.trace(m) * np.eye(2 ** modes)
        close(eta @ matrix + matrix.conj().T @ eta, 0)
        return matrix, operator

    return cone, group, quaternion, a, eta


def test_fermions():
    rng = np.random.default_rng(20260909)
    checks = 0
    minimum = np.inf
    for modes in (1, 2, 3):
        cone, quadratic, gamma, eta = majorana_setup(modes)
        elements = [cone(c)[1] for c in psd_spanning_set(modes)]
        dimension = generated_algebra_dimension(elements)
        assert dimension == 2 ** (2 * modes - 1)
        if modes > 1:
            u = gamma[0] @ gamma[modes]
            v = gamma[1] @ gamma[modes]
            close(u @ v - v @ u, -2 * gamma[0] @ gamma[1])
        print(f"Majorana class, {modes} modes: cone algebra dimension {dimension}")
        b = rng.normal(size=(modes, modes)) + 1j * rng.normal(size=(modes, modes))
        b = (b - b.T) * 0.11
        group_matrix = np.block([[b, np.zeros_like(b)], [np.zeros_like(b), b.conj()]])
        close(eta @ group_matrix + group_matrix.conj().T @ eta, 0)
        matrix, strict = cone(np.eye(modes) * 0.8)
        propagation = expm(group_matrix) @ expm(matrix)
        weight = expm(quadratic(group_matrix)) @ expm(strict)
        assert np.linalg.eigvalsh(eta - propagation.conj().T @ eta @ propagation)[0] > 0
        for length in (1, 2, 3, 4):
            for _ in range(8):
                product = np.eye(2 ** modes, dtype=complex)
                for _ in range(length):
                    product = product @ elements[rng.integers(len(elements))]
                if np.linalg.norm(product) < 1e-12:
                    continue
                value = np.trace(product @ weight)
                close(value.imag, 0)
                relative = value.real / (np.linalg.norm(product) * np.linalg.norm(weight))
                assert relative > 1e-12, (modes, length, relative)
                minimum = min(minimum, relative)
                checks += 1

    for modes in (2, 4):
        cone, group, quaternion, annihilation, eta = kramers_setup(modes)
        zero = np.zeros((modes, modes), complex)
        coefficients = [quaternion(c) for c in psd_spanning_set(modes)]
        elements = [cone(r, zero)[1] for r in coefficients] + [cone(zero, s)[1] for s in coefficients]
        dimension = generated_algebra_dimension(elements)
        assert dimension == (5 if modes == 2 else 2 ** (2 * modes - 1))
        if modes == 2:
            odd = [i for i in range(4) if i.bit_count() % 2]
            for element in elements:
                close(element[:, odd], 0)
        else:
            ai, aj, ak = annihilation[:3]
            creation_pair = ai.conj().T @ ak.conj().T
            annihilation_pair = ak @ aj
            close(creation_pair @ annihilation_pair - annihilation_pair @ creation_pair, ai.conj().T @ aj)
        print(f"Kramers class, {modes} modes: cone algebra dimension {dimension}")
        m = quaternion((rng.normal(size=(modes, modes)) + 1j * rng.normal(size=(modes, modes))) * 0.08)
        matrix_group, h_group = group(m)
        matrix_strict, h_strict = cone(np.eye(modes) * 0.5, np.eye(modes) * 0.7)
        propagation = expm(matrix_group) @ expm(matrix_strict)
        weight = expm(h_group) @ expm(h_strict)
        assert np.linalg.eigvalsh(eta - propagation.conj().T @ eta @ propagation)[0] > 0
        for length in (1, 2, 3, 4):
            for _ in range(8):
                product = np.eye(2 ** modes, dtype=complex)
                for _ in range(length):
                    product = product @ elements[rng.integers(len(elements))]
                if np.linalg.norm(product) < 1e-12:
                    continue
                value = np.trace(product @ weight)
                close(value.imag, 0)
                relative = value.real / (np.linalg.norm(product) * np.linalg.norm(weight))
                assert relative > 1e-12, (modes, length, relative)
                minimum = min(minimum, relative)
                checks += 1
    print(f"Direct nonzero fermionic insertion products checked: {checks}; minimum normalized sign margin {minimum:.6g}")


def test_bosonic_mehler_kernel():
    # g = D_t exp(-beta K), cosh(t)=2, beta=log(2).
    # Evaluate Tr(g), Tr(K^2 g), and Tr(x^4 g) as Gaussian kernel integrals.
    t = math.acosh(2)
    beta = math.log(2)
    r = math.exp(-t)
    sinh, cosh = math.sinh(beta), math.cosh(beta)
    csch, coth = 1 / sinh, cosh / sinh
    gaussian_coefficient = ((r * r + 1) * coth - 2 * r * csch) / 2
    first_a = (-(r * r + 1) * csch ** 2 + 2 * r * csch * coth) / 2
    second_a = (r * r + 1) * csch ** 2 * coth - r * (csch * coth ** 2 + csch ** 3)
    prefactor = math.exp(-t / 2) / math.sqrt(2 * math.pi * sinh)
    first_log_prefactor = -coth / 2
    second_log_prefactor = csch ** 2 / 2
    nodes, weights = np.polynomial.hermite.hermgauss(32)
    x = nodes / math.sqrt(gaussian_coefficient)
    measure = prefactor / math.sqrt(gaussian_coefficient) * weights
    partition = measure.sum()
    second_derivative = np.dot(measure, (first_log_prefactor - first_a * x ** 2) ** 2 + second_log_prefactor - second_a * x ** 2)
    position_fourth = np.dot(measure, x ** 4)
    close(partition, 1 / math.sqrt(3))
    close(second_derivative, -1 / (12 * math.sqrt(3)))
    assert position_fourth > 0
    close(position_fourth / partition, 3 / (4 * gaussian_coefficient ** 2))
    print(f"Commuting strict-cone bosonic insertions: Tr(K^2 g)={second_derivative:.15g}<0")
    print(f"Common-position insertions at the same non-Hermitian g: Tr(x^4 g)={position_fourth:.15g}>0")


if __name__ == "__main__":
    test_fermions()
    test_bosonic_mehler_kernel()
    print("All positive-result and scope checks passed.")
