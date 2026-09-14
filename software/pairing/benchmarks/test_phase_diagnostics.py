#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PhaseDiagnosticsTests(unittest.TestCase):
    def test_local_u_phase_diagnostics_are_recorded_and_reported(self) -> None:
        operator = (ROOT / "src/operator_Hubbard.f90").read_text(encoding="utf-8")
        local_u = (ROOT / "src/localU.f90").read_text(encoding="utf-8")
        local_sweep = (ROOT / "src/local_sweep.f90").read_text(encoding="utf-8")

        operator_lower = operator.lower()
        local_u_lower = local_u.lower()
        self.assertIn("type :: phasecounter", operator_lower)
        self.assertIn("phase_u_local", operator_lower)
        self.assertIn("phase_count", operator_lower)
        self.assertIn("phase_calc_ratio", operator_lower)
        self.assertIn("sum_abs_arg_proposed", operator_lower)
        self.assertIn("count_proposed", operator_lower)
        self.assertIn("count_accepted", operator_lower)
        self.assertIn("ratio_phase = atan2", local_u_lower)
        self.assertIn("call op_u%phase_u_local%count", local_u_lower)
        self.assertIn("Phase_U2_mean_abs_arg_proposed", local_sweep)
        self.assertIn("Phase_U2_branch_pi_fraction", local_sweep)
        self.assertIn("Phase_U2_local_proposals", local_sweep)
        self.assertIn("%sum_abs_arg_proposed", local_sweep)
        self.assertIn("%count_proposed", local_sweep)
        self.assertIn("%count_accepted", local_sweep)


if __name__ == "__main__":
    unittest.main()
