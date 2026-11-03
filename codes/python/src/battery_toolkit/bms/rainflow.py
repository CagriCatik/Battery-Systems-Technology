import math
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class CycleDamage:
    """Extracted micro-cycle from Rainflow analysis."""
    range_dod: float   # Delta Depth of Discharge in [0, 1]
    mean_soc: float    # Mean State of Charge in [0, 1]
    count: float       # 0.5 for half-cycle, 1.0 for full closed loop
    damage: float      # Relative fractional damage: count / N_f


class RainflowCounter:
    """
    Implementation of the standard ASTM E1049-85 Rainflow Cycle Counting Algorithm
    coupled with Palmgren-Miner Linear Cumulative Fatigue Damage rule for battery lifetime estimation.
    """
    def __init__(
        self,
        n0_cycles: float = 3500.0,
        beta_dod: float = 1.65,
        k_soc: float = 1.04,
        activation_energy_ev: float = 0.35,
    ):
        self.n0 = n0_cycles
        self.beta = beta_dod
        self.k_soc = k_soc
        self.ea = activation_energy_ev
        self.k_boltzmann_ev = 8.617333262145e-5 # eV/K

    def extract_turning_points(self, time_series: np.ndarray) -> np.ndarray:
        """Filters intermediate points, extracting local peaks and valleys."""
        diffs = np.diff(time_series)
        turning_mask = np.zeros(len(time_series), dtype=bool)
        turning_mask[0] = True
        turning_mask[-1] = True

        for i in range(1, len(time_series) - 1):
            if (diffs[i - 1] > 0 and diffs[i] < 0) or (diffs[i - 1] < 0 and diffs[i] > 0):
                turning_mask[i] = True

        return time_series[turning_mask]

    def count_cycles(self, soc_history: np.ndarray, temp_celsius: float = 25.0) -> List[CycleDamage]:
        """
        Executes 3-point Rainflow counting algorithm conforming to ASTM E1049-85.
        Returns list of extracted cycles with their respective Palmgren-Miner damage fractions.
        """
        points = self.extract_turning_points(soc_history)
        stack = []
        cycles: List[CycleDamage] = []

        for p in points:
            stack.append(p)
            while len(stack) >= 3:
                s0 = stack[-3]
                s1 = stack[-2]
                s2 = stack[-1]

                delta_y = abs(s1 - s0)
                delta_x = abs(s2 - s1)

                if delta_x >= delta_y:
                    # Inner cycle detected
                    range_dod = delta_y
                    mean_soc = (s0 + s1) / 2.0
                    is_full_cycle = len(stack) > 3

                    count = 1.0 if is_full_cycle else 0.5
                    n_f = self.calculate_cycle_life(range_dod, mean_soc, temp_celsius)
                    damage = count / max(n_f, 1.0)

                    cycles.append(CycleDamage(range_dod=range_dod, mean_soc=mean_soc, count=count, damage=damage))
                    # Remove the middle point s1
                    stack.pop(-2)
                else:
                    break

        # Process residual half-cycles remaining in stack
        while len(stack) >= 2:
            s0 = stack.pop(0)
            s1 = stack[0]
            range_dod = abs(s1 - s0)
            mean_soc = (s0 + s1) / 2.0
            n_f = self.calculate_cycle_life(range_dod, mean_soc, temp_celsius)
            damage = 0.5 / max(n_f, 1.0)
            cycles.append(CycleDamage(range_dod=range_dod, mean_soc=mean_soc, count=0.5, damage=damage))

        return cycles

    def calculate_cycle_life(self, range_dod: float, mean_soc: float, temp_celsius: float) -> float:
        """
        Modified Wöhler-Arrhenius cycle life formulation:
        N_f = N0 * (DoD / 1.0)^(-beta) * exp(-k_soc * (mean_soc - 0.5)) * exp((Ea/k) * (1/T - 1/T_ref))
        """
        dod = max(0.01, min(1.0, range_dod))
        t_kelvin = temp_celsius + 273.15
        t_ref_kelvin = 298.15 # 25°C

        dod_term = (dod / 1.0) ** (-self.beta)
        soc_term = math.exp(-self.k_soc * (mean_soc - 0.5))
        temp_term = math.exp((self.ea / self.k_boltzmann_ev) * ((1.0 / t_kelvin) - (1.0 / t_ref_kelvin)))

        return self.n0 * dod_term * soc_term * temp_term

    def compute_palmgren_miner_damage(self, cycles: List[CycleDamage]) -> float:
        """
        Total cumulative fatigue damage: D_total = sum( 1 / N_f ).
        Failure occurs when D_total >= 1.0 (80% SOH End of Life).
        """
        return sum(c.damage for c in cycles)
