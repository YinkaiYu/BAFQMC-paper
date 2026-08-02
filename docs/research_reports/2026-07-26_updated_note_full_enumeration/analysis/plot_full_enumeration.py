#!/usr/bin/env python3
"""Plot the 64-class semigroup screen and group-only time-reversal fallback."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import font_manager
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
    "group_only": "#eceff1",
    "strict_j2g": "#8fc49b",
    "strict_ij2g": "#91bdd8",
}
COLOR_ORDER = ["group_only", "strict_j2g", "strict_ij2g"]
TRS_COLOR = "#7b3f00"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def register_cjk_font() -> str:
    """Register a local CJK font because Matplotlib may ignore TTC files."""
    candidates = (
        Path("/mnt/c/Windows/Fonts/msyh.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    )
    for path in candidates:
        if path.exists():
            font_manager.fontManager.addfont(path)
            return font_manager.FontProperties(fname=path).get_name()
    raise RuntimeError("a CJK font is required to render the Chinese atlas labels")


def signed_symbol(sign: int, positive: str) -> str:
    return positive if sign == 1 else "-" + positive


def row_label(values: tuple[int, int]) -> str:
    g_sign, square_sign = values
    return "\n".join(
        (
            rf"$J_1^{{T}}gJ_1={signed_symbol(g_sign, 'g')}$",
            rf"$J_1^2={signed_symbol(square_sign, 'I')}$",
        )
    )


def column_label(values: tuple[int, int, int]) -> str:
    g_sign, square_sign, mutual_sign = values
    mutual_relation = (
        r"$J_1J_2=J_2J_1$"
        if mutual_sign == 1
        else r"$J_1J_2=-J_2J_1$"
    )
    return "\n".join(
        (
            rf"$J_2^{{T}}gJ_2={signed_symbol(g_sign, 'g')}$",
            rf"$J_2^2={signed_symbol(square_sign, 'I')}$",
            mutual_relation,
        )
    )


def time_reversal_pair_type(row: dict[str, str]) -> str | None:
    """Read the two induced time-reversal squares and mutual relation."""
    q1 = int(row["q1"])
    q2 = int(row["q2"])
    s1 = int(row["s1"])
    s2 = int(row["s2"])
    time_reversal_mutual = int(row["r"]) * s1 * s2

    if time_reversal_mutual != -1:
        return None
    if sorted((q1, q2)) == [-1, 1]:
        return "plus_minus"
    if q1 == -1 and q2 == -1:
        return "minus_minus"
    return None


def mechanism_to_trs(mechanism: str) -> str | None:
    if mechanism == "conjugate_subsystems":
        return "plus_minus"
    if mechanism == "kramers_pair":
        return "minus_minus"
    return None


def classify(row: dict[str, str]) -> tuple[str, str]:
    if row["status"] == "strict":
        if row["metric"] == "J2g":
            category = "strict_j2g"
            text = "\u6536\u7f29\u534a\u7fa4\n" + r"$\eta=J_2g$"
        else:
            category = "strict_ij2g"
            text = "\u6536\u7f29\u534a\u7fa4\n" + r"$\eta=iJ_2g$"
    else:
        category = "group_only"
        text = "\u53ea\u6709\u6700\u5927\u5b50\u7fa4"
    return category, text


def validate_atlas(
    rows: list[dict[str, str]],
    half_power_rows: list[dict[str, str]],
) -> dict[tuple[str, int], str | None]:
    """Check the enumeration counts before reducing them to a visual atlas."""
    if len(rows) != 64 or len(half_power_rows) != 64:
        raise ValueError(
            "the two source tables must each contain exactly 64 rows"
        )

    trs_lookup: dict[tuple[str, str], str | None] = {}
    for row in half_power_rows:
        key = (row["statistics"], row["class_id"])
        if key in trs_lookup:
            raise ValueError(f"duplicate half-power class: {key}")
        trs_lookup[key] = mechanism_to_trs(row["group_half_power_mechanism"])

    for statistics in ("boson", "fermion"):
        selected = [row for row in rows if row["statistics"] == statistics]
        if len(selected) != 32:
            raise ValueError(f"expected 32 {statistics} classes")

        strict = [row for row in selected if row["status"] == "strict"]
        group_only = [row for row in selected if row["status"] != "strict"]
        metric_counts = {
            metric: sum(row["metric"] == metric for row in strict)
            for metric in ("J2g", "iJ2g")
        }
        if metric_counts != {"J2g": 4, "iJ2g": 4}:
            raise ValueError(
                f"unexpected {statistics} semigroup metrics: {metric_counts}"
            )
        if len(group_only) != 24:
            raise ValueError(
                f"expected 24 group-only {statistics} classes, "
                f"got {len(group_only)}"
            )

        # These obstruction counts remain useful data checks even though the
        # simplified figure deliberately does not display their derivation.
        obstruction_counts = {
            status: sum(row["status"] == status for row in group_only)
            for status in (
                "boundary_only_trace_obstruction",
                "boundary_only_reality_flip",
            )
        }
        expected_obstructions = {
            "boundary_only_trace_obstruction": 16,
            "boundary_only_reality_flip": 8,
        }
        if obstruction_counts != expected_obstructions:
            raise ValueError(
                f"unexpected {statistics} empty-cone counts: "
                f"{obstruction_counts}"
            )

        trs_counts = {"plus_minus": 0, "minus_minus": 0}
        group_only_trs = 0
        for row in selected:
            key = (statistics, row["class_id"])
            if key not in trs_lookup:
                raise ValueError(f"missing half-power class: {key}")
            trs_type = trs_lookup[key]
            if trs_type is not None:
                trs_counts[trs_type] += 1
                group_only_trs += row["status"] != "strict"
            if trs_type != time_reversal_pair_type(row):
                raise ValueError(
                    "time-reversal label disagrees with the five relations: "
                    f"{key}, table={trs_type}, relations="
                    f"{time_reversal_pair_type(row)}"
                )
        if trs_counts != {"plus_minus": 8, "minus_minus": 4}:
            raise ValueError(
                f"unexpected {statistics} TRS counts: {trs_counts}"
            )
        expected_group_only_trs = 8 if statistics == "boson" else 4
        if group_only_trs != expected_group_only_trs:
            raise ValueError(
                f"unexpected {statistics} group-only TRS count: "
                f"{group_only_trs}"
            )

    return trs_lookup


def panel_data(
    rows: list[dict[str, str]],
    trs_lookup: dict[tuple[str, str], str | None],
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
    color_index = {name: index for index, name in enumerate(COLOR_ORDER)}
    values = np.empty((4, 8), dtype=int)
    labels = [["" for _ in range(8)] for _ in range(4)]
    outlines = np.zeros((4, 8), dtype=bool)
    for row_index, (s1, q1) in enumerate(ROW_KEYS):
        for column_index, (s2, q2, r) in enumerate(COL_KEYS):
            row = lookup[(s1, q1, s2, q2, r)]
            trs_type = trs_lookup[(row["statistics"], row["class_id"])]
            category, text = classify(row)
            values[row_index, column_index] = color_index[category]
            labels[row_index][column_index] = text
            outlines[row_index, column_index] = (
                trs_type is not None and row["status"] != "strict"
            )
    return values, labels, outlines


def main() -> None:
    full_rows = load_rows(FULL_TABLE)
    half_power_rows = load_rows(HALF_POWER_TABLE)
    trs_lookup = validate_atlas(full_rows, half_power_rows)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    cjk_font = register_cjk_font()

    mpl.rcParams.update(
        {
            "font.family": cjk_font,
            "font.size": 12,
            "axes.linewidth": 1.0,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    cmap = ListedColormap([COLORS[name] for name in COLOR_ORDER])
    figure, axes = plt.subplots(2, 1, figsize=(19.5, 10.8))

    for panel, statistics in enumerate(("boson", "fermion")):
        selected = [
            row for row in full_rows if row["statistics"] == statistics
        ]
        values, labels, outlines = panel_data(selected, trs_lookup)
        ax = axes[panel]
        ax.imshow(
            values,
            cmap=cmap,
            vmin=-0.5,
            vmax=len(COLOR_ORDER) - 0.5,
            aspect="auto",
        )
        for row_index in range(4):
            for column_index in range(8):
                ax.text(
                    column_index,
                    row_index,
                    labels[row_index][column_index],
                    ha="center",
                    va="center",
                    fontsize=17.0,
                    fontweight="medium",
                    linespacing=1.18,
                    color="#172126",
                )
                if outlines[row_index, column_index]:
                    ax.add_patch(
                        Rectangle(
                            (column_index - 0.465, row_index - 0.455),
                            0.93,
                            0.91,
                            fill=False,
                            edgecolor=TRS_COLOR,
                            linewidth=3.2,
                        )
                    )

        ax.set_xticks(range(8))
        ax.set_xticklabels(
            [column_label(values) for values in COL_KEYS],
            fontsize=15.0,
            linespacing=1.15,
        )
        ax.xaxis.set_ticks_position("top")
        ax.set_yticks(range(4))
        ax.set_yticklabels(
            [row_label(values) for values in ROW_KEYS],
            fontsize=16.0,
            linespacing=1.18,
        )
        ax.set_xticks(np.arange(-0.5, 8, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 4, 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=1.7)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(which="major", length=0, pad=9)
        ax.set_title(
            "a  \u73bb\u8272\u5b50" if panel == 0 else "b  \u8d39\u7c73\u5b50",
            loc="left",
            fontsize=18,
            fontweight="bold",
            pad=12,
        )

    legend = [
        Patch(
            facecolor=COLORS["strict_j2g"],
            label="\u6536\u7f29\u534a\u7fa4  " + r"$\eta=J_2g$",
        ),
        Patch(
            facecolor=COLORS["strict_ij2g"],
            label="\u6536\u7f29\u534a\u7fa4  " + r"$\eta=iJ_2g$",
        ),
        Patch(
            facecolor=COLORS["group_only"],
            label="\u53ea\u6709\u6700\u5927\u5b50\u7fa4",
        ),
        Patch(
            facecolor="none",
            edgecolor=TRS_COLOR,
            linewidth=3.2,
            label="\u7070\u683c\u7c97\u8fb9\u6846\uff1a\u65f6\u95f4\u53cd\u6f14\u5bf9\u79f0\u6027\u8bc1\u660e\u6743\u91cd\u975e\u8d1f",
        ),
    ]
    figure.legend(
        handles=legend,
        loc="lower center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, 0.018),
        fontsize=14.5,
        handlelength=2.2,
        columnspacing=2.4,
    )
    figure.subplots_adjust(
        left=0.145,
        right=0.992,
        top=0.91,
        bottom=0.105,
        hspace=0.68,
    )

    for suffix in ("pdf", "png"):
        output = FIGURE_DIR / f"full_64_class_enumeration.{suffix}"
        figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
