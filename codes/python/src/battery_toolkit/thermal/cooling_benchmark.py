from typing import Dict, List, Any
import numpy as np
import pandas as pd


class CoolingTechnologyBenchmark:
    """
    Evaluates and benchmarks comparative Battery Thermal Management System (BTMS) technologies:
    - Passive Air Cooling
    - Active Forced Air
    - Liquid Cooling (Glycol/Water cold plates)
    - Heat Recovery Architecture
    """
    def __init__(
        self,
        pack_thermal_mass_j_per_k: float = 150000.0,
        initial_temp_c: float = 25.0,
        ambient_temp_c: float = 28.0,
        heat_generation_w: float = 800.0,
    ):
        self.c_th = pack_thermal_mass_j_per_k
        self.t_init = initial_temp_c
        self.t_amb = ambient_temp_c
        self.q_gen = heat_generation_w

    def simulate_technology(
        self,
        system_type: str,
        duration_s: float = 3600.0,
        dt_s: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Simulates thermal response over duration_s under constant or dynamic heat generation.
        """
        steps = int(duration_s / dt_s)
        current_temp = self.t_init
        total_heat_transferred_j = 0.0
        total_energy_consumed_j = 0.0

        # System characteristic parameters
        props = {
            "Passive Air":   {"h_coeff": 15.0,  "aux_power_w": 0.0,   "eff": 1.0},
            "Active Forced Air": {"h_coeff": 45.0,  "aux_power_w": 120.0, "eff": 1.4},
            "Liquid Cooling":    {"h_coeff": 180.0, "aux_power_w": 250.0, "eff": 2.5},
            "Heat Recovery":     {"h_coeff": 110.0, "aux_power_w": 150.0, "eff": 1.8},
        }

        cfg = props.get(system_type, props["Passive Air"])
        temps = []

        for _ in range(steps):
            delta_t = current_temp - self.t_amb
            heat_rejected_w = max(0.0, cfg["h_coeff"] * delta_t * cfg["eff"])
            net_heat_w = self.q_gen - heat_rejected_w

            current_temp += (net_heat_w * dt_s) / self.c_th
            temps.append(current_temp)

            total_heat_transferred_j += heat_rejected_w * dt_s
            total_energy_consumed_j += cfg["aux_power_w"] * dt_s

        temp_arr = np.array(temps)
        return {
            "System Type": system_type,
            "Average Battery Temperature (°C)": float(np.round(np.mean(temp_arr), 2)),
            "Maximum Battery Temperature (°C)": float(np.round(np.max(temp_arr), 2)),
            "Minimum Battery Temperature (°C)": float(np.round(np.min(temp_arr), 2)),
            "Total Heat Transferred (J)": float(np.round(total_heat_transferred_j, 1)),
            "Total Energy Consumed (J)": float(np.round(total_energy_consumed_j, 1)),
            "COP Efficiency Ratio": float(np.round(total_heat_transferred_j / max(1.0, total_energy_consumed_j), 2)),
        }

    def run_full_benchmark(self, duration_s: float = 3600.0) -> pd.DataFrame:
        """Runs comparative benchmark across all 4 cooling technologies returning a DataFrame."""
        systems = ["Passive Air", "Active Forced Air", "Liquid Cooling", "Heat Recovery"]
        records = [self.simulate_technology(s, duration_s=duration_s) for s in systems]
        return pd.DataFrame(records)

