import pytest
from battery_toolkit.testing.xil_client import VirtualXILEnvironment, PinFaultType


def test_virtual_xil_environment_nominal():
    env = VirtualXILEnvironment(pack_size=96)
    v_cell_1 = env.read_variable("Cell_1_Voltage")
    assert v_cell_1 == 3.700
    assert env.read_variable("DUT_Contactor_Closed") is True


def test_virtual_xil_hvil_fault():
    env = VirtualXILEnvironment(pack_size=96)
    # Inject HVIL open-circuit
    env.set_pin_fault("PIN_HVIL_IN", PinFaultType.OPEN_CIRCUIT)

    # Must cause contactor trip to safe state
    assert env.read_variable("DUT_HVIL_Status") is False
    assert env.read_variable("DUT_Contactor_Closed") is False
    assert env.read_variable("DUT_Fault_Latched") is True


def test_virtual_xil_cell_tap_open():
    env = VirtualXILEnvironment(pack_size=96)
    env.set_pin_fault("PIN_CELL_SENSE_12", PinFaultType.OPEN_CIRCUIT)
    assert env.read_variable("Cell_12_Voltage") == 0.000
