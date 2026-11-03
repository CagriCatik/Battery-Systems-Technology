#!/usr/bin/env python3
"""
Example 02: 2-RC Dual Polarization ECM Simulation & HPPC Extraction
Simulates pulse discharge and identifies R0, R1, C1, R2, C2 parameters.
"""

import numpy as np
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel
from battery_toolkit.modeling.hppc import HPPCExtractor


def main():
    print("=== ECM Simulation & HPPC Parameter Extraction ===")

    # 1. Ground Truth 2-RC Model
    r0_true = 0.018
    r1_true = 0.009
    c1_true = 1800.0 # tau1 = 16.2s
    r2_true = 0.015
    c2_true = 8000.0 # tau2 = 120s

    true_ecm = DualPolarizationECM(r0=r0_true, r1=r1_true, c1=c1_true, r2=r2_true, c2=c2_true)
    ocv_model = OCVModel()

    # 2. Simulate 10-second 40A discharge pulse followed by 60-second relaxation
    dt = 0.1
    time_s = np.arange(0.0, 90.0, dt)
    current_a = np.zeros_like(time_s)
    # 40A discharge between t = 10s and t = 20s
    current_a[(time_s >= 10.0) & (time_s < 20.0)] = 40.0

    voltage_v = np.zeros_like(time_s)
    soc = 0.75
    ocv_val = ocv_model.get_equilibrium_ocv(soc)

    for i, t in enumerate(time_s):
        curr = current_a[i]
        true_ecm.step(curr, dt)
        voltage_v[i] = true_ecm.compute_terminal_voltage(ocv_val, curr)

    print(f"Simulated {len(time_s)} steps of HPPC pulse (Peak Current: 40 A).")
    print(f"Initial Voltage: {voltage_v[0]:.3f} V, Min Voltage during pulse: {np.min(voltage_v):.3f} V")

    # 3. Extract parameters using non-linear least squares
    extractor = HPPCExtractor()
    params = extractor.extract_parameters(time_s, voltage_v, current_a, t_pulse_start=10.0, t_pulse_end=20.0)

    print("\n--- Extracted Parameters vs Ground Truth ---")
    print(f"R0: {params.r0 * 1000.0:.2f} mOhm (True: {r0_true * 1000.0:.2f} mOhm)")
    print(f"R1: {params.r1 * 1000.0:.2f} mOhm (True: {r1_true * 1000.0:.2f} mOhm)")
    print(f"C1: {params.c1:.1f} F (True: {c1_true:.1f} F)")
    print(f"R2: {params.r2 * 1000.0:.2f} mOhm (True: {r2_true * 1000.0:.2f} mOhm)")
    print(f"C2: {params.c2:.1f} F (True: {c2_true:.1f} F)")


if __name__ == "__main__":
    main()

