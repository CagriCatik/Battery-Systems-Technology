import numpy as np
import matplotlib.pyplot as plt

class KalmanFilterBMS:
    def __init__(self, A, B, C, Q, R, P, x0):
        self.A = A
        self.B = B
        self.C = C
        self.Q = Q
        self.R = R
        self.P = P
        self.x = x0

    def predict(self, u):
        self.x = self.A @ self.x + self.B @ u
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        S = self.C @ self.P @ self.C.T + self.R
        K = self.P @ self.C.T @ np.linalg.inv(S)
        y = z - (self.C @ self.x)
        self.x = self.x + K @ y
        self.P = (np.eye(self.P.shape[0]) - K @ self.C) @ self.P

    def get_state(self):
        return self.x

if __name__ == "__main__":
    # State-space representation
    A = np.array([[1]])
    B = np.array([[0]])
    C = np.array([[1]])
    Q = np.array([[1e-5]])
    R = np.array([[1e-2]])
    P = np.array([[1]])
    x0 = np.array([[50]])

    # Initialize Kalman Filter
    kf = KalmanFilterBMS(A, B, C, Q, R, P, x0)

    # Simulated data generation
    true_soc = 50
    np.random.seed(0)  # Seed for reproducibility
    noise = np.random.normal(0, 0.2, 200)  # Generate Gaussian noise for 200 time steps
    measurements = [true_soc + n for n in noise]
    time_steps = list(range(len(measurements)))
    true_states = [true_soc for _ in measurements]
    measured_states = []
    estimated_states = []

    # Run Kalman Filter
    for measurement in measurements:
        measured_states.append(measurement)
        kf.predict(np.array([[0]]))  # No control input
        kf.update(np.array([[measurement]]))
        estimated_states.append(kf.get_state()[0, 0])

    # Plotting the results
    plt.figure(figsize=(16, 8))
    plt.plot(time_steps, true_states, label="True SoC", color="blue", linewidth=2)
    plt.plot(time_steps, measured_states, label="Measured SoC", color="orange", linestyle="dotted", linewidth=1)
    plt.plot(time_steps, estimated_states, label="Estimated SoC", color="green", linewidth=2)
    plt.title("Kalman Filter State Estimation for SoC (200 Time Steps)")
    plt.xlabel("Time Step")
    plt.ylabel("State of Charge (SoC)")
    plt.legend()
    plt.grid(True)
    plt.show()
