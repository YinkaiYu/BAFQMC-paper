#!/usr/bin/env python3
"""Generate the classification and counterexample figures for the HTML report."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"

PT_PER_INCH = 72.27
TWO_COLUMN_WIDTH = 492.0 / PT_PER_INCH


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "axes.linewidth": 0.75,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": False,
            "ytick.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.transparent": False,
        }
    )


def style_axis(ax: mpl.axes.Axes) -> None:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.75)
    ax.grid(False)
    ax.tick_params(width=0.75, length=3)


def save_figure(fig: mpl.figure.Figure, stem: str) -> None:
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def classification_map() -> None:
    row_values = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    column_values = [
        (-1, 1, 1),
        (-1, 1, -1),
        (-1, -1, 1),
        (-1, -1, -1),
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1),
    ]
    values = np.zeros((len(row_values), len(column_values)), dtype=int)

    for row, (s1, _q1) in enumerate(row_values):
        for column, (s2, q2, relation) in enumerate(column_values):
            if q2 == 1 and relation == -s1 * s2:
                values[row, column] = 1 if s2 == -1 else 2

    cmap = ListedColormap(["#eef1f3", "#2c6e91", "#3f8c5a"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)
    fig, ax = plt.subplots(figsize=(TWO_COLUMN_WIDTH, 2.85))
    ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")
    style_axis(ax)

    ax.set_xticks(range(len(column_values)))
    ax.set_xticklabels(
        [
            rf"$s_2={s2:+d}$" + "\n" + rf"$q_2={q2:+d},\,r={relation:+d}$"
            for s2, q2, relation in column_values
        ],
        rotation=38,
        ha="right",
        rotation_mode="anchor",
    )
    ax.set_yticks(range(len(row_values)))
    ax.set_yticklabels(
        [rf"$s_1={s1:+d},\ q_1={q1:+d}$" for s1, q1 in row_values]
    )
    ax.set_xlabel("The remaining three binary labels")
    ax.set_ylabel("Reality-structure labels")

    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            label = "listed" if values[row, column] == 1 else "partner"
            if values[row, column] != 0:
                ax.text(
                    column,
                    row,
                    label,
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=7,
                    fontweight="bold",
                )

    handles = [
        mpl.patches.Patch(facecolor="#2c6e91", label=r"$s_2=-1$: listed quartet"),
        mpl.patches.Patch(facecolor="#3f8c5a", label=r"$s_2=+1$: partner quartet"),
        mpl.patches.Patch(facecolor="#eef1f3", edgecolor="#b8c0c7", label="filtered out"),
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.20),
        ncol=3,
        frameon=False,
        fontsize=7.5,
    )
    fig.subplots_adjust(left=0.12, right=0.995, bottom=0.31, top=0.82)
    save_figure(fig, "boson_32_class_filter")


def diagnostic_curves() -> None:
    X = np.array([[0.0, 1.0], [1.0, 0.0]])
    Z = np.array([[1.0, 0.0], [0.0, -1.0]])
    generators = (-2 * X - 2 * Z, -2 * X, 2 * X + Z)

    scaling = np.linspace(0.0, 1.0, 501)
    fermion_weight = []
    for value in scaling:
        product = np.eye(2)
        for generator in generators:
            product = product @ expm(value * generator)
        fermion_weight.append(np.linalg.det(np.eye(2) + product).real)
    fermion_weight = np.asarray(fermion_weight)

    node_parameter = 0.8096748539369405
    partner_t = np.linspace(0.0, 2.5, 501)
    partner_weight = 1.0 / (2.0 * (np.cosh(1.0) * np.cosh(partner_t) - 1.0))
    with (TABLES / "boson_s2_plus_partner_test.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        octave_rows = list(csv.DictReader(handle))
    octave_t = np.array([float(row["t"]) for row in octave_rows])
    octave_weight = np.array(
        [float(row["operator_branch_weight_closed_form"]) for row in octave_rows]
    )

    curve_file = TABLES / "report_curve_data.csv"
    with curve_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            ["curve", "parameter", "weight", "fixed_parameter", "source"]
        )
        for parameter, weight in zip(scaling, fermion_weight):
            writer.writerow(
                ["fermion_case_3", parameter, weight, "", "integer_counterexample"]
            )
        for parameter, weight in zip(partner_t, partner_weight):
            writer.writerow(
                ["boson_s2_plus_partner", parameter, weight, "E=1", "closed_form"]
            )

    fig, axes = plt.subplots(1, 2, figsize=(TWO_COLUMN_WIDTH, 2.65))
    ax = axes[0]
    style_axis(ax)
    ax.axhline(0.0, color="#6d747a", linewidth=0.7)
    ax.plot(scaling, fermion_weight, color="#a23b2a", linewidth=1.2)
    ax.axvline(
        node_parameter,
        color="#a23b2a",
        linewidth=0.8,
        linestyle="--",
        label=rf"$s_\star={node_parameter:.6f}$",
    )
    ax.scatter([1.0], [fermion_weight[-1]], s=17, color="#a23b2a", zorder=3)
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel(r"Common scale $s$")
    ax.set_ylabel(r"Fermion weight $W_{\rm F}(s)$")
    ax.legend(frameon=False, fontsize=7.5, loc="lower left")
    ax.text(
        -0.16,
        1.03,
        "a",
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
    )

    ax = axes[1]
    style_axis(ax)
    ax.plot(partner_t, partner_weight, color="#26734d", linewidth=1.2)
    ax.scatter(
        octave_t,
        octave_weight,
        s=18,
        facecolors="white",
        edgecolors="#26734d",
        linewidths=0.9,
        label="Octave check",
        zorder=3,
    )
    ax.set_xlim(0.0, 2.5)
    ax.set_ylim(bottom=0.0)
    ax.set_xlabel(r"Strict-cone strength $t$")
    ax.set_ylabel(r"Boson weight $W_{\rm B}(E{=}1,t)$")
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    ax.text(
        -0.16,
        1.03,
        "b",
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
    )

    fig.subplots_adjust(left=0.105, right=0.995, bottom=0.20, top=0.95, wspace=0.34)
    save_figure(fig, "counterexample_and_partner")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    apply_style()
    classification_map()
    diagnostic_curves()
    print(f"Wrote figures to {FIGURES}")


if __name__ == "__main__":
    main()
