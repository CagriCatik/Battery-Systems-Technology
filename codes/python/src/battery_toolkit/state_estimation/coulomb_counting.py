from typing import Optional


class CoulombCounter:
    """
    Enhanced Coulomb Counting state estimation with:
    - Direction-dependent Coulombic efficiency eta_c
    - Peukert capacity compensation under high discharge rates
    - Thermal capacity derating factor
    """
    def __init__(
        self,
        nominal_capacity_ah: float,
        initial_soc: float = 1.0,
        coulombic_efficiency_charge: float = 0.985,
        coulombic_efficiency_discharge: float = 1.000,
        peukert_exponent: float = 1.05,
    ):
        self.c_nom = nominal_capacity_ah
        self.soc = float(initial_soc)
        self.eta_chg = coulombic_efficiency_charge
        self.eta_dis = coulombic_efficiency_discharge
        self.peukert_k = peukert_exponent
        self.accumulated_charge_as = 0.0 # Ampere-seconds

    def update(self, current_a: float, dt_s: float, temp_celsius: float = 25.0) -> float:
        """
        Integrates current throughput to advance State of Charge:
        SOC[k+1] = SOC[k] - (eta * I * dt) / (C_eff * 3600)
        Convention: current_a > 0 for discharge, current_a < 0 for charge.
        """
        if current_a < 0:
            # Charging: efficiency < 1.0
            eta = self.eta_chg
            effective_capacity = self.c_nom
        else:
            # Discharging: apply Peukert derating if current > 1C
            eta = self.eta_dis
            c_rate = current_a / max(self.c_nom, 1e-3)
            if c_rate > 1.0 and self.peukert_k > 1.0:
                # C_eff = C_nom / (c_rate)^(k - 1)
                effective_capacity = self.c_nom / (c_rate ** (self.peukert_k - 1.0))
            else:
                effective_capacity = self.c_nom

        # Temperature capacity derating (Arrhenius capacity degradation at sub-zero)
        if temp_celsius < 0.0:
            temp_factor = max(0.40, 1.0 + 0.02 * temp_celsius)
            effective_capacity *= temp_factor

        delta_soc = (eta * current_a * dt_s) / (effective_capacity * 3600.0)
        self.soc -= delta_soc
        self.soc = float(max(0.0, min(1.0, self.soc)))
        self.accumulated_charge_as += abs(current_a) * dt_s

        return self.soc

    def reset_soc(self, new_soc: float) -> None:
        """Resets SOC (e.g. upon OCV-rest calibration)."""
        self.soc = float(max(0.0, min(1.0, new_soc)))

