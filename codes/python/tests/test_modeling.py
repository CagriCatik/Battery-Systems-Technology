import numpy as np
import pytest
from battery_toolkit.modeling.ecm import TheveninECM, DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel
from battery_toolkit.modeling.hppc import HPPCExtractor


def test_thevenin_ecm_step():
    ecm = TheveninECM(r0=0.015, r1=0.010, c1=1000.0) # tau = 10s
    assert ecm.tau1 == 10.0

    # Step response with constant 50A discharge for 1s
    v1 = ecm.step(current_a=50.0, dt_s=1.0)
    assert v1 > 0.0 and v1 < (50.0 * 0.010)

    # Steady-state terminal voltage
    vt = ecm.compute_terminal_voltage(ocv=3.80, current_a=50.0)
    assert vt < 3.80


def test_dual_polarization_ecm():
    dp = DualPolarizationECM(r0=0.015, r1=0.008, c1=1500.0, r2=0.020, c2=10000.0)
    v1, v2 = dp.step(current_a=30.0, dt_s=0.5)
    assert v1 > 0.0
    assert v2 > 0.0
    vt = dp.compute_terminal_voltage(ocv=3.75, current_a=30.0)
    assert vt == pytest.approx(3.75 - 30.0 * 0.015 - v1 - v2, 1e-4)


def test_ocv_model_and_hysteresis():
    ocv_mod = OCVModel()
    # Check baseline OCV at 50% SOC
    v_50 = ocv_mod.get_equilibrium_ocv(0.50, temp_celsius=25.0)
    assert v_50 == pytest.approx(3.82, 0.05)

    # Entropic shift at 45°C
    v_hot = ocv_mod.get_equilibrium_ocv(0.50, temp_celsius=45.0)
    assert v_hot < v_50 # Negative entropic coefficient

    # Derivative dOCV/dSOC
    derivative = ocv_mod.get_derivative(0.50)
    assert derivative > 0.0

    # Hysteresis update
    v_hyst = ocv_mod.update_hysteresis(current_a=20.0, dt_s=10.0)
    assert v_hyst > 0.0


def test_hppc_extractor():
    extractor = HPPCExtractor()
    time_s = np.linspace(0, 50, 501)
    # Synthesize pulse: 0 to 10s rest, 10 to 20s 50A pulse, 20 to 50s rest
    current_a = np.zeros_like(time_s)
    current_a[(time_s >= 10.0) & (time_s <= 20.0)] = 50.0

    voltage_v = np.zeros_like(time_s)
    voltage_v[time_s < 10.0] = 3.80
    # During pulse: IR drop = 50A * 0.02 = 1.0V drop -> 2.80V
    voltage_v[(time_s >= 10.0) & (time_s <= 20.0)] = 2.80
    # Relaxation phase
    voltage_v[time_s > 20.0] = 3.80 - 0.2 * np.exp(-(time_s[time_s > 20.0] - 20.0) / 5.0)

    params = extractor.extract_parameters(time_s, voltage_v, current_a, t_pulse_start=10.0, t_pulse_end=20.0)
    assert params.r0 > 0.01
    assert params.r1 > 0.0
    assert params.c1 > 0.0

