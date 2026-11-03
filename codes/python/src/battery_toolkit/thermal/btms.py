from enum import Enum, auto
from typing import Dict, Any


class CoolingMode(Enum):
    OFF = auto()
    PASSIVE_RADIATOR = auto()
    ACTIVE_CHILLER = auto()
    HEATING = auto()


class BTMSController:
    """
    Battery Thermal Management System (BTMS) closed-loop controller
    regulating pump coolant flow rate and refrigeration chiller engagement.
    """
    def __init__(
        self,
        target_temp_celsius: float = 25.0,
        cooling_start_threshold: float = 33.0,
        chiller_max_threshold: float = 40.0,
        heating_start_threshold: float = 10.0,
        max_coolant_flow_l_per_min: float = 12.0,
    ):
        self.t_target = target_temp_celsius
        self.t_cool_start = cooling_start_threshold
        self.t_chiller_start = chiller_max_threshold
        self.t_heat_start = heating_start_threshold
        self.max_flow = max_coolant_flow_l_per_min

        self.mode = CoolingMode.OFF
        self.flow_rate_l_per_min = 0.0
        self.chiller_duty_cycle = 0.0

    def step(self, max_cell_temp_celsius: float) -> Dict[str, Any]:
        """
        Calculates required cooling/heating mode and coolant flow rate based on peak cell temperature.
        """
        if max_cell_temp_celsius >= self.t_chiller_start:
            # Active Refrigeration Chiller required
            self.mode = CoolingMode.ACTIVE_CHILLER
            self.flow_rate_l_per_min = self.max_flow
            over_temp = max_cell_temp_celsius - self.t_chiller_start
            self.chiller_duty_cycle = min(1.0, 0.5 + 0.1 * over_temp)

        elif max_cell_temp_celsius >= self.t_cool_start:
            # Passive Radiator circulation cooling
            self.mode = CoolingMode.PASSIVE_RADIATOR
            self.chiller_duty_cycle = 0.0
            fraction = (max_cell_temp_celsius - self.t_cool_start) / (self.t_chiller_start - self.t_cool_start)
            self.flow_rate_l_per_min = 3.0 + fraction * (self.max_flow - 3.0)

        elif max_cell_temp_celsius <= self.t_heat_start:
            # Cold ambient heating mode
            self.mode = CoolingMode.HEATING
            self.flow_rate_l_per_min = 4.0
            self.chiller_duty_cycle = 0.0

        else:
            # Optimal temperature window (10°C to 33°C)
            self.mode = CoolingMode.OFF
            self.flow_rate_l_per_min = 0.0
            self.chiller_duty_cycle = 0.0

        return {
            "mode": self.mode.name,
            "flow_rate_lpm": round(self.flow_rate_l_per_min, 1),
            "chiller_duty_cycle": round(self.chiller_duty_cycle, 2),
            "cell_temp_celsius": round(max_cell_temp_celsius, 2),
        }

