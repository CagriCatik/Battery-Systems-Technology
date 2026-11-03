from enum import Enum, auto
from typing import Dict, Any, Optional
import time


class PinFaultType(Enum):
    NOMINAL = auto()
    OPEN_CIRCUIT = auto()
    SHORT_TO_GROUND = auto()
    SHORT_TO_BATTERY = auto()


class VirtualXILEnvironment:
    """
    Virtual ASAM XIL test environment simulating Model Access Port (MAP)
    and Electrical Error Simulation (EES) Fault Injection Unit (FIU).
    """
    def __init__(self, pack_size: int = 96):
        self.pack_size = pack_size
        self.variables: Dict[str, Any] = {}
        self.pin_faults: Dict[str, PinFaultType] = {}

        # Initialize nominal states
        for i in range(1, pack_size + 1):
            self.variables[f"Cell_{i}_Voltage"] = 3.700
            self.pin_faults[f"PIN_CELL_SENSE_{i}"] = PinFaultType.NOMINAL

        self.variables["DUT_Contactor_Closed"] = True
        self.variables["DUT_Pack_Current"] = 0.0
        self.variables["DUT_HVIL_Status"] = True
        self.variables["DUT_Fault_Latched"] = False

    def write_variable(self, name: str, value: Any) -> None:
        """MAP Port: sets simulation model variable."""
        self.variables[name] = value

    def read_variable(self, name: str) -> Any:
        """MAP Port: reads simulation model or DUT feedback variable."""
        return self.variables.get(name, None)

    def set_pin_fault(self, pin_name: str, fault_type: PinFaultType) -> None:
        """EES Port: injects electrical hardware fault."""
        self.pin_faults[pin_name] = fault_type

        # Simulate electrical effect of fault on DUT feedback
        if fault_type == PinFaultType.OPEN_CIRCUIT and "HVIL" in pin_name:
            self.variables["DUT_HVIL_Status"] = False
            # FTTI trip: opening contactors within 15 ms
            self.variables["DUT_Contactor_Closed"] = False
            self.variables["DUT_Fault_Latched"] = True

        elif fault_type == PinFaultType.OPEN_CIRCUIT and "CELL_SENSE" in pin_name:
            cell_num = pin_name.split("_")[-1]
            # AFE pull-down causes voltage collapse to 0V
            self.variables[f"Cell_{cell_num}_Voltage"] = 0.000

    def clear_all_faults(self) -> None:
        """Restores all pins to nominal state."""
        for pin in self.pin_faults:
            self.pin_faults[pin] = PinFaultType.NOMINAL
        self.variables["DUT_HVIL_Status"] = True
        self.variables["DUT_Fault_Latched"] = False

