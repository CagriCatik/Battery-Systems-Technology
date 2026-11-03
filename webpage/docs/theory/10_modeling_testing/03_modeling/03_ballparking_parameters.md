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

## Production Python Implementation: HPPC Parameter Extraction

The following production script implements non-linear curve fitting on a synthetic HPPC pulse relaxation profile, extracting $R_0, R_1, C_1, R_2, C_2$:

```python
"""
HPPC Parameter Extraction Engine for 2-RC Dual Polarization Battery Models.
Uses Levenberg-Marquardt non-linear least squares optimization.
"""

from typing import Dict, Tuple
import numpy as np
from scipy.optimize import curve_fit


def relaxation_model_2rc(t: np.ndarray, u_ocv: float, v1: float, tau1: float, v2: float, tau2: float) -> np.ndarray:
    """
    Theoretical 2-RC relaxation model:
    V(t) = U_ocv - V1 * exp(-t / tau1) - V2 * exp(-t / tau2)
    """
    return u_ocv - v1 * np.exp(-t / tau1) - v2 * np.exp(-t / tau2)


class HPPCParameterExtractor:
    def __init__(self, pulse_current_a: float = 30.0, pulse_duration_s: float = 10.0) -> None:
        self.i_pulse = pulse_current_a
        self.t_pulse = pulse_duration_s

    def extract_parameters(
        self,
        t_relax: np.ndarray,
        v_relax: np.ndarray,
        v_end_of_pulse: float,
    ) -> Dict[str, float]:
        """
        Extracts R0, R1, C1, R2, C2 from post-pulse relaxation data.
        t_relax: time array starting at 0.0 s (pulse turn-off)
        v_relax: measured voltage array starting immediately after IR step
        """
        # 1. Ohmic Resistance R0 from instantaneous step
        delta_v_ir = v_relax[0] - v_end_of_pulse
        r0 = delta_v_ir / self.i_pulse

        # 2. Initial guesses for non-linear fit: [U_ocv, V1, tau1, V2, tau2]
        u_ocv_guess = float(v_relax[-1])
        v_span = u_ocv_guess - v_relax[0]
        initial_guess = [u_ocv_guess, v_span * 0.4, 8.0, v_span * 0.6, 120.0]

        # Bounds: strictly positive physical values
        lower_bounds = [u_ocv_guess - 0.2, 0.0, 0.5, 0.0, 30.0]
        upper_bounds = [u_ocv_guess + 0.2, 0.5, 30.0, 0.5, 800.0]

        # 3. Levenberg-Marquardt curve fitting
        popt, _ = curve_fit(
            relaxation_model_2rc,
            t_relax,
            v_relax,
            p0=initial_guess,
            bounds=(lower_bounds, upper_bounds),
            maxfev=5000,
        )

        u_ocv_fit, v1_fit, tau1_fit, v2_fit, tau2_fit = popt

        # 4. Convert transient voltages into R and C components
        r1 = v1_fit / (self.i_pulse * (1.0 - np.exp(-self.t_pulse / tau1_fit)))
        c1 = tau1_fit / r1

        r2 = v2_fit / (self.i_pulse * (1.0 - np.exp(-self.t_pulse / tau2_fit)))
        c2 = tau2_fit / r2

        return {
            "R0_mOhm": r0 * 1000.0,
            "R1_mOhm": r1 * 1000.0,
            "C1_Farads": c1,
            "tau1_seconds": tau1_fit,
            "R2_mOhm": r2 * 1000.0,
            "C2_Farads": c2,
            "tau2_seconds": tau2_fit,
            "U_ocv_Volts": u_ocv_fit,
        }


# --- Verification Execution ---
if __name__ == "__main__":
    np.random.seed(42)
    # Ground truth parameters: R0=25 mΩ, R1=15 mΩ, C1=1000 F (tau1=15s), R2=20 mΩ, C2=6000 F (tau2=120s)
    extractor = HPPCParameterExtractor(pulse_current_a=30.0, pulse_duration_s=10.0)

    # Generate synthetic relaxation data with noise
    time_vec = np.linspace(0.01, 300.0, 500)
    v1_true = 30.0 * 0.015 * (1.0 - np.exp(-10.0 / 15.0))  # ~ 0.219 V
    v2_true = 30.0 * 0.020 * (1.0 - np.exp(-10.0 / 120.0)) # ~ 0.048 V
    u_ocv_true = 3.850

    v_end_pulse = u_ocv_true - (30.0 * 0.025) - v1_true - v2_true # with IR drop (0.75V)
    v_clean = relaxation_model_2rc(time_vec, u_ocv_true, v1_true, 15.0, v2_true, 120.0)
    v_noisy = v_clean + np.random.normal(0.0, 0.001, size=len(time_vec)) # 1 mV noise

    results = extractor.extract_parameters(time_vec, v_noisy, v_end_of_pulse=v_end_pulse)

    print("=== HPPC 2-RC Model Parameter Extraction Results ===\n")
    print(f"Ohmic Resistance (R_0):       {results['R0_mOhm']:6.2f} mΩ  (Ground Truth: 25.00 mΩ)")
    print(f"Charge-Transfer Res (R_1):    {results['R1_mOhm']:6.2f} mΩ  (Ground Truth: 15.00 mΩ)")
    print(f"Double-Layer Cap (C_1):       {results['C1_Farads']:6.1f} F   (Ground Truth: 1000.0 F)")
    print(f"Fast Time Constant (τ_1):     {results['tau1_seconds']:6.2f} s   (Ground Truth: 15.00 s)")
    print(f"Diffusion Resistance (R_2):   {results['R2_mOhm']:6.2f} mΩ  (Ground Truth: 20.00 mΩ)")
    print(f"Diffusion Capacitance (C_2):  {results['C2_Farads']:6.1f} F   (Ground Truth: 6000.0 F)")
    print(f"Slow Time Constant (τ_2):     {results['tau2_seconds']:6.2f} s   (Ground Truth: 120.00 s)")
```

---

## References

[^plett2015]: Plett, G. L. (2015). *Battery Management Systems, Volume I: Battery Modeling*. Artech House.
[^hu2012]: Hu, X., Li, S., & Peng, H. (2012). A comparative study of equivalent circuit models for Li-ion batteries. *Journal of Power Sources*, 198, 359–367.
[^usabc2003]: United States Advanced Battery Consortium. (2003). *FreedomCAR Battery Test Manual for Electric and Hybrid Electric Vehicles*. Idaho National Engineering and Environmental Laboratory.
[^he2011]: He, H., Xiong, R., & Fan, J. (2011). Evaluation of lithium-ion battery equivalent circuit models for state of charge estimation. *Energies*, 4(4), 582–598.
