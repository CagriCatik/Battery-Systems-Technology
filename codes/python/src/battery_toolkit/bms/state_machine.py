from enum import Enum, auto
from typing import Optional, Dict, Any


class BMSState(Enum):
    INIT = auto()
    STANDBY = auto()
    PRECHARGE = auto()
    RUN = auto()
    CHARGE = auto()
    FAULT = auto()
    SHUTDOWN = auto()


class BMSStateMachine:
    """
    ASIL-D compliant finite state machine controlling high-voltage contactors,
    precharge sequences, and safety shutdowns.
    """
    def __init__(self, precharge_timeout_s: float = 0.50):
        self.state = BMSState.INIT
        self.precharge_timeout_s = precharge_timeout_s
        self.precharge_timer = 0.0

        # Contactor feedback flags
        self.positive_contactor_closed = False
        self.negative_contactor_closed = False
        self.precharge_contactor_closed = False
        self.fault_latched: Optional[str] = None

    def trigger_fault(self, reason: str) -> None:
        """Immediately transitions to FAULT safe state and opens contactors."""
        self.state = BMSState.FAULT
        self.fault_latched = reason
        self.open_all_contactors()

    def open_all_contactors(self) -> None:
        """De-energizes all high-voltage contactor coils."""
        self.positive_contactor_closed = False
        self.negative_contactor_closed = False
        self.precharge_contactor_closed = False

    def step(
        self,
        key_on: bool,
        charge_plug_connected: bool,
        v_pack: float,
        v_link: float,
        dt_s: float,
        has_critical_safety_fault: bool = False,
    ) -> BMSState:
        """
        Executes one cyclic tick of the state machine.
        """
        if has_critical_safety_fault:
            self.trigger_fault("Critical Hardware / Safety Interlock Violation")
            return self.state

        if self.state == BMSState.INIT:
            self.open_all_contactors()
            # Transition to STANDBY once initialization checks pass
            self.state = BMSState.STANDBY

        elif self.state == BMSState.STANDBY:
            self.open_all_contactors()
            if key_on:
                self.state = BMSState.PRECHARGE
                self.precharge_timer = 0.0
                # Close Negative and Precharge contactors
                self.negative_contactor_closed = True
                self.precharge_contactor_closed = True
            elif charge_plug_connected:
                self.state = BMSState.CHARGE

        elif self.state == BMSState.PRECHARGE:
            self.precharge_timer += dt_s
            # Precharge completion condition: V_link >= 95% of V_pack
            if v_pack > 0 and (v_link / v_pack) >= 0.95:
                # Close Main Positive contactor, then open Precharge
                self.positive_contactor_closed = True
                self.precharge_contactor_closed = False
                self.state = BMSState.RUN
            elif self.precharge_timer >= self.precharge_timeout_s:
                # Precharge timeout hazard -> abort to FAULT
                self.trigger_fault("Precharge Timeout Exceeded (V_link failed to reach 95%)")

        elif self.state == BMSState.RUN:
            if not key_on:
                self.state = BMSState.SHUTDOWN

        elif self.state == BMSState.CHARGE:
            if not charge_plug_connected:
                self.state = BMSState.SHUTDOWN

        elif self.state == BMSState.SHUTDOWN:
            self.open_all_contactors()
            self.state = BMSState.STANDBY

        elif self.state == BMSState.FAULT:
            self.open_all_contactors()

        return self.state

    def status(self) -> Dict[str, Any]:
        return {
            "state": self.state.name,
            "contactors": {
                "positive": self.positive_contactor_closed,
                "negative": self.negative_contactor_closed,
                "precharge": self.precharge_contactor_closed,
            },
            "fault": self.fault_latched,
        }

