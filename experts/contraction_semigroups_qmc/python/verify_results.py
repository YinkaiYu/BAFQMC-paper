#!/usr/bin/env python3
"""Cross-check the two enumeration pipelines and the formulas in the note."""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]
DEFAULT_RESULTS = PACKAGE_ROOT / "build"
DEFAULT_REFERENCE = PACKAGE_ROOT / "reference"

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, 1], [-1, 0]], dtype=complex)  # i sigma_y
Z = np.diag([1, -1]).astype(complex)
REAL_PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}

SEMIGROUP_FILE = "semigroup_classes.csv"
GENERATOR_FILE = "generator_spaces.csv"
TIME_REVERSAL_FILE = "time_reversal_subgroups.csv"
MODEL_FILE = "model_slice_checks.csv"
WITNESS_FILE = "sign_problem_witnesses.csv"
PAULI_SCAN_FILE = "pauli_realization_scan.csv"
MAX_PAULI_FACTORS = 3


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def split_terms(value: str) -> list[str]:
    return value.split(";") if value else []


def matrix_sign(left: np.ndarray, right: np.ndarray) -> int:
    if np.array_equal(left, right):
        return 1
    if np.array_equal(left, -right):
        return -1
    raise AssertionError("matrices are not related by a sign")


def pauli_matrix(word: str) -> np.ndarray:
    if not word or len(word) > MAX_PAULI_FACTORS:
        raise AssertionError(
            f"Pauli word must contain one to {MAX_PAULI_FACTORS} factors: {word!r}"
        )
    matrix = np.ones((1, 1), dtype=complex)
    for letter in word:
        matrix = np.kron(matrix, REAL_PAULI[letter])
    return matrix


def named_matrix(name: str) -> np.ndarray:
    return 1j * pauli_matrix(name[1:]) if name.startswith("i") else pauli_matrix(name)


def pauli_words(number_of_factors: int) -> list[str]:
    return [
        "".join(letters)
        for letters in itertools.product("IXYZ", repeat=number_of_factors)
    ]


def canonical_matrices(
    statistics: str, number_of_factors: int
) -> tuple[np.ndarray, np.ndarray]:
    internal = np.eye(2 ** (number_of_factors - 1), dtype=complex)
    g = np.kron(-Y if statistics == "boson" else X, internal)
    conjugation = np.kron(X, internal)
    return g, conjugation


def signs_from_row(row: dict[str, str]) -> tuple[int, int, int, int, int]:
    return tuple(int(row[name]) for name in ("s1", "q1", "s2", "q2", "r"))


def class_number(signs: tuple[int, int, int, int, int]) -> int:
    return 1 + sum(
        (sign == -1) * weight
        for sign, weight in zip(signs, (16, 8, 4, 2, 1))
    )


def case_id(statistics: str, signs: tuple[int, int, int, int, int]) -> str:
    return statistics[0].upper() + f"{class_number(signs):02d}"


def class_label(signs: tuple[int, int, int, int, int]) -> str:
    names = ("s1", "q1", "s2", "q2", "r")
    return "_".join(
        name + ("+" if sign == 1 else "-")
        for name, sign in zip(names, signs)
    )


def verify_five_relations(
    g: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    signs: tuple[int, int, int, int, int],
) -> None:
    identity = np.eye(g.shape[0], dtype=complex)
    actual = (
        matrix_sign(first.T @ g @ first, g),
        matrix_sign(first @ first, identity),
        matrix_sign(second.T @ g @ second, g),
        matrix_sign(second @ second, identity),
        matrix_sign(first @ second, second @ first),
    )
    if actual != signs:
        raise AssertionError(f"five-relation mismatch: {actual} != {signs}")


