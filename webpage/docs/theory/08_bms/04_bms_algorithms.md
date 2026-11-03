# State Estimation Algorithms (SoC, SoH & SoP)

Accurate determination of internal battery states is the core algorithmic challenge of any Battery Management System (BMS). Key physical states—such as the **State of Charge (SoC)**, **State of Health (SoH)**, and **State of Power (SoP)**—cannot be measured directly via physical transducers inside closed commercial cells[^plett2015]. Instead, they must be mathematically reconstructed in real time from external boundary observations: terminal voltage $V(t)$, pack current $I(t)$, and surface temperature $T(t)$[^hu2012].

This chapter provides the formal mathematical derivations, state-space representations, and algorithmic formulations of modern model-based estimation techniques, centering on the Extended Kalman Filter (EKF), Unscented Kalman Filter (UKF), and multi-parameter State of Power (SoP) predictors.

---

## State-Space Modeling: The 1-RC Thevenin Equivalent Circuit

To implement recursive observer algorithms, the non-linear electrochemical behavior of the lithium-ion cell is modeled using an equivalent circuit network (ECM). The **1-RC Thevenin model** provides an optimal trade-off between embedded computational overhead and physical accuracy[^he2011]:

```mermaid
flowchart LR
    subgraph Thevenin_Model["1-RC Thevenin Equivalent Circuit"]
        direction LR
        OCV["U_ocv(SoC)"] --- R0["R_0 (Ohmic)"]
        R0 --- RC_Parallel["RC Polarization Network<br/>(R_1 || C_1)"]
        RC_Parallel --- TermPos["Terminal (+)"]
        OCV --- TermNeg["Terminal (-)"]
    end
```

The continuous-time governing differential equations are:

$$
\frac{d\,\text{SoC}(t)}{dt} = -\frac{\eta_c}{C_{\text{nom}}} I(t)
$$

$$
\frac{d\,V_{RC}(t)}{dt} = -\frac{1}{R_1 C_1} V_{RC}(t) + \frac{1}{C_1} I(t)
$$

Where:
- $\eta_c$ is the Coulombic efficiency ($\eta_c \approx 1.00$ during discharge, $\eta_c \le 1.00$ during charge).
- $C_{\text{nom}}$ is the nominal capacity in Ampere-seconds ($\text{As} = 3600 \times \text{Ah}$).
- $R_0$ denotes the high-frequency ohmic resistance of current collectors, electrolyte, and tabs.
- $R_1$ and $C_1$ represent the charge-transfer resistance and double-layer capacitance of the electrochemical interface.
- $V_{RC}$ is the polarization overpotential across the RC pair.

The terminal voltage $V_{\text{terminal}}(t)$ forms the non-linear observation equation:

$$
V_{\text{terminal}}(t) = U_{\text{ocv}}(\text{SoC}(t)) - R_0 I(t) - V_{RC}(t)
$$

Where $U_{\text{ocv}}(\text{SoC})$ is the non-linear thermodynamic open-circuit voltage function.

---

## Discrete-Time State-Space Formulation

Discretizing the continuous system over a fixed sampling interval $\Delta t$ (typically $\Delta t = 0.01\,\text{s}$ to $0.10\,\text{s}$) yields the linear state transition and non-linear output equations:

$$
\mathbf{x}_k = \begin{bmatrix} \text{SoC}_k \\ V_{RC,k} \end{bmatrix}, \quad u_k = I_k
$$

$$
\mathbf{x}_{k} = \mathbf{A} \mathbf{x}_{k-1} + \mathbf{B} u_{k-1} + \mathbf{w}_{k-1}
$$

$$
y_k = g(\mathbf{x}_k, u_k) + v_k = U_{\text{ocv}}(\text{SoC}_k) - R_0 u_k - V_{RC,k} + v_k
$$

The discrete transition matrix $\mathbf{A}$ and input coupling matrix $\mathbf{B}$ are derived using the zero-order hold (ZOH) exponential matrix solution:

$$
\mathbf{A} = \begin{bmatrix} 1 & 0 \\ 0 & \exp\left(-\frac{\Delta t}{\tau_1}\right) \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} -\frac{\eta_c \Delta t}{C_{\text{nom}}} \\ R_1 \left(1 - \exp\left(-\frac{\Delta t}{\tau_1}\right)\right) \end{bmatrix}
$$

Where $\tau_1 = R_1 C_1$ is the diffusion relaxation time constant. The random variables $\mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q})$ and $v_k \sim \mathcal{N}(0, R_{\text{meas}})$ denote process disturbance noise and voltage measurement sensor noise, respectively.

---

## The Extended Kalman Filter (EKF)

Because the output equation $g(\mathbf{x}_k, u_k)$ is non-linear due to $U_{\text{ocv}}(\text{SoC})$, a standard linear Kalman filter cannot be applied directly. The Extended Kalman Filter linearizes the system around the current state estimate using a first-order Taylor series expansion[^plett2004]:

