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


def sign_label(value):
    return "+" if int(value) == 1 else "-"


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
    figure, axes = plt.subplots(2, 1, figsize=(6.8, 4.7))

    for panel, statistics in enumerate(("boson", "fermion")):
        selected = [row for row in rows if row["statistics"] == statistics]
        row_keys, col_keys, values = panel_matrix(selected)
        ax = axes[panel]
        ax.imshow(values, cmap=cmap, vmin=-0.5, vmax=3.5, aspect="auto")

        ax.set_xticks(range(len(col_keys)))
        ax.set_xticklabels([
            f"{sign_label(s2)} {sign_label(q2)} {sign_label(r)}"
            for s2, q2, r in col_keys
        ])
        ax.set_yticks(range(len(row_keys)))
        ax.set_yticklabels([
            f"{sign_label(s1)} {sign_label(q1)}" for s1, q1 in row_keys
        ])
        ax.set_ylabel(r"$(s_1,\ q_1)$")
        ax.set_xlabel(r"$(s_2,\ q_2,\ r)$")
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
        Patch(facecolor=colors[2], label=r"strict, $\eta=J_2g$"),
        Patch(facecolor=colors[3], label=r"strict, $\eta=iJ_2g$"),
        Patch(facecolor=colors[1], label="reality flips cone"),
        Patch(facecolor=colors[0], label="trace obstruction"),
    ]
    figure.legend(
        handles=legend, loc="lower center", ncol=4, frameon=False,
        bbox_to_anchor=(0.5, -0.005), fontsize=8
    )
    figure.subplots_adjust(
        left=0.105, right=0.99, top=0.965, bottom=0.17, hspace=0.58
    )

    for suffix in ("pdf", "png"):
        output = FIGURE_DIR / f"full_64_class_enumeration.{suffix}"
        figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
