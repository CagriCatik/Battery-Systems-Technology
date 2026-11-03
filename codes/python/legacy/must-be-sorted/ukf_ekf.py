import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import UnscentedKalmanFilter, MerweScaledSigmaPoints
from filterpy.kalman import ExtendedKalmanFilter

# Simulation parameters
np.random.seed(42)
T = 0.1  # Time step (seconds)
steps = 100
true_state = np.array([0, 0, 20, np.pi/6])  # Initial state: [x, y, v, yaw]

# Vehicle parameters
acceleration = 0.5  # m/s^2
yaw_rate = 0.05  # rad/s

# Motion model
def motion_model(state, dt):
    x, y, v, psi = state
    v_new = v + acceleration * dt  # Accelerating vehicle
    psi_new = psi + yaw_rate * dt  # Constant yaw rate
    x_new = x + v_new * np.cos(psi_new) * dt
    y_new = y + v_new * np.sin(psi_new) * dt
    return np.array([x_new, y_new, v_new, psi_new])

# Measurement model
def measurement_model(state):
    x, y, v, _ = state
    return np.array([x, y, v])

# EKF Jacobians
def jacobian_motion(state, dt):
    _, _, v, psi = state
    return np.array([
        [1, 0, np.cos(psi) * dt, -v * np.sin(psi) * dt],
        [0, 1, np.sin(psi) * dt, v * np.cos(psi) * dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def jacobian_measurement(state):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ])

# Generate true trajectory and noisy measurements
true_trajectory = [true_state]
measurements = []
for _ in range(steps):
    true_state = motion_model(true_state, T)
    true_trajectory.append(true_state)
    noisy_measurement = measurement_model(true_state) + np.random.normal(0, [1.0, 1.0, 0.5])
    measurements.append(noisy_measurement)

true_trajectory = np.array(true_trajectory)
measurements = np.array(measurements)

# EKF implementation
ekf = ExtendedKalmanFilter(dim_x=4, dim_z=3)
ekf.x = np.array([0, 0, 15, np.pi / 6])  # Initial estimate
ekf.P = np.eye(4) * 1.0
ekf.R = np.diag([1.0, 1.0, 0.5])  # Measurement noise covariance
ekf.Q = np.diag([0.1, 0.1, 0.1, 0.01])  # Process noise covariance

ekf_trajectory = []
for z in measurements:
    ekf.F = jacobian_motion(ekf.x, T)
    ekf.predict()
    ekf.H = jacobian_measurement(ekf.x)
    ekf.update(z, HJacobian=jacobian_measurement, Hx=measurement_model)
    ekf_trajectory.append(ekf.x.copy())

ekf_trajectory = np.array(ekf_trajectory)

# UKF implementation
sigma_points = MerweScaledSigmaPoints(n=4, alpha=0.1, beta=2, kappa=0)
ukf = UnscentedKalmanFilter(dim_x=4, dim_z=3, dt=T, fx=motion_model, hx=measurement_model, points=sigma_points)
ukf.x = np.array([0, 0, 15, np.pi / 6])  # Initial estimate
ukf.P = np.eye(4) * 1.0
ukf.R = np.diag([1.0, 1.0, 0.5])  # Measurement noise covariance
ukf.Q = np.diag([0.1, 0.1, 0.1, 0.01])  # Process noise covariance

ukf_trajectory = []
for z in measurements:
    ukf.predict()
    ukf.update(z)
    ukf_trajectory.append(ukf.x.copy())

ukf_trajectory = np.array(ukf_trajectory)

# Plot results
plt.figure(figsize=(12, 8))
plt.plot(true_trajectory[:, 0], true_trajectory[:, 1], label="True Trajectory", linestyle="--")
plt.scatter(measurements[:, 0], measurements[:, 1], label="Measurements", color="red", alpha=0.5)
plt.plot(ekf_trajectory[:, 0], ekf_trajectory[:, 1], label="EKF Estimate", marker="o")
plt.plot(ukf_trajectory[:, 0], ukf_trajectory[:, 1], label="UKF Estimate", marker="x")
plt.legend()
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("EKF and UKF for Vehicle Dynamics with Acceleration")
plt.grid()
plt.show()
