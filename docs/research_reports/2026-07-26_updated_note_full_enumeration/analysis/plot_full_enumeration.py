#!/usr/bin/env python3
"""Plot the actual half-power A_group atlas as a periodic table."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FULL_TABLE = ROOT / "tables" / "full_64_class_enumeration.csv"
FIGURE_DIR = ROOT / "figures"

ROW_KEYS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
COL_KEYS = [
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
]

COLORS = {
    "not_fixed": "#e1e4e6",
    "fermion_actual_positive": "#8dbbd8",
    "boson_modulus_square": "#92c3a0",
    "boson_polarization_verified": "#e0c16c",
    "boson_polarization_impossible": "#d99b91",
}

COLOR_ORDER = [
    "not_fixed",
    "fermion_actual_positive",
    "boson_modulus_square",
    "boson_polarization_verified",
    "boson_polarization_impossible",
]

BOSON_POLARIZATION_VERIFIED = {15, 27}
BOSON_POLARIZATION_IMPOSSIBLE = {12, 32}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def row_label(values: tuple[int, int]) -> str:
    g_sign, square_sign = values
    return (
        ("g" if g_sign == 1 else "-g")
        + ", "
        + ("I" if square_sign == 1 else "-I")
    )


def column_label(values: tuple[int, int, int]) -> str:
    g_sign, square_sign, mutual_sign = values
    return "\n".join(
        (
            "g" if g_sign == 1 else "-g",
            "I" if square_sign == 1 else "-I",
            "comm." if mutual_sign == 1 else "anti.",
        )
    )


def anti_linear_pair_type(row: dict[str, str]) -> str | None:
    """Classify the two A_group anti-linear symmetries."""
    q1 = int(row["q1"])
    q2 = int(row["q2"])
    s1 = int(row["s1"])
    s2 = int(row["s2"])
    # The induced anti-linear maps anticommute when r*s1*s2 = -1.
    anti_linear_mutual = int(row["r"]) * s1 * s2

    if anti_linear_mutual != -1:
        return None
    if sorted((q1, q2)) == [-1, 1]:
        return "plus_minus"
    if q1 == -1 and q2 == -1:
        return "minus_minus"
    return None


def classify(
    row: dict[str, str], class_number: int
) -> tuple[str, str, str]:
    """Return actual A_group half-power category, label, and cone detail."""
    pair_type = anti_linear_pair_type(row)

    if row["status"] == "strict":
        cone = (
            r"cone: strict $J_2g$*"
            if row["metric"] == "J2g"
            else r"cone: strict $iJ_2g$*"
        )
    else:
        cone = "cone: none"

    if pair_type is None:
        return (
            "not_fixed",
            r"$A_{\rm group}$: five relations" "\n" "do not fix the half-power",
            cone,
        )

    if row["statistics"] == "fermion":
        mechanism = (
            r"anticomm. $(+,-)$: conjugate Majorana blocks, $W_{\rm F}\geq0$"
            if pair_type == "plus_minus"
            else r"anticomm. $(-,-)$: Kramers polarization"
        )
        return (
            "fermion_actual_positive",
            r"$A_{\rm group}$: actual $W_{\rm F}\geq0$" "\n" + mechanism,
            cone,
        )

    if pair_type == "plus_minus":
        return (
            "boson_modulus_square",
            r"anticomm. $(+,-)$: $W_{\rm B}=|w|^2\geq0$" "\n"
            r"if the pair is Fock-realizable",
            cone,
        )

    if class_number in BOSON_POLARIZATION_VERIFIED:
        return (
            "boson_polarization_verified",
            r"anticomm. $(-,-)$: actual $W_{\rm B}\geq0$" "\n"
            r"positive polarization verified at $d=4$",
            cone,
        )

    if class_number in BOSON_POLARIZATION_IMPOSSIBLE:
        return (
            "boson_polarization_impossible",
            r"anticomm. $(-,-)$: no positive polarization" "\n"
            r"for real orthogonal $J_a$",
            cone,
        )

    raise ValueError(
        f"unclassified bosonic (-,-) class B{class_number:02d}"
    )


def validate_atlas(rows: list[dict[str, str]]) -> None:
    """Guard the 20 + 8 + 4 classification and the independent cone count."""
    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        counts = {None: 0, "plus_minus": 0, "minus_minus": 0}
        for row in selected:
            counts[anti_linear_pair_type(row)] += 1
        expected = {None: 20, "plus_minus": 8, "minus_minus": 4}
        if counts != expected:
            raise ValueError(
                f"unexpected {statistics} A_group classification: {counts}"
            )
        strict_count = sum(row["status"] == "strict" for row in selected)
        if strict_count != 8:
            raise ValueError(
                f"expected 8 strict-cone {statistics} classes, got {strict_count}"
            )


def panel_data(
    rows: list[dict[str, str]],
) -> tuple[np.ndarray, list[list[str]]]:
    lookup = {
        (
            int(row["s1"]),
            int(row["q1"]),
            int(row["s2"]),
            int(row["q2"]),
            int(row["r"]),
        ): (class_number, row)
        for class_number, row in enumerate(rows, start=1)
    }
    color_index = {name: index for index, name in enumerate(COLOR_ORDER)}
    values = np.empty((4, 8), dtype=int)
    labels = [["" for _ in range(8)] for _ in range(4)]
    for i, (s1, q1) in enumerate(ROW_KEYS):
        for j, (s2, q2, r) in enumerate(COL_KEYS):
            number, row = lookup[(s1, q1, s2, q2, r)]
            category, positivity, cone_detail = classify(row, number)
            values[i, j] = color_index[category]
            prefix = "B" if row["statistics"] == "boson" else "F"
            dimension = 2 ** int(row["min_qubits"])
            labels[i][j] = (
                f"{prefix}{number:02d}   d={dimension}\n"
                f"{positivity}\n{cone_detail}"
            )
    return values, labels


def main() -> None:
    full_rows = load_rows(FULL_TABLE)
    validate_atlas(full_rows)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    cmap = ListedColormap([COLORS[name] for name in COLOR_ORDER])
    figure, axes = plt.subplots(2, 1, figsize=(15.3, 10.1))

    for panel, statistics in enumerate(("boson", "fermion")):
        selected = [
            row for row in full_rows if row["statistics"] == statistics
        ]
        values, labels = panel_data(selected)
        ax = axes[panel]
        ax.imshow(
            values,
            cmap=cmap,
            vmin=-0.5,
            vmax=len(COLOR_ORDER) - 0.5,
            aspect="auto",
        )
        for row_index in range(4):
            for col_index in range(8):
                ax.text(
                    col_index,
                    row_index,
                    labels[row_index][col_index],
                    ha="center",
                    va="center",
                    fontsize=6.2,
                    linespacing=1.13,
                    color="#172126",
                )

        ax.set_xticks(range(8))
        ax.set_xticklabels(
            [column_label(values) for values in COL_KEYS],
            fontsize=7.5,
            linespacing=1.05,
        )
        ax.xaxis.set_ticks_position("top")
        ax.xaxis.set_label_position("top")
        ax.set_xlabel(
            r"columns: $J_2^TgJ_2$, $J_2^2$, and "
            r"$J_1,J_2$ commuting (comm.) or anticommuting (anti.)",
            labelpad=8,
        )
        ax.set_yticks(range(4))
        ax.set_yticklabels(
            [row_label(values) for values in ROW_KEYS], fontsize=8
        )
        ax.set_ylabel(
            r"rows: $J_1^TgJ_1$, $J_1^2$",
            labelpad=8,
        )
        ax.set_xticks(np.arange(-0.5, 8, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 4, 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=1.5)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(which="major", length=0)
        ax.set_title(
            (
                r"a  Boson: actual metaplectic half-power on $A_{\rm group}$"
                if panel == 0
                else r"b  Fermion: actual Spin half-power on $A_{\rm group}$"
            ),
            loc="left",
            fontweight="bold",
            pad=7,
        )

    legend = [
        Patch(
            facecolor=COLORS["fermion_actual_positive"],
            label=r"fermion: conjugate Majorana blocks or Kramers give $W_{\rm F}\geq0$ (12/32)",
        ),
        Patch(
            facecolor=COLORS["boson_modulus_square"],
            label=r"boson: $W_{\rm B}=|w|^2$ for physical anticomm. $(+,-)$ pairs (8/32)",
        ),
        Patch(
            facecolor=COLORS["boson_polarization_verified"],
            label="boson B15/B27: positive polarization verified at d=4",
        ),
        Patch(
            facecolor=COLORS["boson_polarization_impossible"],
            label=r"boson B12/B32: impossible for real orthogonal $J_a$",
        ),
        Patch(
            facecolor=COLORS["not_fixed"],
            label="remaining 20/32: five relations do not fix the actual half-power",
        ),
    ]
    figure.legend(
        handles=legend,
        loc="lower center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.052),
        fontsize=8.1,
    )
    figure.text(
        0.5,
        0.013,
        r"Each panel has 8 anticomm. $(+,-)$ classes, 4 anticomm. $(-,-)$ "
        r"classes, and 20 classes not fixed by the five relations.  "
        r"$A_{\rm group}$ labels assume both symmetries hold for every complete "
        r"slice.  * A strict cone is independent (8/32): nonzero "
        r"$A_{\rm cone}$ is mapped to $-A_{\rm cone}$ by $\Theta_2$, so the same "
        r"configuration is not preserved and the $A_{\rm group}$ proof does not apply.",
        ha="center",
        va="bottom",
        fontsize=8.0,
    )
    figure.subplots_adjust(
        left=0.115,
        right=0.99,
        top=0.94,
        bottom=0.17,
        hspace=0.62,
    )

    for suffix in ("pdf", "png"):
        output = FIGURE_DIR / f"full_64_class_enumeration.{suffix}"
        figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
