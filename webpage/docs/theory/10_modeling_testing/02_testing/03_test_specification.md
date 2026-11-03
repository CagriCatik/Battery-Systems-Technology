# Test Case Specification Architecture & Execution

A **Test Case Specification** translates abstract safety and functional requirements into concrete, repeatable, and automated execution scripts. In automotive Battery Management Systems, formal test specifications must satisfy **ISO 26262-8 Clause 9** and **Automotive SPICE (SWE.4 / SWE.6 / SYS.5)** standards, guaranteeing that every test stimulus, tolerance band, timing deadline, and pass/fail criterion is rigorously documented[^iso26262][^automotivespice].

This chapter formalizes the anatomical structure of an automotive test case specification, details three production-grade test cases for safety-critical BMS functions, and outlines automated execution via the **ASAM XIL** API.

---

## Anatomy of an Automotive Test Specification

Under ISO 26262-8, an auditable test case specification consists of ten mandatory structural fields:

```mermaid
flowchart TD
    TC["Formal Test Case Specification (ISO 26262 / ASPICE)"]
    
    TC --> ID["1. Metadata: Unique Test ID, Title, ASIL Classification"]
    TC --> Trace["2. Traceability: Parent Requirement UID (e.g. BMS_SSR_OVP_001)"]
    TC --> Pre["3. Preconditions: Vehicle state, contactors, ambient temp, initial SoC"]
    TC --> Stim["4. Input Stimulus Vector: Precise time-series profile [V(t), I(t), T(t)]"]
    TC --> Step["5. Execution Procedure: Step-by-step stimulus injection sequence"]
    TC --> Exp["6. Expected Outputs: Quantified signals with mathematical tolerance bands"]
    TC --> Criteria["7. Pass/Fail Decision Logic: Real-time assertion formulas"]
    TC --> Post["8. Postconditions: System cleanup, fault clearing, safe state return"]
```

---

## Production Test Case Specifications

### Test Case 1: Cell Overvoltage Disconnect (`TC_HIL_OVP_001`)

```mermaid
gantt
    title TC_HIL_OVP_001 Stimulus and Response Sequence
    dateFormat X
    axisFormat %s ms

    section Voltage Stimulus
    Cell 42 at Nominal (4.10 V)          : 0, 1000
    Voltage Ramp to 4.28 V (Overvoltage): 1000, 1005
    Maintain Overvoltage (4.28 V)        : 1005, 1100

    section BMS Software State
    Nominal Charging (RUN_DRIVE)        : 0, 1000
    Debounce Timer Running (50 ms)      : 1000, 1050
    Safe State Contactor Trip           : 1050, 1060

    section Contactor Physical Hardware
    Coil Energized (PWM 100%)           : 0, 1050
    Coil De-energized (0 V)            : 1050, 1060
```

- **Test Identifier:** `TC_HIL_OVP_001`
- **Safety Classification:** **ASIL-D** | **Traced Requirement:** `BMS_SSR_OVP_001`
- **Test Objective:** Verify that the BMS detects cell overvoltage ($V > 4.250\,\text{V}$), debounces for exactly $50\,\text{ms}$, and opens both main contactors within the $10\,\text{ms}$ FTTI budget.
- **Preconditions:**
  - Ambient Temperature: $T_{\text{amb}} = 25.0^\circ\text{C} \pm 2.0^\circ\text{C}$.
  - Initial Pack Voltage: $V_{\text{pack}} = 393.6\,\text{V}$ (all 96 cells at $4.100\,\text{V}$).
  - BMS State: `RUN_DRIVE`; Main Contactors ($K^+$ and $K^-$) CLOSED.
  - Charging Current: $I_{\text{pack}} = -50.0\,\text{A}$ (continuous regeneration).

#### Step-by-Step Test Execution Procedure