def minimal_pauli_witnesses(
    statistics: str,
) -> dict[tuple[int, int, int, int, int], tuple[int, str, str]]:
    witnesses: dict[
        tuple[int, int, int, int, int], tuple[int, str, str]
    ] = {}
    for number_of_factors in (1, 2, 3):
        words = pauli_words(number_of_factors)
        matrices = {word: pauli_matrix(word) for word in words}
        g, _ = canonical_matrices(statistics, number_of_factors)
        identity = np.eye(g.shape[0], dtype=complex)
        individual = {
            word: (
                matrix_sign(matrix.T @ g @ matrix, g),
                matrix_sign(matrix @ matrix, identity),
            )
            for word, matrix in matrices.items()
        }
        for first_word in words:
            first = matrices[first_word]
            for second_word in words:
                if first_word == second_word:
                    continue
                second = matrices[second_word]
                signs = (
                    individual[first_word][0],
                    individual[first_word][1],
                    individual[second_word][0],
                    individual[second_word][1],
                    matrix_sign(first @ second, second @ first),
                )
                witnesses.setdefault(
                    signs, (number_of_factors, first_word, second_word)
                )
    if len(witnesses) != 32:
        raise AssertionError(
            f"exact Pauli search found {len(witnesses)} classes for {statistics}"
        )
    return witnesses


def strict_contraction(
    statistics: str, signs: tuple[int, int, int, int, int]
) -> bool:
    statistics_sign = -1 if statistics == "boson" else 1
    return signs[3] == -statistics_sign and signs[4] == -signs[0] * signs[2]


def contraction_metric(
    statistics: str,
    g: np.ndarray,
    second: np.ndarray,
    signs: tuple[int, int, int, int, int],
) -> tuple[str, np.ndarray]:
    statistics_sign = -1 if statistics == "boson" else 1
    if statistics_sign * signs[3] * signs[2] == 1:
        return "J2g", second @ g
    return "iJ2g", 1j * second @ g


def verify_semigroup_rows(rows: list[dict[str, str]]) -> None:
    if len(rows) != 64:
        raise AssertionError(f"expected 64 semigroup rows, found {len(rows)}")
    keys: set[tuple[str, tuple[int, ...]]] = set()
    minimal = {
        statistics: minimal_pauli_witnesses(statistics)
        for statistics in ("boson", "fermion")
    }
    for row in rows:
        statistics = row["statistics"]
        if statistics not in minimal:
            raise AssertionError(f"unknown statistics {statistics!r}")
        signs = signs_from_row(row)
        key = (statistics, signs)
        if key in keys:
            raise AssertionError(f"duplicate semigroup class {key}")
        keys.add(key)
        number_of_factors = int(row["min_qubits"])
        if row["class_id"] != class_label(signs):
            raise AssertionError(f"incorrect class label in {key}")
        if (
            number_of_factors,
            row["J1_word"],
            row["J2_word"],
        ) != minimal[statistics][signs]:
            raise AssertionError(f"incorrect minimal Pauli witness in {key}")
        first = pauli_matrix(row["J1_word"])
        second = pauli_matrix(row["J2_word"])
        g, _ = canonical_matrices(statistics, number_of_factors)
        verify_five_relations(g, first, second, signs)

        expected_strict = strict_contraction(statistics, signs)
        if int(row["strict_interior"]) != expected_strict:
            raise AssertionError(f"incorrect cone classification in {key}")
        metric_name, eta = contraction_metric(statistics, g, second, signs)
        if row["metric"] != metric_name:
            raise AssertionError(f"incorrect metric in {key}")
        if not np.array_equal(eta.conj().T, eta):
            raise AssertionError(f"non-Hermitian metric in {key}")
        if not np.array_equal(eta @ eta, np.eye(eta.shape[0])):
            raise AssertionError(f"metric does not square to I in {key}")

        statistics_sign = -1 if statistics == "boson" else 1
        delta = statistics_sign * signs[3] * signs[2]
        kappa = delta * signs[4] * signs[0]
        if int(row["tau"]) != statistics_sign:
            raise AssertionError(f"incorrect statistics sign in {key}")
        if int(row["delta"]) != delta or int(row["kappa"]) != kappa:
            raise AssertionError(f"incorrect derived signs in {key}")
        expected_status = (
            "strict"
            if expected_strict
            else "boundary_only_trace_obstruction"
            if signs[3] != -statistics_sign
            else "boundary_only_reality_flip"
        )
        if row["status"] != expected_status:
            raise AssertionError(f"incorrect semigroup status in {key}")
        for field in (
            "metric_hermiticity_residual",
            "metric_square_residual",
            "max_pauli_relation_residual",
        ):
            if abs(float(row[field])) >= 1.0e-12:
                raise AssertionError(f"nonzero {field} in {key}")

        if expected_strict:
            cone = -eta
            if not np.array_equal(g @ cone + cone.T @ g, np.zeros_like(g)):
                raise AssertionError(f"-eta violates the canonical equation in {key}")
            if not np.array_equal(first.T @ cone @ first, cone.conj()):
                raise AssertionError(f"-eta violates the J1 equation in {key}")
            if not np.array_equal(second.T @ cone @ second, -cone.conj()):
                raise AssertionError(f"-eta violates the J2 equation in {key}")
            if not np.array_equal(
                eta @ cone + cone.conj().T @ eta,
                -2 * np.eye(eta.shape[0]),
            ):
                raise AssertionError(f"-eta is not a strict cone point in {key}")
            for field in (
                "witness_lie_residual",
                "witness_reality_residual",
                "witness_J2_residual",
                "witness_contraction_residual",
            ):
                if abs(float(row[field])) >= 1.0e-12:
                    raise AssertionError(f"nonzero {field} in {key}")
        else:
            for field in (
                "witness_lie_residual",
                "witness_reality_residual",
                "witness_J2_residual",
                "witness_contraction_residual",
            ):
                if not math.isnan(float(row[field])):
                    raise AssertionError(f"unexpected cone witness in {key}")

    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        strict = [row for row in selected if row["strict_interior"] == "1"]
        if len(selected) != 32 or len(strict) != 8:
            raise AssertionError(f"incorrect 32=8+24 count for {statistics}")
        if Counter(row["metric"] for row in strict) != Counter(
            {"J2g": 4, "iJ2g": 4}
        ):
            raise AssertionError(f"incorrect metric count for {statistics}")


