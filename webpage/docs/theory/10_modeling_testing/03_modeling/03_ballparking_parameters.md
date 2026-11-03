# Parameter Identification from Pulse & HPPC Testing

To deploy an equivalent circuit model (ECM) in simulation or real-time BMS firmware, its parameter set—ohmic resistance $R_0$, charge-transfer elements $(R_1, C_1)$, and diffusion elements $(R_2, C_2)$—must be precisely parameterized across the multi-dimensional operating space: State of Charge ($\text{SoC} \in [0\%, 100\%]$), temperature ($T \in [-20^\circ\text{C}, +55^\circ\text{C}]$), and current direction (charge vs. discharge)[^plett2015][^hu2012].

The industry standard methodology for extracting these parameters is the **Hybrid Pulse Power Characterization (HPPC)** protocol, formulated by the United States Advanced Battery Consortium (USABC)[^usabc2003].

This chapter details the HPPC test protocol, the analytical and graphical parameter extraction formulas, and non-linear least squares optimization algorithms.

---

## The Hybrid Pulse Power Characterization (HPPC) Protocol

The HPPC profile applies a standardized sequence of high-rate discharge and regeneration current pulses at fixed State of Charge intervals (typically in $10\%$ SoC decrements from $100\%$ down to $10\%$)[^usabc2003]:

```mermaid
gantt
    title Standard USABC HPPC Test Profile Sequence (at constant SoC)
    dateFormat X
    axisFormat %s s

    section Current Profile
    Discharge Pulse: 1C - 5C (10 s)     : 0, 10
    Intermediate Rest: I = 0 A (40 s)    : 10, 50
    Regeneration Pulse: 0.75C (10 s)    : 50, 60
    Equilibrium Relaxation Rest (1800 s) : 60, 200
```

```
   Terminal Voltage V(t) during a Discharge HPPC Pulse:
      ^
 V_ocv|---------------\  (Pre-pulse equilibrium)
      |               |  ΔV_0 (Ohmic IR Drop)
      |               \
      |                \-------------------\  V(t) under load (Polarization exponential)
      |                                    |
      |                                    |  ΔV_0' (Ohmic IR Jump upon turn-off)
      |                                    \
      |                                     \-------------------> V_relax(t)
    0 +---------------+--------------------+--------------------> Time [s]
      t = 0           t_1                  t_2
                      (Pulse applied)      (Pulse removed)
```

---

## Analytical & Graphical Parameter Extraction

For a 2-RC Thevenin circuit, the voltage response during the relaxation phase ($t \ge t_2$) following a current pulse of amplitude $I_0$ and duration $t_{\text{pulse}} = t_2 - t_1$ is given analytically by:

$$
V_{\text{relax}}(t) = U_{\text{ocv}} - V_1 \exp\left(-\frac{t - t_2}{\tau_1}\right) - V_2 \exp\left(-\frac{t - t_2}{\tau_2}\right)
$$

Where $\tau_1 = R_1 C_1$ is the fast charge-transfer time constant ($1 - 30\,\text{s}$) and $\tau_2 = R_2 C_2$ is the slow diffusion time constant ($100 - 800\,\text{s}$).

### 1. Ohmic Resistance ($R_0$) Extraction

Ohmic resistance is extracted from the instantaneous vertical step change observed at the instant of current interruption ($t = t_2$):

$$
R_0 = \frac{\left| V(t_2^+) - V(t_2^-) \right|}{I_0} = \frac{\Delta V_0}{I_0}
$$

> [!NOTE]
> In discrete sampling systems, the "instantaneous" voltage jump is defined as the voltage difference across the first discrete sample period (typically $\Delta t = 10\,\text{ms}$ or $100\,\text{ms}$).

### 2. Polarization Resistances & Capacitances ($R_1, C_1, R_2, C_2$)

The transient relaxation overpotentials $V_1$ and $V_2$ represent the saturation states of the two RC pairs at the instant of pulse interruption:

