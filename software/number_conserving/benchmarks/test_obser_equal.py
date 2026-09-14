#!/usr/bin/env python3
"""Tests for equal-time observable Green-function conventions."""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OBSER_EQUAL = REPO_ROOT / "src" / "obser_equal.f90"
FOURIER_TRANS = REPO_ROOT / "src" / "fourier_trans.f90"
LATTICE_SOURCE = REPO_ROOT / "src" / "lattice.f90"
PHYSICS_DOC = REPO_ROOT / "docs" / "physics.md"
RUN_LOCAL = REPO_ROOT / "scripts" / "run_local.sh"


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


class ObserEqualGreenConventionTests(unittest.TestCase):
    def test_down_density_matrix_uses_down_green_without_extra_conjugation(self) -> None:
        source = _compact(OBSER_EQUAL.read_text(encoding="utf-8"))

        self.assertIn("grdo=dconjg(prop%gr)", source)
        self.assertIn("grdoc=transpose(grdo)-zkron", source)
        self.assertNotIn("grdoc=dconjg(transpose(grdo))-zkron", source)

    def test_physics_doc_matches_down_green_convention(self) -> None:
        doc = _compact(PHYSICS_DOC.read_text(encoding="utf-8"))

        self.assertIn("grdo=dconjg(prop%gr)", doc)
        self.assertIn("grdoc=transpose(grdo)-zkron", doc)
        self.assertNotIn("grdoc=dconjg(transpose(grdo))-zkron", doc)

    def test_ed_script_emits_equal_time_scalar_observables(self) -> None:
        ed_script = REPO_ROOT / "benchmarks" / "ed" / "EDtriangle_symm_NEblock.py"
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "params.txt").write_text(
                "Lx = 3\n"
                "Ly = 2\n"
                "t = 1.0\n"
                "U1 = 0.0\n"
                "U2 = 1.0\n"
                "beta = 6.0\n"
                "mu = -2.5\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ed_script)],
                cwd=run_dir,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))

        observables = data["observables"]
        self.assertAlmostEqual(observables["doubleOcc"], 5.0104309962475375e-06)
        self.assertAlmostEqual(observables["squareOcc"], 2.3674394261440157e-09)
        self.assertAlmostEqual(observables["numsquare_up"], 0.00041666206338322737)
        self.assertAlmostEqual(observables["numsquare_do"], 0.00041666206338322737)


class EqualTimeCampaignObservableSourceTests(unittest.TestCase):
    def test_obser_equal_declares_and_accumulates_campaign_observables(self) -> None:
        source = _compact(OBSER_EQUAL.read_text(encoding="utf-8"))

        for field in (
            "density_total",
            "density_site_total",
            "onsite_n2_up",
            "onsite_n2_do",
            "interaction_energy_density",
            "energy_density",
            "sf_k",
            "psf_gamma",
            "dw_k",
        ):
            self.assertIn(field, source)

        self.assertIn("2.d0*grupc(ii,ii)*grupc(ii,ii)+grupc(ii,ii)", source)
        self.assertIn("2.d0*grdoc(ii,ii)*grdoc(ii,ii)+grdoc(ii,ii)", source)
        self.assertIn("latt%inv_cell_list(2*nlx/3+1,nly/3+1)", source)
        self.assertIn("exp(dcmplx(0.d0,latt%k_dot_r(indexk,imj)))", source)
        self.assertNotIn("k-pointobservablesrequire", source)

    def test_lattice_uses_common_two_pi_reciprocal_basis_and_zero_displacement(self) -> None:
        source = _compact(LATTICE_SOURCE.read_text(encoding="utf-8"))

        self.assertIn("latt%a1_v(1)=1.d0", source)
        self.assertIn("latt%a1_v(2)=0.d0", source)
        self.assertIn("latt%a2_v(1)=0.5d0", source)
        self.assertIn("latt%a2_v(2)=sqrt(3.d0)/2.d0", source)
        self.assertIn("latt%b1_v(1)=2.d0*pi", source)
        self.assertIn("latt%b1_v(2)=-2.d0*pi/sqrt(3.d0)", source)
        self.assertIn("latt%b2_v(1)=0.d0", source)
        self.assertIn("latt%b2_v(2)=4.d0*pi/sqrt(3.d0)", source)
        self.assertIn("imjx=modulo(ix-jx,nlx)+1", source)
        self.assertIn("imjy=modulo(iy-jy,nly)+1", source)
        self.assertIn("dble(ix-1)*latt%a1_v(1)", source)
        self.assertIn("dble(iy-1)*latt%a2_v(2)", source)

    def test_fourier_trans_writes_campaign_observables(self) -> None:
        source = _compact(FOURIER_TRANS.read_text(encoding="utf-8"))

        for filename in (
            "density_total",
            "density_site_total",
            "onsite_n2_up",
            "onsite_n2_do",
            "interaction_energy_density",
            "energy_density",
            "sf_k",
            "psf_gamma",
            "dw_k",
        ):
            self.assertIn(f"file='{filename}'", source)

        for field in ("sf_k", "psf_gamma", "dw_k"):
            self.assertIn(f"real(obs%{field})", source)
            self.assertIn(f"imag(obs%{field})", source)
            self.assertIn(f"mpi_reduce(obs%{field}", source)
        self.assertIn("write(80,'(*(es24.16,1x))')obs%density_site_total", source)