def coefficient_type(
    g: np.ndarray, first: np.ndarray, pauli: np.ndarray
) -> str:
    transpose_sign = matrix_sign(pauli.T @ g, g @ pauli)
    reality_sign = matrix_sign(first.T @ pauli @ first, pauli)
    return (
        ("i" if reality_sign == -1 else "")
        + "R_"
        + ("A" if transpose_sign == 1 else "S")
    )


def derived_generator_terms(row: dict[str, str]) -> tuple[list[str], list[str]]:
    statistics = row["statistics"]
    number_of_factors = int(row["n"])
    first = pauli_matrix(row["J1_word"])
    second = pauli_matrix(row["J2_word"])
    g, _ = canonical_matrices(statistics, number_of_factors)
    group: list[str] = []
    cone: list[str] = []
    for word in pauli_words(number_of_factors):
        pauli = pauli_matrix(word)
        first_sign = matrix_sign(first.T @ pauli @ first, pauli)
        second_sign = matrix_sign(second.T @ pauli @ second, pauli)
        term = f"{word}:{coefficient_type(g, first, pauli)}"
        (group if first_sign == second_sign else cone).append(term)
    return group, cone


def dimension_formula(terms: list[str]) -> str:
    symmetric = sum(term.endswith("_S") for term in terms)
    antisymmetric = len(terms) - symmetric
    pieces = []
    if symmetric:
        pieces.append(f"{symmetric}*m*(m+1)/2")
    if antisymmetric:
        pieces.append(f"{antisymmetric}*m*(m-1)/2")
    return "+".join(pieces) if pieces else "0"