$$
V_1 = I_0 R_1 \left( 1 - \exp\left(-\frac{t_{\text{pulse}}}{\tau_1}\right) \right)
$$

$$
V_2 = I_0 R_2 \left( 1 - \exp\left(-\frac{t_{\text{pulse}}}{\tau_2}\right) \right)
$$

Solving for the physical circuit resistances and capacitances yields:

$$
R_1 = \frac{V_1}{I_0 \left( 1 - \exp\left(-\frac{t_{\text{pulse}}}{\tau_1}\right) \right)}, \quad C_1 = \frac{\tau_1}{R_1}
$$

$$
R_2 = \frac{V_2}{I_0 \left( 1 - \exp\left(-\frac{t_{\text{pulse}}}{\tau_2}\right) \right)}, \quad C_2 = \frac{\tau_2}{R_2}
$$

---

## Non-Linear Least Squares Optimization: Levenberg-Marquardt

While graphical extraction provides reliable initial estimates ("ballpark parameters"), production battery characterization employs non-linear optimization across the complete sampled transient time series $V_{\text{meas}}(t_k)$[^he2011].

The objective cost function minimizes the sum of squared prediction errors:

$$
\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta}) = \sum_{k=1}^M \left[ V_{\text{meas}}(t_k) - V_{\text{model}}(t_k; \, \boldsymbol{\theta}) \right]^2
$$

Where the parameter optimization vector is:

$$
\boldsymbol{\theta} = \begin{bmatrix} R_0 & R_1 & \tau_1 & R_2 & \tau_2 \end{bmatrix}^T
$$

Subject to thermodynamic physical constraints:

$$
R_0 > 0, \quad R_1 > 0, \quad \tau_1 > 0, \quad R_2 > 0, \quad \tau_2 > \tau_1
$$

---

## HPPC Parameter Identification in Battery Toolkit

The non-linear least squares parameter extraction engine is implemented in [`battery_toolkit.modeling.hppc`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/modeling/hppc.py). It extracts $R_0, R_1, C_1, R_2, C_2$ from dynamic current pulses:

```python
import numpy as np
from battery_toolkit.modeling.hppc import HPPCExtractor

# Configure HPPC parameter extractor with pulse current and duration
extractor = HPPCExtractor(pulse_current_a=30.0, pulse_duration_s=10.0)

# Extract parameters from post-pulse relaxation curve
# time_s: time array starting from pulse shutoff
# voltage_v: measured relaxation voltage
# v_end_of_pulse: terminal voltage right before pulse shutoff
params = extractor.extract_parameters(
    time_s=relaxation_time,
    voltage_v=relaxation_voltage,
    v_end_of_pulse=v_pulse_end
)

print(f"R0: {params['r0_mohm']:.2f} mOhm, R1: {params['r1_mohm']:.2f} mOhm, C1: {params['c1_farads']:.1f} F")
print(f"R2: {params['r2_mohm']:.2f} mOhm, C2: {params['c2_farads']:.1f} F")
```

Full algorithmic implementation and optimization tests are in [`codes/python/src/battery_toolkit/modeling/hppc.py`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/modeling/hppc.py) and [`test_modeling.py`](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/tests/test_modeling.py).

---

## References

[^plett2015]: Plett, G. L. (2015). *Battery Management Systems, Volume I: Battery Modeling*. Artech House.
[^hu2012]: Hu, X., Li, S., & Peng, H. (2012). A comparative study of equivalent circuit models for Li-ion batteries. *Journal of Power Sources*, 198, 359–367.
[^usabc2003]: United States Advanced Battery Consortium. (2003). *FreedomCAR Battery Test Manual for Electric and Hybrid Electric Vehicles*. Idaho National Engineering and Environmental Laboratory.
[^he2011]: He, H., Xiong, R., & Fan, J. (2011). Evaluation of lithium-ion battery equivalent circuit models for state of charge estimation. *Energies*, 4(4), 582–598.
