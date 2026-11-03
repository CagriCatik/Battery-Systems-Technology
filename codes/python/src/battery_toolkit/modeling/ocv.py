import numpy as np
from typing import Dict, Optional


class OCVModel:
    """
    Thermodynamic Open-Circuit Voltage (OCV) model with:
    - Non-linear spline/linear interpolation against State of Charge (SOC)
    - Entropic temperature coefficient scaling: dOCV/dT
    - Continuous dynamic hysteresis state tracking: dh/dt
    """
    def __init__(
        self,
        soc_points: Optional[np.ndarray] = None,
        ocv_points: Optional[np.ndarray] = None,
        entropic_coeff_v_per_k: float = -0.00015, # Typical NMC dU/dT ~ -0.15 mV/K
        hysteresis_gamma: float = 75.0,           # Dynamic rate constant for hysteresis
        hysteresis_max_v: float = 0.025,          # Maximum hysteresis voltage envelope (e.g. 25 mV)
        nominal_capacity_ah: float = 50.0,
    ):
        if soc_points is None or ocv_points is None:
            # Default representative automotive NMC-622 OCV curve (at 25°C)
            self.soc_points = np.array([0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0])
            self.ocv_points = np.array([3.00, 3.32, 3.48, 3.61, 3.68, 3.74, 3.82, 3.90, 4.00, 4.08, 4.15, 4.18, 4.20])
        else:
            self.soc_points = np.asarray(soc_points, dtype=float)
            self.ocv_points = np.asarray(ocv_points, dtype=float)

        self.entropic_coeff = entropic_coeff_v_per_k
        self.gamma = hysteresis_gamma
        self.m_hyst_max = hysteresis_max_v
        self.capacity_ah = nominal_capacity_ah
        self.hysteresis_state = 0.0 # h(t) in [-1, +1]

    def get_equilibrium_ocv(self, soc: float, temp_celsius: float = 25.0) -> float:
        """
        Calculates thermodynamic equilibrium OCV at given SOC and temperature.
        Applies Gibbs-Helmholtz entropic temperature shift:
        U_ocv(SOC, T) = U_ocv(SOC, 25C) + (dOCV/dT) * (T - 25C)
        """
        clamped_soc = float(np.clip(soc, 0.0, 1.0))
        base_ocv = float(np.interp(clamped_soc, self.soc_points, self.ocv_points))
        temp_delta_k = temp_celsius - 25.0
        return base_ocv + self.entropic_coeff * temp_delta_k

    def get_derivative(self, soc: float) -> float:
        """Calculates instantaneous dOCV/dSOC derivative (gradient)."""
        clamped_soc = float(np.clip(soc, 0.0, 1.0))
        # Central difference approximation
        delta = 0.005
        soc_high = min(1.0, clamped_soc + delta)
        soc_low = max(0.0, clamped_soc - delta)
        ocv_high = np.interp(soc_high, self.soc_points, self.ocv_points)
        ocv_low = np.interp(soc_low, self.soc_points, self.ocv_points)
        return float((ocv_high - ocv_low) / (soc_high - soc_low))

    def update_hysteresis(self, current_a: float, dt_s: float) -> float:
        """
        Advances the continuous normalized hysteresis state h(t) in [-1, +1]:
        dh/dt = -gamma * |eta_c * I / C_nom| * h + gamma * |eta_c * I / C_nom| * sgn(I)
        Returns current hysteresis overpotential in Volts.
        """
        if abs(current_a) < 1e-4:
            return self.hysteresis_state * self.m_hyst_max

        # Rate of charge flow normalized
        i_rate = abs(current_a) / self.capacity_ah
        sgn_i = 1.0 if current_a > 0 else -1.0

        # Exact exponential solution over dt_s
        factor = np.exp(-self.gamma * i_rate * (dt_s / 3600.0))
        self.hysteresis_state = factor * self.hysteresis_state + (1.0 - factor) * sgn_i
        self.hysteresis_state = float(np.clip(self.hysteresis_state, -1.0, 1.0))

        return self.hysteresis_state * self.m_hyst_max

    def get_effective_ocv(self, soc: float, current_a: float, dt_s: float, temp_celsius: float = 25.0) -> float:
        """Returns total effective OCV combining equilibrium OCV and hysteresis."""
        eq_ocv = self.get_equilibrium_ocv(soc, temp_celsius)
        v_hyst = self.update_hysteresis(current_a, dt_s)
        return eq_ocv + v_hyst