```mermaid
flowchart TD
    subgraph Prediction["1. Time Update (Prediction)"]
        P1["State A-Priori Prediction:<br/>x̂_k⁻ = A x̂_{k-1}⁺ + B u_{k-1}"]
        P2["Covariance A-Priori Prediction:<br/>P_k⁻ = A P_{k-1}⁺ Aᵀ + Q"]
    end

    subgraph Linearization["2. Linearization"]
        L1["Compute Observation Jacobian:<br/>C_k = [∂U_ocv/∂SoC | x̂_k⁻ ,  -1]"]
    end

    subgraph Correction["3. Measurement Update (Correction)"]
        C1["Kalman Gain Computation:<br/>K_k = P_k⁻ C_kᵀ (C_k P_k⁻ C_kᵀ + R_meas)⁻¹"]
        C2["State A-Posteriori Update:<br/>x̂_k⁺ = x̂_k⁻ + K_k (y_meas,k - g(x̂_k⁻, u_k))"]
        C3["Covariance A-Posteriori Update:<br/>P_k⁺ = (I - K_k C_k) P_k⁻"]
    end

    Prediction --> Linearization
    Linearization --> Correction
    Correction -->|Next Time Step k+1| Prediction
```

### Observation Jacobian Calculation

The measurement matrix $\mathbf{C}_k$ is computed at each time step as the partial derivative of the observation equation evaluated at the a-priori state $\hat{\mathbf{x}}_k^-$:

$$
\mathbf{C}_k = \left. \frac{\partial g(\mathbf{x}_k, u_k)}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}_k^-} = \begin{bmatrix} \left. \frac{\partial U_{\text{ocv}}}{\partial \text{SoC}} \right|_{\hat{\text{SoC}}_k^-} & -1 \end{bmatrix}
$$

> [!NOTE]
> For chemistries with flat OCV curves such as Lithium Iron Phosphate ($\text{LiFePO}_4$), $\frac{\partial U_{\text{ocv}}}{\partial \text{SoC}} \approx 0$ across $20\% \le \text{SoC} \le 80\%$. In this regime, the Kalman gain for the SoC state approaches zero, causing the filter to rely almost entirely on Coulomb counting until the OCV steepens near the knees.

---

## Observer Comparison: EKF vs. UKF vs. Particle Filter

| Metric / Attribute | Extended Kalman Filter (EKF) | Unscented Kalman Filter (UKF) | Particle Filter (PF / Sequential Monte Carlo) |
| :--- | :--- | :--- | :--- |
| **Linearization Method** | 1st-order Taylor series expansion (Jacobian) | Unscented Transform via deterministic sigma points | Empirical probability distribution via random particles |
| **Posterior Distribution** | Assumes Gaussian | Captures true mean and covariance to 3rd order | Arbitrary non-Gaussian, multimodal distributions |
| **Computational Overhead** | Low ($\mathcal{O}(n^3)$, minimal floating point ops) | Moderate ($\approx 2n+1$ deterministic sigma point evaluations) | Extremely High ($100-1000$ particles evaluated per cycle) |
| **Tuning Complexity** | Covariance matrices $\mathbf{Q}$ and $R_{\text{meas}}$ | Matrices $\mathbf{Q}, R_{\text{meas}}$ plus UKF spread scalars ($\alpha, \beta, \kappa$) | Particle count, resampling threshold, noise injection |
| **Automotive Production Suitability** | Industry benchmark; native execution on AUTOSAR Classic | Increasing adoption in premium dual-core BMS | Primarily research; exceeds standard ISO 26262 microcontrollers |

---

## State of Power (SoP) Dynamic Prediction

The State of Power (SoP) defines the maximum charge and discharge electrical power ($P_{\text{chg,max}}, P_{\text{dis,max}}$) the pack can sustain over a future prediction horizon $\Delta t_p$ (typically $1\,\text{s}, 2\,\text{s}, 10\,\text{s}$, or $30\,\text{s}$) without violating design constraints[^xiong2018].

### Multi-Constraint Formulation

The maximum current is constrained simultaneously by three physical boundaries:

```mermaid
flowchart TD
    Limits["Peak Current Constraints over Horizon Δt_p"]
    Limits --> C1["1. Terminal Voltage Limits<br/>V_min ≤ V(t + Δt_p) ≤ V_max"]
    Limits --> C2["2. Design Current Limits<br/>I_min_fuse ≤ I ≤ I_max_fuse"]
    Limits --> C3["3. Electrochemical SoC Limits<br/>SoC_min ≤ SoC(t + Δt_p) ≤ SoC_max"]
```

#### 1. Voltage Constraint Current

Predicting the terminal voltage after a pulse of duration $\Delta t_p$ using the 1-RC model:

$$
V(t + \Delta t_p) = U_{\text{ocv}}\left(\text{SoC}(t + \Delta t_p)\right) - I \cdot R_0 - V_{RC}(t) e^{-\frac{\Delta t_p}{\tau_1}} - I \cdot R_1 \left(1 - e^{-\frac{\Delta t_p}{\tau_1}}\right)
$$

