#!/usr/bin/env python3
"""Draw the contraction-semigroup and time-reversal periodic table."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "experts" / "time_reversal_subspaces_64.csv"
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
CATEGORY_COLORS = ("#F0F1EF", "#CFE4D1", "#CFE1ED")
BADGE_COLORS = {
    "M": "#8C2D4B",
    "K": "#315F83",
    "S": "#8A6500",
}

FIGURE_WIDTH = 7.05
FIGURE_HEIGHT = 4.72
GRID_LEFT = 0.183
GRID_RIGHT = 0.992
GRID_WIDTH = GRID_RIGHT - GRID_LEFT
PANEL_HEIGHT = 0.225
TOP_PANEL_BOTTOM = 0.500
BOTTOM_PANEL_BOTTOM = 0.190


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


def category_index(row: dict[str, str]) -> int:
    if row["semigroup_status"] == "maximal subgroup only":
        if row["metric"]:
            raise ValueError(
                f"group-only class {row['class_id']} unexpectedly has metric "
                f"{row['metric']}"
            )
        return CATEGORIES.index("group")

    if row["semigroup_status"] != "contraction semigroup":
        raise ValueError(
            f"unknown semigroup status in {row['class_id']}: "
            f"{row['semigroup_status']}"
        )
    if row["metric"] not in {"J2g", "iJ2g"}:
        raise ValueError(
            f"unknown contraction metric in {row['class_id']}: {row['metric']}"
        )
    return CATEGORIES.index(row["metric"])


def badge_properties(row: dict[str, str]) -> tuple[str, bool]:
    class_to_letter = {
        "Majorana": "M",
        "Kramers": "K",
        "split-orthogonal": "S",
    }
    try:
        letter = class_to_letter[row["time_reversal_class"]]
    except KeyError as error:
        raise ValueError(
            f"unknown time-reversal class in {row['class_id']}: "
            f"{row['time_reversal_class']}"
        ) from error

    if row["time_reversal_result"] == "whole A_group":
        whole_space = True
    elif row["time_reversal_result"] == "proper A_group subspace":
        whole_space = False
    else:
        raise ValueError(
            f"unknown time-reversal result in {row['class_id']}: "
            f"{row['time_reversal_result']}"
        )

    expected_tag = letter if whole_space else f"{letter}*"
    if row["figure_tag"] != expected_tag:
        raise ValueError(
            f"inconsistent figure tag in {row['class_id']}: "
            f"expected {expected_tag}, found {row['figure_tag']}"
        )
    if whole_space and letter == "S":
        raise ValueError(
            f"the figure convention reserves S for a proper subspace: "
            f"{row['class_id']}"
        )
    return letter, whole_space


def validate(rows: list[dict[str, str]]) -> None:
    if len(rows) != 64:
        raise ValueError(f"expected 64 classes, found {len(rows)}")

    keys = {(row["statistics"], row["class_id"]) for row in rows}
    if len(keys) != len(rows):
        raise ValueError("classification contains duplicate class identifiers")

    for statistics in ("boson", "fermion"):
        statistics_rows = [row for row in rows if row["statistics"] == statistics]
        if len(statistics_rows) != 32:
            raise ValueError(
                f"expected 32 {statistics} classes, found {len(statistics_rows)}"
            )

        relation_lookup = {
            (
                int(row["s1"]),
                int(row["q1"]),
                int(row["s2"]),
                int(row["q2"]),
                int(row["r"]),
            ): row
            for row in statistics_rows
        }
        if len(relation_lookup) != 32:
            raise ValueError(f"duplicate five-relation class for {statistics}")

        for row_index, first_relations in enumerate(ROW_RELATIONS):
            for column_index, second_relations in enumerate(COLUMN_RELATIONS):
                row = relation_lookup[(*first_relations, *second_relations)]
                expected_number = row_index * 8 + column_index + 1
                if int(row["class_number"]) != expected_number:
                    raise ValueError(
                        f"unexpected number for {row['class_id']}: "
                        f"expected {expected_number}, found {row['class_number']}"
                    )

        semigroups = [
            row
            for row in statistics_rows
            if row["semigroup_status"] == "contraction semigroup"
        ]
        if len(semigroups) != 8:
            raise ValueError(
                f"expected eight {statistics} semigroup classes, "
                f"found {len(semigroups)}"
            )
        metric_counts = Counter(row["metric"] for row in semigroups)
        if metric_counts != Counter({"J2g": 4, "iJ2g": 4}):
            raise ValueError(
                f"unexpected {statistics} metric counts: {metric_counts}"
            )

    for row in rows:
        category_index(row)
        _, whole_space = badge_properties(row)
        full_dimension = int(row["A_group_dimension"])
        subspace_dimension = int(row["time_reversal_subspace_dimension"])
        if full_dimension <= 0 or subspace_dimension <= 0:
            raise ValueError(f"empty generator space in {row['class_id']}")
        if whole_space and subspace_dimension != full_dimension:
            raise ValueError(
                f"whole-space badge has unequal dimensions in {row['class_id']}"
            )
        if not whole_space and not subspace_dimension < full_dimension:
            raise ValueError(
                f"proper-subspace badge is not proper in {row['class_id']}"
            )


def panel_lookup(rows: list[dict[str, str]]) -> dict[tuple[int, ...], dict[str, str]]:
    return {
        (
            int(row["s1"]),
            int(row["q1"]),
            int(row["s2"]),
            int(row["q2"]),
            int(row["r"]),
        ): row
        for row in rows
    }


def draw_badge(
    ax: plt.Axes,
    x: float,
    y: float,
    letter: str,
    whole_space: bool,
) -> None:
    width = 0.27
    height = 0.35
    color = BADGE_COLORS[letter]
    ax.add_patch(
        Rectangle(
            (x - width / 2, y - height / 2),
            width,
            height,
            facecolor=color if whole_space else "none",
            edgecolor=color,
            linewidth=1.05,
            joinstyle="miter",
            zorder=4,
        )
    )
    ax.text(
        x,
        y - 0.01,
        letter,
        ha="center",
        va="center",
        fontsize=6.6,
        fontweight="bold",
        color="white" if whole_space else color,
        zorder=5,
    )


def draw_panel(
    ax: plt.Axes,
    rows: list[dict[str, str]],
    statistics_prefix: str,
) -> None:
    lookup = panel_lookup(rows)
    categories = np.zeros((4, 8), dtype=int)

    for row_index, first_relations in enumerate(ROW_RELATIONS):
        for column_index, second_relations in enumerate(COLUMN_RELATIONS):
            row = lookup[(*first_relations, *second_relations)]
            categories[row_index, column_index] = category_index(row)

    ax.imshow(
        categories,
        cmap=ListedColormap(CATEGORY_COLORS),
        vmin=-0.5,
        vmax=len(CATEGORIES) - 0.5,
        aspect="auto",
        interpolation="nearest",
    )

    for row_index, first_relations in enumerate(ROW_RELATIONS):
        for column_index, second_relations in enumerate(COLUMN_RELATIONS):
            row = lookup[(*first_relations, *second_relations)]
            class_label = f"{statistics_prefix}{int(row['class_number']):02d}"
            letter, whole_space = badge_properties(row)
            ax.text(
                column_index - 0.41,
                row_index - 0.33,
                class_label,
                ha="left",
                va="top",
                fontsize=7.0,
                fontweight="bold",
                color="#24292C",
                zorder=5,
            )
            draw_badge(
                ax,
                column_index + 0.23,
                row_index + 0.17,
                letter,
                whole_space,
            )

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(3.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks(range(4))
    ax.set_yticklabels(
        [row_label(relations) for relations in ROW_RELATIONS],
        fontsize=7.1,
        linespacing=1.12,
        ha="right",
    )
    ax.tick_params(axis="y", length=0, pad=7.0)

    ax.set_xticks(np.arange(-0.5, 8.0, 1.0), minor=True)
    ax.set_yticks(np.arange(-0.5, 4.0, 1.0), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for boundary, linewidth in ((1.5, 0.55), (3.5, 0.9), (5.5, 0.55)):
        ax.axvline(boundary, color="#62696C", linewidth=linewidth, zorder=3)
    ax.axhline(1.5, color="#62696C", linewidth=0.75, zorder=3)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.7)
        spine.set_color("#555C60")


def draw_span(
    ax: plt.Axes,
    x0: float,
    x1: float,
    y: float,
    label: str,
    fontsize: float,
) -> None:
    ax.plot([x0, x1], [y, y], color="#60676A", linewidth=0.65, clip_on=False)
    tick = 0.035
    ax.plot([x0, x0], [y, y + tick], color="#60676A", linewidth=0.65, clip_on=False)
    ax.plot([x1, x1], [y, y + tick], color="#60676A", linewidth=0.65, clip_on=False)
    ax.text(
        (x0 + x1) / 2,
        y + 0.055,
        label,
        ha="center",
        va="bottom",
        fontsize=fontsize,
        color="#202528",
    )


def draw_shared_column_header(figure: plt.Figure) -> None:
    ax = figure.add_axes([GRID_LEFT, 0.790, GRID_WIDTH, 0.190])
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    draw_span(ax, -0.46, 3.46, 0.765, r"$J_2^{\mathsf{T}}gJ_2=g$", 7.4)
    draw_span(ax, 3.54, 7.46, 0.765, r"$J_2^{\mathsf{T}}gJ_2=-g$", 7.4)

    for center, square_sign in ((0.5, 1), (2.5, -1), (4.5, 1), (6.5, -1)):
        draw_span(
            ax,
            center - 0.96,
            center + 0.96,
            0.455,
            rf"$J_2^2={signed_right_hand_side(square_sign, 'I')}$",
            6.9,
        )

    for column_index, (_, _, mutual_sign) in enumerate(COLUMN_RELATIONS):
        relation = (
            r"$J_1J_2=J_2J_1$"
            if mutual_sign == 1
            else r"$J_1J_2=-J_2J_1$"
        )
        ax.text(
            column_index,
            0.105,
            relation,
            ha="center",
            va="center",
            fontsize=6.8,
            color="#202528",
        )


def figure_rectangle(
    figure: plt.Figure,
    x: float,
    y: float,
    width: float,
    height: float,
    facecolor: str,
    edgecolor: str = "#596064",
    linewidth: float = 0.65,
) -> None:
    figure.add_artist(
        Rectangle(
            (x, y),
            width,
            height,
            transform=figure.transFigure,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            clip_on=False,
        )
    )


def figure_badge(
    figure: plt.Figure,
    x: float,
    y: float,
    letter: str,
    whole_space: bool,
) -> None:
    width = 0.024
    height = 0.031
    color = BADGE_COLORS[letter]
    figure_rectangle(
        figure,
        x,
        y,
        width,
        height,
        color if whole_space else "none",
        color,
        0.9,
    )
    figure.text(
        x + width / 2,
        y + height / 2 - 0.001,
        letter,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight="bold",
        color="white" if whole_space else color,
    )


def draw_legend(figure: plt.Figure) -> None:
    swatch_width = 0.027
    swatch_height = 0.024
    fill_items = (
        (0.130, CATEGORY_COLORS[0], r"$A_{\rm group}$ only"),
        (
            0.354,
            CATEGORY_COLORS[1],
            r"$\eta A_{\rm cone}<0$, $\eta=J_2g$",
        ),
        (
            0.675,
            CATEGORY_COLORS[2],
            r"$\eta A_{\rm cone}<0$, $\eta=\mathrm{i}J_2g$",
        ),
    )
    for x, color, label in fill_items:
        figure_rectangle(
            figure,
            x,
            0.132,
            swatch_width,
            swatch_height,
            color,
        )
        figure.text(
            x + swatch_width + 0.009,
            0.144,
            label,
            ha="left",
            va="center",
            fontsize=6.7,
            color="#303538",
        )

    badge_items = (
        (0.090, "M", True, r"Majorana $\{+,-\}$"),
        (0.290, "K", True, r"Kramers $\{-,-\}$"),
        (0.455, "S", False, r"split-orthogonal $\{+,+,+\}$"),
    )
    for x, letter, whole_space, label in badge_items:
        figure_badge(figure, x, 0.068, letter, whole_space)
        figure.text(
            x + 0.033,
            0.083,
            label,
            ha="left",
            va="center",
            fontsize=6.5,
            color="#303538",
        )

    figure_rectangle(
        figure,
        0.238,
        0.018,
        0.022,
        0.026,
        "#4D5356",
        "#4D5356",
        0.8,
    )
    figure.text(
        0.269,
        0.031,
        r"filled badge = whole $A_{\rm group}$",
        ha="left",
        va="center",
        fontsize=6.9,
        color="#303538",
    )
    figure_rectangle(
        figure,
        0.515,
        0.018,
        0.022,
        0.026,
        "none",
        "#4D5356",
        0.9,
    )
    figure.text(
        0.546,
        0.031,
        r"outlined badge = restricted nonzero part of $A_{\rm group}$",
        ha="left",
        va="center",
        fontsize=6.9,
        color="#303538",
    )


def print_summary(rows: list[dict[str, str]]) -> None:
    print(f"Validated {len(rows)} classes from {CLASSIFICATION}")
    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        semigroup_counts = Counter(
            row["metric"]
            for row in selected
            if row["semigroup_status"] == "contraction semigroup"
        )
        badge_counts = Counter(row["figure_tag"] for row in selected)
        print(
            f"  {statistics}: metrics {dict(semigroup_counts)}, "
            f"badges {dict(sorted(badge_counts.items()))}"
        )


def main() -> None:
    rows = read_csv(CLASSIFICATION)
    validate(rows)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "mathtext.fontset": "dejavusans",
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )

    figure = plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    top_ax = figure.add_axes(
        [GRID_LEFT, TOP_PANEL_BOTTOM, GRID_WIDTH, PANEL_HEIGHT]
    )
    bottom_ax = figure.add_axes(
        [GRID_LEFT, BOTTOM_PANEL_BOTTOM, GRID_WIDTH, PANEL_HEIGHT]
    )

    draw_panel(
        top_ax,
        [row for row in rows if row["statistics"] == "boson"],
        "B",
    )
    draw_panel(
        bottom_ax,
        [row for row in rows if row["statistics"] == "fermion"],
        "F",
    )
    draw_shared_column_header(figure)

    figure.text(
        0.018,
        TOP_PANEL_BOTTOM + PANEL_HEIGHT + 0.022,
        "(a)  Bosons",
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
        color="#171A1C",
    )
    figure.text(
        0.018,
        BOTTOM_PANEL_BOTTOM + PANEL_HEIGHT + 0.022,
        "(b)  Fermions",
        ha="left",
        va="bottom",
        fontsize=9.2,
        fontweight="bold",
        color="#171A1C",
    )
    draw_legend(figure)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF)
    figure.savefig(OUTPUT_PNG, dpi=320)
    plt.close(figure)

    print_summary(rows)
    print(f"Wrote {OUTPUT_PDF}")
    print(f"Wrote {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