def verify_generator_rows(
    rows: list[dict[str, str]], semigroup_rows: list[dict[str, str]]
) -> None:
    if len(rows) != 64:
        raise AssertionError(f"expected 64 generator rows, found {len(rows)}")
    classes = {
        (row["statistics"], row["class_id"]): row for row in semigroup_rows
    }
    for row in rows:
        key = (row["statistics"], row["class_id"])
        source = classes[key]
        for field, source_field in (
            ("n", "min_qubits"),
            ("J1_word", "J1_word"),
            ("J2_word", "J2_word"),
            ("metric", "metric"),
            ("strict_interior", "strict_interior"),
        ):
            if row[field] != source[source_field]:
                raise AssertionError(f"generator/class mismatch for {key}: {field}")
        for field in ("s1", "q1", "s2", "q2", "r"):
            if row[field] != source[field]:
                raise AssertionError(f"generator/class mismatch for {key}: {field}")

        expected_group, expected_cone = derived_generator_terms(row)
        actual_group = split_terms(row["maximal_terms"])
        actual_cone = split_terms(row["cone_linear_terms"])
        if actual_group != expected_group or actual_cone != expected_cone:
            raise AssertionError(f"incorrect generator basis for {key}")
        words = [term.split(":", 1)[0] for term in actual_group + actual_cone]
        if len(words) != len(set(words)) or set(words) != set(
            pauli_words(int(row["n"]))
        ):
            raise AssertionError(f"generator decomposition is incomplete for {key}")
        if row["maximal_dimension_formula"] != dimension_formula(actual_group):
            raise AssertionError(f"incorrect group dimension for {key}")
        if row["cone_dimension_formula"] != dimension_formula(actual_cone):
            raise AssertionError(f"incorrect cone dimension for {key}")
        if abs(float(row["maximal_residual"])) >= 1.0e-10:
            raise AssertionError(f"nonzero group residual for {key}")
        if abs(float(row["cone_residual"])) >= 1.0e-10:
            raise AssertionError(f"nonzero cone residual for {key}")
        if split_terms(row["maximal_number_conserving_terms"]) != [
            term for term in actual_group if term[0] in "IZ"
        ]:
            raise AssertionError(f"incorrect number-conserving group terms for {key}")
        if split_terms(row["cone_number_conserving_terms"]) != [
            term for term in actual_cone if term[0] in "IZ"
        ]:
            raise AssertionError(f"incorrect number-conserving cone terms for {key}")


def group_basis(
    statistics: str, first_word: str, second_word: str
) -> dict[str, np.ndarray]:
    number_of_factors = len(first_word)
    first = pauli_matrix(first_word)
    second = pauli_matrix(second_word)
    g, _ = canonical_matrices(statistics, number_of_factors)
    result: dict[str, np.ndarray] = {}
    for word in pauli_words(number_of_factors):
        for name, candidate in ((word, pauli_matrix(word)), (f"i{word}", 1j * pauli_matrix(word))):
            if not np.array_equal(g @ candidate + candidate.T @ g, np.zeros_like(g)):
                continue
            if not np.array_equal(first.T @ candidate @ first, candidate.conj()):
                continue
            if not np.array_equal(second.T @ candidate @ second, candidate.conj()):
                continue
            result[name] = candidate
    return result


def verify_time_reversal_rows(rows: list[dict[str, str]]) -> None:
    if len(rows) != 64:
        raise AssertionError(f"expected 64 time-reversal rows, found {len(rows)}")
    for row in rows:
        statistics = row["statistics"]
        signs = signs_from_row(row)
        if int(row["class_number"]) != class_number(signs):
            raise AssertionError(f"incorrect case number in {row['class_id']}")
        number_of_factors = int(row["number_of_pauli_factors"])
        first = pauli_matrix(row["J1_word"])
        second = pauli_matrix(row["J2_word"])
        g, conjugation = canonical_matrices(statistics, number_of_factors)
        verify_five_relations(g, first, second, signs)
        basis = group_basis(statistics, row["J1_word"], row["J2_word"])
        if len(basis) != int(row["A_group_dimension"]):
            raise AssertionError(f"incorrect A_group dimension in {row['class_id']}")
        selected_names = row["time_reversal_subspace_basis"].split(";")
        if len(selected_names) != int(row["time_reversal_subspace_dimension"]):
            raise AssertionError(f"incorrect selected dimension in {row['class_id']}")
        if not set(selected_names) <= set(basis):
            raise AssertionError(f"selected basis is outside A_group in {row['class_id']}")

        for field in ("induced_U1", "induced_U2"):
            linear_part = named_matrix(row[field])
            if not np.array_equal(linear_part.T @ g @ linear_part, g):
                raise AssertionError(f"noncanonical time reversal in {row['class_id']}")
            if not np.array_equal(
                conjugation @ linear_part.conj() @ conjugation, linear_part
            ):
                raise AssertionError(f"unphysical Nambu action in {row['class_id']}")

        if row["extra_U"]:
            extra = named_matrix(row["extra_U"])
            selected = {
                name
                for name, generator in basis.items()
                if np.array_equal(
                    np.linalg.solve(extra, generator.conj() @ extra), generator
                )
            }
            if selected != set(selected_names):
                raise AssertionError(f"incorrect proper subgroup in {row['class_id']}")
        elif set(selected_names) != set(basis):
            raise AssertionError(f"whole-group row omits generators in {row['class_id']}")


