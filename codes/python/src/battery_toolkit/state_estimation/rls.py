import numpy as np
from typing import Tuple


class RecursiveLeastSquares:
    """
    Recursive Least Squares (RLS) with exponential forgetting factor (lambda)
    for online parameter identification (Ohmic resistance R0 and State of Health tracking).
    
    Model formulation:
    y(k) = phi(k)^T * theta(k) + e(k)
    where:
    y(k) = OCV(k) - V_t(k)
    phi(k) = I(k)
    theta(k) = R_0
    """
    def __init__(self, forgetting_factor: float = 0.995, initial_r0: float = 0.020):
        self.lam = forgetting_factor
        self.theta = float(initial_r0)
        self.p = 1.0 # Initial parameter covariance scalar

    @property
    def estimated_r0(self) -> float:
        return float(self.theta)

    def step(self, current_a: float, terminal_voltage_v: float, ocv_v: float) -> float:
        """
        Executes one RLS recursion:
        1. Regressor phi = current_a
        2. Measurement y = ocv_v - terminal_voltage_v
        3. Gain K = P * phi / (lambda + phi^T * P * phi)
        4. Parameter update: theta = theta + K * (y - phi * theta)
        5. Covariance update: P = (P - K * phi * P) / lambda
        """
        phi = current_a
        y = ocv_v - terminal_voltage_v

        # Avoid updating when current is practically zero (loss of excitation)
        if abs(phi) < 0.5:
            return self.estimated_r0

        # RLS Gain
        denominator = self.lam + (phi ** 2) * self.p
        k_gain = (self.p * phi) / denominator

        # Innovation
        error = y - phi * self.theta

        # Parameter update
        self.theta += k_gain * error
        self.theta = max(0.001, self.theta) # Resistance must be positive

        # Covariance update
        self.p = (self.p - k_gain * phi * self.p) / self.lam

        return self.estimated_r0

    def compute_soh_resistance(self, r0_fresh: float, r0_eol_multiplier: float = 2.0) -> float:
        """
        Calculates State of Health based on resistance increase:
        SOH_R = 100% * (R_eol - R_current) / (R_eol - R_fresh)
        """
        r_eol = r0_fresh * r0_eol_multiplier
        if r_eol <= r0_fresh:
            return 1.0
        soh = (r_eol - self.theta) / (r_eol - r0_fresh)
        return float(max(0.0, min(1.0, soh)))

