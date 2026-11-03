#!/usr/bin/env python3
"""
Example 01: Complete Battery Pack Sizing Pipeline
Calculates vehicle road loads, iterative pack mass convergence, and series-parallel topology.
Generates sizing tradeoff plots and road-load CSV logs.
"""

import os
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.sizing.vehicle import VehicleParameters
from battery_toolkit.sizing.optimizer import PackSizingOptimizer, SizingRequirements
from battery_toolkit.simulation_runner import SimulationRunner


def main():
    print("=== Battery Pack Sizing Pipeline ===")

    # 1. Select cell chemistry and cell specifications
    cell = BatteryCell(
        name="Automotive NMC-811 21700",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.65,
        capacity_ah=5.0,
        r0_mohm=22.0,
        mass_g=69.0,
        diameter_mm=21.0,
        length_mm=70.0,
    )
    print(f"Cell: {cell.name} ({cell.nominal_energy_wh:.1f} Wh, {cell.gravimetric_energy_density_wh_per_kg:.1f} Wh/kg)")

    # 2. Define Vehicle Parameters
    vehicle = VehicleParameters(
        curb_weight_kg=1850.0,
        drag_coefficient=0.23,
        frontal_area_m2=2.22,
        rolling_resistance_coeff=0.009,
        auxiliary_load_kw=0.75,
    )

    # 3. Define Sizing Requirements
    reqs = SizingRequirements(
        target_range_km=500.0,
        target_system_voltage_v=400.0,
        buffer_percentage=12.0, # 12% reserve buffer
        avg_speed_kmh=105.0,    # Highway cruising condition
    )

    optimizer = PackSizingOptimizer(cell, vehicle)
    results = optimizer.size_for_range(reqs)

    print("\n--- Sizing Results ---")
    print(f"Consumption at {reqs.avg_speed_kmh} km/h: {results['consumption_wh_per_km']} Wh/km")
    print(f"Net Energy Required: {results['net_energy_kwh']} kWh")
    print(f"Total Vehicle Mass (with Pack): {results['total_vehicle_mass_kg']} kg")
    print(f"Achieved Range: {results['achieved_range_km']} km")

    print("\n--- Pack Specifications ---")
    for k, v in results["pack_summary"].items():
        print(f"  {k}: {v}")

    # 4. Generate Plot & Log Artifacts
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    runner = SimulationRunner(output_root=out_dir)
    res = runner.run_01_pack_sizing()
    print(f"\n[Artifact Generated] Plot: {res['plot_path']}")
    print(f"[Artifact Generated] Log:  {res['log_path']}")


if __name__ == "__main__":
    main()


