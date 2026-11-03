import pytest
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel
from battery_toolkit.state_estimation.coulomb_counting import CoulombCounter
from battery_toolkit.state_estimation.ekf import ExtendedKalmanFilter
from battery_toolkit.state_estimation.ukf import UnscentedKalmanFilter
from battery_toolkit.state_estimation.rls import RecursiveLeastSquares


def test_coulomb_counter():
    cc = CoulombCounter(nominal_capacity_ah=50.0, initial_soc=1.0)
    # 50A discharge for 1800s (0.5 hour) = 25 Ah = 50% SOC drop
    soc = cc.update(current_a=50.0, dt_s=1800.0)
    assert soc == pytest.approx(0.50, 0.01)


def test_ekf_convergence():
    ecm = DualPolarizationECM(r0=0.015, r1=0.008, c1=1000.0, r2=0.015, c2=8000.0)
    ocv = OCVModel(nominal_capacity_ah=50.0)

    # Initialize EKF with intentional initial error: true SOC = 0.80, EKF initialized at 0.60
    ekf = ExtendedKalmanFilter(ecm=ecm, ocv_model=ocv, nominal_capacity_ah=50.0, initial_soc=0.60)

    true_soc = 0.80
    for _ in range(50):
        # Simulate true terminal voltage under 10A current
        true_vt = ocv.get_equilibrium_ocv(true_soc) - 10.0 * 0.015
        est_soc = ekf.step(current_a=10.0, measured_voltage_v=true_vt, dt_s=0.1)

    # EKF must correct toward true SOC (0.80)
    assert est_soc > 0.70


def test_ukf_step():
    ecm = DualPolarizationECM(r0=0.015, r1=0.008, c1=1000.0, r2=0.015, c2=8000.0)
    ocv = OCVModel(nominal_capacity_ah=50.0)
    ukf = UnscentedKalmanFilter(ecm=ecm, ocv_model=ocv, nominal_capacity_ah=50.0, initial_soc=0.75)

    soc = ukf.step(current_a=5.0, measured_voltage_v=3.95, dt_s=0.1)
    assert soc > 0.0 and soc <= 1.0


def test_rls_parameter_tracking():
    rls = RecursiveLeastSquares(forgetting_factor=0.99, initial_r0=0.010)
    true_r0 = 0.025

    # Excite with alternating current pulses
    for step in range(100):
        current = 30.0 if (step % 2 == 0) else -20.0
        ocv = 3.80
        vt = ocv - current * true_r0
        est_r0 = rls.step(current_a=current, terminal_voltage_v=vt, ocv_v=ocv)

    assert est_r0 == pytest.approx(true_r0, 0.002)
    assert rls.compute_soh_resistance(r0_fresh=0.015) < 1.0
