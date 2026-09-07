#!/usr/bin/env python3
"""Audit the time-reversal TeX formulas against the enumeration CSV.

The main note and its three time-reversal includes use different presentation
styles.  This script parses the scientific data that they display, converts
every Pauli tensor to the word convention used by
``time_reversal_subgroups.csv``, and checks it against the enumerated result.
All matrix identities are evaluated exactly: the matrices contain only
Gaussian integers (0, +/-1, +/-i).
"""

from __future__ import annotations

import argparse
import csv
import itertools
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_CSV = PACKAGE_ROOT / "build" / "time_reversal_subgroups.csv"
DEFAULT_WHOLE_GROUP = REPOSITORY_ROOT / "note" / "ContractionSemigroupWholeGroup.tex"
DEFAULT_MAJORANA = (
    REPOSITORY_ROOT / "note" / "ContractionSemigroupMajoranaProper.tex"
)
DEFAULT_KRAMERS = (
    REPOSITORY_ROOT / "note" / "ContractionSemigroupKramersProper.tex"
)
DEFAULT_SPLIT_ORTHOGONAL = (
    REPOSITORY_ROOT / "note" / "ContractionSemigroupsQMC.tex"
)

CASE_PATTERN = re.compile(r"[BF]\d{2}")


Matrix = tuple[tuple[complex, ...], ...]

I2: Matrix = ((1, 0), (0, 1))
X2: Matrix = ((0, 1), (1, 0))
Y2: Matrix = ((0, 1), (-1, 0))  # Y = i sigma_y
Z2: Matrix = ((1, 0), (0, -1))
PAULI = {"I": I2, "X": X2, "Y": Y2, "Z": Z2}
MAX_PAULI_FACTORS = 3


@dataclass(frozen=True)
class ParsedCase:
    case_id: str
    j1_word: str
    j2_word: str
    extra_u: str
    retained_basis: frozenset[str] | None
    stated_relations: tuple[int, int, int] | None
    stated_class: str
    source: Path


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.check_count = 0

    def check(self, condition: bool, message: str) -> None:
        self.check_count += 1
        if not condition:
            self.errors.append(message)

    def equal(self, actual: object, expected: object, context: str) -> None:
        self.check(actual == expected, f"{context}: expected {expected!r}, found {actual!r}")


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    if len(left[0]) != len(right):
        raise ValueError("incompatible exact-matrix dimensions")
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def matrix_transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matrix_conjugate(matrix: Matrix) -> Matrix:
    return tuple(tuple(value.conjugate() for value in row) for row in matrix)


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(len(left[0])))
        for row in range(len(left))
    )


def matrix_scale(factor: complex, matrix: Matrix) -> Matrix:
    return tuple(tuple(factor * value for value in row) for row in matrix)


def kronecker(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            left[left_row][left_column] * right[right_row][right_column]
            for left_column in range(len(left[0]))
            for right_column in range(len(right[0]))
        )
        for left_row in range(len(left))
        for right_row in range(len(right))
    )


def identity(dimension: int) -> Matrix:
    return tuple(
        tuple(1 if row == column else 0 for column in range(dimension))
        for row in range(dimension)
    )


def pauli_word_matrix(word: str) -> Matrix:
    leading_i = word.startswith("i")
    letters = word[1:] if leading_i else word
    if not letters or any(letter not in PAULI for letter in letters):
        raise ValueError(f"invalid Pauli word {word!r}")
    if len(letters) > MAX_PAULI_FACTORS:
        raise ValueError(
            f"Pauli word exceeds the {MAX_PAULI_FACTORS}-factor search: {word!r}"
        )
    matrix: Matrix = ((1,),)
    for letter in letters:
        matrix = kronecker(matrix, PAULI[letter])
    return matrix_scale(1j if leading_i else 1, matrix)


def signed_relation(left: Matrix, right: Matrix, context: str) -> int:
    if left == right:
        return 1
    if left == matrix_scale(-1, right):
        return -1
    raise ValueError(f"{context}: matrices are not related by a sign")


def canonical_g(statistics: str, factor_count: int) -> Matrix:
    internal = identity(2 ** (factor_count - 1))
    if statistics == "boson":
        return kronecker(matrix_scale(-1, Y2), internal)
    if statistics == "fermion":
        return kronecker(X2, internal)
    raise ValueError(f"unknown statistics {statistics!r}")