def cross_check_classifications(
    semigroup_rows: list[dict[str, str]], time_reversal_rows: list[dict[str, str]]
) -> None:
    first = {
        (row["statistics"], signs_from_row(row)): row for row in semigroup_rows
    }
    second = {
        (row["statistics"], signs_from_row(row)): row for row in time_reversal_rows
    }
    if set(first) != set(second):
        raise AssertionError("Octave and Python enumerate different classes")
    for key in first:
        is_strict = first[key]["strict_interior"] == "1"
        expected_status = "contraction semigroup" if is_strict else "maximal subgroup only"
        if second[key]["semigroup_status"] != expected_status:
            raise AssertionError(f"cross-pipeline status mismatch in {key}")
        expected_metric = first[key]["metric"] if is_strict else ""
        if second[key]["metric"] != expected_metric:
            raise AssertionError(f"cross-pipeline metric mismatch in {key}")


TERM_PATTERN = re.compile(
    r"P(?:&\\in|&=|\\in)(.*?)"
    r"&&\\overline\{K_P\}=(-?)K_P,"
    r"\\quad K_P\^\\trans=(-?)K_P",
    re.S,
)
PAULI_PATTERN = re.compile(r"\\ii\\sigma_y|\\sigma_[xz]|I_2")
LATEX_MATRIX_FACTOR_PATTERN = re.compile(
    r"\\ii\\sigma_y|\\sigma_[xyz]|I_2"
)
PAULI_LETTER = {
    r"\ii\sigma_y": "Y",
    r"\sigma_x": "X",
    r"\sigma_z": "Z",
    "I_2": "I",
}


def parse_tex_terms(segment: str) -> list[str]:
    terms: list[str] = []
    for match in TERM_PATTERN.finditer(segment):
        pauli_text, conjugation_minus, transpose_minus = match.groups()
        kind = (
            ("i" if conjugation_minus else "")
            + "R_"
            + ("A" if transpose_minus else "S")
        )
        for item in pauli_text.split(","):
            factors = PAULI_PATTERN.findall(item)
            if factors:
                terms.append(
                    "".join(PAULI_LETTER[factor] for factor in factors)
                    + ":"
                    + kind
                )
    return terms


def latex_pauli_word(expression: str) -> str:
    factors = PAULI_PATTERN.findall(expression)
    return "".join(PAULI_LETTER[factor] for factor in factors)


def latex_matrix(expression: str, expected_dimension: int) -> np.ndarray:
    factor_matrices = {
        r"\ii\sigma_y": Y,
        r"\sigma_x": X,
        r"\sigma_y": -1j * Y,
        r"\sigma_z": Z,
        "I_2": I2,
    }
    factors = LATEX_MATRIX_FACTOR_PATTERN.findall(expression)
    if not factors:
        raise AssertionError(f"cannot parse matrix expression {expression!r}")
    parsed_dimension = 1 << len(factors)
    if parsed_dimension != expected_dimension:
        raise AssertionError(
            "matrix-expression dimension mismatch: "
            f"parsed {len(factors)} Pauli factors ({parsed_dimension}x{parsed_dimension}), "
            f"expected {expected_dimension}x{expected_dimension}"
        )
    matrix = np.ones((1, 1), dtype=complex)
    for factor in factors:
        matrix = np.kron(matrix, factor_matrices[factor])
    leading = re.sub(r"^[\s(\[]+", "", expression)
    if leading.startswith("-"):
        matrix = -matrix
    return matrix