| Step | Time Offset ($t$) | Test Stimulus Injected | Expected System Response | Measurement Assertion |
| :---: | :---: | :--- | :--- | :--- |
| **01** | $0.000\,\text{s}$ | Maintain all 96 cells at $4.100\,\text{V}$, $I = -50.0\,\text{A}$. | BMS remains in `RUN_DRIVE`. | Contactor coil status == `CLOSED`. |
| **02** | $1.000\,\text{s}$ | Step Cell 42 voltage from $4.100\,\text{V}$ to $4.280\,\text{V}$ via cell emulator in $< 1.0\,\text{ms}$. | Internal software overvoltage debounce timer initiates. | Contactors remain `CLOSED` during debounce. |
| **03** | $1.050\,\text{s}$ | Maintain Cell 42 at $4.280\,\text{V}$ (Debounce expires at $50\,\text{ms}$). | BMS transitions to `FAULT_TRIP`; de-energizes contactor coils. | Contactor coil drive output drops to $0.0\,\text{V}$. |
| **04** | $1.058\,\text{s}$ | Main contactor auxiliary contacts open mechanically. | Contactors physically open; line current drops to $0.0\,\text{A}$. | Elapsed time $t_{\text{trip}} \le 10.0\,\text{ms}$ from $t = 1.050\,\text{s}$. |
| **05** | $1.100\,\text{s}$ | Query Diagnostic Server via UDS Service `0x19`. | DTC `P0A80-17` (Cell Overvoltage) present and confirmed. | UDS Positive Response `0x59 02 09`. |

- **Pass/Fail Criteria:**
  - Pass: Total elapsed time from debounce expiration ($t = 1.050\,\text{s}$) to coil de-energization $\le 10.0\,\text{ms}$ AND line current drops to $0.0\,\text{A} \pm 0.5\,\text{A}$ AND DTC logged correctly.
  - Fail: Disconnect time $>10.0\,\text{ms}$, or contactors fail to open, or incorrect DTC logged.

---

### Test Case 2: Inverter Precharge Timeout Abort (`TC_HIL_PRE_002`)

- **Test Identifier:** `TC_HIL_PRE_002`
- **Safety Classification:** **ASIL-B** | **Traced Requirement:** `BMS_SSR_SEQ_006`
- **Test Objective:** Verify that during a precharge fault (simulated dead short across the inverter DC bus), precharge aborts at $t = 250\,\text{ms} \pm 5\,\text{ms}$, preventing thermal overload of resistor $R_{\text{pre}}$.
- **Preconditions:**
  - Pack Terminal Voltage: $V_{\text{pack}} = 400.0\,\text{V}$.
  - DC-Link Bus: Shorted to ground via a $1.0\,\Omega$ high-power fault resistor (simulating a shorted inverter bridge).
  - BMS State: `STANDBY`; all contactors OPEN.

#### Execution Procedure & Assertions
1. At $t = 0.500\,\text{s}$, send CAN-FD `Drive_Command = TRUE`.
2. BMS engages $K^-$ and $K_{\text{pre}}$. Current flows through $R_{\text{pre}}$, but $V_{\text{link}}$ remains clamped below $10.0\,\text{V}$ due to the short.
3. **Pass Assertion:** Exactly at $t = 0.750\,\text{s} \pm 0.005\,\text{s}$ ($250\,\text{ms}$ after precharge initiation), the BMS must open $K_{\text{pre}}$ and $K^-$.
4. **Thermal Energy Assertion:** Total energy dissipated in $R_{\text{pre}}$ ($E = \int I^2 R \, dt$) must not exceed $250.0\,\text{Joules}$ (well below the $500\,\text{J}$ rating).
5. **Diagnostic Assertion:** `DTC_PRECHARGE_ABORT` confirmed in non-volatile memory.

---

### Test Case 3: High-Voltage Interlock Loop Dynamic Break (`TC_HIL_HVIL_003`)

