#!/usr/bin/env python3
"""Search reproducible sign/phase-problem witnesses outside protected subgroups.

For every relation-class row labelled ``proper A_group subspace``, this script
samples short ordered products from the complete maximal-subgroup Lie algebra,
first in the displayed representation and then, if needed, after appending a
two-dimensional spectator.  Fermionic weights are evaluated in the finite Fock space,
which retains the sign lost by the Nambu determinant square.  Bosonic square
root branches are followed by analytic continuation from a stable positive
reference configuration, with a small complex detour around determinant zeros.

The search is numerical evidence, not a proof that the displayed witness is
minimal or that no larger sign-free subgroup exists.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from enumerate_time_reversal_subgroups import (
    canonical_matrices,
    five_relations,
    generator_is_invariant,
    group_basis,
    pauli_matrix,
    pauli_words,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PACKAGE_ROOT / "reference" / "time_reversal_subgroups.csv"
DEFAULT_OUTPUT = PACKAGE_ROOT / "build" / "sign_problem_witnesses.csv"
DEFAULT_SEED = 20260809
TOLERANCE = 1.0e-9


def fermion_annihilation_operators(number_of_modes: int) -> list[np.ndarray]:
    identity = np.eye(2, dtype=complex)
    lowering = np.array([[0, 1], [0, 0]], dtype=complex)
    parity = np.diag([1, -1]).astype(complex)
    operators: list[np.ndarray] = []
    for mode in range(number_of_modes):
        factors = [parity] * mode + [lowering] + [identity] * (
            number_of_modes - mode - 1
        )
        operator = np.ones((1, 1), dtype=complex)
        for factor in factors:
            operator = np.kron(operator, factor)
        operators.append(operator)
    return operators


def fock_generator(
    generator: np.ndarray,
    canonical: np.ndarray,
    annihilation: list[np.ndarray],
) -> np.ndarray:
    chi = annihilation + [operator.conj().T for operator in annihilation]
    coefficient = canonical @ generator
    result = np.zeros_like(annihilation[0])
    for row, left in enumerate(chi):
        for column, right in enumerate(chi):
            result += 0.5 * coefficient[row, column] * (left @ right)
    return result


def fermion_ordered_products(
    slices: list[np.ndarray],
    canonical: np.ndarray,
) -> tuple[np.ndarray, complex]:
    one_body = np.eye(slices[0].shape[0], dtype=complex)
    for generator in slices:
        one_body = one_body @ expm(generator)

    number_of_modes = slices[0].shape[0] // 2
    annihilation = fermion_annihilation_operators(number_of_modes)
    fock = np.eye(2**number_of_modes, dtype=complex)
    for generator in slices:
        lifted_generator = fock_generator(
            generator, canonical, annihilation
        )
        fock = fock @ expm(lifted_generator)
    return one_body, complex(np.trace(fock))


def classify_fermion_witness(
    one_body: np.ndarray,
    fock_weight: complex,
) -> tuple[str | None, complex, float]:
    identity = np.eye(one_body.shape[0], dtype=complex)
    determinant = complex(np.linalg.det(identity + one_body))
    square_residual = abs(fock_weight * fock_weight - determinant) / max(
        1.0, abs(determinant)
    )
    if square_residual >= 1.0e-7:
        return None, determinant, square_residual
    if abs(fock_weight.imag) >= TOLERANCE:
        return "complex_weight", determinant, square_residual
    if fock_weight.real < -TOLERANCE:
        return "negative_weight", determinant, square_residual
    return None, determinant, square_residual


def read_proper_rows(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    proper = [
        row
        for row in rows
        if row["time_reversal_result"] == "proper A_group subspace"
    ]
    if len(proper) != 40:
        raise AssertionError(f"expected 40 proper-subgroup rows, found {len(proper)}")
    return proper


def continued_boson_weight(
    target_slices: list[np.ndarray],
    stable_generator: np.ndarray,
    steps: int,
    detour: float,
) -> tuple[complex, complex, int, float]:
    number_of_modes = target_slices[0].shape[0] // 2
    identity = np.eye(target_slices[0].shape[0], dtype=complex)
    start_slices = [
        stable_generator,
        *[np.zeros_like(stable_generator) for _ in target_slices[1:]],
    ]
    phases: list[float] = []
    magnitudes: list[float] = []
    minimum_magnitude = np.inf
    endpoint_radicand = 0.0j
    for path_parameter in np.linspace(0.0, 1.0, steps):
        interpolation = path_parameter + 1j * detour * np.sin(
            np.pi * path_parameter
        )
        slices = [
            (1.0 - interpolation) * start + interpolation * target
            for start, target in zip(start_slices, target_slices)
        ]
        one_body = identity.copy()
        for generator in slices:
            one_body = one_body @ expm(generator)
        radicand = complex(
            ((-1) ** number_of_modes) * np.linalg.det(identity - one_body)
        )
        magnitude = abs(radicand)
        if magnitude < 1.0e-12:
            raise FloatingPointError("continuation path approaches a bosonic pole")
        phases.append(float(np.angle(radicand)))
        magnitudes.append(magnitude)
        minimum_magnitude = min(minimum_magnitude, magnitude)
        endpoint_radicand = radicand

    if abs(phases[0]) >= TOLERANCE:
        raise AssertionError("bosonic continuation did not start on the positive branch")

    unwrapped_phase = float(np.unwrap(np.asarray(phases))[-1])
    weight = complex(
        np.exp(-0.5 * (np.log(magnitudes[-1]) + 1j * unwrapped_phase))
    )
    winding = int(np.rint((unwrapped_phase - phases[-1]) / (2.0 * np.pi)))
    return weight, endpoint_radicand, winding, minimum_magnitude


def sample_boson_witness(
    row: dict[str, str],
    basis_names: list[str],
    basis_matrices: list[np.ndarray],
    canonical: np.ndarray,
    protected_names: set[str],
    random: np.random.Generator,
    class_seed: int,
    attempts: int,
) -> dict[str, object]:
    stable_name = "Z" + "I" * (int(row["number_of_pauli_factors"]) - 1)
    if stable_name not in basis_names:
        raise AssertionError(f"no stable number direction in boson {row['class_number']}")
    stable_index = basis_names.index(stable_name)

    active_indices = [
        index for index in range(len(basis_matrices)) if index != stable_index
    ]
    unprotected_active = [
        index
        for index in active_indices
        if basis_names[index] not in protected_names
    ]
    if not unprotected_active:
        raise RuntimeError(f"boson {row['class_number']} has no unprotected direction")

    damping = 3.0
    stable_generator = -damping * basis_matrices[stable_index]
    slice_counts = (1, 2, 3, 4)
    scales = (0.5, 1.0, 2.0, 3.0, 4.0)

    for attempt in range(1, attempts + 1):
        random_slice_count = slice_counts[(attempt - 1) % len(slice_counts)]
        scale = scales[((attempt - 1) // len(slice_counts)) % len(scales)]
        coefficients = np.zeros((random_slice_count, len(basis_matrices)), dtype=float)
        coefficients[:, :] = random.normal(
            scale=scale,
            size=(random_slice_count, len(basis_matrices)),
        )
        if np.linalg.norm(coefficients[:, unprotected_active]) < 1.0e-6:
            continue
        slices = [
            sum(
                (coefficient * matrix for coefficient, matrix in zip(values, basis_matrices)),
                start=np.zeros_like(basis_matrices[0]),
            )
            for values in coefficients
        ]
        try:
            weight, radicand, winding, minimum_magnitude = continued_boson_weight(
                slices, stable_generator, steps=129, detour=0.1
            )
        except FloatingPointError:
            continue
        if abs(weight.imag) >= 1.0e-7 or weight.real >= -1.0e-7:
            continue
        try:
            verified_weight, verified_radicand, verified_winding, verified_minimum = (
                continued_boson_weight(
                    slices, stable_generator, steps=513, detour=0.05
                )
            )
            opposite_weight, _, opposite_winding, opposite_minimum = (
                continued_boson_weight(
                    slices, stable_generator, steps=513, detour=-0.05
                )
            )
        except FloatingPointError:
            continue
        continuation_residual = abs(verified_weight - weight) / max(
            1.0, abs(verified_weight)
        )
        identity_residual = abs(
            1.0 / (verified_weight * verified_weight) - verified_radicand
        ) / max(1.0, abs(verified_radicand))
        if (
            abs(verified_weight.imag) >= 1.0e-7
            or verified_weight.real >= -1.0e-7
            or verified_winding != winding
            or abs(opposite_winding) != abs(verified_winding)
            or abs(opposite_weight - verified_weight.conjugate()) >= 1.0e-7
            or continuation_residual >= 1.0e-7
            or identity_residual >= 1.0e-9
        ):
            continue

        return {
            "statistics": "boson",
            "class_number": row["class_number"],
            "class_id": row["class_id"],
            "J1_word": row["J1_word"],
            "J2_word": row["J2_word"],
            "A_group_basis": ";".join(basis_names),
            "protected_basis": row["time_reversal_subspace_basis"],
            "seed": class_seed,
            "attempt": attempt,
            "slice_count": len(slices),
            "coefficient_scale": scale,
            "coefficients": json.dumps(coefficients.tolist(), separators=(",", ":")),
            "witness_type": "negative_weight",
            "weight_real": f"{verified_weight.real:.12g}",
            "weight_imag": f"{verified_weight.imag:.12g}",
            "determinant_or_radicand_real": f"{verified_radicand.real:.12g}",
            "determinant_or_radicand_imag": f"{verified_radicand.imag:.12g}",
            "identity_residual": f"{identity_residual:.3e}",
            "cutoff_check": "",
            "continuation_winding": verified_winding,
            "continuation_minimum": (
                f"{min(minimum_magnitude, verified_minimum, opposite_minimum):.3e}"
            ),
            "representation": row.get("witness_representation", "displayed"),
        }

    raise RuntimeError(
        f"no converged boson witness found for {row['class_number']} "
        f"after {attempts} attempts"
    )


def sample_witness(
    row: dict[str, str],
    seed: int,
    attempts: int,
) -> dict[str, object]:
    statistics = row["statistics"]
    number_of_factors = int(row["number_of_pauli_factors"])
    matrices = {
        word: pauli_matrix(word)
        for word in pauli_words(number_of_factors)
    }
    canonical, _ = canonical_matrices(statistics, number_of_factors)
    basis = group_basis(
        canonical,
        matrices[row["J1_word"]],
        matrices[row["J2_word"]],
        matrices,
    )
    expected_signs = tuple(
        int(row[field]) for field in ("s1", "q1", "s2", "q2", "r")
    )
    if five_relations(
        canonical, matrices[row["J1_word"]], matrices[row["J2_word"]]
    ) != expected_signs:
        raise AssertionError(f"five-relation mismatch in {statistics} {row['class_number']}")
    basis_names = [name for name, _ in basis]
    basis_matrices = [matrix for _, matrix in basis]
    if len(basis) != int(row["A_group_dimension"]):
        raise AssertionError(f"A_group dimension mismatch in {statistics} {row['class_number']}")

    protected_names = set(row["time_reversal_subspace_basis"].split(";"))
    unprotected_indices = [
        index for index, name in enumerate(basis_names) if name not in protected_names
    ]
    if not unprotected_indices:
        raise AssertionError("proper subgroup has no complementary direction")

    class_seed = seed + (0 if statistics == "boson" else 1000) + int(
        row["class_number"]
    )
    random = np.random.default_rng(class_seed)
    if statistics == "boson":
        return sample_boson_witness(
            row,
            basis_names,
            basis_matrices,
            canonical,
            protected_names,
            random,
            class_seed,
            attempts,
        )

    slice_counts = (2, 3, 4)
    scales = (0.25, 0.5, 1.0, 2.0, 3.0)

    for attempt in range(1, attempts + 1):
        slice_count = slice_counts[(attempt - 1) % len(slice_counts)]
        scale = scales[((attempt - 1) // len(slice_counts)) % len(scales)]
        coefficients = random.normal(
            scale=scale, size=(slice_count, len(basis_matrices))
        )
        if np.linalg.norm(coefficients[:, unprotected_indices]) < 1.0e-6:
            continue
        slices = [
            sum(
                (coefficient * matrix for coefficient, matrix in zip(values, basis_matrices)),
                start=np.zeros_like(basis_matrices[0]),
            )
            for values in coefficients
        ]
        one_body, fock_weight = fermion_ordered_products(slices, canonical)
        issue, determinant_or_radicand, residual = classify_fermion_witness(
            one_body, fock_weight
        )
        if issue is None:
            continue

        return {
            "statistics": statistics,
            "class_number": row["class_number"],
            "class_id": row["class_id"],
            "J1_word": row["J1_word"],
            "J2_word": row["J2_word"],
            "A_group_basis": ";".join(basis_names),
            "protected_basis": row["time_reversal_subspace_basis"],
            "seed": class_seed,
            "attempt": attempt,
            "slice_count": slice_count,
            "coefficient_scale": scale,
            "coefficients": json.dumps(coefficients.tolist(), separators=(",", ":")),
            "witness_type": issue,
            "weight_real": f"{fock_weight.real:.12g}",
            "weight_imag": f"{fock_weight.imag:.12g}",
            "determinant_or_radicand_real": f"{determinant_or_radicand.real:.12g}",
            "determinant_or_radicand_imag": f"{determinant_or_radicand.imag:.12g}",
            "identity_residual": f"{residual:.3e}",
            "cutoff_check": "",
            "continuation_winding": "",
            "continuation_minimum": "",
            "representation": row.get("witness_representation", "displayed"),
        }

    raise RuntimeError(
        f"no witness found for {statistics} {row['class_number']} "
        f"after {attempts} attempts"
    )


def append_identity_factor(name: str) -> str:
    return f"i{name[1:]}I" if name.startswith("i") else f"{name}I"


def spectator_extension(row: dict[str, str]) -> dict[str, str]:
    extended = dict(row)
    number_of_factors = int(row["number_of_pauli_factors"]) + 1
    extended["number_of_pauli_factors"] = str(number_of_factors)
    extended["nambu_dimension"] = str(2**number_of_factors)
    extended["J1_word"] = append_identity_factor(row["J1_word"])
    extended["J2_word"] = append_identity_factor(row["J2_word"])
    extended["witness_representation"] = "two-dimensional spectator extension"

    matrices = {
        word: pauli_matrix(word)
        for word in pauli_words(number_of_factors)
    }
    canonical, _ = canonical_matrices(row["statistics"], number_of_factors)
    basis = group_basis(
        canonical,
        matrices[extended["J1_word"]],
        matrices[extended["J2_word"]],
        matrices,
    )
    extra_name = append_identity_factor(row["extra_U"])
    extra = (
        1j * matrices[extra_name[1:]]
        if extra_name.startswith("i")
        else matrices[extra_name]
    )
    protected = [
        name for name, generator in basis if generator_is_invariant(generator, extra)
    ]
    if not 0 < len(protected) < len(basis):
        raise AssertionError("spectator extension did not preserve a proper subgroup")
    extended["A_group_dimension"] = str(len(basis))
    extended["time_reversal_subspace_dimension"] = str(len(protected))
    extended["time_reversal_subspace_basis"] = ";".join(protected)
    return extended


def write_csv(records: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(records[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)


def validate_records(records: list[dict[str, object]]) -> None:
    if len(records) != 40:
        raise AssertionError(f"expected 40 witnesses, found {len(records)}")
    keys = {(record["statistics"], int(record["class_number"])) for record in records}
    if len(keys) != len(records):
        raise AssertionError("duplicate proper-subgroup witness")
    for record in records:
        if float(record["weight_real"]) >= -TOLERANCE:
            raise AssertionError("reported witness is not negative")
        if abs(float(record["weight_imag"])) >= 1.0e-7:
            raise AssertionError("reported witness is not real")
        if float(record["identity_residual"]) >= 1.0e-7:
            raise AssertionError("Gaussian trace identity residual is too large")
        if record["statistics"] == "boson":
            if abs(int(record["continuation_winding"])) % 2 != 1:
                raise AssertionError("bosonic witness did not change square-root sign")
            if float(record["continuation_minimum"]) <= 1.0e-12:
                raise AssertionError("bosonic continuation approaches a pole")
    f02 = next(
        record
        for record in records
        if record["statistics"] == "fermion" and int(record["class_number"]) == 2
    )
    if f02["representation"] != "displayed":
        raise AssertionError("F02 witness should use the displayed representation")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--attempts", type=int, default=5000)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    records = []
    for row in read_proper_rows(arguments.input):
        row["witness_representation"] = "displayed"
        try:
            record = sample_witness(
                row, arguments.seed, min(arguments.attempts, 250)
            )
        except RuntimeError:
            record = sample_witness(
                spectator_extension(row), arguments.seed, arguments.attempts
            )
        records.append(record)
    validate_records(records)
    write_csv(records, arguments.output)
    bosonic = sum(record["statistics"] == "boson" for record in records)
    fermionic = len(records) - bosonic
    print(
        f"Found sign/phase-problem witnesses for {len(records)} proper-subgroup "
        f"relation classes ({bosonic} bosonic, {fermionic} fermionic)."
    )
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