def verify_tex_five_relations(
    identifier: str,
    block_before_generators: str,
    signs: tuple[int, int, int, int, int],
) -> None:
    compact = re.sub(r"\s+", "", block_before_generators)
    sign_text = lambda sign: "" if sign == 1 else "-"
    expected = (
        rf"J_1^\transgJ_1={sign_text(signs[0])}g",
        rf"J_1^2={sign_text(signs[1])}I",
        rf"J_2^\transgJ_2={sign_text(signs[2])}g",
        rf"J_2^2={sign_text(signs[3])}I",
        rf"J_1J_2={sign_text(signs[4])}J_2J_1",
    )
    for relation in expected:
        if compact.count(relation) != 2:
            raise AssertionError(
                f"TeX five-relation transcription mismatch in {identifier}: "
                f"expected two copies of {relation}"
            )


def verify_tex_contraction_witness(
    identifier: str, block: str, expected_eta: np.ndarray
) -> None:
    inline_expressions = re.findall(
        r"\\\(((?:(?!\\\)).)*)\\\)", block, re.S
    )
    inequalities = [
        expression.removesuffix(r"A_{\rm cone}<0")
        for expression in inline_expressions
        if expression.endswith(r"A_{\rm cone}<0")
    ]
    if len(inequalities) != 1:
        raise AssertionError(
            f"expected one explicit cone inequality in {identifier}, "
            f"found {len(inequalities)}"
        )
    if not np.array_equal(
        latex_matrix(inequalities[0], expected_eta.shape[0]), expected_eta
    ):
        raise AssertionError(f"TeX cone metric mismatch in {identifier}")

    witness = re.search(
        r"K_\{(.*?)\}\s*=\s*(-?\\ii\s*I|-?I)", block, re.S
    )
    if witness is None:
        raise AssertionError(f"cannot parse A_cone=-eta witness in {identifier}")
    pauli = pauli_matrix(latex_pauli_word(witness.group(1)))
    coefficient_text = re.sub(r"\s+", "", witness.group(2))
    coefficient = {
        "I": 1,
        "-I": -1,
        r"\iiI": 1j,
        r"-\iiI": -1j,
    }[coefficient_text]
    if not np.array_equal(coefficient * pauli, -expected_eta):
        raise AssertionError(f"TeX A_cone=-eta witness mismatch in {identifier}")


def verify_generator_tex(rows: list[dict[str, str]], repo_root: Path) -> None:
    path = repo_root / "experts" / "ContractionSemigroupGenerators.tex"
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"\\cellentry\{([BF]\d\d)\}", text))
    if len(starts) != 16:
        raise AssertionError(f"expected 16 generator cases in TeX, found {len(starts)}")
    blocks = {
        match.group(1): text[
            match.start() : starts[index + 1].start()
            if index + 1 < len(starts)
            else len(text)
        ]
        for index, match in enumerate(starts)
    }
    expected = {
        case_id(row["statistics"], signs_from_row(row)): row
        for row in rows
        if row["strict_interior"] == "1"
    }
    if set(blocks) != set(expected):
        raise AssertionError("TeX and CSV list different contraction cases")

    for identifier, block in blocks.items():
        row = expected[identifier]
        group_marker = re.search(r"A_\{\\rm group\}", block)
        if group_marker is None:
            raise AssertionError(f"missing A_group marker in {identifier}")
        cone_marker = re.search(r"A_\{\\rm cone\}", block[group_marker.end() :])
        if cone_marker is None:
            raise AssertionError(f"missing A_cone marker in {identifier}")
        cone_position = group_marker.end() + cone_marker.start()
        actual_group = parse_tex_terms(block[group_marker.start() : cone_position])
        actual_cone = parse_tex_terms(block[cone_position:])
        if len(actual_group) != len(set(actual_group)):
            raise AssertionError(f"duplicate A_group term in {identifier}")
        if len(actual_cone) != len(set(actual_cone)):
            raise AssertionError(f"duplicate A_cone term in {identifier}")
        if set(actual_group) != set(split_terms(row["maximal_terms"])):
            raise AssertionError(f"TeX A_group transcription mismatch in {identifier}")
        if set(actual_cone) != set(split_terms(row["cone_linear_terms"])):
            raise AssertionError(f"TeX A_cone transcription mismatch in {identifier}")

        verify_tex_five_relations(
            identifier, block[: group_marker.start()], signs_from_row(row)
        )

        representative = re.search(
            r"J_1=(.*?),\\qquad\s*J_2=(.*?),\\qquad\s*\\eta=(.*?)\.",
            block[: group_marker.start()],
            re.S,
        )
        if representative is None:
            raise AssertionError(f"cannot parse J1, J2, eta in {identifier}")
        if latex_pauli_word(representative.group(1)) != row["J1_word"]:
            raise AssertionError(f"TeX J1 transcription mismatch in {identifier}")
        if latex_pauli_word(representative.group(2)) != row["J2_word"]:
            raise AssertionError(f"TeX J2 transcription mismatch in {identifier}")
        number_of_factors = int(row["n"])
        g, _ = canonical_matrices(row["statistics"], number_of_factors)
        second = pauli_matrix(row["J2_word"])
        _, expected_eta = contraction_metric(
            row["statistics"], g, second, signs_from_row(row)
        )
        if not np.array_equal(
            latex_matrix(representative.group(3), expected_eta.shape[0]), expected_eta
        ):
            raise AssertionError(f"TeX eta transcription mismatch in {identifier}")
        verify_tex_contraction_witness(identifier, block, expected_eta)


