#!/usr/bin/env python3
"""
Example 04: BMS ASIL-D State Machine & Multi-Channel Cell Balancing Simulation
Demonstrates key-on precharge, contactor sequencing, and dissipative passive balancing.
"""

import numpy as np
from battery_toolkit.bms.state_machine import BMSStateMachine, BMSState
from battery_toolkit.bms.balancing import PassiveBalancingSimulator


def main():
    print("=== BMS State Machine & Cell Balancing Simulation ===")

    # 1. Initialize State Machine
    fsm = BMSStateMachine(precharge_timeout_s=0.50)
    print(f"Initial State: {fsm.state.name}")

    # Step into Standby
    fsm.step(key_on=False, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01)
    print(f"After Power-up Checks: {fsm.state.name}")

    # Key-on requested
    print("\n--- Key-On Event Triggered ---")
    fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01)
    print(f"State: {fsm.state.name} (Precharge: {fsm.precharge_contactor_closed}, Negative: {fsm.negative_contactor_closed})")

    # Simulate DC Link bus capacitor charging up
    for step in range(30):
        # Inrush through precharge resistor
        v_link = 380.0 * (1.0 - np.exp(-(step * 0.01) / 0.15))
        fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=v_link, dt_s=0.01)

    print(f"After Precharge: State: {fsm.state.name} (V_link = {v_link:.1f} V)")
    print(f"Positive Contactor: {fsm.positive_contactor_closed}, Precharge Contactor: {fsm.precharge_contactor_closed}")

    # 2. Multi-Channel Cell Balancing Simulation
    print("\n--- Passive Cell Balancing Simulation ---")
    balancer = PassiveBalancingSimulator(bleed_resistor_ohms=33.0, threshold_voltage_v=0.010)

    # 16-channel cell voltages with 2 imbalanced cells
    cell_voltages = np.array([
        4.100, 4.102, 4.101, 4.145, # Cell 4 imbalanced high (+45 mV)
        4.100, 4.099, 4.102, 4.100,
        4.138, 4.101, 4.100, 4.102, # Cell 9 imbalanced high (+38 mV)
        4.101, 4.100, 4.099, 4.100
    ])

    results = balancer.compute_dissipation(cell_voltages)
    print(f"Min Voltage: {np.min(cell_voltages):.3f} V, Max Voltage: {np.max(cell_voltages):.3f} V")
    print(f"Active Balancing Channels: {results['active_channels_count']}")
    print(f"Total PCB Heat Dissipation: {results['total_pcb_dissipation_w']} W")
    print(f"Balancing Currents (mA): {results['balancing_currents_ma']}")

    # 3. Generate Plot & Log Artifacts
    import os
    from battery_toolkit.simulation_runner import SimulationRunner
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    runner = SimulationRunner(output_root=out_dir)
    res = runner.run_04_cell_balancing_and_state_machine()
    print(f"\n[Artifact Generated] Balancing Plot: {res['balancing_plot']}")
    print(f"[Artifact Generated] Balancing Log:  {res['balancing_log']}")
    print(f"[Artifact Generated] State Machine Plot: {res['sm_plot']}")
    print(f"[Artifact Generated] State Machine Trace: {res['sm_trace']}")


if __name__ == "__main__":
    main()