def five_relations(statistics: str, j1_word: str, j2_word: str) -> tuple[int, ...]:
    j1 = pauli_word_matrix(j1_word)
    j2 = pauli_word_matrix(j2_word)
    if len(j1) != len(j2):
        raise ValueError(f"J1 and J2 have different dimensions: {j1_word}, {j2_word}")
    factor_count = len(j1_word.removeprefix("i"))
    g = canonical_g(statistics, factor_count)
    unit = identity(len(j1))
    return (
        signed_relation(
            matrix_multiply(matrix_multiply(matrix_transpose(j1), g), j1),
            g,
            "J1 action on g",
        ),
        signed_relation(matrix_multiply(j1, j1), unit, "J1 square"),
        signed_relation(
            matrix_multiply(matrix_multiply(matrix_transpose(j2), g), j2),
            g,
            "J2 action on g",
        ),
        signed_relation(matrix_multiply(j2, j2), unit, "J2 square"),
        signed_relation(
            matrix_multiply(j1, j2),
            matrix_multiply(j2, j1),
            "J1-J2 relation",
        ),
    )


def induced_time_reversal(word: str, action_on_g: int) -> Matrix:
    return matrix_scale(1j if action_on_g == -1 else 1, pauli_word_matrix(word))


def time_reversal_square(linear_part: Matrix) -> int:
    return signed_relation(
        matrix_multiply(linear_part, matrix_conjugate(linear_part)),
        identity(len(linear_part)),
        "time-reversal square",
    )


def time_reversal_mutual_sign(first: Matrix, second: Matrix) -> int:
    return signed_relation(
        matrix_multiply(first, matrix_conjugate(second)),
        matrix_multiply(second, matrix_conjugate(first)),
        "time-reversal mutual relation",
    )


def physical_time_reversal(statistics: str, linear_part: Matrix) -> bool:
    factor_count = (len(linear_part).bit_length() - 1)
    g = canonical_g(statistics, factor_count)
    conjugation = kronecker(X2, identity(2 ** (factor_count - 1)))
    return (
        matrix_multiply(
            matrix_multiply(matrix_transpose(linear_part), g), linear_part
        )
        == g
        and matrix_multiply(
            matrix_multiply(conjugation, matrix_conjugate(linear_part)),
            conjugation,
        )
        == linear_part
    )


def generator_is_invariant(generator: Matrix, linear_part: Matrix) -> bool:
    # U^{-1} conjugate(A) U = A, written without an explicit inverse.
    return matrix_multiply(matrix_conjugate(generator), linear_part) == matrix_multiply(
        linear_part, generator
    )


def group_basis(
    statistics: str, j1_word: str, j2_word: str
) -> dict[str, Matrix]:
    factor_count = len(j1_word.removeprefix("i"))
    g = canonical_g(statistics, factor_count)
    j1 = pauli_word_matrix(j1_word)
    j2 = pauli_word_matrix(j2_word)
    zero = matrix_scale(0, g)
    basis: dict[str, Matrix] = {}
    for letters in itertools.product("IXYZ", repeat=factor_count):
        word = "".join(letters)
        for prefix in ("", "i"):
            name = prefix + word
            generator = pauli_word_matrix(name)
            if matrix_add(
                matrix_multiply(g, generator),
                matrix_multiply(matrix_transpose(generator), g),
            ) != zero:
                continue
            if (
                matrix_multiply(
                    matrix_multiply(matrix_transpose(j1), generator), j1
                )
                != matrix_conjugate(generator)
            ):
                continue
            if (
                matrix_multiply(
                    matrix_multiply(matrix_transpose(j2), generator), j2
                )
                != matrix_conjugate(generator)
            ):
                continue
            basis[name] = generator
    return basis


def class_from_pair(first: Matrix, second: Matrix) -> str | None:
    if time_reversal_mutual_sign(first, second) != -1:
        return None
    squares = sorted((time_reversal_square(first), time_reversal_square(second)))
    if squares == [-1, 1]:
        return "Majorana"
    if squares == [-1, -1]:
        return "Kramers"
    return None


