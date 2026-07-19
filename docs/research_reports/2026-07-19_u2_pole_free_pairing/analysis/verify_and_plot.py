#!/usr/bin/env python3
"""Generate the figures and numerical spot-check for the U2 pole-free report."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
import numpy as np
from scipy.linalg import expm, svdvals

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"
PT_PER_INCH = 72.27


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.linewidth": 0.8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": False,
            "ytick.right": False,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.bbox": "tight",
        }
    )


def triangular_adjacency(length: int = 3) -> np.ndarray:
    nsite = length * length
    adjacency = np.zeros((nsite, nsite), dtype=float)

    def index(x: int, y: int) -> int:
        return (x % length) * length + (y % length)

    for x in range(length):
        for y in range(length):
            i = index(x, y)
            for dx, dy in ((1, 0), (0, 1), (1, -1)):
                j = index(x + dx, y + dy)
                adjacency[i, j] = 1.0
                adjacency[j, i] = 1.0
    return adjacency


def save_figure(fig: plt.Figure, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".pdf"))
    fig.savefig(stem.with_suffix(".png"), dpi=300)
    plt.close(fig)


def make_stability_figure() -> None:
    epsilon_min = -3.0
    beta = 4.0
    delta = np.linspace(0.0, 1.2, 400)
    boundary = epsilon_min - delta

    width = 492.0 / PT_PER_INCH
    fig, axes = plt.subplots(1, 2, figsize=(width, 0.47 * width))
    ax = axes[0]
    ax.fill_between(delta, -5.7, boundary, color="#dff2e3", label="stable")
    ax.fill_between(delta, boundary, -2.45, color="#f8e3dc", label="not strictly stable")
    ax.plot(delta, boundary, color="#333333", lw=1.0)
    ax.plot([0.0, 0.30], [-5.0, -5.0], color="#176b87", lw=2.0)
    ax.scatter([0.0, 0.30], [-5.0, -5.0], s=20, color="#176b87", zorder=3)
    ax.text(0.34, -4.92, "Fig. 3", color="#176b87", fontsize=8)
    ax.text(0.62, -3.73, r"$\mu=\epsilon_{\min}-|\Delta|$", rotation=-30, fontsize=8)
    ax.set_xlim(0.0, 1.2)
    ax.set_ylim(-5.7, -2.45)
    ax.set_xlabel(r"$|\Delta|$")
    ax.set_ylabel(r"$\mu$")
    ax.legend(loc="lower right", fontsize=7)
    ax.text(-0.17, 1.02, "a", transform=ax.transAxes, fontweight="bold", fontsize=10)

    ax = axes[1]
    benchmark_delta = np.linspace(0.0, 0.30, 301)
    xi_min = epsilon_min - (-5.0)
    gap = np.sqrt(xi_min**2 - benchmark_delta**2)
    ax.plot(benchmark_delta, gap, color="#176b87", lw=1.6)
    ax.scatter([0.0, 0.30], [gap[0], gap[-1]], s=18, color="#176b87")
    ax.axhline(0.0, color="#a23b2a", lw=0.9, ls="--")
    ax.set_xlim(0.0, 0.30)
    ax.set_ylim(0.0, 2.08)
    ax.set_xlabel(r"$|\Delta|$")
    ax.set_ylabel(r"$E_{\min}$")
    ax.set_yticks([0.0, 1.0, 1.9, 2.0])
    ax.text(0.015, 0.19, "pole boundary", color="#a23b2a", fontsize=7)
    ax.text(0.09, 1.90, r"$E_{\min}\geq 1.977$", color="#176b87", fontsize=8)
    ax.text(-0.17, 1.02, "b", transform=ax.transAxes, fontweight="bold", fontsize=10)

    for current in axes:
        current.set_box_aspect(1.0)
        for spine in current.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.8)
        current.grid(False)
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.18, top=0.96, wspace=0.35)
    save_figure(fig, FIGURE_DIR / "stability_region")


def random_phase_samples() -> list[dict[str, float]]:
    adjacency = triangular_adjacency(3)
    nsite = adjacency.shape[0]
    identity = np.eye(nsite)
    mu = -5.0
    dtau = 0.01
    beta = 4.0
    ltau = int(round(beta / dtau))
    u2 = 1.0
    alpha2 = np.sqrt(2.0 * u2 * dtau)
    sample_count = 128
    deltas = np.arange(0.0, 0.3001, 0.05)
    rng = np.random.default_rng(20260719)
    records: list[dict[str, float]] = []

    normal_block = adjacency - mu * identity
    for pairing in deltas:
        sector_generator = np.block(
            [
                [normal_block, pairing * identity],
                [-pairing * identity, -normal_block],
            ]
        )
        free_slice = expm(-dtau * sector_generator)
        gap = np.sqrt((np.linalg.eigvalsh(adjacency).min() - mu) ** 2 - pairing**2)

        for sample in range(sample_count):
            propagation = np.eye(2 * nsite, dtype=complex)
            for _ in range(ltau):
                theta = alpha2 * rng.normal(size=nsite)
                phase = np.exp(1j * theta)
                # In the (b,c^+) sector, the U2 field multiplies both components
                # by the same onsite phase. The other sector is its conjugate.
                propagation = free_slice @ (np.r_[phase, phase][:, None] * propagation)

            determinant_matrix = np.eye(2 * nsite) - propagation
            eigenvalue_distance = np.min(np.abs(np.linalg.eigvals(propagation) - 1.0))
            singular_distance = svdvals(determinant_matrix)[-1]
            records.append(
                {
                    "delta": float(pairing),
                    "sample": sample,
                    "free_gap": float(gap),
                    "min_eigenvalue_distance": float(eigenvalue_distance),
                    "sigma_min_I_minus_M": float(singular_distance),
                }
            )
    return records


def write_random_phase_table(records: list[dict[str, float]]) -> None:
    path = TABLE_DIR / "random_phase_check.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    summary_path = TABLE_DIR / "random_phase_summary.csv"
    summary_rows = []
    for delta in sorted({record["delta"] for record in records}):
        selected = [record for record in records if record["delta"] == delta]
        eigenvalue_distance = np.array(
            [record["min_eigenvalue_distance"] for record in selected]
        )
        singular_distance = np.array(
            [record["sigma_min_I_minus_M"] for record in selected]
        )
        summary_rows.append(
            {
                "delta": delta,
                "sample_count": len(selected),
                "free_gap": selected[0]["free_gap"],
                "min_eigenvalue_distance": eigenvalue_distance.min(),
                "median_eigenvalue_distance": np.median(eigenvalue_distance),
                "min_sigma_min_I_minus_M": singular_distance.min(),
                "median_sigma_min_I_minus_M": np.median(singular_distance),
            }
        )
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(summary_rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(summary_rows)


def make_random_phase_figure(records: list[dict[str, float]]) -> None:
    deltas = sorted({record["delta"] for record in records})
    eig_data = [
        [record["min_eigenvalue_distance"] for record in records if record["delta"] == delta]
        for delta in deltas
    ]
    sv_data = [
        [record["sigma_min_I_minus_M"] for record in records if record["delta"] == delta]
        for delta in deltas
    ]

    width = 492.0 / PT_PER_INCH
    fig, axes = plt.subplots(1, 2, figsize=(width, 0.47 * width))
    colors = ["#176b87", "#9a5b13"]
    for ax, values, ylabel, panel, color in zip(
        axes,
        (eig_data, sv_data),
        (r"$\min_j|\lambda_j(\mathcal{M})-1|$", r"$\sigma_{\min}(I-\mathcal{M})$"),
        ("a", "b"),
        colors,
    ):
        violin = ax.violinplot(values, positions=deltas, widths=0.036, showextrema=False)
        for body in violin["bodies"]:
            body.set_facecolor(color)
            body.set_edgecolor(color)
            body.set_alpha(0.25)
        medians = [np.median(value) for value in values]
        minima = [np.min(value) for value in values]
        ax.plot(deltas, medians, "o-", ms=3.0, lw=1.0, color=color, label="median")
        ax.plot(deltas, minima, "s--", ms=2.8, lw=0.8, color="#333333", label="minimum")
        ax.set_yscale("log")
        ax.set_xlim(-0.025, 0.325)
        ax.set_ylim(1e-3, 1.5)
        ax.set_xticks([0.0, 0.1, 0.2, 0.3])
        ax.set_xlabel(r"$|\Delta|$")
        ax.set_ylabel(ylabel)
        ax.legend(loc="lower left", fontsize=7)
        ax.text(-0.17, 1.02, panel, transform=ax.transAxes, fontweight="bold", fontsize=10)
        ax.set_box_aspect(1.0)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.8)
        ax.grid(False)
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.18, top=0.96, wspace=0.40)
    save_figure(fig, FIGURE_DIR / "random_phase_check")


def print_summary(records: list[dict[str, float]]) -> None:
    for delta in sorted({record["delta"] for record in records}):
        selected = [record for record in records if record["delta"] == delta]
        eig = np.array([record["min_eigenvalue_distance"] for record in selected])
        sigma = np.array([record["sigma_min_I_minus_M"] for record in selected])
        print(
            f"Delta={delta:.2f}: eig distance min/median={eig.min():.6g}/{np.median(eig):.6g}; "
            f"sigma_min min/median={sigma.min():.6g}/{np.median(sigma):.6g}"
        )


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    apply_style()
    make_stability_figure()
    records = random_phase_samples()
    write_random_phase_table(records)
    make_random_phase_figure(records)
    print_summary(records)


if __name__ == "__main__":
    main()
