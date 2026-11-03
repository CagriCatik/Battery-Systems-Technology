import math
from typing import Tuple


class TheveninECM:
    """
    Standard 1-RC Thevenin Equivalent Circuit Model:
    Terminal Voltage: V_t = OCV(SOC) - I * R_0 - v_1
    """
    def __init__(self, r0: float, r1: float, c1: float):
        self.r0 = r0  # Ohms (Ohmic internal resistance)
        self.r1 = r1  # Ohms (Charge-transfer resistance)
        self.c1 = c1  # Farads (Double-layer capacitance)
        self.v1 = 0.0 # Volts (Overpotential state)

    @property
    def tau1(self) -> float:
        """Time constant of the RC network (seconds)."""
        return self.r1 * self.c1

    def reset(self, initial_v1: float = 0.0) -> None:
        """Resets dynamic overpotential state."""
        self.v1 = initial_v1

    def step(self, current_a: float, dt_s: float) -> float:
        """
        Advances the 1-RC state by dt_s using exact Zero-Order Hold (ZOH) discretization:
        v1[k+1] = exp(-dt/tau1) * v1[k] + r1 * (1 - exp(-dt/tau1)) * current_a
        Returns current overpotential v1.
        """
        alpha = math.exp(-dt_s / self.tau1)
        beta = self.r1 * (1.0 - alpha)
        self.v1 = alpha * self.v1 + beta * current_a
        return self.v1

    def compute_terminal_voltage(self, ocv: float, current_a: float) -> float:
        """Calculates instantaneous terminal voltage V_t under load."""
        return ocv - current_a * self.r0 - self.v1


class DualPolarizationECM:
    """
    2-RC Dual Polarization Equivalent Circuit Model:
    Decouples fast charge-transfer / double-layer dynamics (R1 || C1)
    from slow solid-state diffusion kinetics (R2 || C2).
    Terminal Voltage: V_t = OCV(SOC) - I * R_0 - v_1 - v_2
    """
    def __init__(self, r0: float, r1: float, c1: float, r2: float, c2: float):
        self.r0 = r0
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
        self.v1 = 0.0
        self.v2 = 0.0

    @property
    def tau1(self) -> float:
        """Fast electrochemical time constant (seconds)."""
        return self.r1 * self.c1

    @property
    def tau2(self) -> float:
        """Slow mass-transport diffusion time constant (seconds)."""
        return self.r2 * self.c2

    def reset(self, initial_v1: float = 0.0, initial_v2: float = 0.0) -> None:
        self.v1 = initial_v1
        self.v2 = initial_v2

    def step(self, current_a: float, dt_s: float) -> Tuple[float, float]:
        """
        Updates overpotential states using discrete ZOH analytical integration.
        Returns (v1, v2).
        """
        alpha1 = math.exp(-dt_s / self.tau1)
        beta1 = self.r1 * (1.0 - alpha1)
        self.v1 = alpha1 * self.v1 + beta1 * current_a

        alpha2 = math.exp(-dt_s / self.tau2)
        beta2 = self.r2 * (1.0 - alpha2)
        self.v2 = alpha2 * self.v2 + beta2 * current_a

        return self.v1, self.v2

    def compute_terminal_voltage(self, ocv: float, current_a: float) -> float:
        """V_t = OCV - I*R0 - v1 - v2."""
        return ocv - current_a * self.r0 - self.v1 - self.v2