def remove_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def normalize_pauli_expression(expression: str) -> str:
    """Convert a displayed Pauli tensor to the CSV word convention.

    The CSV uses ``Y`` for ``i sigma_y``.  Consequently an unaccompanied
    ``sigma_y`` contributes an additional overall factor of ``i`` up to an
    irrelevant real minus sign.
    """

    expression = remove_comments(expression)
    paired_y = len(re.findall(r"\\ii\s*\\sigma_y", expression))
    all_i = len(re.findall(r"\\ii", expression))
    all_y = len(re.findall(r"\\sigma_y", expression))
    phase_is_imaginary = (all_i - paired_y + all_y - paired_y) % 2 == 1

    token_pattern = re.compile(r"I(?:_2)?(?![A-Za-z])|\\sigma_([xyz])")
    letters: list[str] = []
    for match in token_pattern.finditer(expression):
        token = match.group(0)
        letters.append("I" if token.startswith("I") else match.group(1).upper())
    if not letters:
        compact = re.sub(r"\s+", " ", expression).strip()
        raise ValueError(f"no Pauli factors found in {compact!r}")
    return ("i" if phase_is_imaginary else "") + "".join(letters)


def split_tuple(body: str, expected_length: int, context: str) -> list[str]:
    # TeX's ``\,`` spacing command contains a literal comma; it is not a
    # tuple separator.
    parts = [part.strip() for part in body.replace(r"\,", "").split(",")]
    if len(parts) != expected_length:
        raise ValueError(
            f"{context}: expected {expected_length} tuple entries, found {len(parts)}"
        )
    return parts


def parse_relation_sign(expression: str, right_hand_side: str) -> int:
    compact = re.sub(r"\s+", "", expression)
    return -1 if f"=-{right_hand_side}" in compact else 1


def relation_triplet(text: str) -> tuple[int, int, int]:
    first = re.search(r"J_1\^\\trans\s*gJ_1\s*=\s*(-?)g", text)
    second = re.search(r"J_2\^\\trans\s*gJ_2\s*=\s*(-?)g", text)
    mutual = re.search(r"J_1J_2\s*=\s*(-?)J_2J_1", text)
    if first is None or second is None or mutual is None:
        raise ValueError("could not parse the three displayed matrix relations")
    return tuple(-1 if match.group(1) else 1 for match in (first, second, mutual))


def find_spans(text: str) -> list[tuple[int, frozenset[str]]]:
    pattern = re.compile(
        r"A_\{\\rm group\}\\in\\operatorname\{span\}_\{\\mathbb R\}"
        r"\s*(?:\\left)?\\\{(.*?)(?:\\right)?\\\}",
        re.DOTALL,
    )
    spans: list[tuple[int, frozenset[str]]] = []
    for match in pattern.finditer(text):
        entries = [
            entry
            for entry in match.group(1).replace(r"\,", "").split(",")
            if entry.strip()
        ]
        spans.append(
            (
                match.start(),
                frozenset(normalize_pauli_expression(entry) for entry in entries),
            )
        )
    return spans


def nearest_preceding_span(
    spans: list[tuple[int, frozenset[str]]], position: int, context: str
) -> frozenset[str]:
    candidates = [basis for start, basis in spans if start < position]
    if not candidates:
        raise ValueError(f"{context}: no preceding retained A_group span found")
    return candidates[-1]


