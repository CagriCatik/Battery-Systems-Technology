import math
import numpy as np
from scipy.linalg import cholesky
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel


class UnscentedKalmanFilter:
    """
    Unscented Kalman Filter (UKF) for battery state estimation.
    Avoids explicit Jacobian derivatives by deterministically propagating 2L + 1 sigma points
    through the non-linear OCV mapping.
    """
    def __init__(
        self,
        ecm: DualPolarizationECM,
        ocv_model: OCVModel,
        nominal_capacity_ah: float,
        initial_soc: float = 0.80,
        alpha: float = 1e-3,
        beta: float = 2.0,   # Optimal for Gaussian distributions
        kappa: float = 0.0,
    ):
        self.ecm = ecm
        self.ocv_model = ocv_model
        self.c_nom = nominal_capacity_ah

        # Dimension of state vector: L = 3 ([SOC, v1, v2])
        self.L = 3
        self.x = np.array([initial_soc, 0.0, 0.0], dtype=float)
        self.P = np.diag([1e-3, 1e-4, 1e-4])

        self.Q = np.diag([1e-6, 1e-5, 1e-5])
        self.R = 1e-4

        # UKF Tuning parameters
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa
        self.lambda_param = (alpha ** 2) * (self.L + kappa) - self.L

        # Compute weights for mean and covariance
        self.w_m = np.zeros(2 * self.L + 1)
        self.w_c = np.zeros(2 * self.L + 1)

        self.w_m[0] = self.lambda_param / (self.L + self.lambda_param)
        self.w_c[0] = self.w_m[0] + (1.0 - alpha ** 2 + beta)

        for i in range(1, 2 * self.L + 1):
            weight = 1.0 / (2.0 * (self.L + self.lambda_param))
            self.w_m[i] = weight
            self.w_c[i] = weight

    @property
    def estimated_soc(self) -> float:
        return float(self.x[0])

    def generate_sigma_points(self) -> np.ndarray:
        """Generates 2L+1 sigma points from mean and covariance."""
        sigma_points = np.zeros((2 * self.L + 1, self.L))
        sigma_points[0] = self.x

        # Matrix square root using Cholesky factorization
        scale = math.sqrt(self.L + self.lambda_param)
        try:
            sqrt_P = cholesky(self.P, lower=True)
        except Exception:
            # Fallback if P loses positive definiteness
            sqrt_P = np.diag(np.sqrt(np.maximum(1e-9, np.diag(self.P))))

        for i in range(self.L):
            sigma_points[i + 1] = self.x + scale * sqrt_P[:, i]
            sigma_points[i + 1 + self.L] = self.x - scale * sqrt_P[:, i]

        return sigma_points

    def step(self, current_a: float, measured_voltage_v: float, dt_s: float, temp_celsius: float = 25.0) -> float:
        """Executes one UKF measurement and state update."""
        sigma_points = self.generate_sigma_points()

        # Propagate sigma points through non-linear state transition f(x, u)
        alpha1 = math.exp(-dt_s / self.ecm.tau1)
        beta1 = self.ecm.r1 * (1.0 - alpha1)
        alpha2 = math.exp(-dt_s / self.ecm.tau2)
        beta2 = self.ecm.r2 * (1.0 - alpha2)
        delta_soc = -(current_a * dt_s) / (self.c_nom * 3600.0)

        sigmas_pred = np.zeros_like(sigma_points)
        for i in range(2 * self.L + 1):
            soc_i = sigma_points[i, 0] + delta_soc
            v1_i = alpha1 * sigma_points[i, 1] + beta1 * current_a
            v2_i = alpha2 * sigma_points[i, 2] + beta2 * current_a
            sigmas_pred[i] = [soc_i, v1_i, v2_i]

        # Predicted state mean
        x_pred = np.sum(self.w_m[:, None] * sigmas_pred, axis=0)

        # Predicted state covariance
        P_pred = np.zeros((self.L, self.L))
        for i in range(2 * self.L + 1):
            diff = sigmas_pred[i] - x_pred
            P_pred += self.w_c[i] * np.outer(diff, diff)
        P_pred += self.Q

        # Propagate predicted sigma points through measurement function h(x, u)
        y_sigmas = np.zeros(2 * self.L + 1)
        for i in range(2 * self.L + 1):
            ocv_i = self.ocv_model.get_equilibrium_ocv(sigmas_pred[i, 0], temp_celsius)
            y_sigmas[i] = ocv_i - current_a * self.ecm.r0 - sigmas_pred[i, 1] - sigmas_pred[i, 2]

        # Predicted measurement mean
        y_pred = float(np.sum(self.w_m * y_sigmas))

        # Innovation covariance Pyy and cross-covariance Pxy
        P_yy = float(np.sum(self.w_c * (y_sigmas - y_pred) ** 2) + self.R)
        P_xy = np.zeros(self.L)
        for i in range(2 * self.L + 1):
            P_xy += self.w_c[i] * (sigmas_pred[i] - x_pred) * (y_sigmas[i] - y_pred)

        # Kalman gain K = Pxy / Pyy
        K = P_xy / P_yy

        # Correction
        residual = measured_voltage_v - y_pred
        self.x = x_pred + K * residual
        self.x[0] = np.clip(self.x[0], 0.0, 1.0)
        self.P = P_pred - np.outer(K, K) * P_yy

        return self.estimated_soc
