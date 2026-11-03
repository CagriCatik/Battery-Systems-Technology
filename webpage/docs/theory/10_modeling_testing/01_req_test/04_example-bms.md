# Industrial BMS Requirements Specification Catalog

This chapter presents a formal, production-grade requirements catalog for a high-voltage ($800\,\text{V}_{\text{nom}}$) automotive traction Battery Management System (BMS). Each specification is formulated according to the **EARS framework**, assigned an **Automotive Safety Integrity Level (ASIL)** under **ISO 26262**, and accompanied by physical rationales and quantified acceptance criteria[^iso26262][^andrea2020].

---

## High-Voltage BMS Requirements Catalog

### 1. Cell Overvoltage Protection (OVP)
- **Requirement ID:** `BMS_SSR_OVP_001`
- **Safety Level:** **ASIL-D** | **Parent:** `BMS_SYS_SAF_003`
- **EARS Specification:**  
  *WHEN any individual cell terminal voltage exceeds $4.250\,\text{V} \pm 0.005\,\text{V}$ continuously for duration $t \ge 50\,\text{ms}$, the BMS shall command the main traction contactors to transition to the OPEN state within $t \le 10\,\text{ms}$.*
- **Physical Rationale:** Overcharging beyond the upper electrochemical stability window triggers irreversible cathode delithiation, lattice collapse, exothermic electrolyte oxidation, and oxygen release—initiating thermal runaway[^doughty2012].
- **Verification Method:** Test on Hardware-in-the-Loop (HIL) simulator with automated cell overvoltage injection.
- **Acceptance Criteria:** Main contactor coil drive PWM drops to $0\,\text{V}$ within $\le 10.0\,\text{ms}$ of the 50 ms debounce expiration.

---

### 2. Cell Undervoltage Protection (UVP)
- **Requirement ID:** `BMS_SSR_UVP_002`
- **Safety Level:** **ASIL-C** | **Parent:** `BMS_SYS_SAF_004`
- **EARS Specification:**  
  *WHEN any individual cell terminal voltage drops below $2.500\,\text{V} \pm 0.010\,\text{V}$ continuously for duration $t \ge 100\,\text{ms}$, the BMS shall issue a propulsion torque limit of $0\,\text{Nm}$ to the motor inverter and open contactors within $t \le 500\,\text{ms}$.*
- **Physical Rationale:** Discharging below $2.5\,\text{V}$ reverses anode polarity, causing the copper current collector foil to oxidize and dissolve into the electrolyte ($\text{Cu} \to \text{Cu}^{2+} + 2e^-$). Subsequent recharging deposits metallic copper dendrites, creating catastrophic internal short-circuits[^waldmann2014].
- **Verification Method:** Test on HIL with dynamic discharge load profiles.
- **Acceptance Criteria:** Inverter CAN-FD torque command transitions to $0\,\text{Nm}$ within $100\,\text{ms}$; contactors open within $\le 500\,\text{ms}$.

---

### 3. Pack Overcurrent Discharge (OCD)
- **Requirement ID:** `BMS_SSR_OCD_003`
- **Safety Level:** **ASIL-D** | **Parent:** `BMS_SYS_SAF_001`
- **EARS Specification:**  
  *WHEN measured pack discharge current exceeds $1500\,\text{A} \pm 15\,\text{A}$ continuously for duration $t \ge 15\,\text{ms}$, the BMS shall de-energize main contactor coils within $t \le 5\,\text{ms}$.*
- **Physical Rationale:** Sustained excessive discharge currents induce violent Joule heating ($I^2 R$) across internal tab welds and busbars, leading to thermal failure of separator membranes.
- **Verification Method:** Automated HIL testbench with high-speed current pulse injection.
- **Acceptance Criteria:** Contactor disconnect response latency $\le 5.0\,\text{ms}$ measured from the $15\,\text{ms}$ timeout.

---

### 4. Over-Temperature Protection (OTP)
- **Requirement ID:** `BMS_SSR_OTP_004`
- **Safety Level:** **ASIL-D** | **Parent:** `BMS_SYS_SAF_002`
- **EARS Specification:**  
  *WHEN any module NTC temperature sensor reports a temperature exceeding $60.0^\circ\text{C} \pm 0.5^\circ\text{C}$ continuously for duration $t \ge 200\,\text{ms}$, the BMS shall transition to `LIMP_HOME` mode and derate permissible continuous discharge current to $\le 50\,\text{A}$ within $t \le 100\,\text{ms}$.*