@unittest.skipUnless(
    os.environ.get("RUN_DQMC_SMOKE") == "1",
    "set RUN_DQMC_SMOKE=1 to run MPI DQMC smoke tests",
)
class EqualTimeCampaignObservableRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        if shutil.which("mpirun") is None:
            self.skipTest("mpirun is not available")

    def test_non_k_lattice_runs_and_leaves_k_observables_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            self._write_run_inputs(
                run_dir,
                lx=3,
                ly=2,
                ltrot=10,
                beta=0.1,
                u1=0.0,
                u2=0.5,
                mu=-3.5,
            )

            result = subprocess.run(
                ["bash", str(RUN_LOCAL), str(run_dir), "1"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
                timeout=120,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in ("sf_K", "dw_K"):
                value = self._read_complex_last(run_dir / name)
                self.assertAlmostEqual(value.real, 0.0)
                self.assertAlmostEqual(value.imag, 0.0)
            self._read_complex_last(run_dir / "psf_Gamma")

    def test_three_by_three_smoke_writes_all_campaign_observables(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            self._write_run_inputs(
                run_dir,
                lx=3,
                ly=3,
                ltrot=10,
                beta=0.1,
                u1=0.0,
                u2=0.5,
                mu=-3.5,
            )

            result = subprocess.run(
                ["bash", str(RUN_LOCAL), str(run_dir), "1"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
                timeout=120,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in (
                "density_total",
                "density_site_total",
                "onsite_n2_up",
                "onsite_n2_do",
                "interaction_energy_density",
                "energy_density",
            ):
                self.assertTrue(math.isfinite(self._read_scalar_last(run_dir / name)))
            for name in ("sf_K", "psf_Gamma", "dw_K"):
                value = self._read_complex_last(run_dir / name)
                self.assertTrue(math.isfinite(value.real))
                self.assertTrue(math.isfinite(value.imag))
            self.assertEqual(
                len(self._read_vector_last(run_dir / "density_site_total")),
                9,
            )

    def _write_run_inputs(
        self,
        run_dir: Path,
        *,
        lx: int,
        ly: int,
        ltrot: int,
        beta: float,
        u1: float,
        u2: float,
        mu: float,
    ) -> None:
        run_dir.joinpath("paramC_sets.txt").write_text(
            f"{u1:<12}{u2:<12}{mu}\n"
            f"{lx:<12}{ly:<12}{ltrot:<12}{beta}\n"
            f"{lx:<12}{ly:<12}{ltrot}\n"
            f"{10:<12}{2:<12}{1:<12}{1.5}\n"
            f"{'.false.':<12}{0}\n"
            f"{'.false.':<12}{0:<12}{1.0:<12}{1.0}\n"
            f"{2:<12}{0.1:<12}{0.0:<12}{0.0}\n\n"
            "RU1         RU2         mu\n"
            "Nlx         Nly         Ltrot       Beta\n"
            "NlxTherm    NlyTherm    LtrotTherm\n"
            "Nwrap       Nbin        Nsweep      shiftLoc\n"
            "is_tau      Nthermal\n"
            "is_warm     Nwarm       shiftWarm1  shiftWarm2\n"
            "iniType     iniAmpl     iniBias1    iniBias2\n",
            encoding="utf-8",
        )
        run_dir.joinpath("confin.txt").write_text("0\n", encoding="utf-8")
        run_dir.joinpath("seeds.txt").write_text("64464988\n", encoding="utf-8")

    def _read_scalar_last(self, path: Path) -> float:
        values = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        return float(values[-1].split()[0])

    def _read_complex_last(self, path: Path) -> complex:
        values = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        real, imag = values[-1].split()[:2]
        return complex(float(real), float(imag))

    def _read_vector_last(self, path: Path) -> list[float]:
        values = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        return [float(token) for token in values[-1].split()]


if __name__ == "__main__":
    unittest.main()
