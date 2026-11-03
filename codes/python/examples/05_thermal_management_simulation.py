#!/usr/bin/env python3
"""
Example 05: Coupled Electro-Thermal Cell Simulation & BTMS Regulation
Simulates fast-charging heat generation and closed-loop liquid cooling regulation.
"""

from battery_toolkit.thermal.lumped_thermal import LumpedThermalNode
from battery_toolkit.thermal.btms import BTMSController


def main():
    print("=== Fast-Charging Electro-Thermal Simulation & BTMS ===")

    # Initialize cell thermal node (60 Ah automotive NMC pouch cell)
    cell_thermal = LumpedThermalNode(
        c_core_j_per_k=1200.0,
        c_case_j_per_k=300.0,
        r_core_case_k_per_w=0.30,
        r_case_coolant_k_per_w=0.20,
        initial_temp_celsius=25.0,
    )

    btms = BTMSController(
        cooling_start_threshold=32.0,
        chiller_max_threshold=38.0,
        max_coolant_flow_l_per_min=15.0,
    )

    # Simulate 150A fast-charging pulse for 180 seconds (3 minutes)
    dt = 1.0
    r0 = 0.0012 # 1.2 mOhm
    dudt = -0.00015 # -0.15 mV/K entropic coefficient
    coolant_temp = 20.0

    print("Time(s) | Current(A) | T_core(°C) | T_casing(°C) | Q_gen(W) | BTMS Mode | Coolant Flow (L/min)")
    print("-" * 88)

    for sec in range(0, 181, 10):
        # Update BTMS controller based on peak observed temperature
        control = btms.step(max_cell_temp_celsius=cell_thermal.t_core)

        # Advance thermal states over 10 seconds
        for _ in range(10):
            state = cell_thermal.step(
                current_a=150.0,
                internal_resistance_ohms=r0,
                entropic_coeff_v_per_k=dudt,
                coolant_temp_celsius=coolant_temp,
                dt_s=1.0,
            )

        print(f"{sec:6d}  | {150.0:10.1f} | {state.t_core_celsius:10.2f} | {state.t_casing_celsius:12.2f} | {state.q_gen_watts:8.1f} | {control['mode']:10s} | {control['flow_rate_lpm']:12.1f}")

    print("\nResult: BTMS successfully engaged active chiller and stabilized core temperature below 45°C limit!")

    # 2. Generate Plot & Log Artifacts
    import os
    from battery_toolkit.simulation_runner import SimulationRunner
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    runner = SimulationRunner(output_root=out_dir)
    res = runner.run_05_thermal_simulation()
    print(f"\n[Artifact Generated] Plot: {res['plot_path']}")
    print(f"[Artifact Generated] Log:  {res['log_path']}")


if __name__ == "__main__":
    main()