- **Physical Rationale:** Operating above $60^\circ\text{C}$ accelerates Solid Electrolyte Interphase (SEI) breakdown and transition-metal dissolution, transitioning toward the exothermic runaway threshold ($>80^\circ\text{C}$)[^pesaran2002].
- **Verification Method:** Thermal chamber environmental HIL test.
- **Acceptance Criteria:** CAN-FD limit message $I_{\text{dis,max}}$ decrements to $\le 50.0\,\text{A}$ within $\le 100\,\text{ms}$.

---

### 5. Low-Temperature Charge Prevention (LTP)
- **Requirement ID:** `BMS_SSR_LTP_005`
- **Safety Level:** **ASIL-C** | **Parent:** `BMS_SYS_CHG_006`
- **EARS Specification:**  
  *IF the minimum battery module temperature is below $0.0^\circ\text{C} \pm 0.5^\circ\text{C}$, THEN the BMS shall restrict maximum permissible charge current to $0.0\,\text{A}$ until active battery heating elevates temperatures above $+5.0^\circ\text{C}$.*
- **Physical Rationale:** Sub-zero charging forces lithium ions to plate as metallic lithium onto the graphite anode rather than intercalating, creating dendritic structures that penetrate separators[^ecker2014].
- **Verification Method:** Software-in-the-Loop (SIL) automated unit test.
- **Acceptance Criteria:** Charge current limit remains strictly $0.0\,\text{A}$ whenever $T < 0.0^\circ\text{C}$.

---

### 6. Contactor Precharge Timeout Abort
- **Requirement ID:** `BMS_SSR_SEQ_006`
- **Safety Level:** **ASIL-B** | **Parent:** `BMS_SYS_PWR_008`
- **EARS Specification:**  
  *WHILE in the `PRECHARGE` state, IF the DC-link capacitor voltage fails to reach $95\%$ of pack terminal voltage within $t = 250\,\text{ms} \pm 5\,\text{ms}$, THEN the BMS shall open the precharge contactor $K_{\text{pre}}$ and negative contactor $K^-$ within $t \le 10\,\text{ms}$ and set `DTC_PRECHARGE_ABORT`.*
- **Physical Rationale:** Prolonged precharge under shorted DC bus conditions over-dissipates the precharge resistor ($P = V^2 / R$), leading to resistor thermal explosion.
- **Verification Method:** HIL emulation of faulted inverter DC-link capacitor.
- **Acceptance Criteria:** Precharge contactor opened at exactly $250\,\text{ms} \pm 5\,\text{ms}$; resistor energy capped below rated pulse limits.

---

### 7. Contactor Weld Diagnostic Check
- **Requirement ID:** `BMS_SSR_SEQ_007`
- **Safety Level:** **ASIL-D** | **Parent:** `BMS_SYS_SAF_005`
- **EARS Specification:**  
  *WHILE transitioning from `RUN_DRIVE` to `STANDBY`, WHEN contactors are commanded OPEN, the BMS shall verify via differential voltage sense that DC-link voltage decays below $50\,\text{V}$ within $t \le 200\,\text{ms}$; IF DC-link voltage remains above $50\,\text{V}$, THEN the BMS shall flag `DTC_CONTACTOR_WELD` and inhibit subsequent vehicle restart.*
- **Physical Rationale:** A welded contactor leaves the external vehicle bus live even when the vehicle is keyed off, posing fatal electrical shock hazards to occupants and emergency first responders.
- **Verification Method:** HIL contactor weld simulation.
- **Acceptance Criteria:** Successful latching of non-volatile fault code and permanent restart lockout upon welded terminal emulation.

---

### 8. High-Voltage Interlock Loop (HVIL) Interrupt
- **Requirement ID:** `BMS_SSR_SAF_008`
- **Safety Level:** **ASIL-D** | **Parent:** `BMS_SYS_SAF_007`
- **EARS Specification:**  
  *WHEN the High-Voltage Interlock Loop (HVIL) physical circuit is broken for duration $t \ge 2\,\text{ms}$, the BMS shall command the main contactor coils to de-energize within $t \le 8\,\text{ms}$.*
- **Physical Rationale:** Ensures that if a connector is unplugged or an enclosure opened during operation, high-voltage power is de-energized before human fingers can contact live pins (break-before-make protection).
- **Verification Method:** Physical line-break testing on HIL break-out box.
- **Acceptance Criteria:** Total elapsed time from physical circuit break to contactor coil voltage drop $\le 10.0\,\text{ms}$.

---

