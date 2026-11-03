import math
import numpy as np
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.modeling.ocv import OCVModel


class ExtendedKalmanFilter:
    """
    Discrete Extended Kalman Filter (EKF) for non-linear SOC estimation
    coupled with a 2-RC Dual Polarization battery cell model.

    State vector: x = [SOC, v1, v2]^T
    Input: u = Current I (A) (Discharge > 0, Charge < 0)
    Measurement: y = Terminal Voltage V_t (V)
    """
    def __init__(
        self,
        ecm: DualPolarizationECM,
        ocv_model: OCVModel,
        nominal_capacity_ah: float,
        initial_soc: float = 0.80,
        process_noise_diag: tuple = (1e-6, 1e-5, 1e-5),
        measurement_noise: float = 1e-4,
    ):
        self.ecm = ecm
        self.ocv_model = ocv_model
        self.c_nom = nominal_capacity_ah

        # State vector: [SOC, v1, v2]
        self.x = np.array([initial_soc, 0.0, 0.0], dtype=float)

        # State error covariance matrix P
        self.P = np.diag([1e-3, 1e-4, 1e-4])

        # Process noise covariance Q
        self.Q = np.diag(process_noise_diag)

        # Measurement noise scalar R
        self.R = float(measurement_noise)

    @property
    def estimated_soc(self) -> float:
        return float(self.x[0])

    @property
    def estimated_v1(self) -> float:
        return float(self.x[1])

    @property
    def estimated_v2(self) -> float:
        return float(self.x[2])

    def step(self, current_a: float, measured_voltage_v: float, dt_s: float, temp_celsius: float = 25.0) -> float:
        """
        Executes one EKF recursion cycle:
        1. State Prediction (Time Update)
        2. Covariance Prediction
        3. Measurement Jacobian Calculation
        4. Innovation and Kalman Gain Calculation
        5. State & Covariance Correction (Measurement Update)
        """
        # --- 1. State Prediction ---
        soc_prev = self.x[0]
        v1_prev = self.x[1]
        v2_prev = self.x[2]

        # Coulomb counting update for SOC
        # Discharge > 0 decreases SOC
        delta_soc = -(current_a * dt_s) / (self.c_nom * 3600.0)
        soc_pred = soc_prev + delta_soc

        # 2-RC ZOH updates
        alpha1 = math.exp(-dt_s / self.ecm.tau1)
        beta1 = self.ecm.r1 * (1.0 - alpha1)
        v1_pred = alpha1 * v1_prev + beta1 * current_a

        alpha2 = math.exp(-dt_s / self.ecm.tau2)
        beta2 = self.ecm.r2 * (1.0 - alpha2)
        v2_pred = alpha2 * v2_prev + beta2 * current_a

        x_pred = np.array([soc_pred, v1_pred, v2_pred], dtype=float)

        # State transition matrix F = df/dx
        F = np.array([
            [1.0, 0.0,    0.0],
            [0.0, alpha1, 0.0],
            [0.0, 0.0,    alpha2]
        ], dtype=float)

        # --- 2. Covariance Prediction ---
        P_pred = F @ self.P @ F.T + self.Q

        # --- 3. Measurement Update ---
        # Predicted terminal voltage: y_pred = OCV(soc_pred, T) - I*R0 - v1_pred - v2_pred
        ocv_pred = self.ocv_model.get_equilibrium_ocv(soc_pred, temp_celsius)
        y_pred = ocv_pred - current_a * self.ecm.r0 - v1_pred - v2_pred

        # Measurement Jacobian H = dh/dx = [ dOCV/dSOC, -1, -1 ]
        docv_dsoc = self.ocv_model.get_derivative(soc_pred)
        H = np.array([[docv_dsoc, -1.0, -1.0]], dtype=float)

        # Innovation residual
        residual = measured_voltage_v - y_pred

        # Innovation covariance S = H P_pred H^T + R
        S = float((H @ P_pred @ H.T).item() + self.R)

        # Kalman Gain K = P_pred H^T S^-1
        K = (P_pred @ H.T) / S

        # --- 4. State & Covariance Correction ---
        self.x = x_pred + (K.flatten() * residual)
        self.x[0] = np.clip(self.x[0], 0.0, 1.0) # Clamp SOC

        # Joseph form covariance update for numerical stability: P = (I - KH)P(I - KH)^T + KRK^T
        I_mat = np.eye(3)
        IKH = I_mat - K @ H
        self.P = IKH @ P_pred @ IKH.T + (K * self.R @ K.T)

        return self.estimated_soc