Solving for the maximum discharge current ($I_{\text{dis}}^{V}$) such that $V(t + \Delta t_p) \ge V_{\min}$:

$$
I_{\text{dis}}^{V} = \frac{U_{\text{ocv}}(\text{SoC}_t) - V_{\min} - V_{RC}(t) e^{-\frac{\Delta t_p}{\tau_1}}}{R_0 + R_1 \left(1 - e^{-\frac{\Delta t_p}{\tau_1}}\right)}
$$

Similarly, solving for the maximum charge current ($I_{\text{chg}}^{V} < 0$) to keep $V(t + \Delta t_p) \le V_{\max}$:

$$
I_{\text{chg}}^{V} = \frac{U_{\text{ocv}}(\text{SoC}_t) - V_{\max} - V_{RC}(t) e^{-\frac{\Delta t_p}{\tau_1}}}{R_0 + R_1 \left(1 - e^{-\frac{\Delta t_p}{\tau_1}}\right)}
$$

#### 2. SoC Constraint Current

To prevent deep depletion ($\text{SoC} < \text{SoC}_{\min}$) or overfill ($\text{SoC} > \text{SoC}_{\max}$):

$$
I_{\text{dis}}^{\text{SoC}} = \frac{(\text{SoC}_t - \text{SoC}_{\min}) \cdot C_{\text{nom}}}{\eta_c \cdot \Delta t_p}
$$

$$
I_{\text{chg}}^{\text{SoC}} = -\frac{(\text{SoC}_{\max} - \text{SoC}_t) \cdot C_{\text{nom}}}{\Delta t_p}
$$

#### 3. Power Boundary Execution

Combining all bounding conditions:

$$
I_{\text{dis,max}} = \min\left( I_{\text{spec,dis}}, \; I_{\text{dis}}^{V}, \; I_{\text{dis}}^{\text{SoC}} \right)
$$

$$
I_{\text{chg,max}} = \max\left( -I_{\text{spec,chg}}, \; I_{\text{chg}}^{V}, \; I_{\text{chg}}^{\text{SoC}} \right)
$$

The instantaneous State of Power transmitted over CAN to the motor inverter is:

$$
P_{\text{dis,max}} = I_{\text{dis,max}} \cdot V_{\min}, \quad P_{\text{chg,max}} = |I_{\text{chg,max}}| \cdot V_{\max}
$$

---

## Production EKF Implementation in Battery Toolkit

The industrial-grade Kalman filtering engine is available in [`battery_toolkit.state_estimation.ekf`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/state_estimation/ekf.py). It couples directly with 1-RC and 2-RC Thevenin ECM models, incorporating Joseph-form stabilized covariance updates:

```python
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.state_estimation.ekf import ExtendedKalmanFilter

# Configure high-fidelity 2-RC equivalent circuit model
ecm = DualPolarizationECM(
    r0=0.025,    # 25 mOhm ohmic resistance
    r1=0.015,    # 15 mOhm fast charge-transfer resistance
    c1=1200.0,   # 1200 F double-layer capacitance
    r2=0.020,    # 20 mOhm slow diffusion resistance
    c2=8000.0    # 8000 F diffusion capacitance
)

# Initialize Extended Kalman Filter with nominal cell capacity
ekf = ExtendedKalmanFilter(ecm=ecm, nominal_capacity_ah=50.0, initial_soc=0.60)

# Periodic measurement step (invoked inside 10 ms BMS cyclic task)
estimated_soc = ekf.step(current_a=35.0, voltage_v=3.82, dt_s=0.01)
print(f"Online Estimated SOC: {estimated_soc * 100:.2f}%")
```

For full implementation details, mathematical derivations, and unit test benchmarks comparing EKF vs. UKF vs. RLS, see [`codes/python/src/battery_toolkit/state_estimation/ekf.py`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/state_estimation/ekf.py) and [`test_state_estimation.py`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/tests/test_state_estimation.py).

---

## References

[^plett2015]: Plett, G. L. (2015). *Battery Management Systems, Volume II: Equivalent-Circuit Methods*. Artech House.
[^hu2012]: Hu, X., Li, S., & Peng, H. (2012). A comparative study of equivalent circuit models for Li-ion batteries. *Journal of Power Sources*, 198, 359–367.
[^he2011]: He, H., Xiong, R., & Fan, J. (2011). Evaluation of lithium-ion battery equivalent circuit models for state of charge estimation by an experimental approach. *Energies*, 4(4), 582–598.
[^plett2004]: Plett, G. L. (2004). Extended Kalman filtering for battery management systems of LiPB-based HEV battery packs: Part 1. Background and Part 2. Modeling and identification. *Journal of Power Sources*, 134(2), 252–276.
[^xiong2018]: Xiong, R., et al. (2018). Towards a smarter battery management system: A critical review on battery state of power estimation. *Journal of Cleaner Production*, 202, 1228–1240.
