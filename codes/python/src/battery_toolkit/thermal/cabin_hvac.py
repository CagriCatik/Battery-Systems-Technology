from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CabinHVACState:
    cabin_temp_c: float
    battery_temp_c: float
    battery_soc_percent: float
    power_draw_kw: float
    hvac_mode: str


class CabinHVACModel:
    """
    Thermal model for vehicle passenger cabin.
    Balances heat infiltration from ambient against AC compressor cooling.
    """
    def __init__(
        self,
        cabin_temp_c: float = 32.0,
        target_temp_c: float = 22.0,
        heat_transfer_coeff: float = 0.05,
    ):
        self.cabin_temp = cabin_temp_c
        self.target_temp = target_temp_c
        self.k_transfer = heat_transfer_coeff

    def step(self, ambient_temp_c: float, cooling_effort: float, dt_min: float = 1.0) -> float:
        """
        Updates cabin temperature:
        - Natural warming/cooling toward ambient: k * (T_amb - T_cabin)
        - Active HVAC cooling: cooling_effort * 2.0 °C/min
        """
        heat_leak = self.k_transfer * (ambient_temp_c - self.cabin_temp) * dt_min
        cooling = cooling_effort * 1.5 * dt_min
        self.cabin_temp += heat_leak - cooling
        return self.cabin_temp


class IntegratedThermalManager:
    """
    Integrated Thermal Manager coordinating vehicle passenger cabin HVAC
    and high-voltage battery pack cooling loops.
    """
    def __init__(
        self,
        battery_capacity_kwh: float = 60.0,
        initial_battery_temp_c: float = 25.0,
        initial_cabin_temp_c: float = 32.0,
        ambient_temp_c: float = 28.0,
    ):
        self.capacity_kwh = battery_capacity_kwh
        self.battery_temp = initial_battery_temp_c
        self.ambient_temp = ambient_temp_c
        self.soc = 1.0 # 100%

        self.cabin = CabinHVACModel(cabin_temp_c=initial_cabin_temp_c)
        self.battery_thermal_mass = 120000.0 # J/°C (~300 kg pack)

    def step(self, vehicle_traction_power_kw: float, dt_min: float = 1.0) -> CabinHVACState:
        """
        Executes one minute of coupled thermal management:
        1. Determines HVAC compressor demand for cabin
        2. Computes battery Joule heat from traction + HVAC power
        3. Updates temperatures and battery SOC
        """
        # Cabin cooling effort (proportional to error)
        cabin_error = max(0.0, self.cabin.cabin_temp - self.cabin.target_temp)
        cabin_cooling_effort = min(1.0, cabin_error / 10.0)
        hvac_compressor_power_kw = cabin_cooling_effort * 2.5 # Up to 2.5 kW compressor

        # Battery cooling effort (starts cooling above 35°C)
        battery_cooling_effort = min(1.0, max(0.0, (self.battery_temp - 32.0) / 8.0))
        chiller_power_kw = battery_cooling_effort * 3.0

        total_battery_power_kw = vehicle_traction_power_kw + hvac_compressor_power_kw + chiller_power_kw

        # Battery heat generation: internal resistance loss ~ 2% of total power
        q_gen_w = 0.02 * (total_battery_power_kw * 1000.0)
        # Cooling heat extraction
        q_cool_w = battery_cooling_effort * 4000.0 # Up to 4 kW heat extraction

        net_q_w = q_gen_w - q_cool_w
        # dt in seconds = dt_min * 60
        delta_t_battery = (net_q_w * (dt_min * 60.0)) / self.battery_thermal_mass
        self.battery_temp += delta_t_battery

        # Cabin update
        self.cabin.step(self.ambient_temp, cabin_cooling_effort, dt_min)

        # SOC update
        energy_used_kwh = total_battery_power_kw * (dt_min / 60.0)
        self.soc = max(0.0, self.soc - (energy_used_kwh / self.capacity_kwh))

        mode = "ACTIVE_COOLING" if (cabin_cooling_effort > 0.1 or battery_cooling_effort > 0.1) else "STANDBY"

        return CabinHVACState(
            cabin_temp_c=round(self.cabin.cabin_temp, 2),
            battery_temp_c=round(self.battery_temp, 2),
            battery_soc_percent=round(self.soc * 100.0, 1),
            power_draw_kw=round(total_battery_power_kw, 2),
            hvac_mode=mode,
        )
