from dataclasses import dataclass
from typing import Tuple


@dataclass
class ThermalState:
    t_core_celsius: float
    t_casing_celsius: float
    q_gen_watts: float
    q_cooling_watts: float


class LumpedThermalNode:
    """
    Two-node lumped electro-thermal model for a battery cell or module:
    - Node 1: Cell Core (heat generation, high thermal mass)
    - Node 2: Cell Casing / Busbar (surface interface with cooling plate)
    
    Differential Equations:
    C_core * dT_core/dt = Q_gen - (T_core - T_case) / R_core_case
    C_case * dT_case/dt = (T_core - T_case) / R_core_case - (T_case - T_coolant) / R_case_coolant
    """
    def __init__(
        self,
        c_core_j_per_k: float = 60.0,
        c_case_j_per_k: float = 15.0,
        r_core_case_k_per_w: float = 2.5,
        r_case_coolant_k_per_w: float = 1.8,
        initial_temp_celsius: float = 25.0,
    ):
        self.c_core = c_core_j_per_k
        self.c_case = c_case_j_per_k
        self.r_cc = r_core_case_k_per_w
        self.r_cp = r_case_coolant_k_per_w

        self.t_core = float(initial_temp_celsius)
        self.t_case = float(initial_temp_celsius)

    def step(
        self,
        current_a: float,
        internal_resistance_ohms: float,
        entropic_coeff_v_per_k: float,
        coolant_temp_celsius: float,
        dt_s: float,
    ) -> ThermalState:
        """
        Calculates heat generation and updates temperatures over time interval dt_s.
        Q_gen = I^2 * R + I * T_core_K * (dU/dT)
        """
        t_core_k = self.t_core + 273.15

        # Joule heating: always positive
        q_joule = (current_a ** 2) * internal_resistance_ohms

        # Entropic reversible heat: positive (heating) or negative (cooling) depending on current direction
        q_reversible = current_a * t_core_k * entropic_coeff_v_per_k

        q_gen = max(0.0, q_joule + q_reversible)

        # Core to casing conductive heat transfer
        q_core_to_case = (self.t_core - self.t_case) / self.r_cc

        # Casing to coolant plate heat transfer
        q_cooling = (self.t_case - coolant_temp_celsius) / self.r_cp

        # Numerical integration (Forward Euler)
        dt_core = (q_gen - q_core_to_case) / self.c_core * dt_s
        dt_case = (q_core_to_case - q_cooling) / self.c_case * dt_s

        self.t_core += dt_core
        self.t_case += dt_case

        return ThermalState(
            t_core_celsius=round(self.t_core, 2),
            t_casing_celsius=round(self.t_case, 2),
            q_gen_watts=round(q_gen, 2),
            q_cooling_watts=round(q_cooling, 2),
        )

