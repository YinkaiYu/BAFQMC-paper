#!/usr/bin/env python3
"""Draw the bosonic and fermionic contraction-semigroup classifications."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "research_reports" / "2026-07-26_updated_note_full_enumeration"
ENUMERATION = REPORT / "tables" / "full_64_class_enumeration.csv"
TIME_REVERSAL = REPORT / "tables" / "half_power_symmetry_64_classes.csv"
OUTPUT_PDF = ROOT / "figures" / "contraction_semigroup_periodic_table.pdf"
OUTPUT_PNG = ROOT / "figures" / "contraction_semigroup_periodic_table.png"


ROW_RELATIONS = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

COLUMN_RELATIONS = [
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
]

CATEGORIES = ("group", "J2g", "iJ2g")
COLORS = ("#F0F1EF", "#CFE4D1", "#CFE1ED")
TIME_REVERSAL_COLOR = "#8C2D4B"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def signed_right_hand_side(sign: int, symbol: str) -> str:
    return symbol if sign == 1 else f"-{symbol}"


def row_label(relations: tuple[int, int]) -> str:
    metric_sign, square_sign = relations
    return "\n".join(
        (
            rf"$J_1^{{\mathsf{{T}}}}gJ_1={signed_right_hand_side(metric_sign, 'g')}$",
            rf"$J_1^2={signed_right_hand_side(square_sign, 'I')}$",
        )
    )


def column_label(relations: tuple[int, int, int]) -> str:
    metric_sign, square_sign, mutual_sign = relations
    mutual_relation = (
        r"$J_1J_2=J_2J_1$"
        if mutual_sign == 1
        else r"$J_1J_2=-J_2J_1$"
    )
    return "\n".join(
        (
            rf"$J_2^{{\mathsf{{T}}}}gJ_2={signed_right_hand_side(metric_sign, 'g')}$",
            rf"$J_2^2={signed_right_hand_side(square_sign, 'I')}$",
            mutual_relation,
        )
    )


def cell_category(row: dict[str, str]) -> tuple[int, str]:
    if row["status"] != "strict":
        return CATEGORIES.index("group"), "maximal\nsubgroup\nonly"
    if row["metric"] == "J2g":
        return CATEGORIES.index("J2g"), "contraction\nsemigroup\n$\\eta=J_2g$"
    if row["metric"] == "iJ2g":
        return CATEGORIES.index("iJ2g"), "contraction\nsemigroup\n$\\eta=iJ_2g$"
    raise ValueError(f"unknown metric in {row['class_id']}: {row['metric']}")


def time_reversal_positive_classes(
    rows: list[dict[str, str]],
) -> set[tuple[str, str]]:
    positive = set()
    for row in rows:
        if row["group_half_power_mechanism"] in {
            "conjugate_subsystems",
            "kramers_pair",
        }:
            positive.add((row["statistics"], row["class_id"]))
    return positive


def validate(
    enumeration: list[dict[str, str]],
    time_reversal_positive: set[tuple[str, str]],
) -> None:
    if len(enumeration) != 64:
        raise ValueError(f"expected 64 classes, found {len(enumeration)}")

    for statistics, expected_outlined in (("boson", 8), ("fermion", 4)):
        rows = [row for row in enumeration if row["statistics"] == statistics]
        semigroups = [row for row in rows if row["status"] == "strict"]
        if len(rows) != 32 or len(semigroups) != 8:
            raise ValueError(
                f"unexpected {statistics} counts: {len(rows)} classes, "
                f"{len(semigroups)} semigroups"
            )
        metric_counts = {
            metric: sum(row["metric"] == metric for row in semigroups)
            for metric in ("J2g", "iJ2g")
        }
        if metric_counts != {"J2g": 4, "iJ2g": 4}:
            raise ValueError(f"unexpected {statistics} metric counts: {metric_counts}")

        outlined = sum(
            row["status"] != "strict"
            and (statistics, row["class_id"]) in time_reversal_positive
            for row in rows
        )
        if outlined != expected_outlined:
            raise ValueError(
                f"expected {expected_outlined} outlined {statistics} cells, "
                f"found {outlined}"
            )


def panel_arrays(
    rows: list[dict[str, str]],
    time_reversal_positive: set[tuple[str, str]],
) -> tuple[np.ndarray, list[list[str]], np.ndarray]:
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

    colors = np.zeros((4, 8), dtype=int)
    labels = [["" for _ in range(8)] for _ in range(4)]
    outlines = np.zeros((4, 8), dtype=bool)

    for row_index, first_relations in enumerate(ROW_RELATIONS):
        for column_index, second_relations in enumerate(COLUMN_RELATIONS):
            row = lookup[(*first_relations, *second_relations)]
            colors[row_index, column_index], labels[row_index][column_index] = (
                cell_category(row)
            )
            outlines[row_index, column_index] = (
                row["status"] != "strict"
                and (row["statistics"], row["class_id"])
                in time_reversal_positive
            )

    return colors, labels, outlines


def draw_panel(
    ax: plt.Axes,
    rows: list[dict[str, str]],
    time_reversal_positive: set[tuple[str, str]],
    panel_label: str,
    title: str,
) -> None:
    colors, labels, outlines = panel_arrays(rows, time_reversal_positive)
    ax.imshow(
        colors,
        cmap=ListedColormap(COLORS),
        vmin=-0.5,
        vmax=len(CATEGORIES) - 0.5,
        aspect="auto",
        interpolation="nearest",
    )

    for row_index in range(4):
        for column_index in range(8):
            ax.text(
                column_index,
                row_index,
                labels[row_index][column_index],
                ha="center",
                va="center",
                fontsize=5.9,
                linespacing=1.04,
                color="#202528",
            )
            if outlines[row_index, column_index]:
                ax.add_patch(
                    Rectangle(
                        (column_index - 0.46, row_index - 0.44),
                        0.92,
                        0.88,
                        facecolor="none",
                        edgecolor=TIME_REVERSAL_COLOR,
                        linewidth=1.7,
                        joinstyle="miter",
                    )
                )

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(3.5, -0.5)
    ax.set_xticks(range(8))
    ax.set_xticklabels(
        [column_label(relations) for relations in COLUMN_RELATIONS],
        fontsize=5.5,
        linespacing=1.08,
    )
    ax.xaxis.tick_top()
    ax.set_yticks(range(4))
    ax.set_yticklabels(
        [row_label(relations) for relations in ROW_RELATIONS],
        fontsize=7.0,
        linespacing=1.15,
        ha="right",
    )
    ax.tick_params(axis="x", length=0, pad=5.0)
    ax.tick_params(axis="y", length=0, pad=6.0)

    ax.set_xticks(np.arange(-0.5, 8.0, 1.0), minor=True)
    ax.set_yticks(np.arange(-0.5, 4.0, 1.0), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.1)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.65)
        spine.set_color("#5A6063")

    ax.text(
        -0.145,
        1.29,
        panel_label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
    )
    ax.text(
        -0.095,
        1.29,
        title,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
    )


def main() -> None:
    enumeration = read_csv(ENUMERATION)
    positive = time_reversal_positive_classes(read_csv(TIME_REVERSAL))
    validate(enumeration, positive)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "mathtext.fontset": "dejavusans",
            "axes.linewidth": 0.65,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )

    figure, axes = plt.subplots(2, 1, figsize=(7.05, 6.35))
    for ax, statistics, panel_label, title in zip(
        axes,
        ("boson", "fermion"),
        ("(a)", "(b)"),
        ("Bosons", "Fermions"),
        strict=True,
    ):
        draw_panel(
            ax,
            [row for row in enumeration if row["statistics"] == statistics],
            positive,
            panel_label,
            title,
        )

    key_x = 0.175
    key_y = 0.023
    key_width = 0.033
    key_height = 0.025
    figure.add_artist(
        Rectangle(
            (key_x, key_y),
            key_width,
            key_height,
            transform=figure.transFigure,
            facecolor=COLORS[0],
            edgecolor=TIME_REVERSAL_COLOR,
            linewidth=1.7,
            clip_on=False,
        )
    )
    figure.text(
        key_x + key_width + 0.012,
        key_y + key_height / 2,
        "Outlined maximal-subgroup cells admit time-reversal-positive representatives.",
        ha="left",
        va="center",
        fontsize=7.2,
        color="#303538",
    )

    figure.subplots_adjust(
        left=0.205,
        right=0.993,
        top=0.865,
        bottom=0.09,
        hspace=0.77,
    )

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight", pad_inches=0.025)
    figure.savefig(OUTPUT_PNG, dpi=320, bbox_inches="tight", pad_inches=0.025)
    plt.close(figure)


if __name__ == "__main__":
    main()
