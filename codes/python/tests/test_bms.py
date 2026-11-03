import numpy as np
import pytest
from battery_toolkit.bms.state_machine import BMSStateMachine, BMSState
from battery_toolkit.bms.balancing import PassiveBalancingSimulator, ActiveBalancingSimulator
from battery_toolkit.bms.rainflow import RainflowCounter


def test_bms_state_machine_precharge_success():
    fsm = BMSStateMachine(precharge_timeout_s=0.5)
    assert fsm.state == BMSState.INIT

    # 1. Step to STANDBY
    fsm.step(key_on=False, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01)
    assert fsm.state == BMSState.STANDBY

    # 2. Key-on triggers PRECHARGE
    fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01)
    assert fsm.state == BMSState.PRECHARGE
    assert fsm.precharge_contactor_closed is True
    assert fsm.negative_contactor_closed is True

    # 3. Precharge completion: V_link reaches 96% of V_pack (365V)
    fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=366.0, dt_s=0.01)
    assert fsm.state == BMSState.RUN
    assert fsm.positive_contactor_closed is True
    assert fsm.precharge_contactor_closed is False


def test_bms_state_machine_precharge_timeout():
    fsm = BMSStateMachine(precharge_timeout_s=0.1)
    fsm.step(key_on=False, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01)
    fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=0.0, dt_s=0.01) # PRECHARGE

    # Let timer exceed 0.1s without V_link ramping
    for _ in range(15):
        fsm.step(key_on=True, charge_plug_connected=False, v_pack=380.0, v_link=50.0, dt_s=0.01)

    assert fsm.state == BMSState.FAULT
    assert fsm.positive_contactor_closed is False
    assert fsm.precharge_contactor_closed is False


def test_passive_balancing():
    sim = PassiveBalancingSimulator(bleed_resistor_ohms=33.0, threshold_voltage_v=0.010)
    # Cells: 3 cells at 4.00V, 1 unbalanced cell at 4.05V (+50 mV delta)
    voltages = np.array([4.00, 4.00, 4.05, 4.00])
    res = sim.compute_dissipation(voltages)

    assert res["active_channels_count"] == 1
    assert res["active_mask"] == [False, False, True, False]
    assert res["total_pcb_dissipation_w"] > 0.40


def test_rainflow_cycle_counting():
    counter = RainflowCounter()
    # Synthetic micro-cycles in SOC profile
    soc_series = np.array([1.0, 0.8, 0.9, 0.7, 0.85, 0.6, 0.95, 0.2, 1.0])
    cycles = counter.count_cycles(soc_series)
    assert len(cycles) > 0

    damage = counter.compute_palmgren_miner_damage(cycles)
    assert damage > 0.0 and damage < 0.1