def verify_time_reversal_case_coverage(
    rows: list[dict[str, str]], repo_root: Path
) -> None:
    whole_expected = {
        row["statistics"][0].upper() + f"{int(row['class_number']):02d}"
        for row in rows
        if row["time_reversal_result"] == "whole A_group"
    }
    proper_majorana_expected = {
        row["statistics"][0].upper() + f"{int(row['class_number']):02d}"
        for row in rows
        if row["time_reversal_result"] != "whole A_group"
        and row["time_reversal_class"] == "Majorana"
    }
    proper_kramers_expected = {
        row["statistics"][0].upper() + f"{int(row['class_number']):02d}"
        for row in rows
        if row["time_reversal_result"] != "whole A_group"
        and row["time_reversal_class"] == "Kramers"
    }
    files = {
        "whole": (
            repo_root / "experts" / "ContractionSemigroupWholeGroup.tex",
            whole_expected,
        ),
        "Majorana": (
            repo_root / "experts" / "ContractionSemigroupMajoranaProper.tex",
            proper_majorana_expected,
        ),
        "Kramers": (
            repo_root / "experts" / "ContractionSemigroupKramersProper.tex",
            proper_kramers_expected,
        ),
    }
    for name, (path, expected) in files.items():
        actual = set(re.findall(r"\b[BF]\d\d\b", path.read_text(encoding="utf-8")))
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise AssertionError(
                f"{name} TeX case coverage mismatch; missing={missing}, extra={extra}"
            )


def verify_model_rows(rows: list[dict[str, str]]) -> None:
    expected_fields = {
        "model",
        "class_number",
        "field_value",
        "relation_residual",
        "lie_residual",
        "reality_residual",
        "group_J2_residual",
        "cone_J2_residual",
        "group_metric_residual",
        "cone_metric_residual",
        "maximum_contraction_eigenvalue",
        "extra_symmetry_residual",
        "broken_extra_symmetry_residual",
        "minimum_coefficient_margin",
    }
    if len(rows) != 9 or Counter(row["model"] for row in rows) != Counter(
        {"B05": 3, "B13": 3, "F04": 3}
    ):
        raise AssertionError("model checker did not produce the expected nine rows")
    if set(rows[0]) != expected_fields:
        raise AssertionError("model checker CSV has an unexpected schema")

    zero_residuals = (
        "relation_residual",
        "lie_residual",
        "reality_residual",
        "group_J2_residual",
        "cone_J2_residual",
        "group_metric_residual",
        "cone_metric_residual",
    )
    for model in ("B05", "B13", "F04"):
        selected = [row for row in rows if row["model"] == model]
        if {float(row["field_value"]) for row in selected} != {-2.0, 0.0, 1.5}:
            raise AssertionError(f"unexpected auxiliary fields in {model}")
        for row in selected:
            if row["class_number"] != model:
                raise AssertionError(f"incorrect class label in {model}")
            if any(abs(float(row[field])) >= 1.0e-9 for field in zero_residuals):
                raise AssertionError(f"algebraic residual failed in {model}")
            if float(row["maximum_contraction_eigenvalue"]) >= -1.0e-9:
                raise AssertionError(f"contraction inequality failed in {model}")
            if abs(float(row["extra_symmetry_residual"])) >= 1.0e-9:
                raise AssertionError(f"stated extra symmetry failed in {model}")
            if model == "B05":
                if row["broken_extra_symmetry_residual"] or row["minimum_coefficient_margin"]:
                    raise AssertionError("B05 has unexpected coefficient diagnostics")
            else:
                if float(row["broken_extra_symmetry_residual"]) <= 1.0e-9:
                    raise AssertionError(f"stated symmetry-breaking term failed in {model}")
                if float(row["minimum_coefficient_margin"]) <= 1.0e-9:
                    raise AssertionError(f"coefficient inequality failed in {model}")


