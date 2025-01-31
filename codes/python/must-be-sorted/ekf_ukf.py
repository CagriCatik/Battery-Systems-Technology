import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import UnscentedKalmanFilter, MerweScaledSigmaPoints
from filterpy.kalman import ExtendedKalmanFilter

# Simulation parameters
np.random.seed(42)
T = 1.0  # Time step (seconds)
steps = 50
v = 1.0  # Velocity (m/s)
true_state = np.array([0, 0, np.pi/4])  # Initial state [x, y, theta]

# Motion model

def motion_model(state, dt):
    x, y, theta = state
    x_new = x + dt * v * np.cos(theta)
    y_new = y + dt * v * np.sin(theta)
    theta_new = theta  # Constant orientation for simplicity
    return np.array([x_new, y_new, theta_new])

# Measurement model
def measurement_model(state):
    x, y, _ = state
    r = np.sqrt(x**2 + y**2)  # Range
    b = np.arctan2(y, x)  # Bearing
    return np.array([r, b])

# EKF Jacobians
def jacobian_motion(state, dt):
    _, _, theta = state
    return np.array([
        [1, 0, -dt * v * np.sin(theta)],
        [0, 1, dt * v * np.cos(theta)],
        [0, 0, 1],
    ])

def jacobian_measurement(state):
    x, y, _ = state
    r = np.sqrt(x**2 + y**2)
    return np.array([
        [x / r, y / r, 0],
        [-y / (r**2), x / (r**2), 0],
    ])

# Generate true trajectory and noisy measurements
true_trajectory = [true_state]
measurements = []
for _ in range(steps):
    true_state = motion_model(true_state, T)
    true_trajectory.append(true_state)
    noisy_measurement = measurement_model(true_state) + np.random.normal(0, [0.1, 0.05])
    measurements.append(noisy_measurement)

true_trajectory = np.array(true_trajectory)
measurements = np.array(measurements)

# EKF implementation
ekf = ExtendedKalmanFilter(dim_x=3, dim_z=2)
ekf.x = np.array([0, 0, np.pi / 4])  # Initial estimate
ekf.P = np.eye(3) * 0.1
ekf.R = np.diag([0.1, 0.05])  # Measurement noise covariance
ekf.Q = np.diag([0.01, 0.01, 0.01])  # Process noise covariance

ekf_trajectory = []
for z in measurements:
    ekf.F = jacobian_motion(ekf.x, T)
    ekf.predict()
    ekf.H = jacobian_measurement(ekf.x)
    ekf.update(z, HJacobian=jacobian_measurement, Hx=measurement_model)
    ekf_trajectory.append(ekf.x.copy())

ekf_trajectory = np.array(ekf_trajectory)

# UKF implementation
sigma_points = MerweScaledSigmaPoints(n=3, alpha=0.1, beta=2, kappa=0)
ukf = UnscentedKalmanFilter(dim_x=3, dim_z=2, dt=T, fx=motion_model, hx=measurement_model, points=sigma_points)
ukf.x = np.array([0, 0, np.pi / 4])  # Initial estimate
ukf.P = np.eye(3) * 0.1
ukf.R = np.diag([0.1, 0.05])  # Measurement noise covariance
ukf.Q = np.diag([0.01, 0.01, 0.01])  # Process noise covariance

ukf_trajectory = []
for z in measurements:
    ukf.predict(T)
    ukf.update(z)
    ukf_trajectory.append(ukf.x.copy())

ukf_trajectory = np.array(ukf_trajectory)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(true_trajectory[:, 0], true_trajectory[:, 1], label="True Trajectory", linestyle="--")
plt.scatter(measurements[:, 0] * np.cos(measurements[:, 1]), 
            measurements[:, 0] * np.sin(measurements[:, 1]), label="Measurements", color="red", alpha=0.5)
plt.plot(ekf_trajectory[:, 0], ekf_trajectory[:, 1], label="EKF Estimate", marker="o")
plt.plot(ukf_trajectory[:, 0], ukf_trajectory[:, 1], label="UKF Estimate", marker="x")
plt.legend()
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Comparison of EKF and UKF")
plt.grid()
plt.show()
