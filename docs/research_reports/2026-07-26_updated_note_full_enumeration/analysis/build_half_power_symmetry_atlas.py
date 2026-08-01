#!/usr/bin/env python3
"""Build the 64-class atlas for the actual Nambu half-power weight."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


REPORT_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = REPORT_DIR / "tables" / "tensor_block_structures.csv"
PHYSICAL_BOSON_PATH = (
    REPORT_DIR / "tables" / "bosonic_physical_representation_suborbits_le4.csv"
)
OUTPUT_PATH = REPORT_DIR / "tables" / "half_power_symmetry_64_classes.csv"
HTML_PATH = REPORT_DIR / "half_power_symmetry_64_table.fragment.html"

BOSON_POLARIZATION_VERIFIED = {15, 27}
BOSON_POLARIZATION_IMPOSSIBLE = {12, 32}


def signed_permutation_matrix(text: str) -> np.ndarray:
    """Decode the one-based signed-permutation notation used by the CSV files."""
    entries = [int(value) for value in text.strip("[]").split()]
    matrix = np.zeros((len(entries), len(entries)), dtype=complex)
    for column, entry in enumerate(entries):
        matrix[abs(entry) - 1, column] = 1 if entry > 0 else -1
    return matrix


def boson_matrices(dimension: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    modes = dimension // 2
    identity = np.eye(modes, dtype=complex)
    zero = np.zeros_like(identity)
    g = np.block([[zero, -identity], [identity, zero]])
    conjugation = np.block([[zero, identity], [identity, zero]])
    commutator = np.block([[identity, zero], [zero, -identity]])
    return g, conjugation, commutator


def positive_polarization_exists(
    first: np.ndarray,
    second: np.ndarray,
    first_g_sign: int,
    second_g_sign: int,
) -> bool:
    """Check whether one Q eigenspace has positive bosonic commutator."""
    _, _, commutator = boson_matrices(first.shape[0])
    first_u = first if first_g_sign == 1 else 1j * first
    second_u = second if second_g_sign == 1 else 1j * second
    product = first_u @ second_u.conj()
    for eigenvalue in (1j, -1j):
        _, singular_values, right = np.linalg.svd(product - eigenvalue * np.eye(len(product)))
        vectors = right.conj().T[:, singular_values < 1e-9]
        if vectors.shape[1] != first.shape[0] // 2:
            continue
        restricted = vectors.conj().T @ commutator @ vectors
        eigenvalues = np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)
        if np.min(eigenvalues) > 1e-8:
            return True
    return False


def validate_boson_physical_representations(
    boson_rows: list[dict[str, str]],
) -> None:
    """Verify every reader-facing low-dimensional physical-representation claim."""
    by_class = {row["class_id"]: row for row in boson_rows}
    with PHYSICAL_BOSON_PATH.open(newline="", encoding="utf-8") as handle:
        physical_rows = list(csv.DictReader(handle))
    physical_classes: set[str] = set()
    positive_polarization_classes: set[str] = set()
    for physical in physical_rows:
        relation = by_class[physical["class_id"]]
        dimension = int(physical["matrix_dimension"])
        first = signed_permutation_matrix(physical["representative_J1"])
        second = signed_permutation_matrix(physical["representative_J2"])
        g, conjugation, _ = boson_matrices(dimension)
        identity = np.eye(dimension, dtype=complex)
        generalized: list[np.ndarray] = []
        for index, matrix in enumerate((first, second), start=1):
            g_sign = int(relation[f"s{index}"])
            square_sign = int(relation[f"q{index}"])
            transformed = matrix if g_sign == 1 else 1j * matrix
            assert np.allclose(transformed.T @ g @ transformed, g)
            assert np.allclose(
                conjugation @ transformed.conj() @ conjugation,
                transformed,
            )
            assert np.allclose(
                transformed @ transformed.conj(), square_sign * identity
            )
            generalized.append(transformed)
        expected_mutual = (
            int(relation["r"]) * int(relation["s1"]) * int(relation["s2"])
        )
        assert np.allclose(
            generalized[0] @ generalized[1].conj(),
            expected_mutual * generalized[1] @ generalized[0].conj(),
        )
        physical_classes.add(physical["class_id"])
        if positive_polarization_exists(
            first,
            second,
            int(relation["s1"]),
            int(relation["s2"]),
        ):
            positive_polarization_classes.add(physical["class_id"])

    for row in boson_rows:
        if mechanism(row) == "conjugate_subsystems":
            assert row["class_id"] in physical_classes
    verified_ids = {
        boson_rows[number - 1]["class_id"] for number in BOSON_POLARIZATION_VERIFIED
    }
    impossible_ids = {
        boson_rows[number - 1]["class_id"] for number in BOSON_POLARIZATION_IMPOSSIBLE
    }
    assert verified_ids <= positive_polarization_classes
    assert impossible_ids.isdisjoint(physical_classes)


def relation_html(row: dict[str, str]) -> str:
    first_g = "g" if int(row["s1"]) == 1 else "-g"
    first_square = "I" if int(row["q1"]) == 1 else "-I"
    second_g = "g" if int(row["s2"]) == 1 else "-g"
    second_square = "I" if int(row["q2"]) == 1 else "-I"
    mutual = "J_2J_1" if int(row["r"]) == 1 else "-J_2J_1"
    return (
        r"\(\begin{gathered}"
        rf"J_1^TgJ_1={first_g},\quad J_1^2={first_square};\\"
        rf"J_2^TgJ_2={second_g},\quad J_2^2={second_square};\\"
        rf"J_1J_2={mutual}"
        r"\end{gathered}\)"
    )


def mechanism(row: dict[str, str]) -> str:
    relative = int(row["r"]) * int(row["s1"]) * int(row["s2"])
    squares = (int(row["q1"]), int(row["q2"]))
    if relative == -1 and sorted(squares) == [-1, 1]:
        return "conjugate_subsystems"
    if relative == -1 and squares == (-1, -1):
        return "kramers_polarization"
    return "not_fixed"


def boson_status(class_number: int, mechanism_name: str) -> tuple[str, str]:
    if mechanism_name == "conjugate_subsystems":
        return (
            "yes",
            "已找到四维、满足物理 Nambu 共轭关系的具体表示；"
            r"对通过 \(C\overline U_aC=U_a\) 检查的表示，"
            r"\(W_{\rm B}=|w|^2\geq0\)",
        )
    if mechanism_name == "kramers_polarization":
        if class_number in BOSON_POLARIZATION_VERIFIED:
            return (
                "yes",
                "四维具体表示的 commutator matrix 已验证为正定；"
                r"该表示中 \(W_{\rm B}\geq0\)，更高维仍须逐表示检查",
            )
        if class_number in BOSON_POLARIZATION_IMPOSSIBLE:
            return (
                "no",
                "两条反线性变换都平方为负一并彼此反对易，但当前实正交 "
                r"\(J_a\) 设定在任意维都不能给出物理 annihilation space",
            )
        raise AssertionError("Unexpected bosonic Kramers class")
    return (
        "partial",
        "五条关系不足以固定实际 metaplectic half-power；需增加物理粒子空间、"
        "reflected-square 结构或额外反线性对称性",
    )


def fermion_status(mechanism_name: str) -> tuple[str, str]:
    if mechanism_name == "conjugate_subsystems":
        return (
            "yes",
            "共轭 Majorana 分块定理：偶数模时权重为模平方；"
            "奇数模加入一个解耦辅助模后，原权重为模平方的一半；"
            r"两种情形均有 \(W_{\rm F}\geq0\)",
        )
    if mechanism_name == "kramers_polarization":
        return (
            "yes",
            "物理粒子空间加 Kramers theorem："
            r"\(W_{\rm F}=e^{-\sum_\ell\operatorname{Tr}K_\ell/2}"
            r"\det(I+\mathcal B)\geq0\)",
        )
    return (
        "partial",
        "五条关系不足以固定实际 Spin half-power；需增加物理粒子空间、"
        "reflected-square 结构、split-orthogonal subgroup 或额外反线性对称性",
    )


def cone_status(row: dict[str, str]) -> str:
    if not int(row["strict_interior"]):
        return r"严格 \(A_{\rm cone}\) 无解"
    return (
        r"严格 \(A_{\rm cone}\) 有解；使用非零 \(A_{\rm cone}\) 时，"
        r"\(\Theta_2\) 把它变为 \(-A_{\rm cone}\)，不再保持同一构型"
    )


def span(css_class: str, text: str) -> str:
    return f'<span class="{css_class}">{text}</span>'


def build_html(rows: list[dict[str, str]]) -> str:
    bosons = [row for row in rows if row["statistics"] == "boson"]
    fermions = [row for row in rows if row["statistics"] == "fermion"]
    assert len(bosons) == len(fermions) == 32
    validate_boson_physical_representations(bosons)
    body: list[str] = []
    for number, (boson, fermion) in enumerate(
        zip(bosons, fermions, strict=True), 1
    ):
        assert boson["class_id"] == fermion["class_id"]
        name = mechanism(boson)
        assert name == mechanism(fermion)
        boson_css, boson_text = boson_status(number, name)
        fermion_css, fermion_text = fermion_status(name)
        body.append(
            "<tr>"
            f'<td class="num">{number:02d}</td>'
            f"<td>{relation_html(boson)}</td>"
            f'<td><a href="part_3_enumeration_models.html#class-boson-{number:02d}">'
            f"玻色 {number:02d}</a><br>{span(boson_css, boson_text)}</td>"
            f"<td>{cone_status(boson)}</td>"
            f'<td><a href="part_3_enumeration_models.html#class-fermion-{number:02d}">'
            f"费米 {number:02d}</a><br>{span(fermion_css, fermion_text)}</td>"
            f"<td>{cone_status(fermion)}</td>"
            "</tr>"
        )
    return r"""
