"""Main-text U/Delta benchmark and the supplemental U1 scan.

All points and error bars come from the archived or freshly processed records.
The original model parameters remain unchanged; the main-text U denotes U2.
"""
from __future__ import annotations

import copy
from pathlib import Path

from . import plot_number, plot_pairing, plot_style


OBSERVABLES = ("density_total", "minus_total_energy", "S_SF_K", "S_DW_K")


def plot_figures(cases: list[dict], output: Path) -> None:
    import matplotlib.pyplot as plt

    records = []
    for case in cases:
        record = copy.deepcopy(case)
        record["ed_reliable"] = True  # Preserve the published reference selection.
        nsite = case["parameters"]["Lx"] * case["parameters"]["Ly"]
        energy = case["observables"]["energy_density"]
        record["observables"]["minus_total_energy"] = {
            "dqmc": -nsite * energy["dqmc"],
            "ed": -nsite * energy["ed"],
            "stderr": nsite * energy["stderr"],
        }
        records.append(record)

    repulsive = [c for c in records if c["model"] == "number_conserving" and c["row"] == 0]
    attractive = [c for c in records if c["model"] == "number_conserving" and c["row"] == 1]
    paired = [c for c in records if c["model"] == "pairing"]
    main_rows = [(r"$U$", repulsive), (r"$\Delta$", paired)]
    _draw(plt, output, [(label, row) for label, row in main_rows if row], "benchmark_combined")
    if attractive:
        _draw(plt, output, [(r"$U_1$", attractive)], "benchmark_attractive")


def _draw(plt, output: Path, rows: list[tuple[str, list[dict]]], stem: str) -> None:
    if not rows:
        return
    with plt.rc_context():
        plot_style.apply_revtex_style(plt, label_size=7.5, tick_size=6.0, legend_size=6.0)
        fig, axes = plt.subplots(
            len(rows), len(OBSERVABLES), squeeze=False,
            figsize=plot_style.revtex_figure_size(
                width_pt=plot_style.REVTEX_DOUBLE_COLUMN_WIDTH_PT,
                ncols=len(OBSERVABLES), nrows=len(rows), panel_aspect=1.03,
            ),
        )
        fig.subplots_adjust(
            left=0.066, right=0.992, bottom=0.22 if len(rows) == 1 else 0.112,
            top=0.970, wspace=0.24, hspace=0.18,
        )
        for row_index, (xlabel, records) in enumerate(rows):
            for column, observable in enumerate(OBSERVABLES):
                ax = axes[row_index, column]
                plot_number._plot_observable_axis(ax, records, observable, plot_checkpoints=False)
                if records[0]["model"] == "pairing":
                    # Retain the linear axes of the original paired benchmark.
                    x = [float(record["x"]) for record in records]
                    ed = [record["observables"][observable]["ed"] for record in records]
                    dqmc = [record["observables"][observable]["dqmc"] for record in records]
                    ax.set_yscale("linear")
                    ax.set_xlim(min(x) - 0.015, max(x) + 0.015)
                    ax.set_ylim(*plot_pairing.y_limits(ed, dqmc))
                plot_style.style_axis(ax)
                exponent = plot_style.compact_linear_y_tick_labels(ax)
                ax.set_ylabel(plot_number._observable_label(observable))
                plot_style.add_y_scale_text(ax, exponent)
                ax.set_xlabel(xlabel)
        axes[0, 1].legend(
            loc="upper right", frameon=False, handlelength=1.5,
            borderaxespad=0.15, handletextpad=0.45, labelspacing=0.25,
        )
        plot_style.add_panel_labels(axes, x=-0.12, y=1.0, fontsize=8.0)
        output.mkdir(parents=True, exist_ok=True)
        fig.savefig(output / f"{stem}.pdf", metadata={"CreationDate": None, "ModDate": None})
        fig.savefig(output / f"{stem}.png", dpi=300)
        plt.close(fig)