- **Test Identifier:** `TC_HIL_HVIL_003`
- **Safety Classification:** **ASIL-D** | **Traced Requirement:** `BMS_SSR_SAF_008`
- **Test Objective:** Verify that breaking the physical HVIL circuit during active high-power driving opens contactors within $t \le 10.0\,\text{ms}$, preventing lethal arc-flash exposure.
- **Preconditions:**
  - BMS in `RUN_DRIVE` mode; $K^+$ and $K^-$ CLOSED.
  - Simulated vehicle driving at $100\,\text{km/h}$; load current $I_{\text{pack}} = 250.0\,\text{A}$.
  - HVIL circuit active ($1\,\text{kHz}, 50\%$ PWM, closed loop).

#### Execution Procedure & Assertions
1. At $t = 2.0000\,\text{s}$, HIL Fault Injection Unit (FIU) opens the HVIL relay line.
2. **Pass Assertion 1:** BMS detects HVIL loss and de-energizes contactor coils at $t \le 2.0080\,\text{s}$ ($\le 8.0\,\text{ms}$ response latency).
3. **Pass Assertion 2:** Contactor auxiliary sensing confirms contacts open at $t \le 2.0200\,\text{s}$.
4. **Pass Assertion 3:** High-priority emergency broadcast frame `BMS_Alert_HVIL` transmitted across CAN-FD with transmission delay $\le 10.0\,\text{ms}$.

---

## Automated Execution via Python & ASAM XIL API

Automated HIL test sequences are executed using standardized Python scripts interfacing with real-time testbench hardware (dSPACE SCALEXIO / Vector CANoe)[^asamxil]:

```python
"""
Automated Test Case Execution Script: TC_HIL_OVP_001
Conforms to ASAM XIL Standard and ISO 26262 ASIL-D Validation.
"""

import time
from typing import Tuple


class HILAutomatedTestOVP:
    def __init__(self, hil_session) -> None:
        self.hil = hil_session
        self.test_id = "TC_HIL_OVP_001"

    def setup_preconditions(self) -> None:
        """Establish 96S baseline at 4.10 V and engaged contactors."""
        print(f"[{self.test_id}] Setting up preconditions...")
        for cell_idx in range(1, 97):
            self.hil.set_cell_voltage(cell_idx, 4.100)
        self.hil.set_pack_current(-50.0)  # 50A regen
        self.hil.wait_ms(500)
        assert self.hil.read_contactor_state("K_PLUS") == "CLOSED"
        assert self.hil.read_bms_state() == "RUN_DRIVE"

    def execute_test(self) -> Tuple[bool, float]:
        """Execute step stimulus and measure precise opening latency."""
        self.setup_preconditions()
        print(f"[{self.test_id}] Injecting 4.280 V on Cell 42...")

        # Step stimulus: Cell 42 stepped to 4.280 V
        t_trigger = self.hil.get_realtime_clock()
        self.hil.set_cell_voltage(42, 4.280)

        # Wait for 50 ms debounce + 10 ms FTTI window
        self.hil.wait_ms(70)

        # Measure disconnect timestamp
        t_disconnect = self.hil.get_contactor_open_timestamp("K_PLUS")
        elapsed_ms = (t_disconnect - t_trigger) * 1000.0

        # Debounce is 50 ms, so response latency is elapsed - 50 ms
        response_latency_ms = elapsed_ms - 50.0
        print(f"[{self.test_id}] Contactor opened after {elapsed_ms:.2f} ms (Response Latency: {response_latency_ms:.2f} ms)")

        # Evaluate assertions
        dtc_logged = self.hil.read_active_dtc() == "P0A80-17"
        passed = (response_latency_ms <= 10.0) and dtc_logged
        return passed, response_latency_ms
```

---

## References

[^iso26262]: International Organization for Standardization. (2018). *ISO 26262-4 / Part 6 / Part 8: Road vehicles — Functional safety*. ISO.
[^automotivespice]: VDA QMC Working Group 13. (2017). *Automotive SPICE Process Assessment Model v3.1*. VDA.
[^asamxil]: ASAM e.V. (2020). *ASAM XIL Standard: Generic Test Automation Interface*. ASAM.