def parse_whole_group(path: Path) -> list[ParsedCase]:
    text = remove_comments(path.read_text(encoding="utf-8"))
    entry_pattern = re.compile(
        r"\\cellentry\{([^}]*)\}\s*\{([^}]*)\}\s*\{([^}]*)\}\s*\{([^}]*)\}"
    )
    entries = list(entry_pattern.finditer(text))
    if not entries:
        raise ValueError(f"{path}: no cellentry blocks found")

    parsed: list[ParsedCase] = []
    tuple_pattern = re.compile(
        r"\(J_1,J_2\)_\{\\rm\s+([BF]\d{2})\}\s*=\s*(?:\{\})?\s*&?\s*"
        r"\\bigl\((.*?)\\bigr\)",
        re.DOTALL,
    )
    for index, entry in enumerate(entries):
        end = entries[index + 1].start() if index + 1 < len(entries) else len(text)
        block = text[entry.start() : end]
        title_cases = set(CASE_PATTERN.findall(entry.group(1)))
        relations = relation_triplet(" ".join(entry.groups()[1:]))
        stated_classes: dict[str, str] = {}
        class_pattern = re.compile(
            r"((?:[BF]\d{2}(?:\s*,\s*(?:and\s+)?|\s+and\s+))+[BF]\d{2})\s+"
            r"(?:realize|are in)\s+the\s+(Majorana|Kramers)\s+class"
        )
        for class_match in class_pattern.finditer(block):
            for case_id in CASE_PATTERN.findall(class_match.group(1)):
                stated_classes[case_id] = class_match.group(2)
        matrix_cases: set[str] = set()
        for match in tuple_pattern.finditer(block):
            case_id = match.group(1)
            first, second = split_tuple(match.group(2), 2, f"{path}:{case_id}")
            matrix_cases.add(case_id)
            parsed.append(
                ParsedCase(
                    case_id=case_id,
                    j1_word=normalize_pauli_expression(first),
                    j2_word=normalize_pauli_expression(second),
                    extra_u="",
                    retained_basis=None,
                    stated_relations=relations,
                    stated_class=stated_classes.get(case_id, ""),
                    source=path,
                )
            )
        if title_cases != matrix_cases:
            raise ValueError(
                f"{path}: cellentry {sorted(title_cases)} displays matrices for "
                f"{sorted(matrix_cases)}"
            )
        if title_cases != set(stated_classes):
            raise ValueError(
                f"{path}: cellentry {sorted(title_cases)} states classes for "
                f"{sorted(stated_classes)}"
            )
    return parsed


def parse_majorana(path: Path) -> list[ParsedCase]:
    text = remove_comments(path.read_text(encoding="utf-8"))
    if "Majorana \\(\\{+,-\\}\\) proper subgroups" not in text:
        raise ValueError(f"{path}: expected Majorana-class heading not found")
    spans = find_spans(text)
    tuple_pattern = re.compile(
        r"\\mathrm\{([BF]\d{2})\}:\\quad\s*&\(J_1,J_2,U_3\)\s*=\s*"
        r"\\bigl\((.*?)\\bigr\)",
        re.DOTALL,
    )
    parsed: list[ParsedCase] = []
    for match in tuple_pattern.finditer(text):
        case_id = match.group(1)
        first, second, extra = split_tuple(match.group(2), 3, f"{path}:{case_id}")
        parsed.append(
            ParsedCase(
                case_id=case_id,
                j1_word=normalize_pauli_expression(first),
                j2_word=normalize_pauli_expression(second),
                extra_u=normalize_pauli_expression(extra),
                retained_basis=nearest_preceding_span(spans, match.start(), case_id),
                stated_relations=None,
                stated_class="Majorana",
                source=path,
            )
        )
    if not parsed:
        raise ValueError(f"{path}: no Majorana cases found")
    return parsed