<div class="scroll half-power-atlas-table">
  <table>
    <thead>
      <tr>
        <th class="num">编号</th>
        <th>五条矩阵关系</th>
        <th>玻色：只含 \(A_{\rm group}\) 的实际权重</th>
        <th>玻色：\(A_{\rm cone}\)</th>
        <th>费米：只含 \(A_{\rm group}\) 的实际权重</th>
        <th>费米：\(A_{\rm cone}\)</th>
      </tr>
    </thead>
    <tbody>
""" + "\n".join(body) + """
    </tbody>
  </table>
</div>
"""


def main() -> None:
    with INPUT_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 64

    counters = {"boson": 0, "fermion": 0}
    output_rows: list[dict[str, str]] = []
    for row in rows:
        statistics = row["statistics"]
        counters[statistics] += 1
        name = mechanism(row)
        if statistics == "boson":
            _, actual = boson_status(counters[statistics], name)
        else:
            _, actual = fermion_status(name)
        output_rows.append(
            {
                "statistics": statistics,
                "class_number": str(counters[statistics]),
                "class_id": row["class_id"],
                "group_half_power_mechanism": name,
                "group_actual_weight_result": actual,
                "strict_cone_exists": row["strict_interior"],
                "cone_actual_weight_result": cone_status(row),
            }
        )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    HTML_PATH.write_text(build_html(rows), encoding="utf-8")

    summary: dict[tuple[str, str], int] = {}
    for row in output_rows:
        key = (row["statistics"], row["group_half_power_mechanism"])
        summary[key] = summary.get(key, 0) + 1
    for key, count in sorted(summary.items()):
        print(f"{key[0]} {key[1]}: {count}")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {HTML_PATH}")


if __name__ == "__main__":
    main()
