#!/usr/bin/env python3
"""Plot strict-cone screening with group-only time-reversal fallbacks."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, Rectangle
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FULL_TABLE = ROOT / "tables" / "full_64_class_enumeration.csv"
HALF_POWER_TABLE = ROOT / "tables" / "half_power_symmetry_64_classes.csv"
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
    "empty_trace_obstruction": "#e2e5e7",
    "empty_flip_obstruction": "#efc2b8",
    "strict_j2g": "#70aa7f",
    "strict_ij2g": "#6f9fc4",
}

COLOR_ORDER = [
    "empty_trace_obstruction",
    "empty_flip_obstruction",
    "strict_j2g",
    "strict_ij2g",
]

BOSON_KRAMERS_MIN_DIMENSION = {12: 8, 15: 4, 27: 4, 32: 8}


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


def time_reversal_pair_type(row: dict[str, str]) -> str | None:
    """Classify the two A_group time-reversal symmetries."""
    q1 = int(row["q1"])
    q2 = int(row["q2"])
    s1 = int(row["s1"])
    s2 = int(row["s2"])
    # The induced time-reversal maps anticommute when r*s1*s2 = -1.
    time_reversal_mutual = int(row["r"]) * s1 * s2

    if time_reversal_mutual != -1:
        return None
    if sorted((q1, q2)) == [-1, 1]:
        return "plus_minus"
    if q1 == -1 and q2 == -1:
        return "minus_minus"
    return None


def classify(
    row: dict[str, str], class_number: int
) -> tuple[str, str, bool]:
    """Return cone category, cell text, and group-only positivity outline."""
    if row["status"] == "strict":
        category = (
            "strict_j2g" if row["metric"] == "J2g" else "strict_ij2g"
        )
        metric = r"$J_2g$" if row["metric"] == "J2g" else r"$iJ_2g$"
        if row["statistics"] == "boson" and row["metric"] == "iJ2g":
            description = (
                "strict matrix cone\n"
                + rf"$\eta={metric[1:-1]}$"
                + "\nfixed-$N$ weight"
            )
        else:
            description = (
                "strict cone\n"
                + rf"$\eta={metric[1:-1]}$"
                + "\nsemigroup branch"
            )
        return (
            category,
            description,
            False,
        )

    pair_type = time_reversal_pair_type(row)
    category = (
        "empty_trace_obstruction"
        if row["status"] == "boundary_only_trace_obstruction"
        else "empty_flip_obstruction"
    )
    if row["statistics"] == "fermion" and pair_type == "plus_minus":
        return (
            category,
            "group only\n" + r"$\Theta(+,-)$: $W_{\rm F}\geq0$",
            True,
        )
    if row["statistics"] == "boson" and pair_type == "plus_minus":
        return category, "group only\n" + r"$\Theta(+,-)$: $W_{\rm B}=|w|^2$", True
    if row["statistics"] == "boson" and pair_type == "minus_minus":
        dimension = BOSON_KRAMERS_MIN_DIMENSION[class_number]
        return (
            category,
            "group only\n"
            + r"$\Theta(-,-)$: Kramers"
            + "\n"
            + rf"physical $d_{{\rm N}}={dimension}$",
            True,
        )
    return category, "group only\nno theorem from\noriginal $J_1,J_2$", False


def validate_atlas(
    rows: list[dict[str, str]],
    half_power_rows: list[dict[str, str]],
) -> None:
    """Guard cone counts and the empty-cone time-reversal fallback counts."""
    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        strict = [row for row in selected if row["status"] == "strict"]
        empty = [row for row in selected if row["status"] != "strict"]
        metric_counts = {
            metric: sum(row["metric"] == metric for row in strict)
            for metric in ("J2g", "iJ2g")
        }
        obstruction_counts = {
            status: sum(row["status"] == status for row in empty)
            for status in (
                "boundary_only_trace_obstruction",
                "boundary_only_reality_flip",
            )
        }
        if metric_counts != {"J2g": 4, "iJ2g": 4}:
            raise ValueError(
                f"unexpected {statistics} strict metrics: {metric_counts}"
            )
        expected_obstructions = {
            "boundary_only_trace_obstruction": 16,
            "boundary_only_reality_flip": 8,
        }
        if obstruction_counts != expected_obstructions:
            raise ValueError(
                f"unexpected {statistics} empty-cone counts: {obstruction_counts}"
            )

        positives = 0
        for class_number, row in enumerate(selected, start=1):
            if row["status"] == "strict":
                continue
            _, _, positive = classify(row, class_number)
            positives += positive
        expected_positive = 8 if statistics == "boson" else 4
        if positives != expected_positive:
            raise ValueError(
                f"expected {expected_positive} group-only positive {statistics} "
                f"classes, got {positives}"
            )

    evidence_positive: dict[str, set[int]] = {"boson": set(), "fermion": set()}
    for row in half_power_rows:
        if int(row["strict_cone_exists"]):
            continue
        mechanism = row["group_half_power_mechanism"]
        result = row["group_actual_weight_result"]
        if row["statistics"] == "fermion" and mechanism in {
            "conjugate_subsystems",
            "kramers_pair",
        }:
            evidence_positive["fermion"].add(int(row["class_number"]))
        if row["statistics"] == "boson" and mechanism in {
            "conjugate_subsystems",
            "kramers_pair",
        } and r"W_{\rm B}" in result:
            evidence_positive["boson"].add(int(row["class_number"]))

    plotted_positive: dict[str, set[int]] = {"boson": set(), "fermion": set()}
    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        for class_number, row in enumerate(selected, start=1):
            if row["status"] != "strict" and classify(row, class_number)[2]:
                plotted_positive[statistics].add(class_number)
    if plotted_positive != evidence_positive:
        raise ValueError(
            "figure outlines disagree with half-power evidence table: "
            f"plot={plotted_positive}, evidence={evidence_positive}"
        )


def panel_data(
    rows: list[dict[str, str]],
) -> tuple[np.ndarray, list[list[str]], np.ndarray]:
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
    outlines = np.zeros((4, 8), dtype=bool)
    for i, (s1, q1) in enumerate(ROW_KEYS):
        for j, (s2, q2, r) in enumerate(COL_KEYS):
            number, row = lookup[(s1, q1, s2, q2, r)]
            category, description, outlined = classify(row, number)
            values[i, j] = color_index[category]
            outlines[i, j] = outlined
            prefix = "B" if row["statistics"] == "boson" else "F"
            dimension = 2 ** int(row["min_qubits"])
            labels[i][j] = (
                f"{prefix}{number:02d}   "
                + rf"$d_{{\rm alg}}={dimension}$"
                + "\n"
                + description
            )
    return values, labels, outlines


def main() -> None:
    full_rows = load_rows(FULL_TABLE)
    half_power_rows = load_rows(HALF_POWER_TABLE)
    validate_atlas(full_rows, half_power_rows)
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
        values, labels, outlines = panel_data(selected)
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
                    fontsize=6.8,
                    linespacing=1.16,
                    color="#172126",
                )
                if outlines[row_index, col_index]:
                    ax.add_patch(
                        Rectangle(
                            (col_index - 0.47, row_index - 0.47),
                            0.94,
                            0.94,
                            fill=False,
                            edgecolor="#174f46",
                            linewidth=2.5,
                        )
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
                r"a  Boson: strict-cone screening; group-only time-reversal fallback"
                if panel == 0
                else r"b  Fermion: strict-cone screening; group-only time-reversal fallback"
            ),
            loc="left",
            fontweight="bold",
            pad=7,
        )

    legend = [
        Patch(
            facecolor=COLORS["strict_j2g"],
            label=r"strict cone: $\eta=J_2g$ (4/32 per panel)",
        ),
        Patch(
            facecolor=COLORS["strict_ij2g"],
            label=r"strict cone: $\eta=iJ_2g$ (4/32 per panel)",
        ),
        Patch(
            facecolor=COLORS["empty_trace_obstruction"],
            label="first screen: cone empty by Lemma 1 (16/32)",
        ),
        Patch(
            facecolor=COLORS["empty_flip_obstruction"],
            label="second screen: remaining cone empty by Lemma 2 (8/32)",
        ),
        Patch(
            facecolor="none",
            edgecolor="#174f46",
            linewidth=2.5,
            label=(
                "outlined group-only cell: time-reversal theorem proves "
                "the weight nonnegative"
            ),
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
        r"Primary classification: 8 strict-cone classes and 24 group-only classes per panel.  "
        r"Time-reversal positivity is tested only for the group-only cells: 8 bosonic and "
        r"4 fermionic classes have a verified physical representation using their original "
        r"$J_1,J_2$ pair.  Blue bosonic cells use fixed-$N$ weights.",
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