def parse_split_orthogonal(path: Path) -> list[ParsedCase]:
    text = remove_comments(path.read_text(encoding="utf-8"))
    start_marker = r"\subsubsection*{\texorpdfstring{Bosonic split-orthogonal"
    end_marker = r"\input{note/ContractionSemigroupMajoranaProper}"
    start = text.find(start_marker)
    end = text.find(end_marker, start)
    if start < 0 or end < 0:
        raise ValueError(f"{path}: split-orthogonal section boundaries not found")
    section = text[start:end]

    listed = re.search(r"The four cases (.*?) satisfy", section, re.DOTALL)
    if listed is None:
        raise ValueError(f"{path}: split-orthogonal case list not found")
    listed_cases = set(CASE_PATTERN.findall(listed.group(1)))

    retained = re.search(
        r"retains the generator\s*\\\(A_\{\\rm group\}=\\kappa\\,\s*(.*?)\\\)",
        section,
        re.DOTALL,
    )
    if retained is None:
        raise ValueError(f"{path}: split-orthogonal retained generator not found")
    retained_basis = frozenset({normalize_pauli_expression(retained.group(1))})

    compact = re.sub(r"\s+", "", section)
    required_algebra = (
        r"\Theta_1^2=\Theta_2^2=\Theta_3^2=I",
        r"\Theta_1\Theta_2=-\Theta_2\Theta_1",
        r"\Theta_1\Theta_3=-\Theta_3\Theta_1",
        r"\Theta_2\Theta_3=-\Theta_3\Theta_2",
    )
    for relation in required_algebra:
        if relation not in compact:
            raise ValueError(
                f"{path}: split-orthogonal algebra is missing {relation}"
            )

    tuple_pattern = re.compile(
        r"\\mathrm\{(B\d{2})\}:\\quad\s*&\(J_1,J_2,U_3\)\s*=\s*"
        r"\\bigl\((.*?)\\bigr\)",
        re.DOTALL,
    )
    parsed: list[ParsedCase] = []
    for match in tuple_pattern.finditer(section):
        case_id = match.group(1)
        first, second, extra = split_tuple(match.group(2), 3, f"{path}:{case_id}")
        parsed.append(
            ParsedCase(
                case_id=case_id,
                j1_word=normalize_pauli_expression(first),
                j2_word=normalize_pauli_expression(second),
                extra_u=normalize_pauli_expression(extra),
                retained_basis=retained_basis,
                stated_relations=None,
                stated_class="split-orthogonal",
                source=path,
            )
        )
    parsed_cases = {case.case_id for case in parsed}
    if parsed_cases != listed_cases or len(parsed) != 4:
        raise ValueError(
            f"{path}: split-orthogonal list {sorted(listed_cases)} displays "
            f"matrices for {sorted(parsed_cases)}"
        )
    return parsed


def variable_expression(block: str, variable: str, context: str) -> str:
    match = re.search(
        rf"^\s*{re.escape(variable)}\s*&?=\s*(.*?)(?:,|\.)",
        block,
        re.DOTALL | re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"{context}: could not find {variable}")
    return match.group(1)


def retained_scalar(block: str) -> frozenset[str] | None:
    match = re.search(
        r"It retains\s+\$?\\?\(?.*?A_\{\\rm group\}\s*=\s*"
        r"\\kappa\\,\s*(.*?)(?:,\s*with)",
        block,
        re.DOTALL,
    )
    if match is None:
        return None
    return frozenset({normalize_pauli_expression(match.group(1))})


def parse_kramers(path: Path) -> list[ParsedCase]:
    text = remove_comments(path.read_text(encoding="utf-8"))
    if "Kramers \\(\\{-,-\\}\\) proper subgroups" not in text:
        raise ValueError(f"{path}: expected Kramers-class heading not found")
    markers = list(re.finditer(r"\\textit\{([BF]\d{2})\.\}", text))
    if not markers:
        raise ValueError(f"{path}: no Kramers case markers found")

    parsed: list[ParsedCase] = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        block = text[marker.start() : end]
        case_id = marker.group(1)
        scalar = retained_scalar(block)
        spans = find_spans(block)
        if scalar is not None:
            retained = scalar
        elif spans:
            retained = spans[-1][1]
        else:
            raise ValueError(f"{path}:{case_id}: no retained A_group basis found")
        parsed.append(
            ParsedCase(
                case_id=case_id,
                j1_word=normalize_pauli_expression(
                    variable_expression(block, "J_1", case_id)
                ),
                j2_word=normalize_pauli_expression(
                    variable_expression(block, "J_2", case_id)
                ),
                extra_u=normalize_pauli_expression(
                    variable_expression(block, "U_3", case_id)
                ),
                retained_basis=retained,
                stated_relations=relation_triplet(block),
                stated_class="Kramers",
                source=path,
            )
        )
    return parsed


def read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        prefix = "B" if row["statistics"] == "boson" else "F"
        case_id = f"{prefix}{int(row['class_number']):02d}"
        if case_id in lookup:
            raise ValueError(f"{path}: duplicate row for {case_id}")
        lookup[case_id] = row
    if len(lookup) != 64:
        raise ValueError(f"{path}: expected 64 rows, found {len(lookup)}")
    return lookup


def expected_signs(row: dict[str, str]) -> tuple[int, ...]:
    return tuple(int(row[column]) for column in ("s1", "q1", "s2", "q2", "r"))


