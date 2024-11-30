# Battery Management System Development in Simulink

## Introduction

Battery Management Systems (BMS) are critical components in modern battery-powered systems, ensuring safety, efficiency, and longevity of batteries. In electric vehicles (EVs), the BMS monitors and controls the battery pack, balancing cells, preventing unsafe conditions, and optimizing performance. This documentation outlines the design, simulation, and development of a BMS using Simulink, detailing the components, algorithms, and methodologies involved.

---

## 1. Battery Management System Overview

The primary objective of a BMS is to manage and safeguard the battery system by monitoring its key parameters, such as voltage, temperature, current, and state of charge (SOC). Additionally, the BMS protects the battery from operating outside its safe limits, optimizes energy usage through cell balancing, and provides diagnostics and reporting for maintenance and performance evaluation. In the context of electric vehicles, the BMS ensures that the battery operates safely across different environmental conditions, drive cycles, and charging profiles. The ability to simulate such scenarios is crucial for understanding and mitigating potential issues without risking damage to actual battery packs.

### 1.1 Purpose
The BMS ensures the following:
- **Monitoring:** Tracks critical parameters such as temperature, voltage, current, and state of charge (SOC).
- **Protection:** Prevents operations outside safe limits to avoid thermal runaway, overcharging, or deep discharge.
- **Optimization:** Balances cell voltages and SOC for maximum performance.
- **Diagnostics and Reporting:** Provides insights for maintenance and performance evaluation.

### 1.2 Use Case
In the context of EVs, the BMS enables:
- Safe operation across varying environmental conditions.
- Evaluation of battery responses to diverse drive cycles and charging profiles.
- Protection against unsafe conditions such as over-temperature or under-voltage.

---

## 2. Simulation Model in Simulink

The BMS simulation model is implemented in Simulink and is organized into several interconnected subsystems that replicate the functionality of a real-world BMS. These subsystems include driving scenario definitions, fault indicators, the BMS ECU model, and the battery pack along with its associated circuitry.

At the top level, the model defines various driving scenarios that serve as test sequences for evaluating the BMS. Fault indicators within the model provide visual feedback on whether any unsafe condition, such as over-temperature or over-voltage, has occurred. The core BMS logic resides in the BMS ECU model, which implements monitoring, control, and balancing algorithms. The battery pack and its circuitry are represented using Simscape, which accurately models their physical and electrical characteristics.

The model incorporates two variants of battery packs. The first is a small pack with six cells connected in series, while the second is a larger pack with 16 modules, each containing six cells in series, resulting in a total of 96 cells. These packs are modeled as a single parallel string. Simscape enables a detailed representation of these battery packs, using distinct physical domains such as electrical and thermal to capture their behavior under varying conditions.

### 2.1 Model Architecture
The BMS model in Simulink consists of:
- **Driving Scenarios Subsystem:** Defines test sequences for driving and charging cycles.
- **Fault Indicators:** Detects conditions like over-temperature or over-voltage.
- **BMS ECU Model:** Implements monitoring, control, and balancing algorithms.
- **Battery Pack and Circuitry Representation:** Models the physical and electrical characteristics of the battery.

### 2.2 Battery Pack Variants
- **Small Pack:** Six cells in series modeled in Simscape.
- **Large Pack:** Sixteen modules, each with six cells in series, resulting in 96 cells.

### 2.3 Physical Domains
- **Electrical (Blue):** Models voltage, current, and resistance.
- **Thermal (Orange):** Models heat dissipation and thermal gradients.

---

## 3. Battery Pack Design and Characteristics

The battery pack design is fundamental to the BMS. Each cell in the pack is modeled to reflect real-life lithium-ion chemistries, such as Nickel Manganese Cobalt (NMC). The cells are connected in series, allowing for heat exchange between adjacent cells. However, the thermal layout is asymmetrical, with significant differences in thermal behavior between cells.

For example, in the six-cell configuration, cell 6 is thermally insulated on one side, while cell 1 is exposed to the ambient air, allowing for convective cooling. This asymmetry creates notable temperature gradients within the pack, with cell 6 experiencing higher temperatures than cell 1. Such gradients are critical in understanding thermal management needs and their impact on cell degradation and performance.

Each cell is represented by an equivalent circuit model that simulates its electrical behavior. This model includes parameters that account for dependencies on temperature, SOC, and aging. These parameters are derived from experimental data, ensuring that the simulation closely mirrors real-world battery behavior.

### 3.1 Cell Configuration
Cells are connected in series:
- Heat exchange occurs between cells.
- Asymmetrical thermal layout:
  - Cell 6: Insulated on one side.
  - Cell 1: Exposed to ambient air for convective cooling.

### 3.2 Equivalent Circuit Model
Represents real-life lithium-ion chemistries (e.g., Nickel Manganese Cobalt, NMC):
- Includes temperature, SOC, and aging dependencies.
- Parameter estimation aligns with experimental data.

---

## 4. BMS Algorithms

The BMS algorithms are designed to monitor, protect, and optimize the battery system. These algorithms include current limiting, state-of-charge estimation, cell balancing, and state machine logic.

The monitoring subsystem calculates maximum allowable charge and discharge current levels based on individual cell voltages and temperatures. For instance, at low SOC, a cell's voltage is low, and allowing it to deliver a large current could cause its voltage to drop below the cutoff threshold specified by the manufacturer. By comparing the minimum cell voltage against this threshold and dividing it by the maximum internal resistance, the system computes a voltage-based current limit.

Temperature-based current thresholds are also implemented using lookup tables. These thresholds prevent high or low temperatures from causing physical damage to the cell materials during charging or discharging. The system compares these thresholds and selects the lowest value as the current limit.