### 9. Electrical Insulation Resistance Degradation
- **Requirement ID:** `BMS_SSR_ISO_009`
- **Safety Level:** **ASIL-B** | **Parent:** `BMS_SYS_SAF_008`
- **EARS Specification:**  
  *WHEN measured electrical isolation resistance between high-voltage positive or negative poles and chassis ground drops below $500\,\Omega/\text{V}$ continuously for $t \ge 3000\,\text{ms}$, the BMS shall transmit an insulation warning message across CAN-FD and limit vehicle power to $\le 30\,\text{kW}$.*
- **Physical Rationale:** Satisfies ISO 6469-1 electrical safety mandates, preventing chassis electrification upon a second single-point short.
- **Verification Method:** HIL variable isolation resistance injection box ($10\,\text{k}\Omega$ to $100\,\text{M}\Omega$).
- **Acceptance Criteria:** Warning flag set on CAN-FD within $3.0\,\text{s}$ of resistance dropping below $500\,\Omega/\text{V}$.

---

### 10. Passive Cell Balancing Activation
- **Requirement ID:** `BMS_SSR_BAL_010`
- **Safety Level:** **QM** | **Parent:** `BMS_SYS_BAL_002`
- **EARS Specification:**  
  *WHILE charging, WHEN the terminal voltage of any cell exceeds the pack minimum cell voltage by $\Delta V \ge 15\,\text{mV}$ AND cell voltage exceeds $3.90\,\text{V}$, the BMS shall activate the passive balancing bleed resistor switch for that cell with an $80\%$ duty cycle.*
- **Physical Rationale:** Equalizes State of Charge across series cells, maximizing pack usable energy without creating excessive localized PCB heat flux.
- **Verification Method:** Automated Software-in-the-Loop unit simulation.
- **Acceptance Criteria:** Balancing command bit active for target cells; duty cycle confirmed at $80\%$ (8 s ON, 2 s OFF).

---

## Requirements Traceability Matrix Summary

| Requirement UID | Domain | ASIL | Target Verification Level | Primary Hazard Mitigated |
| :--- | :--- | :--- | :--- | :--- |
| `BMS_SSR_OVP_001` | Overvoltage | ASIL-D | HIL Simulator | Cell thermal runaway & fire |
| `BMS_SSR_UVP_002` | Undervoltage | ASIL-C | HIL Simulator | Anode copper dissolution & dendrites |
| `BMS_SSR_OCD_003` | Overcurrent | ASIL-D | Fast HIL Pulse | Busbar & tab vaporization |
| `BMS_SSR_OTP_004` | Overtemperature | ASIL-D | Environmental Chamber HIL | Electrolyte degradation & runaway |
| `BMS_SSR_LTP_005` | Low Temp Charge | ASIL-C | SIL Unit Test | Metallic lithium plating |
| `BMS_SSR_SEQ_006` | Precharge Timeout| ASIL-B | Inverter Emulation HIL | Precharge resistor explosion |
| `BMS_SSR_SEQ_007` | Contactor Weld | ASIL-D | HIL Fault Injection | Electric shock to technician/driver |
| `BMS_SSR_SAF_008` | HVIL Interrupt | ASIL-D | Hardware Breakout Box | Arc flash upon manual unplugging |
| `BMS_SSR_ISO_009` | Insulation | ASIL-B | Resistance Injection HIL | Chassis electrification |
| `BMS_SSR_BAL_010` | Cell Balancing | QM | SIL Model Testing | Premature charging termination |

---

## References

[^iso26262]: International Organization for Standardization. (2018). *ISO 26262-4: Road vehicles — Functional safety — Part 4: Product development at the system level*. ISO.
[^andrea2020]: Andrea, D. (2020). *Battery Management Systems for Large Lithium-Ion Battery Packs*. Artech House.
[^doughty2012]: Doughty, D. H., & Roth, E. P. (2012). A general discussion of Li-ion battery safety. *The Electrochemical Society Interface*, 21(2), 37–44.
[^waldmann2014]: Waldmann, T., et al. (2014). Temperature-dependent ageing mechanisms in Lithium-ion batteries—A Post-Mortem study. *Journal of Power Sources*, 262, 129–135.
[^pesaran2002]: Pesaran, A. A. (2002). Battery thermal management in EVs and HEVs: Issues and solutions. *Advanced Automotive Battery Conference*, Las Vegas, NV.
[^ecker2014]: Ecker, M., et al. (2014). Parameterization of a physico-chemical model of a lithium-ion battery. *Journal of The Electrochemical Society*, 162(1), A1836.