def compare_reference(results: Path, reference: Path) -> None:
    for name in (
        SEMIGROUP_FILE,
        GENERATOR_FILE,
        TIME_REVERSAL_FILE,
        WITNESS_FILE,
        MODEL_FILE,
    ):
        produced = (results / name).read_bytes()
        approved = (reference / name).read_bytes()
        if produced != approved:
            raise AssertionError(f"generated output differs from reference/{name}")


def verify_full_pauli_scan(
    results: Path, reference: Path, *, compare_snapshot: bool
) -> None:
    rows = read_csv(results / PAULI_SCAN_FILE)
    if len(rows) != 144:
        raise AssertionError(f"expected 144 Pauli-scan aggregates, found {len(rows)}")
    if sum(int(row["realization_count"]) for row in rows) != 8568:
        raise AssertionError("full scan did not cover 8568 ordered realizations")
    if sum(
        int(row["realization_count"])
        for row in rows
        if row["strict_interior"] == "1"
    ) != 2184:
        raise AssertionError("full scan did not cover 2184 contraction realizations")
    for row in rows:
        if row["strict_interior"] == "1" and any(
            float(row[field]) != 0.0
            for field in (
                "worst_A0_lie_residual",
                "worst_A0_reality_residual",
                "worst_A0_J2_residual",
                "worst_A0_contraction_residual",
            )
        ):
            raise AssertionError(f"A_cone=-eta failed in full scan row {row}")
    if compare_snapshot and (results / PAULI_SCAN_FILE).read_bytes() != (
        reference / PAULI_SCAN_FILE
    ).read_bytes():
        raise AssertionError("full Pauli scan differs from the committed reference")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify all machine-generated results used by the note."
    )
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--skip-reference-comparison",
        action="store_true",
        help="run algebraic checks without comparing committed CSV snapshots",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="also verify the optional 8568-realization Pauli scan",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    semigroup_rows = read_csv(arguments.results / SEMIGROUP_FILE)
    generator_rows = read_csv(arguments.results / GENERATOR_FILE)
    time_reversal_rows = read_csv(arguments.results / TIME_REVERSAL_FILE)
    model_rows = read_csv(arguments.results / MODEL_FILE)

    verify_semigroup_rows(semigroup_rows)
    verify_generator_rows(generator_rows, semigroup_rows)
    verify_time_reversal_rows(time_reversal_rows)
    cross_check_classifications(semigroup_rows, time_reversal_rows)
    verify_generator_tex(generator_rows, arguments.repo_root)
    verify_time_reversal_case_coverage(time_reversal_rows, arguments.repo_root)
    verify_model_rows(model_rows)
    if not arguments.skip_reference_comparison:
        compare_reference(arguments.results, arguments.reference)
    if arguments.full:
        verify_full_pauli_scan(
            arguments.results,
            arguments.reference,
            compare_snapshot=not arguments.skip_reference_comparison,
        )

    print("Verified 64 bosonic/fermionic five-relation classes.")
    print("Verified all A_group and A_cone Pauli directions for 64 representatives.")
    print("Verified the 16 generator formulas transcribed into the note.")
    print("Verified all 64 time-reversal subgroup constructions and M/K TeX case lists.")
    print("Verified the B05, B13, and F04 model slices.")
    if not arguments.skip_reference_comparison:
        print("All generated CSV files match the committed reference results.")
    if arguments.full:
        print("Verified A_cone=-eta in all 2184 contraction realizations from the full scan.")


if __name__ == "__main__":
    main()