The state machine, implemented using Simulink Stateflow, governs the overall operation of the BMS. It includes four parallel states: the main operating state (standby, driving, charging, or fault), fault detection, and the contactor switching sequences for the charger and inverter. The contactor logic ensures that excessive inrush currents are avoided during charging.

### 4.1 Monitoring and Current Limiting
- **Low SOC:** Limits current to prevent excessive voltage drops below the cutoff.
- **Temperature-Based Thresholds:** Lookup tables set current limits for safe operation at high and low temperatures.

### 4.2 State Machine
Modeled using Simulink Stateflow, the state machine includes:
- **BMS States:** Standby, Driving, Charging, and Fault.
- **Parallel States:** Fault detection, contactor switching for charger/inverter, and state-specific logic.

---

## 5. State of Charge (SOC) Estimation Methods

The state of charge (SOC) is a critical parameter that indicates the remaining energy in the battery. Since SOC cannot be measured directly, the BMS relies on estimation techniques. Three methods are implemented in the simulation: Coulomb counting, the Extended Kalman Filter (EKF), and the Unscented Kalman Filter (UKF).

Coulomb counting calculates SOC by integrating the current entering and leaving the cell over time. Although computationally efficient, this method suffers from cumulative errors and lacks the ability to correct inaccuracies without feedback from voltage measurements.

The EKF and UKF, on the other hand, are variations of nonlinear Kalman filters that use a cell model to predict terminal voltage based on current input. They then compare this prediction with actual measurements to estimate SOC and other internal states. The EKF is typically sufficient for systems with mild nonlinearity, such as the voltage-SOC relationship in lithium-ion cells. Both Kalman filters demonstrated the ability to recover from an initial SOC estimation error during the simulation, with the EKF slightly outperforming the UKF.

### 5.1 Methods
1. **Coulomb Counting:**
   - Tracks charge based on current flow.
   - Low computational cost but accumulates errors over time.
2. **Extended Kalman Filter (EKF):**
   - Nonlinear estimation using voltage and current data.
   - Suitable for mild system nonlinearities.
3. **Unscented Kalman Filter (UKF):**
   - Similar to EKF but better for severe nonlinearities.

### 5.2 Performance Comparison
- EKF and UKF recover from initial SOC errors, with EKF slightly outperforming UKF.
- Coulomb counting lacks feedback for error correction.

---

## 6. Cell Balancing

Cell balancing ensures that all cells in the pack have a similar SOC. Without balancing, cells with higher SOC levels limit the total capacity that can be utilized, leading to inefficiencies. The balancing logic in the BMS calculates the voltage difference between the highest and lowest cell voltages and activates resistive balancing circuits as needed. These circuits discharge cells with higher SOC, gradually equalizing their charge levels.



### 6.1 Purpose
Maintains uniform SOC across cells to:
- Maximize capacity utilization.
- Reduce degradation rates.

### 6.2 Balancing Logic
- Voltage difference triggers balancing.
- Resistors discharge cells with higher SOC.
- Balancing commands are boolean vectors activating resistors.

---

## 7. Thermal Management

Thermal management addresses the temperature gradients caused by the asymmetrical thermal layout of the battery pack. For example, in the six-cell configuration, cell 6 heats up significantly more than cell 1 due to its insulation. Such thermal imbalances can lead to uneven aging and degradation of cells, reducing the overall lifespan of the battery pack. Active thermal management strategies are necessary to minimize these differences and maintain cell temperatures within a safe range.

### 7.1 Thermal Asymmetry
- Causes temperature gradients across cells.
- Cell 6 (insulated) heats faster than Cell 1 (exposed).

### 7.2 Active Management
- Equalizes cell temperatures.
- Prevents accelerated degradation of hotter cells.

---

## 8. Simulation Insights

The simulation results highlight the importance of proper design and management of the battery system. During the driving, charging, and balancing sequences, the individual cell voltages initially exhibit differences due to SOC imbalances. These differences converge over time as the balancing algorithm is applied.

The current limiting algorithm demonstrated its effectiveness in preventing unsafe operating conditions by dynamically adjusting current thresholds based on cell voltages and temperatures. The simulation also revealed the limitations of Coulomb counting for SOC estimation, as it failed to recover from initial errors, unlike the Kalman filter methods.

Temperature traces showed significant discrepancies between the hottest and coldest cells, emphasizing the need for robust thermal management solutions. The results also underscored the benefits of using more accurate resistance-based current limiting approaches, which consider real-time SOC and temperature data.

### 8.1 Results
1. **Voltage Behavior:**
   - Voltage differences at the start due to SOC imbalance.
   - Convergence after balancing procedure.
2. **Current Limiting:**
   - Conservative limits based on maximum resistance.
   - Optimized limits use SOC and temperature data.
3. **Temperature Variance:**
   - Uneven heating highlights the need for thermal management.

### 8.2 SOC Estimation
- Coulomb counting fails to correct initial errors.
- Kalman filter methods recover accuracy within simulated time.

---

## 9. Practical Considerations

### 9.1 Precharge Circuitry
Prevents inrush currents during connection to a charger:
- Sequential preconnection via resistors.

### 9.2 Load and Charging Profiles
- Represented by current sources.
- Follow predefined driving and charging sequences.

---

## 10. Summary

The Simulink-based BMS model provides a comprehensive platform for:
- **Simulation:** Testing various operational scenarios without physical risk.
- **Validation:** Ensuring safety and performance across diverse conditions.
- **Development:** Supporting robust design of algorithms for monitoring, balancing, and thermal management.
