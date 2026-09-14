#!/usr/bin/env python3
"""Tests for publication plotting style helpers."""

from __future__ import annotations

import unittest

from benchmarks import plot_style


class PlotStyleTests(unittest.TestCase):
    def test_compact_linear_y_tick_labels_factor_common_power(self) -> None:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([0, 1], [4.5e-4, 7.5e-4])
        plot_style.style_axis(ax)

        exponent = plot_style.compact_linear_y_tick_labels(ax)
        ax.set_ylabel(r"$S_{\rm DW}(K)$")
        scale_text = plot_style.add_y_scale_text(ax, exponent)
        fig.canvas.draw()

        self.assertEqual(exponent, -4)
        self.assertEqual(ax.get_ylabel(), r"$S_{\rm DW}(K)$")
        self.assertIsNotNone(scale_text)
        self.assertEqual(scale_text.get_text(), r"$\times10^{-4}$")
        self.assertIn("7.5", [label.get_text() for label in ax.get_yticklabels()])
        self.assertNotIn(
            r"$7.5\times10^{-4}$",
            [label.get_text() for label in ax.get_yticklabels()],
        )

        plt.close(fig)

    def test_compact_linear_y_tick_labels_keeps_ordinary_values_unscaled(self) -> None:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([0, 1], [0.03, 0.12])
        plot_style.style_axis(ax)

        self.assertIsNone(plot_style.compact_linear_y_tick_labels(ax))

        plt.close(fig)

    def test_style_axis_centers_rotated_y_tick_labels_on_ticks(self) -> None:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([0, 1], [0.001, 0.1])
        ax.set_yscale("log")
        plot_style.style_axis(ax)
        fig.canvas.draw()

        for label in ax.get_yticklabels():
            self.assertEqual(label.get_rotation(), 90)
            self.assertEqual(label.get_rotation_mode(), "anchor")
            self.assertEqual(label.get_verticalalignment(), "center")
            self.assertEqual(label.get_horizontalalignment(), "center")

        plt.close(fig)

    def test_compact_numeric_tick_uses_mathtext_times_not_e_notation(self) -> None:
        self.assertEqual(
            plot_style._compact_numeric_tick(4.5e-3),
            r"$4.5\times10^{-3}$",
        )
        self.assertEqual(
            plot_style._compact_numeric_tick(-4.5e-3),
            r"$-4.5\times10^{-3}$",
        )
        self.assertEqual(
            plot_style._compact_numeric_tick(1.0e3),
            r"$1\times10^{3}$",
        )

    def test_compact_numeric_tick_keeps_plain_labels_for_ordinary_values(self) -> None:
        self.assertEqual(plot_style._compact_numeric_tick(0.0), "0")
        self.assertEqual(plot_style._compact_numeric_tick(0.032), "0.032")


if __name__ == "__main__":
    unittest.main()