def audit_cases(
    cases: Iterable[ParsedCase], rows: dict[str, dict[str, str]], audit: Audit
) -> dict[str, int]:
    counts = {"whole": 0, "Majorana": 0, "Kramers": 0, "split-orthogonal": 0}
    seen: set[str] = set()
    for case in cases:
        context = f"{case.source.name}:{case.case_id}"
        audit.check(case.case_id not in seen, f"{context}: case appears more than once")
        seen.add(case.case_id)
        row = rows.get(case.case_id)
        if row is None:
            audit.check(False, f"{context}: no matching CSV row")
            continue

        statistics = row["statistics"]
        whole_group = case.retained_basis is None and not case.extra_u
        if not whole_group:
            # Proper-subgroup bases depend on the representation.  These
            # literal comparisons ensure that the CSV and TeX refer to the
            # same J1, J2, and U3 before their bases are compared below.
            audit.equal(case.j1_word, row["J1_word"], f"{context} J1")
            audit.equal(case.j2_word, row["J2_word"], f"{context} J2")
            audit.equal(case.extra_u, row["extra_U"], f"{context} added U")

        try:
            algebraic_signs = five_relations(statistics, case.j1_word, case.j2_word)
        except ValueError as error:
            audit.check(False, f"{context}: exact Pauli algebra failed: {error}")
            continue
        audit.equal(algebraic_signs, expected_signs(row), f"{context} five relations")
        if case.stated_relations is not None:
            audit.equal(
                (algebraic_signs[0], algebraic_signs[2], algebraic_signs[4]),
                case.stated_relations,
                f"{context} displayed relations",
            )

        audit.equal(
            case.stated_class,
            row["time_reversal_class"],
            f"{context} time-reversal class",
        )
        if whole_group:
            audit.equal(
                row["time_reversal_result"],
                "whole A_group",
                f"{context} subgroup scope",
            )
            counts["whole"] += 1
        else:
            audit.equal(
                row["time_reversal_result"],
                "proper A_group subspace",
                f"{context} subgroup scope",
            )
            counts[case.stated_class] += 1

        action_first, square_first, action_second, square_second, mutual = algebraic_signs
        first_u = induced_time_reversal(case.j1_word, action_first)
        second_u = induced_time_reversal(case.j2_word, action_second)
        audit.check(
            physical_time_reversal(statistics, first_u),
            f"{context}: induced Theta1 is not a physical Nambu time reversal",
        )
        audit.check(
            physical_time_reversal(statistics, second_u),
            f"{context}: induced Theta2 is not a physical Nambu time reversal",
        )
        audit.equal(time_reversal_square(first_u), square_first, f"{context} Theta1 square")
        audit.equal(
            time_reversal_square(second_u), square_second, f"{context} Theta2 square"
        )
        audit.equal(
            time_reversal_mutual_sign(first_u, second_u),
            mutual * action_first * action_second,
            f"{context} induced time-reversal mutual sign",
        )

        full_basis = group_basis(statistics, case.j1_word, case.j2_word)
        audit.check(bool(full_basis), f"{context}: empty maximal-subgroup basis")
        for name, generator in full_basis.items():
            audit.check(
                generator_is_invariant(generator, first_u),
                f"{context}: full A_group direction {name} is not Theta1 invariant",
            )
            audit.check(
                generator_is_invariant(generator, second_u),
                f"{context}: full A_group direction {name} is not Theta2 invariant",
            )

        if whole_group:
            audit.equal(
                class_from_pair(first_u, second_u),
                case.stated_class,
                f"{context} class from the displayed pair",
            )
            audit.equal(
                row["figure_tag"],
                {"Majorana": "M", "Kramers": "K"}[case.stated_class],
                f"{context} figure tag",
            )
        else:
            extra_u = pauli_word_matrix(case.extra_u)
            audit.check(
                physical_time_reversal(statistics, extra_u),
                f"{context}: displayed U3 is not a physical Nambu time reversal",
            )
            audit.equal(
                str(time_reversal_square(extra_u)),
                row["extra_square"],
                f"{context} Theta3 square",
            )
            if case.stated_class == "split-orthogonal":
                split_matrices = (first_u, second_u, extra_u)
                audit.check(
                    all(time_reversal_square(matrix) == 1 for matrix in split_matrices)
                    and all(
                        time_reversal_mutual_sign(split_matrices[left], split_matrices[right])
                        == -1
                        for left, right in ((0, 1), (0, 2), (1, 2))
                    ),
                    f"{context}: displayed transformations do not form the "
                    "split-orthogonal {+,+,+} algebra",
                )
                partners = [
                    label
                    for label, original in (("Theta1", first_u), ("Theta2", second_u))
                    if time_reversal_square(original) == 1
                    and time_reversal_mutual_sign(original, extra_u) == -1
                ]
            else:
                partners = [
                    label
                    for label, original in (("Theta1", first_u), ("Theta2", second_u))
                    if class_from_pair(original, extra_u) == case.stated_class
                ]
            audit.check(
                bool(partners),
                f"{context}: U3 forms no {case.stated_class} pair with Theta1 or Theta2",
            )
            audit.equal(
                " and ".join(partners),
                row["extra_pairs_with"],
                f"{context} U3 partner",
            )

            selected = frozenset(
                name
                for name, generator in full_basis.items()
                if generator_is_invariant(generator, extra_u)
            )
            audit.check(
                0 < len(selected) < len(full_basis),
                f"{context}: displayed U3 does not select a nonempty proper subgroup",
            )
            audit.equal(
                case.retained_basis,
                selected,
                f"{context} retained A_group basis from J1, J2, and U3",
            )
            csv_basis = frozenset(
                word for word in row["time_reversal_subspace_basis"].split(";") if word
            )
            audit.equal(case.retained_basis, csv_basis, f"{context} retained A_group basis")
            audit.equal(
                len(case.retained_basis),
                int(row["time_reversal_subspace_dimension"]),
                f"{context} retained-space dimension",
            )
            audit.equal(
                len(full_basis),
                int(row["A_group_dimension"]),
                f"{context} maximal-subgroup dimension",
            )
            audit.equal(
                row["figure_tag"],
                {
                    "Majorana": "M*",
                    "Kramers": "K*",
                    "split-orthogonal": "S*",
                }[case.stated_class],
                f"{context} figure tag",
            )
    return counts


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the time-reversal TeX formulas against the enumerated "
            "representatives and retained generator spaces."
        )
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--whole-group", type=Path, default=DEFAULT_WHOLE_GROUP)
    parser.add_argument("--majorana", type=Path, default=DEFAULT_MAJORANA)
    parser.add_argument("--kramers", type=Path, default=DEFAULT_KRAMERS)
    parser.add_argument(
        "--split-orthogonal", type=Path, default=DEFAULT_SPLIT_ORTHOGONAL
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        rows = read_csv(arguments.csv)
        whole = parse_whole_group(arguments.whole_group)
        majorana = parse_majorana(arguments.majorana)
        kramers = parse_kramers(arguments.kramers)
        split_orthogonal = parse_split_orthogonal(arguments.split_orthogonal)
    except (OSError, ValueError) as error:
        print(f"TeX audit setup failed: {error}", file=sys.stderr)
        return 2

    audit = Audit()
    all_cases = whole + majorana + kramers + split_orthogonal
    counts = audit_cases(all_cases, rows, audit)
    audit.equal(len(whole), 24, "whole-group TeX case count")
    audit.equal(len(majorana), 28, "Majorana proper-subgroup TeX case count")
    audit.equal(len(kramers), 8, "Kramers proper-subgroup TeX case count")
    audit.equal(
        len(split_orthogonal), 4, "split-orthogonal proper-subgroup TeX case count"
    )
    audit.equal(len({case.case_id for case in all_cases}), 64, "distinct audited case count")

    if audit.errors:
        print(f"Time-reversal TeX audit failed with {len(audit.errors)} error(s):", file=sys.stderr)
        for error in audit.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        "Verified 64 TeX cases: "
        f"{counts['whole']} whole maximal subgroups, "
        f"{counts['Majorana']} Majorana proper subgroups, "
        f"{counts['Kramers']} Kramers proper subgroups, and "
        f"{counts['split-orthogonal']} split-orthogonal proper subgroups."
    )
    print(
        "Checked displayed case membership, J1/J2, exact five-relation "
        "algebra, added U3, class, and every displayed retained A_group basis."
    )
    print(f"Completed {audit.check_count} consistency checks against {arguments.csv.resolve()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
