# Kalman Filter for SoC Estimation

The equations implemented in the Kalman Filter model can be derived from its components: **state prediction**, **state update**, and **measurement update**. Below are the detailed equations used in the Python code.

---

## **State-Space Representation**
The Kalman Filter relies on the state-space model of a system, which is defined as:

1. **State Prediction:**
   \[
   x_k = A \cdot x_{k-1} + B \cdot u_k + w_k
   \]
   - \(x_k\): Predicted state at time step \(k\).
   - \(A\): State transition matrix.
   - \(x_{k-1}\): Previous state.
   - \(B\): Control input matrix.
   - \(u_k\): Control input (e.g., current flow in the battery).
   - \(w_k\): Process noise, assumed to be Gaussian with covariance \(Q\).

2. **Measurement Model:**
   \[
   z_k = C \cdot x_k + v_k
   \]
   - \(z_k\): Measurement at time step \(k\).
   - \(C\): Measurement matrix.
   - \(x_k\): Current state.
   - \(v_k\): Measurement noise, assumed to be Gaussian with covariance \(R\).

---

## **Kalman Filter Equations**

### **Prediction Step**
1. **State Prediction:**
   \[
   \hat{x}_k^- = A \cdot \hat{x}_{k-1} + B \cdot u_k
   \]
   - \(\hat{x}_k^-\): Predicted state estimate before incorporating the measurement.
   - \(\hat{x}_{k-1}\): Previous state estimate.

2. **Error Covariance Prediction:**
   \[
   P_k^- = A \cdot P_{k-1} \cdot A^T + Q
   \]
   - \(P_k^-\): Predicted error covariance matrix.
   - \(P_{k-1}\): Previous error covariance matrix.
   - \(Q\): Process noise covariance matrix.

### **Update Step**
1. **Innovation or Residual:**
   \[
   y_k = z_k - C \cdot \hat{x}_k^-
   \]
   - \(y_k\): Innovation (difference between the actual measurement and predicted measurement).

2. **Innovation Covariance:**
   \[
   S_k = C \cdot P_k^- \cdot C^T + R
   \]
   - \(S_k\): Covariance of the innovation.

3. **Kalman Gain:**
   \[
   K_k = P_k^- \cdot C^T \cdot S_k^{-1}
   \]
   - \(K_k\): Kalman gain, which determines how much the prediction should be adjusted based on the measurement.

4. **State Update:**
   \[
   \hat{x}_k = \hat{x}_k^- + K_k \cdot y_k
   \]
   - \(\hat{x}_k\): Updated state estimate after incorporating the measurement.

5. **Error Covariance Update:**
   \[
   P_k = (I - K_k \cdot C) \cdot P_k^-
   \]
   - \(P_k\): Updated error covariance matrix.
   - \(I\): Identity matrix.

---

## **Application to the Code**

### **Initialization:**
1. Matrices:
   - \(A = [1]\): No change in the state between time steps.
   - \(B = [0]\): No external control input.
   - \(C = [1]\): Direct measurement of the state (SoC).
   - \(Q = [1 \times 10^{-5}]\): Small process noise covariance.
   - \(R = [1 \times 10^{-2}]\): Measurement noise covariance.
   - \(P = [1]\): Initial error covariance.

2. Initial state:
   - \(x_0 = [50]\): Initial State of Charge (SoC) estimate.

### **Prediction:**
The prediction is done in the `predict` method:
```python
self.x = self.A @ self.x + self.B @ u
self.P = self.A @ self.P @ self.A.T + self.Q
```

### **Update:**
The update is done in the `update` method:
```python
S = self.C @ self.P @ self.C.T + self.R
K = self.P @ self.C.T @ np.linalg.inv(S)
y = z - (self.C @ self.x)
self.x = self.x + K @ y
self.P = (np.eye(self.P.shape[0]) - K @ self.C) @ self.P
```

---

## **Key Notes**

1. **Measurement Incorporation:**
   The Kalman Gain (\(K_k\)) ensures the state update balances prediction and measurement based on their respective uncertainties (\(Q\) and \(R\)).

2. **Dynamic Behavior:**
   This implementation assumes a stationary system with no external input (\(B \cdot u_k = 0\)), making it suitable for a simple constant SoC system.
