#!/usr/bin/env python3
"""Tests for the 3x3 observable benchmark campaign helpers."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from benchmarks import campaign_3x3 as campaign


class Campaign3x3Tests(unittest.TestCase):
    def write_matching_outputs(self, run_dir: Path) -> None:
        for name, values in {
            "num_up": ["2.0", "2.0", "2.0", "2.0"],
            "num_do": ["2.0", "2.0", "2.0", "2.0"],
            "density_total": ["4.0", "4.0", "4.0", "4.0"],
            "energy_density": ["-1.0", "-1.0", "-1.0", "-1.0"],
            "doubleOcc": ["0.25", "0.25", "0.25", "0.25"],
            "onsite_n2_up": ["2.0", "2.0", "2.0", "2.0"],
            "onsite_n2_do": ["2.0", "2.0", "2.0", "2.0"],
        }.items():
            (run_dir / name).write_text("\n".join(values) + "\n", encoding="utf-8")
        for name in ("sf_K", "psf_Gamma", "dw_K"):
            (run_dir / name).write_text(
                "1.0 0.0\n1.0 0.0\n1.0 0.0\n1.0 0.0\n",
                encoding="utf-8",
            )
        (run_dir / "density_site_total").write_text(
            "\n".join([" ".join(["4.0"] * 9)] * 4) + "\n",
            encoding="utf-8",
        )

        observables = {
            "density_total": 4.0,
            "total_kinetic": -9.0,
            "doubleOcc": 0.25,
            "onsite_n2_up": 2.0,
            "onsite_n2_do": 2.0,
            "interaction_energy_density": 0.0,
            "energy_density": -1.0,
            "S_SF_K": 1.0,
            "S_PSF_Gamma": 1.0,
            "S_DW_K": 1.0,
            "num_up": 2.0,
            "num_do": 2.0,
        }
        (run_dir / "results.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "parameters": {
                        "Lx": 3,
                        "Ly": 3,
                        "beta": 4.0,
                        "mu": -3.5,
                        "U1": 0.0,
                        "U2": 0.0,
                        "max_total_particles": 6,
                    },
                    "status": "converged",
                    "completed_shells": 3,
                    "observables": observables,
                    "relative_last_shell": {
                        name: 1.0e-4 for name in observables
                    },
                    "convergence_policy": {
                        "tail_tolerance": 1.0e-3,
                        "max_density_total": 1.0,
                        "min_completed_shells": 2,
                    },
                }
            ),
            encoding="utf-8",
        )

    def test_default_manifest_records_reviewed_design_defaults(self) -> None:
        manifest = campaign.default_manifest()

        self.assertEqual(manifest["campaign"], "triangle_3x3_observables")
        self.assertEqual(manifest["lattice"], {"Lx": 3, "Ly": 3})
        self.assertEqual(
            [sweep["name"] for sweep in manifest["sweeps"]],
            ["U2_sweep", "U1_sweep"],
        )
        self.assertEqual(manifest["dqmc_defaults"]["dtau"], 0.01)
        self.assertEqual(
            manifest["observables"],
            [
                "density_total",
                "energy_density",
                "doubleOcc",
                "IPR",
                "S_SF_K",
                "S_PSF_Gamma",
                "S_DW_K",
            ],
        )
        self.assertEqual(manifest["sweeps"][0]["mu"], -3.5)
        self.assertEqual(manifest["sweeps"][1]["U2"], 1.0)
        self.assertEqual(manifest["ed_policy"]["max_total_particles"], 6)
        self.assertEqual(manifest["analysis_defaults"]["stderr_tolerance"], 3.0)
        self.assertEqual(manifest["hpc"]["job_prefix"], "yyk/")

    def test_iter_cases_expands_both_sweeps(self) -> None:
        cases = list(campaign.iter_cases(campaign.default_manifest()))
        labels = {case["label"] for case in cases}

        self.assertIn("U2_0_mu-3.5_b4", labels)
        self.assertIn("U1_0_mu-5_b1", labels)
        self.assertEqual({case["sweep"] for case in cases}, {"U2_sweep", "U1_sweep"})
        self.assertTrue(
            any(case["U2"] == 0.0 and case["mu"] == -3.5 for case in cases)
        )
        self.assertTrue(
            any(case["U1"] == 0.0 and case["U2"] == 1.0 for case in cases)
        )

    def test_case_name_uses_stable_parameter_label(self) -> None:
        case = {
            "sweep": "U2_sweep",
            "Lx": 3,
            "Ly": 3,
            "beta": 4.0,
            "mu": -3.5,
            "U1": 0.0,
            "U2": 1.5,
        }

        self.assertEqual(
            campaign.case_name(case),
            "triangle_3x3_U2_1.5_mu-3.5_b4",
        )

    def test_slurm_job_name_uses_hpc_prefix_and_kind(self) -> None:
        case = {
            "sweep": "U2_sweep",
            "Lx": 3,
            "Ly": 3,
            "beta": 4.0,
            "mu": -3.5,
            "U1": 0.0,
            "U2": 1.5,
        }

        self.assertEqual(
            campaign.slurm_job_name("BAFQMC", case),
            "yyk/BAFQMC/U2_1.5_mu-3.5_b4",
        )
        self.assertEqual(
            campaign.slurm_job_name("ED", case),
            "yyk/ED/U2_1.5_mu-3.5_b4",
        )

    def test_write_dqmc_case_creates_fixed_runtime_inputs(self) -> None:
        manifest = campaign.default_manifest()
        case = {
            "sweep": "U2_sweep",
            "Lx": 3,
            "Ly": 3,
            "beta": 4.0,
            "mu": -3.5,
            "U1": 0.0,
            "U2": 1.5,
        }
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = campaign.write_dqmc_case(
                Path(tmp),
                case,
                manifest["dqmc_defaults"],
                seed=13579,
            )
            names = {path.name for path in run_dir.iterdir()}
            param_text = (run_dir / "paramC_sets.txt").read_text(encoding="utf-8")
            confin_text = (run_dir / "confin.txt").read_text(encoding="utf-8")
            seeds_text = (run_dir / "seeds.txt").read_text(encoding="utf-8")

        self.assertGreaterEqual(names, {"paramC_sets.txt", "confin.txt", "seeds.txt"})
        self.assertEqual(confin_text, "0\n")
        self.assertEqual(seeds_text, "13579\n")
        self.assertIn("3           3           400         4.0", param_text)
        self.assertIn("10          100000      1           1.5", param_text)
        self.assertIn(".false.     0", param_text)
        self.assertIn(".true.      500         1.0         1.0", param_text)
        self.assertIn("2           0.1         0.0         0.0", param_text)
        self.assertIn("Nwrap       Nbin        Nsweep      shiftLoc", param_text)
        self.assertIn("is_warm     Nwarm       shiftWarm1  shiftWarm2", param_text)

    def test_write_dqmc_case_removes_stale_output_files_on_regeneration(self) -> None:
        manifest = campaign.default_manifest()
        case = next(iter(campaign.iter_cases(manifest)))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = campaign.write_dqmc_case(
                root, case, manifest["dqmc_defaults"], seed=13579
            )
            (run_dir / "density_total").write_text("old\n", encoding="utf-8")
            (run_dir / "density_site_total").write_text("old\n", encoding="utf-8")
            (run_dir / "sf_K").write_text("old\n", encoding="utf-8")
            (run_dir / "notes.txt").write_text("keep\n", encoding="utf-8")

            rerun_dir = campaign.write_dqmc_case(
                root, case, manifest["dqmc_defaults"], seed=24680
            )

            self.assertEqual(rerun_dir, run_dir)
            self.assertFalse((run_dir / "density_total").exists())
            self.assertFalse((run_dir / "density_site_total").exists())
            self.assertFalse((run_dir / "sf_K").exists())
            self.assertEqual(
                (run_dir / "notes.txt").read_text(encoding="utf-8"), "keep\n"
            )
            self.assertEqual(
                (run_dir / "seeds.txt").read_text(encoding="utf-8"), "24680\n"
            )

    def test_write_ed_case_creates_script_compatible_json(self) -> None:
        manifest = campaign.default_manifest()
        case = next(iter(campaign.iter_cases(manifest)))
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = campaign.write_ed_case(Path(tmp), case, manifest["ed_policy"])
            params = json.loads((run_dir / "params.json").read_text(encoding="utf-8"))

        self.assertEqual(run_dir.name, campaign.case_name(case))
        self.assertEqual(params["parameters"]["Lx"], 3)
        self.assertEqual(params["parameters"]["Ly"], 3)
        self.assertEqual(params["parameters"]["max_total_particles"], 6)
        self.assertEqual(params["convergence_policy"]["tail_tolerance"], 1.0e-3)
        self.assertNotIn("max_total_particles", params["convergence_policy"])

    def test_init_local_writes_dqmc_and_ed_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "inputs"
            status = campaign.main(
                ["init-local", "--output-dir", str(output_dir), "--seed", "13579"]
            )
            case = next(iter(campaign.iter_cases(campaign.default_manifest())))
            run_dir = output_dir / campaign.case_name(case)

            names = {path.name for path in run_dir.iterdir()}

        self.assertEqual(status, 0)
        self.assertGreaterEqual(
            names, {"paramC_sets.txt", "confin.txt", "seeds.txt", "params.json"}
        )

    def test_write_stage1_report_contains_chinese_skeleton(self) -> None:
        manifest = campaign.default_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            report = campaign.write_stage1_report(Path(tmp), manifest)
            html = report.read_text(encoding="utf-8")

        self.assertEqual(report.name, "report_stage_1_observable_definitions.html")
        self.assertIn("MathJax", html)
        self.assertIn("BAFQMC vs ED", html)
        for observable in ("S_SF", "S_PSF", "S_DW", "IPR"):
            self.assertIn(observable, html)
        self.assertIn("mu < -3", html)
        self.assertIn("low_density_cutoff_accepted", html)
        self.assertIn("ssh cluster.example", html)
        self.assertIn("compute", html)
        self.assertIn("large-memory", html)
        self.assertIn("本报告", html)

    def test_write_results_summary_writes_fail_closed_outputs(self) -> None:
        manifest = campaign.default_manifest()
        manifest["sweeps"] = [{**manifest["sweeps"][0], "U2": [0.0]}]
        manifest["dqmc_defaults"]["block_size"] = 2
        case = next(iter(campaign.iter_cases(manifest)))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "inputs"
            output_dir = root / "summary"
            run_dir = campaign.write_dqmc_case(
                input_dir,
                case,
                manifest["dqmc_defaults"],
                seed=13579,
            )
            campaign.write_ed_case(input_dir, case, manifest["ed_policy"])
            self.write_matching_outputs(run_dir)
            (output_dir / "submitted_jobs.json").parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            (output_dir / "submitted_jobs.json").write_text(
                json.dumps(
                    [
                        {
                            "case_name": campaign.case_name(case),
                            "job_id": "12345",
                            "job_name": "yyk/BAFQMC/U2_0_mu-3.5_b4",
                            "kind": "BAFQMC",
                            "partition": "compute",
                            "run_dir": (
                                "/path/to/campaign/production_inputs/"
                                f"{campaign.case_name(case)}"
                            ),
                            "sbatch_stdout": "Submitted batch job 12345",
                            "time_limit": "168:00:00",
                        }
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            paths = campaign.write_results_summary(input_dir, output_dir, manifest)

            payload = json.loads(paths["json"].read_text(encoding="utf-8"))
            csv_text = paths["csv"].read_text(encoding="utf-8")
            html = paths["html"].read_text(encoding="utf-8")

            self.assertTrue(payload["cases"][0]["trusted"])
            self.assertEqual(payload["counts"], {"trusted": 1})
            self.assertEqual(payload["job_counts"], {"BAFQMC": 1})
            self.assertEqual(payload["submitted_jobs"][0]["job_id"], "12345")
            self.assertEqual(
                payload["submitted_jobs"][0]["stdout_path"],
                "/path/to/campaign/logs/12345.out",
            )
            self.assertTrue(payload["figures"])
            first_figure = payload["figures"][0]
            if first_figure["status"] == "written":
                self.assertTrue((output_dir / first_figure["relative_path"]).exists())
                self.assertIn("<img", html)
            else:
                self.assertEqual(first_figure["status"], "unavailable")
                self.assertIn("Figure generation skipped", html)
            self.assertIn("S_SF_K", csv_text)
            self.assertIn("run_dir", csv_text)
            self.assertIn("paramC_sets.txt", csv_text)
            self.assertIn("Raw Index", html)
            self.assertIn("HPC Job Index", html)
            self.assertIn("12345", html)
            self.assertIn("Results Summary", html)

    def test_write_queue_snapshot_report_indexes_submitted_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary_dir = root / "summary"
            output_dir = root / "reports"
            summary_dir.mkdir()
            (summary_dir / "submitted_jobs.json").write_text(
                json.dumps(
                    [
                        {
                            "case_name": "triangle_3x3_U2_0_mu-3.5_b4",
                            "job_id": "1338587",
                            "job_name": "yyk/BAFQMC/U2_0_mu-3.5_b4",
                            "kind": "BAFQMC",
                            "partition": "compute",
                            "run_dir": (
                                "/path/to/campaign/production_inputs/"
                                "triangle_3x3_U2_0_mu-3.5_b4"
                            ),
                            "time_limit": "168:00:00",
                        },
                        {
                            "case_name": "triangle_3x3_U2_0_mu-3.5_b4",
                            "job_id": "1338588",
                            "job_name": "yyk/ED/U2_0_mu-3.5_b4",
                            "kind": "ED",
                            "partition": "compute",
                            "run_dir": (
                                "/path/to/campaign/production_inputs/"
                                "triangle_3x3_U2_0_mu-3.5_b4"
                            ),
                            "time_limit": "168:00:00",
                        },
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (summary_dir / "summary_campaign_results.json").write_text(
                json.dumps(
                    {
                        "counts": {"dqmc_unavailable": 1},
                        "job_counts": {"BAFQMC": 1, "ED": 1},
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            path = campaign.write_queue_snapshot_report(
                summary_dir,
                output_dir,
                checked_at="2026-06-03T08:00:32+0800",
                hpc_root="/path/to/campaign",
                repo_commit="abc123",
                default_state="PENDING",
                default_reason="Priority",
                default_start_time="2026-06-05T20:27:11",
                default_time_limit="7-00:00:00",
            )

            html = path.read_text(encoding="utf-8")
            self.assertEqual(path.name, "report_stage_4_hpc_queue_snapshot.html")
            self.assertIn("HPC Queue Snapshot", html)
            self.assertIn("dqmc_unavailable=1", html)
            self.assertIn("PENDING=2", html)
            self.assertIn("BAFQMC=1", html)
            self.assertIn("1338587", html)
            self.assertIn("1338588", html)
            self.assertIn("/path/to/campaign/logs/1338587.out", html)


if __name__ == "__main__":
    unittest.main()
