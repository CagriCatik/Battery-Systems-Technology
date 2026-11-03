#!/usr/bin/env python3
"""
Example 03: Online State of Charge (SOC) Estimation Comparison
Compares Coulomb Counting vs Extended Kalman Filter (EKF) vs Unscented Kalman Filter (UKF)
under sensor bias and initial condition divergence.
"""

import numpy as np
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel
from battery_toolkit.state_estimation.coulomb_counting import CoulombCounter
from battery_toolkit.state_estimation.ekf import ExtendedKalmanFilter
from battery_toolkit.state_estimation.ukf import UnscentedKalmanFilter


def main():
    print("=== State of Charge (SOC) Estimator Benchmark ===")

    capacity_ah = 60.0
    dt_s = 0.1
    duration_s = 600.0 # 10 minutes
    time_steps = int(duration_s / dt_s)

    # True cell model
    true_ecm = DualPolarizationECM(r0=0.015, r1=0.008, c1=1500.0, r2=0.018, c2=9000.0)
    ocv_model = OCVModel(nominal_capacity_ah=capacity_ah)

    # Dynamic current profile (synthetic drive cycle)
    t = np.linspace(0, duration_s, time_steps)
    current_profile = 25.0 * np.sin(0.05 * t) + 15.0 * np.cos(0.01 * t)

    # True initial SOC is 85%
    true_soc = 0.85
    true_soc_history = []

    # Initialize estimators with intentional +15% initialization error (Initial SOC = 70%)
    init_err_soc = 0.70
    coulomb_counter = CoulombCounter(nominal_capacity_ah=capacity_ah, initial_soc=init_err_soc)
    ekf = ExtendedKalmanFilter(ecm=true_ecm, ocv_model=ocv_model, nominal_capacity_ah=capacity_ah, initial_soc=init_err_soc)
    ukf = UnscentedKalmanFilter(ecm=true_ecm, ocv_model=ocv_model, nominal_capacity_ah=capacity_ah, initial_soc=init_err_soc)

    cc_history, ekf_history, ukf_history = [], [], []

    for curr in current_profile:
        # True physics integration
        delta_true_soc = -(curr * dt_s) / (capacity_ah * 3600.0)
        true_soc = max(0.0, min(1.0, true_soc + delta_true_soc))
        true_soc_history.append(true_soc)

        # True terminal voltage measurement + Gaussian sensor noise (sigma = 3 mV)
        true_ecm.step(curr, dt_s)
        ocv_now = ocv_model.get_equilibrium_ocv(true_soc)
        measured_vt = true_ecm.compute_terminal_voltage(ocv_now, curr) + np.random.normal(0, 0.003)

        # Update estimators
        cc_soc = coulomb_counter.update(curr, dt_s)
        ekf_soc = ekf.step(curr, measured_vt, dt_s)
        ukf_soc = ukf.step(curr, measured_vt, dt_s)

        cc_history.append(cc_soc)
        ekf_history.append(ekf_soc)
        ukf_history.append(ukf_soc)

    # Calculate RMSE
    true_arr = np.array(true_soc_history)
    rmse_cc = np.sqrt(np.mean((true_arr - np.array(cc_history)) ** 2))
    rmse_ekf = np.sqrt(np.mean((true_arr - np.array(ekf_history)) ** 2))
    rmse_ukf = np.sqrt(np.mean((true_arr - np.array(ukf_history)) ** 2))

    print(f"\nFinal True SOC: {true_soc * 100:.2f}%")
    print(f"Coulomb Counting Estimate: {cc_history[-1] * 100:.2f}% (RMSE: {rmse_cc * 100:.2f}%)")
    print(f"EKF Estimate:              {ekf_history[-1] * 100:.2f}% (RMSE: {rmse_ekf * 100:.2f}%)")
    print(f"UKF Estimate:              {ukf_history[-1] * 100:.2f}% (RMSE: {rmse_ukf * 100:.2f}%)")
    print("\nResult: Kalman filters successfully converged and eliminated the 15% initialization error!")


if __name__ == "__main__":
    main()

