# **Battery Management System (BMS) Development in Simulink**  

## **1. System Overview**  
The BMS model in Simulink enables **desktop simulations** to evaluate system responses under diverse conditions (e.g., temperature extremes, aggressive drive cycles, SOC variations). Key goals include:  
- Preventing unsafe conditions (over/under-voltage, over-temperature).  
- Validating BMS algorithms (balancing, SOC estimation, state transitions).  
- Ensuring compliance with electrical/thermal limits.  

### **1.1 Model Structure**  
- **Top-Level Components**:  
  - **Test Scenarios**: Driving/charging profiles defined in the `Source` subsystem (bottom left).  
  - **Battery Pack**: Modeled with Simscape for multi-domain physics (electrical, thermal).  
  - **BMS ECU**: Contains monitoring, control algorithms, and state machines (Stateflow).  
  - **Fault Indicators**: Green/red lights signal faults (e.g., cell over-temperature).  

---

## **2. Battery Pack Modeling**  
### **2.1 Battery Configurations**  
- **Small Pack**: 6 cells in series (for rapid prototyping).  
- **Large Pack**: 96 cells (16 modules × 6 cells) for scalability.  
- **Thermal Layout**:  
  - **Asymmetric Design**:  
    - Cell 6 (bottom) is insulated, limiting heat dissipation.  
    - Cell 1 (top) exposed to ambient convection.  
  - **Impact**: Significant temperature differences between cells (e.g., Cell 6 degrades faster).  

### **2.2 Cell Equivalent Circuit**  
- Represents lithium-ion chemistry (e.g., NMC) with temperature/SOC-dependent parameters.  
- **Components**: Resistors, capacitors, voltage sources to mimic real-world behavior.  

### **2.3 Peripheral Circuits**  
1. **Passive Balancing**:  
   - Switches discharge high-SOC cells via resistors.  
   - `balance_commands` (boolean vector) activates specific cell resistors.  
2. **Pre-Charge Contactor Logic**:  
   - Resistor pre-connection avoids inrush current during charging.  
3. **Charger/Load**: Modeled as current sources following test profiles.  

---

## **3. BMS Algorithm Components**  
### **3.1 Current Limiting Logic**  
- **Voltage-Based Threshold**:  
  - Compares minimum cell voltage against cutoff voltage.  
  - Max current = `(V_min - V_cutoff) / R_max` (conservative estimate).  
- **Temperature-Based Threshold**:  
  - Uses lookup tables with S-shaped profiles to limit current at extreme temperatures.  
  - Prevents damage during charge (low temps) and discharge (high temps).  

### **3.2 State Machine (Stateflow)**  
Four parallel states:  
1. **Main Operational States**:  
   - `Standby`, `Driving`, `Charging` (CC/CV stages), `Fault`.  
2. **Fault Monitoring**:  
   - Triggers `Fault` state on over-current/voltage/temperature.  
3. **Contactor Control**:  
   - Manages charger/inverter contactor sequences to prevent inrush currents.  

---

## **4. SOC Estimation Methods**  
### **4.1 Coulomb Counting**  
- **Principle**: Integrate current over time (`SOC = SOC_initial + ∫I dt / Capacity`).  
- **Pros**: Simple, low computational cost.  
- **Cons**: Accumulates sensor errors, no feedback (cannot recover from incorrect initial SOC).  

### **4.2 Kalman Filters**  
1. **Extended Kalman Filter (EKF)**:  
   - Linearizes cell model for state prediction/correction.  
   - Suitable for mild non-linearities (e.g., SOC vs. OCV curve).  
2. **Unscented Kalman Filter (UKF)**:  
   - Handles non-linearities without linearization.  
   - Computationally heavier than EKF.  
- **Both Methods**:  
  - Use cell terminal voltage feedback to correct predictions.  
  - Outperform Coulomb counting in error recovery (e.g., initial SOC mismatch).  

---

## **5. Simulation Results**  
### **5.1 Voltage and Balancing**  
- **Cell Voltages**: Converge during balancing (reducing SOC imbalance).  
- **Balancing Logic**: Activates resistors for high-SOC cells, ensuring uniform charge utilization.  

### **5.2 Temperature Dynamics**  
- **Cell 6 vs. Cell 1**:  
  - Cell 6 (insulated) reaches higher temperatures, accelerating degradation.  
  - Highlights need for active thermal management (e.g., cooling plates).  

### **5.3 SOC Estimation Comparison**  
- **Coulomb Counting**: Fails to recover from initial 80% SOC error (no feedback).  
- **EKF/UKF**: Correct SOC to true 75% within 1 hour (EKF slightly faster).  

### **5.4 Fault Handling**  
- **Over-Voltage Protection**: Limits charging current when cell voltage nears 4.4V.  

---

## **6. Key Tools and Workflow**  
- **Simscape**: Multi-domain modeling (electrical, thermal).  
- **Stateflow**: State machine design for operational/fault modes.  
- **Control System Toolbox**: Implements Kalman filters for SOC estimation.  
- **Simulation Workflow**:  
  1. Define test scenarios (drive cycles, ambient conditions).  
  2. Simulate BMS response to edge cases (e.g., 40°C, 30% initial SOC).  
  3. Validate compliance with safety/performance requirements.  

---

## **Summary**  
The BMS model in Simulink enables:  
- **Risk-Free Testing**: Validate algorithms without physical hardware.  
- **Accurate SOC Estimation**: Combines Coulomb counting with Kalman filters.  
- **Thermal Insights**: Identifies design flaws (e.g., asymmetric heat dissipation).  
- **Scalability**: Supports small (6-cell) to large (96-cell) packs.  
