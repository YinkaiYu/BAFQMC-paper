#!/usr/bin/env python3
"""Find fermionic representations with an abelian Hermitian maximal group.

This is a representation-specific sufficient test, separate from the
five-relation semigroup and time-reversal classifications.  If the complete
real ``A_group`` basis lifts to mutually commuting Hermitian Fock generators,
then every ordered product has the strictly positive weight

    Tr prod_l exp(h_l) = Tr exp(sum_l h_l) > 0.

The search covers physical real-Pauli representatives with one to three tensor
factors, including nonfaithful realizations with ``J1 == J2``.  It establishes
existence within that searched family, not a classification of arbitrary
orthogonal representations.
"""

from __future__ import annotations

import argparse
import csv
import itertools
from pathlib import Path

import numpy as np

from enumerate_time_reversal_subgroups import (
    canonical_matrices,
    class_id,
    five_relations,
    group_basis,
    pauli_matrix,
    pauli_words,
    physical_time_reversal,
    time_reversal_is_physical,
)
from search_sign_problem_witnesses import (
    fermion_annihilation_operators,
    fock_generator,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSIFICATION = (
    PACKAGE_ROOT / "reference" / "time_reversal_subgroups.csv"
)
DEFAULT_OUTPUT = (
    PACKAGE_ROOT / "build" / "abelian_hermitian_representations.csv"
)
TOLERANCE = 1.0e-9
RANDOM_SAMPLES_PER_CLASS = 1000
RANDOM_SEED = 20260809


def class_number(signs: tuple[int, int, int, int, int]) -> int:
    return 1 + sum(
        (sign == -1) * weight
        for sign, weight in zip(signs, (16, 8, 4, 2, 1))
    )


def is_abelian_hermitian(
    generators: list[np.ndarray], canonical: np.ndarray
) -> tuple[bool, float, float]:
    number_of_modes = canonical.shape[0] // 2
    annihilation = fermion_annihilation_operators(number_of_modes)
    lifted = [
        fock_generator(generator, canonical, annihilation)
        for generator in generators
    ]
    hermiticity_residual = max(
        np.linalg.norm(generator - generator.conj().T)
        for generator in lifted
    )
    commutator_residual = max(
        np.linalg.norm(first @ second - second @ first)
        for first in lifted
        for second in lifted
    )
    return (
        hermiticity_residual < TOLERANCE
        and commutator_residual < TOLERANCE,
        hermiticity_residual,
        commutator_residual,
    )


def invariant_antiunitary_ambient_space(
    generators: list[np.ndarray],
    conjugation: np.ndarray,
    matrices: dict[str, np.ndarray],
) -> tuple[list[str], int, bool]:
    """Solve the real-linear Nambu-adjoint and invariance equations for U.

    Canonicality, ``U.T @ g @ U = g``, is nonlinear and is imposed only on
    physical antiunitaries.  This routine first finds the full ambient linear
    solution space containing every such U.  For Pauli generators the
    constraint map is diagonal in the physical real-Pauli basis; the nullity
    check below verifies that selecting its zero directions loses no linear
    combinations.
    """

    nambu_adjoint_basis: list[tuple[str, np.ndarray]] = []
    for word, matrix in matrices.items():
        for phase, name in ((1, word), (1j, f"i{word}")):
            candidate = phase * matrix
            if (
                np.linalg.norm(
                    conjugation @ candidate.conj() @ conjugation
                    - candidate
                )
                < TOLERANCE
            ):
                nambu_adjoint_basis.append((name, candidate))

    def residual_vector(candidate: np.ndarray) -> np.ndarray:
        residual = np.concatenate(
            [
                (generator.conj() @ candidate - candidate @ generator)
                .reshape(-1)
                for generator in generators
            ]
        )
        return np.concatenate((residual.real, residual.imag))

    constraint = np.column_stack(
        [residual_vector(candidate) for _, candidate in nambu_adjoint_basis]
    )
    rank = int(
        np.count_nonzero(
            np.linalg.svd(constraint, compute_uv=False) > TOLERANCE
        )
    )
    nullity = len(nambu_adjoint_basis) - rank
    invariant = [
        (name, candidate)
        for name, candidate in nambu_adjoint_basis
        if np.linalg.norm(residual_vector(candidate)) < TOLERANCE
    ]
    if len(invariant) != nullity:
        raise AssertionError(
            "Pauli directions do not span the invariant antiunitary space"
        )
    all_symmetric = all(
        np.linalg.norm(candidate.T - candidate) < TOLERANCE
        for _, candidate in invariant
    )
    return [name for name, _ in invariant], nullity, all_symmetric


def three_level_projector(
    generator: np.ndarray, eigenvalue: int
) -> np.ndarray:
    identity = np.eye(generator.shape[0], dtype=complex)
    if eigenvalue == -1:
        return 0.5 * generator @ (generator - identity)
    if eigenvalue == 0:
        return identity - generator @ generator
    if eigenvalue == 1:
        return 0.5 * generator @ (generator + identity)
    raise ValueError(eigenvalue)


def exact_weight_formula(
    generators: list[np.ndarray], canonical: np.ndarray
) -> tuple[str, str]:
    annihilation = fermion_annihilation_operators(canonical.shape[0] // 2)
    lifted = [
        fock_generator(generator, canonical, annihilation)
        for generator in generators
    ]
    if len(lifted) == 1 and lifted[0].shape == (2, 2):
        if not np.allclose(
            np.linalg.eigvalsh(lifted[0]), (-0.5, 0.5), atol=TOLERANCE
        ):
            raise AssertionError("unexpected one-mode Fock spectrum")
        return "2 cosh(alpha/2)", "(-1/2);(1/2)"
    if len(lifted) == 2 and lifted[0].shape == (4, 4):
        expected_single = (-1.0, 0.0, 0.0, 1.0)
        for generator in lifted:
            if not np.allclose(
                np.linalg.eigvalsh(generator),
                expected_single,
                atol=TOLERANCE,
            ):
                raise AssertionError("unexpected two-mode Fock spectrum")
        expected_joint = {
            (-1, 0): 1,
            (0, -1): 1,
            (0, 1): 1,
            (1, 0): 1,
        }
        actual_joint: dict[tuple[int, int], int] = {}
        for first_eigenvalue in (-1, 0, 1):
            first_projector = three_level_projector(
                lifted[0], first_eigenvalue
            )
            for second_eigenvalue in (-1, 0, 1):
                second_projector = three_level_projector(
                    lifted[1], second_eigenvalue
                )
                multiplicity = complex(
                    np.trace(first_projector @ second_projector)
                )
                rounded = int(round(multiplicity.real))
                if abs(multiplicity - rounded) >= TOLERANCE:
                    raise AssertionError("nonintegral joint multiplicity")
                if rounded:
                    actual_joint[
                        (first_eigenvalue, second_eigenvalue)
                    ] = rounded
        if actual_joint != expected_joint:
            raise AssertionError(
                f"unexpected two-mode joint spectrum: {actual_joint}"
            )
        return (
            "2 cosh(alpha) + 2 cosh(beta)",
            "(-1,0);(0,-1);(0,1);(1,0)",
        )
    raise AssertionError("unrecognized abelian-Hermitian Fock algebra")


def random_ordered_product_check(
    generators: list[np.ndarray],
    canonical: np.ndarray,
    formula: str,
    seed: int,
) -> float:
    """Compare direct ordered Fock products with the analytic trace formula."""

    annihilation = fermion_annihilation_operators(canonical.shape[0] // 2)
    lifted = [
        fock_generator(generator, canonical, annihilation)
        for generator in generators
    ]
    random = np.random.default_rng(seed)
    maximum_relative_error = 0.0
    for sample in range(RANDOM_SAMPLES_PER_CLASS):
        slice_count = 1 + sample % 4
        coefficients = random.normal(size=(slice_count, len(lifted)))
        product = np.eye(lifted[0].shape[0], dtype=complex)
        for values in coefficients:
            fock_slice = sum(
                (
                    coefficient * generator
                    for coefficient, generator in zip(values, lifted)
                ),
                start=np.zeros_like(lifted[0]),
            )
            eigenvalues, eigenvectors = np.linalg.eigh(fock_slice)
            exponential = (
                eigenvectors * np.exp(eigenvalues)
            ) @ eigenvectors.conj().T
            product = product @ exponential
        weight = complex(np.trace(product))
        totals = coefficients.sum(axis=0)
        if formula == "2 cosh(alpha/2)":
            expected = 2.0 * np.cosh(totals[0] / 2.0)
        elif formula == "2 cosh(alpha) + 2 cosh(beta)":
            expected = 2.0 * (
                np.cosh(totals[0]) + np.cosh(totals[1])
            )
        else:
            raise ValueError(formula)
        relative_error = abs(weight - expected) / max(1.0, abs(expected))
        maximum_relative_error = max(
            maximum_relative_error, relative_error
        )
        if weight.real <= 0.0 or abs(weight.imag) >= TOLERANCE:
            raise AssertionError("random ordered product is not positive")
    if maximum_relative_error >= 1.0e-12:
        raise AssertionError("random ordered products disagree with formula")
    return maximum_relative_error


def read_scope_rows(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["statistics"] == "fermion"
        ]
    if len(rows) != 32:
        raise AssertionError(f"expected 32 fermionic rows, found {len(rows)}")
    return {int(row["class_number"]): row for row in rows}


def enumerate_candidates(
    scope_rows: dict[int, dict[str, str]],
) -> list[dict[str, object]]:
    candidates: dict[int, list[dict[str, object]]] = {
        number: [] for number in range(1, 33)
    }
    for number_of_factors in (1, 2, 3):
        words = pauli_words(number_of_factors)
        matrices = {word: pauli_matrix(word) for word in words}
        canonical, conjugation = canonical_matrices(
            "fermion", number_of_factors
        )
        for first_word, second_word in itertools.product(words, repeat=2):
            first = matrices[first_word]
            second = matrices[second_word]
            signs = five_relations(canonical, first, second)
            first_u = physical_time_reversal(first, signs[0])
            second_u = physical_time_reversal(second, signs[2])
            if not time_reversal_is_physical(
                first_u, canonical, conjugation
            ) or not time_reversal_is_physical(
                second_u, canonical, conjugation
            ):
                continue
            basis = group_basis(
                canonical, first, second, matrices
            )
            if not basis:
                continue
            qualifies, hermiticity_residual, commutator_residual = (
                is_abelian_hermitian(
                    [generator for _, generator in basis], canonical
                )
            )
            if not qualifies:
                continue
            number = class_number(signs)
            candidates[number].append(
                {
                    "number_of_pauli_factors": number_of_factors,
                    "nambu_dimension": 2**number_of_factors,
                    "J1_word": first_word,
                    "J2_word": second_word,
                    "A_group_dimension": len(basis),
                    "A_group_basis": ";".join(name for name, _ in basis),
                    "hermiticity_residual": hermiticity_residual,
                    "commutator_residual": commutator_residual,
                }
            )

    records: list[dict[str, object]] = []
    for number, representations in candidates.items():
        if not representations:
            continue
        minimum_factors = min(
            int(row["number_of_pauli_factors"])
            for row in representations
        )
        at_minimum = [
            row
            for row in representations
            if int(row["number_of_pauli_factors"]) == minimum_factors
        ]
        scope = scope_rows[number]
        displayed = [
            row
            for row in representations
            if row["J1_word"] == scope["J1_word"]
            and row["J2_word"] == scope["J2_word"]
        ]
        selection = (
            "displayed time-reversal-table representation"
            if displayed
            else "lowest-dimensional representation"
        )
        minimum_representative = min(
            at_minimum,
            key=lambda row: (
                -int(row["A_group_dimension"]),
                str(row["J1_word"]),
                str(row["J2_word"]),
            ),
        )
        representative = min(
            displayed or at_minimum,
            key=lambda row: (
                int(row["number_of_pauli_factors"]),
                -int(row["A_group_dimension"]),
                str(row["J1_word"]),
                str(row["J2_word"]),
            ),
        )
        signs = tuple(
            int(scope[field]) for field in ("s1", "q1", "s2", "q2", "r")
        )
        minimum_matrices = {
            word: pauli_matrix(word)
            for word in pauli_words(minimum_factors)
        }
        minimum_canonical, _ = canonical_matrices(
            "fermion", minimum_factors
        )
        minimum_basis = group_basis(
            minimum_canonical,
            minimum_matrices[str(minimum_representative["J1_word"])],
            minimum_matrices[str(minimum_representative["J2_word"])],
            minimum_matrices,
        )
        minimum_formula, minimum_joint_spectrum = exact_weight_formula(
            [generator for _, generator in minimum_basis],
            minimum_canonical,
        )
        number_of_factors = int(representative["number_of_pauli_factors"])
        matrices = {
            word: pauli_matrix(word)
            for word in pauli_words(number_of_factors)
        }
        canonical, conjugation = canonical_matrices(
            "fermion", number_of_factors
        )
        chosen_basis = group_basis(
            canonical,
            matrices[str(representative["J1_word"])],
            matrices[str(representative["J2_word"])],
            matrices,
        )
        formula, joint_spectrum = exact_weight_formula(
            [generator for _, generator in chosen_basis], canonical
        )
        invariant_names, invariant_dimension, all_symmetric = (
            invariant_antiunitary_ambient_space(
                [generator for _, generator in chosen_basis],
                conjugation,
                matrices,
            )
        )
        if not all_symmetric:
            raise AssertionError(
                "an invariant antiunitary direction is not symmetric"
            )
        random_error = random_ordered_product_check(
            [generator for _, generator in chosen_basis],
            canonical,
            formula,
            RANDOM_SEED + number,
        )
        records.append(
            {
                "class_number": f"F{number:02d}",
                "class_id": class_id(signs),
                "semigroup_status": scope["semigroup_status"],
                "time_reversal_table_scope": scope["time_reversal_result"],
                "outside_current_whole_group_TR_criterion": int(
                    scope["time_reversal_result"]
                    == "proper A_group subspace"
                ),
                "matches_displayed_J_pair": int(
                    representative["J1_word"] == scope["J1_word"]
                    and representative["J2_word"] == scope["J2_word"]
                ),
                "reported_representation_selection": selection,
                "minimum_number_of_pauli_factors": minimum_factors,
                "minimum_nambu_dimension": 2**minimum_factors,
                "minimum_J1_word": minimum_representative["J1_word"],
                "minimum_J2_word": minimum_representative["J2_word"],
                "minimum_A_group_basis": ";".join(
                    name for name, _ in minimum_basis
                ),
                "minimum_fock_joint_spectrum": minimum_joint_spectrum,
                "minimum_exact_weight_formula": minimum_formula,
                **representative,
                "fock_joint_spectrum": joint_spectrum,
                "exact_weight_formula": formula,
                "ambient_invariant_U_real_dimension": invariant_dimension,
                "ambient_invariant_U_basis": ";".join(invariant_names),
                "all_ambient_invariant_U_symmetric": int(all_symmetric),
                "random_seed": RANDOM_SEED + number,
                "random_samples": RANDOM_SAMPLES_PER_CLASS,
                "maximum_random_weight_relative_error": random_error,
                "qualifying_representations_at_minimum_dimension": len(
                    at_minimum
                ),
                "qualifying_representations_through_three_factors": len(
                    representations
                ),
            }
        )
    return records


def validate_records(records: list[dict[str, object]]) -> None:
    if not records:
        raise AssertionError("no abelian-Hermitian representations found")
    if len({row["class_number"] for row in records}) != len(records):
        raise AssertionError("duplicate relation class")
    expected_classes = {"F01", "F05", "F06", "F17", "F18", "F21"}
    actual_classes = {str(row["class_number"]) for row in records}
    if actual_classes != expected_classes:
        raise AssertionError(
            f"unexpected abelian-Hermitian classes: {sorted(actual_classes)}"
        )
    for row in records:
        if float(row["hermiticity_residual"]) >= TOLERANCE:
            raise AssertionError("non-Hermitian Fock generator was retained")
        if float(row["commutator_residual"]) >= TOLERANCE:
            raise AssertionError("noncommuting Fock generators were retained")


def write_csv(records: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(records[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--classification", type=Path, default=DEFAULT_CLASSIFICATION
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    records = enumerate_candidates(
        read_scope_rows(arguments.classification)
    )
    validate_records(records)
    write_csv(records, arguments.output)
    new_cases = [
        str(row["class_number"])
        for row in records
        if row["outside_current_whole_group_TR_criterion"] == 1
    ]
    print(
        f"Found abelian-Hermitian maximal-group representations in "
        f"{len(records)} fermionic relation classes."
    )
    print(
        "Outside the current whole-group M/K entries: "
        + (", ".join(new_cases) if new_cases else "none")
    )
    print(f"Wrote {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
