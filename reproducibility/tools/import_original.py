#!/usr/bin/env python3
"""Maintainer-only import of the two historical campaigns; readers need no siblings.

Only the 22 points actually selected by the original paper plot are archived.
Raw text is preserved byte for byte in deterministic per-case gzip tar archives.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import sys

RAW_FILES = ("density_total", "energy_density", "sf_K", "dw_K")
INPUT_FILES = ("paramC_sets.txt", "confin.txt", "seeds.txt", "params.json")
CAMPAIGNS = {
    "number_conserving": ("code_bosonDQMC", "20260603_bafqmc_ed_3x3_observables_v2_standard"),
    "pairing": ("code_bosonDQMC_paring", "20260605_pairing_delta_mu_m5_production"),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-parent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        parser.error("output already exists; import into a new directory")
    all_cases, sources = [], {}
    for model, (repo_name, campaign_name) in CAMPAIGNS.items():
        repo = args.source_parent.resolve() / repo_name
        base = repo / "data" / campaign_name
        target = out / model
        source = {
            "repository": repo_name, "campaign": campaign_name,
            "source_checkout_commit": subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(),
            "commit_scope": "Source snapshot at integration; ignored historical data were not versioned by this commit.",
        }
        if model == "number_conserving":
            records_path = base / "publication_report/publication_records.json"
            records = json.loads(records_path.read_text())
            selected = []
            for record in records:
                u2 = (record["group"], record["sweep"]) in {
                    ("main", "U2_sweep"), ("main_u2_refine", "U2_refine"),
                    ("main_u2_low_refine", "U2_low_refine"),
                }
                rho = record["observables"]["density_total"]
                u1 = record["group"] in {"u1_mu7_extended_local", "u1_mu7_fill_local"} and 0 < rho["dqmc"] <= .05 and 0 < rho["ed"] <= .05
                if record["ed_reliable"] and (u2 or u1):
                    selected.append((0 if u2 else 1, record))
            selected.sort(key=lambda item: (item[0], item[1]["x"]))
            entries = []
            for row, record in selected:
                case_id = record["case_name"]
                run_dir = base / record["group"] / "production_inputs" / case_id
                entries.append((case_id, run_dir, run_dir / "results.json", row, record["x"], record))
            figure = base / "publication_report/figures/paper_candidate_main_4x2.pdf"
            source["selection"] = "Original _paper_candidate_u2_records and _paper_candidate_u1_records; reliable reference plus 0 < rho <= 0.05 for the U1 row."
            script = base / "make_publication_report.py"
        else:
            records_path = base / "summary/comparison_dqmc_ed_nmax3_ncut4.json"
            payload = json.loads(records_path.read_text())
            entries = [(r["case"], base / "inputs" / r["case"], base / "ed_results_nmax3_ncut4" / (r["case"] + ".json"), 0, r["Delta"], r) for r in sorted(payload["cases"], key=lambda r: r["Delta"])]
            manifest = json.loads((base / "manifest_mu_m5_D0_to_D0p3_Nbin100000.json").read_text())
            manifest.pop("production_decision", None)
            manifest["seed_policy"] = "Initial seeds are base_seed + case_index, expanded to per-MPI-rank seeds by the campaign writer. The paper used one rank. Archived inputs preserve the actual seeds.txt bytes."
            write_json(target / "manifest.json", manifest)
            figure = base / "publication_report/figures/paper_candidate_main_delta_1x4_linear.pdf"
            script = base / "publication_report/make_production_figures.py"
            source["original_comparison_status"] = payload["status"]
        source.update({"summary_sha256": digest(records_path), "plot_script_sha256": digest(script), "original_pdf_sha256": digest(figure), "plot_style_sha256": digest(repo / "benchmarks/plot_style.py")})
        manifest_cases = []
        for case_id, run_dir, ed_path, row, x, original in entries:
            destination = target / "inputs" / case_id
            destination.mkdir(parents=True)
            for name in INPUT_FILES:
                shutil.copyfile(run_dir / name, destination / name)
            ed_dest = target / "ed" / (case_id + ".json")
            ed_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ed_path, ed_dest)
            archive = target / "raw" / (case_id + ".tar.gz")
            archive.parent.mkdir(parents=True, exist_ok=True)
            raw_hashes = {}
            with archive.open("wb") as output, gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0, compresslevel=6) as gz, tarfile.open(fileobj=gz, mode="w|") as tar:
                for name in RAW_FILES:
                    content = (run_dir / name).read_bytes()
                    raw_hashes[name] = hashlib.sha256(content).hexdigest()
                    info = tarfile.TarInfo(name)
                    info.size, info.mtime, info.mode = len(content), 0, 0o644
                    tar.addfile(info, io.BytesIO(content))
            params = json.loads((run_dir / "params.json").read_text())
            parameters = params.get("parameters", params)
            observables = {}
            for name in ("density_total", "energy_density", "S_SF_K", "S_DW_K"):
                values = original["observables"][name]
                observables[name] = {k: values[k] for k in ("dqmc", "ed", "stderr", "reason", "reliable", "z_score", "pass_uncertainty") if k in values}
            case = {
                "id": case_id, "model": model, "row": row, "x": x,
                "parameters": parameters, "block_size": 10000, "samples": 100000,
                "skip_samples": 0, "observables": observables,
                "input_dir": str(destination.relative_to(out)),
                "ed_file": str(ed_dest.relative_to(out)),
                "raw_archive": str(archive.relative_to(out)), "raw_sha256": raw_hashes,
                "original_run_dir": str(run_dir.relative_to(repo)),
                "ed_status": json.loads(ed_path.read_text()).get("status", "fixed_cutoff_dense_trace"),
                "reference_kind": "exact_free_boson" if model == "number_conserving" and parameters["U1"] == parameters["U2"] == 0 else "finite_cutoff_ed",
            }
            all_cases.append(case)
            manifest_cases.append({"id": case_id, "input_dir": "inputs/" + case_id, "ed_params": "inputs/" + case_id + "/params.json", "parameters": parameters, "analysis": {"block_size": 10000, "skip_samples": 0}, "ed_policy": params.get("convergence_policy", {})})
            print(model, case_id, f"{archive.stat().st_size / 1e6:.2f} MB", flush=True)
        if model == "number_conserving":
            write_json(target / "manifest.json", {"schema_version": 1, "cases": manifest_cases})
        sources[model] = source
    index = {"schema_version": 1, "sources": sources, "cases": all_cases}
    write_json(out / "index.json", index)
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from reproducibility.analysis import recompute, save_tables
    from reproducibility.manuscript import select_index
    cases, blocks = recompute(select_index(index), out)
    save_tables(cases, blocks, out)
    # Raw measurements are intentionally local/ignored; the tracked package is small.
    write_json(out / "checksums.json", {str(p.relative_to(out)): digest(p) for p in sorted(out.rglob("*")) if p.is_file() and "raw" not in p.relative_to(out).parts and p.name != "checksums.json"})


if __name__ == "__main__":
    main()
