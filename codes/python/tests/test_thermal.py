import pytest
from battery_toolkit.thermal.lumped_thermal import LumpedThermalNode
from battery_toolkit.thermal.btms import BTMSController, CoolingMode


def test_lumped_thermal_node():
    node = LumpedThermalNode(initial_temp_celsius=25.0)
    # Heavy 100A discharge pulse generates heat
    state = node.step(
        current_a=100.0,
        internal_resistance_ohms=0.015,
        entropic_coeff_v_per_k=-0.00015,
        coolant_temp_celsius=25.0,
        dt_s=1.0,
    )
    assert state.q_gen_watts > 100.0 # I^2 * R = 100^2 * 0.015 = 150W
    assert state.t_core_celsius > 25.0


def test_btms_controller():
    btms = BTMSController(cooling_start_threshold=33.0, chiller_max_threshold=40.0)

    # 1. Mild temperature: Cooling OFF
    res_mild = btms.step(max_cell_temp_celsius=25.0)
    assert res_mild["mode"] == "OFF"
    assert res_mild["flow_rate_lpm"] == 0.0

    # 2. Moderate temperature: Radiator cooling
    res_mod = btms.step(max_cell_temp_celsius=36.0)
    assert res_mod["mode"] == "PASSIVE_RADIATOR"
    assert res_mod["flow_rate_lpm"] > 0.0

    # 3. High temperature: Active chiller
    res_hot = btms.step(max_cell_temp_celsius=45.0)
    assert res_hot["mode"] == "ACTIVE_CHILLER"
    assert res_hot["chiller_duty_cycle"] > 0.5
