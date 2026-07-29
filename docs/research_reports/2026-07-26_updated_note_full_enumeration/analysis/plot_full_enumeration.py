#!/usr/bin/env python3
"""Plot the 64-class atlas as an annotated periodic table."""

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
MAXIMAL_TABLE = ROOT / "tables" / "maximal_subgroup_structures.csv"
PHYSICAL_BOSON_TABLE = (
    ROOT / "tables" / "bosonic_physical_representation_suborbits_le4.csv"
)
FIGURE_DIR = ROOT / "figures"

BOSON_TRS_CLASS = "s1+_q1-_s2-_q2-_r+"
BOSON_RP_CLASS = "s1+_q1+_s2+_q2-_r-"

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
    "group_trace": "#e2e5e7",
    "group_flip": "#efc2b8",
    "cone_j2g": "#70aa7f",
    "cone_ij2g": "#6f9fc4",
    "trs": "#e3bf61",
    "rp": "#d99a62",
    "mtr": "#d8b56f",
}

COLOR_ORDER = [
    "group_trace",
    "group_flip",
    "cone_j2g",
    "cone_ij2g",
    "trs",
    "rp",
    "mtr",
]


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
    mutual = int(row["r"]) * int(row["s1"]) * int(row["s2"])
    squares = sorted((int(row["q1"]), int(row["q2"])))
    if mutual == -1 and squares == [-1, 1]:
        return "Θ(+,-)"
    if (
        mutual == -1
        and int(row["q1"]) == -1
        and int(row["q2"]) == -1
    ):
        return "Θ(-,-)"
    return None


def classify(
    row: dict[str, str],
    maximal: dict[tuple[str, str], dict[str, str]],
    physical_boson_counts: dict[str, int],
) -> tuple[str, str, str]:
    """Return color category, positivity label, cone detail."""
    if row["status"] == "strict":
        cone = "C(J)" if row["metric"] == "J2g" else "C(iJ)"
        if (
            row["statistics"] == "fermion"
            and int(
                maximal[(row["statistics"], row["class_id"])][
                    "maximal_subgroup_sign_guaranteed"
                ]
            )
        ):
            cone += "+Θ"
        color = "cone_j2g" if row["metric"] == "J2g" else "cone_ij2g"
        return color, cone, "strict cone"

    obstruction = (
        "cone: Lemma 1"
        if row["status"] == "boundary_only_trace_obstruction"
        else "cone: Lemma 2"
    )
    if row["statistics"] == "boson" and row["class_id"] == BOSON_RP_CLASS:
        count = physical_boson_counts.get(row["class_id"], 0)
        return "rp", f"Θ(+,-)+RP; p={count}", obstruction
    pair_type = anti_linear_pair_type(row)
    if row["statistics"] == "boson" and pair_type is not None:
        count = physical_boson_counts.get(row["class_id"], 0)
        return "trs", f"{pair_type}; p={count}", obstruction
    if (
        row["statistics"] == "fermion"
        and int(
            maximal[(row["statistics"], row["class_id"])][
                "maximal_subgroup_sign_guaranteed"
            ]
        )
    ):
        return "mtr", pair_type or "Θ-pair", obstruction
    if (
        row["statistics"] == "fermion"
        and row["class_id"] == "s1+_q1+_s2+_q2+_r+"
    ):
        return "mtr", "SO / split-O", obstruction
    color = (
        "group_trace"
        if row["status"] == "boundary_only_trace_obstruction"
        else "group_flip"
    )
    return color, "G; +Θ3", obstruction


def panel_data(
    rows: list[dict[str, str]],
    maximal: dict[tuple[str, str], dict[str, str]],
    physical_boson_counts: dict[str, int],
) -> tuple[np.ndarray, list[list[str]]]:
    lookup = {
        (
            int(row["s1"]),
            int(row["q1"]),
            int(row["s2"]),
            int(row["q2"]),
            int(row["r"]),
        ): row
        for row in rows
    }
    color_index = {name: index for index, name in enumerate(COLOR_ORDER)}
    values = np.empty((4, 8), dtype=int)
    labels = [["" for _ in range(8)] for _ in range(4)]
    for i, (s1, q1) in enumerate(ROW_KEYS):
        for j, (s2, q2, r) in enumerate(COL_KEYS):
            row = lookup[(s1, q1, s2, q2, r)]
            category, positivity, cone_detail = classify(
                row, maximal, physical_boson_counts
            )
            values[i, j] = color_index[category]
            prefix = "B" if row["statistics"] == "boson" else "F"
            number = rows.index(row) + 1
            dimension = 2 ** int(row["min_qubits"])
            labels[i][j] = (
                f"{prefix}{number:02d}   d={dimension}\n"
                f"{positivity}\n{cone_detail}"
            )
    return values, labels


def main() -> None:
    full_rows = load_rows(FULL_TABLE)
    maximal_rows = {
        (row["statistics"], row["class_id"]): row
        for row in load_rows(MAXIMAL_TABLE)
    }
    physical_boson_counts: dict[str, int] = {}
    for row in load_rows(PHYSICAL_BOSON_TABLE):
        physical_boson_counts[row["class_id"]] = (
            physical_boson_counts.get(row["class_id"], 0) + 1
        )
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
    figure, axes = plt.subplots(2, 1, figsize=(13.2, 8.7))

    for panel, statistics in enumerate(("boson", "fermion")):
        selected = [
            row for row in full_rows if row["statistics"] == statistics
        ]
        values, labels = panel_data(
            selected, maximal_rows, physical_boson_counts
        )
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
                    fontsize=7.2,
                    linespacing=1.22,
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
            ("a  Boson" if panel == 0 else "b  Fermion"),
            loc="left",
            fontweight="bold",
            pad=7,
        )

    legend = [
        Patch(facecolor=COLORS["cone_j2g"], label=r"strict cone, $\eta=J_2g$"),
        Patch(facecolor=COLORS["cone_ij2g"], label=r"strict cone, $\eta=iJ_2g$"),
        Patch(
            facecolor=COLORS["trs"],
            label="bosonic physical anti-linear pair (p = low-d physical orbits)",
        ),
        Patch(
            facecolor=COLORS["rp"],
            label="bosonic reflected-factor class plus RP condition",
        ),
        Patch(
            facecolor=COLORS["mtr"],
            label="fermionic anti-linear, compact-SO, or split-O theorem",
        ),
        Patch(facecolor=COLORS["group_trace"], label=r"group only; $\mathrm{Tr}H=0$"),
        Patch(facecolor=COLORS["group_flip"], label=r"group only; $J_1$ flips $H$"),
    ]
    figure.legend(
        handles=legend,
        loc="lower center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, 0.005),
        fontsize=8.4,
    )
    figure.subplots_adjust(
        left=0.115,
        right=0.99,
        top=0.94,
        bottom=0.13,
        hspace=0.62,
    )

    for suffix in ("pdf", "png"):
        output = FIGURE_DIR / f"full_64_class_enumeration.{suffix}"
        figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
