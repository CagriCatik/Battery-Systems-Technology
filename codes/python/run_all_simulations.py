#!/usr/bin/env python3
"""
Battery Toolkit Master Simulation & Artifact Generator.
Runs all multi-domain battery simulations, exporting publication-quality plots,
time-series CSV logs, and an executive technical report.
"""

import os
import shutil
from battery_toolkit.simulation_runner import SimulationRunner


def main():
    print("=" * 70)
    print("    BATTERY SYSTEMS TECHNOLOGY — MASTER SIMULATION PIPELINE")
    print("=" * 70)

    # 1. Output directories
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    webpage_assets_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "webpage", "docs", "assets", "images", "generated"
    )
    os.makedirs(webpage_assets_dir, exist_ok=True)

    # 2. Run all simulations
    runner = SimulationRunner(output_root=output_dir)
    results = runner.run_all()

    # 3. Mirror generated plots to webpage docs assets for web presentation
    print("\n--- Mirroring Plots to Webpage Assets ---")
    for plot_path in results["plots_generated"]:
        fname = os.path.basename(plot_path)
        dest = os.path.join(webpage_assets_dir, fname)
        shutil.copy2(plot_path, dest)
        print(f"  Copied {fname} -> webpage/docs/assets/images/generated/")

    # 4. Summary print
    print("\n" + "=" * 70)
    print("  SIMULATION & ARTIFACT GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Executive Markdown Report: {results['md_report']}")
    print(f"Structured JSON Summary:   {results['json_report']}")
    print(f"Plots Generated:           {len(results['plots_generated'])} figures in {runner.plots_dir}")
    print(f"Time-Series Logs:          {len(results['logs_generated'])} datasets in {runner.logs_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
