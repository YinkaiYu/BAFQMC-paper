#!/usr/bin/env python3
from pathlib import Path
import csv

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TABLE = ROOT / "tables" / "full_64_class_enumeration.csv"
FIGURE_DIR = ROOT / "figures"


def g_relation(index, value):
    right_hand_side = "g" if int(value) == 1 else "-g"
    return rf"$J_{index}^TgJ_{index}={right_hand_side}$"


def square_relation(index, value):
    right_hand_side = "I" if int(value) == 1 else "-I"
    return rf"$J_{index}^2={right_hand_side}$"


def mutual_relation(value):
    if int(value) == 1:
        return r"$[J_1,J_2]=0$"
    return r"$\{J_1,J_2\}=0$"


def load_rows():
    with TABLE.open(newline="") as handle:
        return list(csv.DictReader(handle))


def class_code(row):
    if row["status"] == "boundary_only_trace_obstruction":
        return 0
    if row["status"] == "boundary_only_reality_flip":
        return 1
    if row["metric"] == "J2g":
        return 2
    return 3


def panel_matrix(rows):
    row_keys = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    col_keys = [
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
        (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
    ]
    lookup = {
        (
            int(row["s1"]), int(row["q1"]), int(row["s2"]),
            int(row["q2"]), int(row["r"])
        ): class_code(row)
        for row in rows
    }
    values = np.empty((len(row_keys), len(col_keys)), dtype=int)
    for i, (s1, q1) in enumerate(row_keys):
        for j, (s2, q2, r) in enumerate(col_keys):
            values[i, j] = lookup[(s1, q1, s2, q2, r)]
    return row_keys, col_keys, values


def main():
    rows = load_rows()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.linewidth": 0.75,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    colors = ["#d9dde0", "#d78672", "#4c9b69", "#3b78a6"]
    cmap = ListedColormap(colors)
    figure, axes = plt.subplots(2, 1, figsize=(10.4, 7.1))

    for panel, statistics in enumerate(("boson", "fermion")):
        selected = [row for row in rows if row["statistics"] == statistics]
        row_keys, col_keys, values = panel_matrix(selected)
        ax = axes[panel]
        ax.imshow(values, cmap=cmap, vmin=-0.5, vmax=3.5, aspect="auto")

        ax.set_xticks(range(len(col_keys)))
        ax.set_xticklabels([
            "\n".join([
                g_relation(2, s2),
                square_relation(2, q2),
                mutual_relation(r),
            ])
            for s2, q2, r in col_keys
        ], rotation=28, ha="right", rotation_mode="anchor")
        ax.set_yticks(range(len(row_keys)))
        ax.set_yticklabels([
            "\n".join([g_relation(1, s1), square_relation(1, q1)])
            for s1, q1 in row_keys
        ])
        ax.tick_params(direction="in", top=False, right=False, length=3)
        ax.set_xticks(np.arange(-0.5, len(col_keys), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(row_keys), 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=1.2)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.text(
            -0.085, 1.03, "a" if panel == 0 else "b",
            transform=ax.transAxes, fontweight="bold", va="bottom"
        )
        ax.text(
            0.0, 1.03, "Boson" if panel == 0 else "Fermion",
            transform=ax.transAxes, va="bottom"
        )

    legend = [
        Patch(facecolor=colors[2], label=r"$\eta A+A^\dagger\eta<0$, $\eta=J_2g$"),
        Patch(facecolor=colors[3], label=r"$\eta A+A^\dagger\eta<0$, $\eta=iJ_2g$"),
        Patch(
            facecolor=colors[1],
            label=(
                r"$J_1^T\overline{(\eta A+A^\dagger\eta)}J_1"
                r"=-(\eta A+A^\dagger\eta)$"
            ),
        ),
        Patch(
            facecolor=colors[0],
            label=r"$\mathrm{Tr}(\eta A+A^\dagger\eta)=0$",
        ),
    ]
    figure.legend(
        handles=legend, loc="lower center", ncol=2, frameon=False,
        bbox_to_anchor=(0.5, -0.005), fontsize=9
    )
    figure.subplots_adjust(
        left=0.19, right=0.99, top=0.97, bottom=0.31, hspace=1.03
    )

    for suffix in ("pdf", "png"):
        output = FIGURE_DIR / f"full_64_class_enumeration.{suffix}"
        figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
