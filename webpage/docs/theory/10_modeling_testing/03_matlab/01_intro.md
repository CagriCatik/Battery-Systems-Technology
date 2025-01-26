# Battery Management System in Simulink

## **1. System Overview**  
The Battery Management System (BMS) model in Simulink is designed to facilitate **desktop simulations** for evaluating system responses under various conditions such as temperature extremes, aggressive drive cycles, and State of Charge (SOC) variations. The primary objectives of the BMS model include:  
- **Preventing Unsafe Conditions**: Monitoring and mitigating risks such as over/under-voltage and over-temperature scenarios.  
- **Validating BMS Algorithms**: Testing and refining algorithms for cell balancing, SOC estimation, and state transitions.  
- **Ensuring Compliance**: Adhering to electrical and thermal limits to ensure safe and efficient operation.  

### **1.1 Model Structure**  
The BMS model is structured into several key components:  
- **Test Scenarios**: Defined in the `Source` subsystem (bottom left), these include driving and charging profiles to simulate real-world conditions.  
- **Battery Pack**: Modeled using Simscape, this component captures multi-domain physics, including electrical and thermal behaviors.  
- **BMS ECU**: This subsystem contains monitoring and control algorithms, as well as state machines implemented using Stateflow.  
- **Fault Indicators**: Visual indicators (green/red lights) are used to signal faults such as cell over-temperature or over-voltage conditions.  

---

## **2. Battery Pack Modeling**  
### **2.1 Battery Configurations**  
The BMS model supports two primary battery configurations:  
- **Small Pack**: Consists of 6 cells in series, ideal for rapid prototyping and initial testing.  
- **Large Pack**: Comprises 96 cells arranged in 16 modules of 6 cells each, designed for scalability and more comprehensive testing.  

#### **Thermal Layout**  
The thermal design of the battery pack is **asymmetric**:  
- **Cell 6 (Bottom)**: Insulated, which limits heat dissipation and leads to higher temperatures.  
- **Cell 1 (Top)**: Exposed to ambient convection, resulting in lower temperatures compared to Cell 6.  
- **Impact**: This asymmetry causes significant temperature differences between cells, with Cell 6 degrading faster due to higher thermal stress.  

### **2.2 Cell Equivalent Circuit**  
The battery cell is modeled using an equivalent circuit approach, which represents lithium-ion chemistry (e.g., NMC) with parameters that depend on temperature and SOC.  
- **Components**: The circuit includes resistors, capacitors, and voltage sources to mimic real-world battery behavior.  
- **Behavior**: The model captures the dynamic response of the battery under various operating conditions, including charge/discharge cycles and temperature variations.  

### **2.3 Peripheral Circuits**  
The BMS model includes several peripheral circuits to simulate real-world battery management scenarios:  
1. **Passive Balancing**:  
   - **Mechanism**: High-SOC cells are discharged through resistors using boolean `balance_commands` to activate specific cell resistors.  
   - **Purpose**: Ensures uniform charge utilization across all cells in the pack.  
2. **Pre-Charge Contactor Logic**:  
   - **Function**: A resistor is connected in series with the battery pack to avoid inrush current during charging.  
   - **Benefit**: Protects the battery and connected electronics from damage due to sudden current surges.  
3. **Charger/Load**:  
   - **Modeling**: Chargers and loads are modeled as current sources that follow predefined test profiles.  

---

## **3. BMS Algorithm Components**  
### **3.1 Current Limiting Logic**  
The BMS includes logic to limit current based on voltage and temperature thresholds:  
- **Voltage-Based Threshold**:  
  - **Calculation**: The maximum allowable current is determined by the formula:  
    \[
    I_{max} = \frac{V_{min} - V_{cutoff}}{R_{max}}
    \]
    where \(V_{min}\) is the minimum cell voltage, \(V_{cutoff}\) is the cutoff voltage, and \(R_{max}\) is the maximum resistance.  
  - **Purpose**: Prevents over-voltage conditions during charging.  
- **Temperature-Based Threshold**:  
  - **Implementation**: Uses lookup tables with S-shaped profiles to limit current at extreme temperatures.  
  - **Application**: Prevents damage during charging at low temperatures and discharging at high temperatures.  

### **3.2 State Machine (Stateflow)**  
The BMS state machine, implemented using Stateflow, operates in four parallel states:  
1. **Main Operational States**:  
   - `Standby`: The system is idle, waiting for a command to start charging or discharging.  
   - `Driving`: The battery is discharging to power the vehicle.  
   - `Charging`: The battery is being charged, with Constant Current (CC) and Constant Voltage (CV) stages.  
   - `Fault`: The system enters this state when a fault condition is detected.  
2. **Fault Monitoring**:  
   - **Triggers**: Over-current, over-voltage, or over-temperature conditions.  
   - **Response**: The system transitions to the `Fault` state and takes appropriate protective actions.  
3. **Contactor Control**:  
   - **Function**: Manages the sequence of charger and inverter contactor operations to prevent inrush currents.  

---

## **4. SOC Estimation Methods**  
### **4.1 Coulomb Counting**  
- **Principle**: The SOC is estimated by integrating the current over time:  
  \[
  SOC = SOC_{initial} + \frac{\int I \, dt}{Capacity}
  \]
- **Advantages**: Simple to implement and computationally inexpensive.  
- **Disadvantages**: Accumulates sensor errors over time and lacks feedback to correct initial SOC inaccuracies.  

### **4.2 Kalman Filters**  
The BMS model employs two types of Kalman filters for SOC estimation:  
1. **Extended Kalman Filter (EKF)**:  
   - **Method**: Linearizes the cell model for state prediction and correction.  
   - **Use Case**: Suitable for systems with mild non-linearities, such as the SOC vs. Open Circuit Voltage (OCV) curve.  
2. **Unscented Kalman Filter (UKF)**:  
   - **Method**: Handles non-linearities without requiring linearization.  
   - **Use Case**: More accurate than EKF for highly non-linear systems but computationally heavier.  
- **Both Methods**:  
  - **Feedback**: Use cell terminal voltage measurements to correct SOC predictions.  
  - **Performance**: Outperform Coulomb counting in scenarios with initial SOC mismatches, providing faster and more accurate error recovery.  

---

## **5. Simulation Results**  
### **5.1 Voltage and Balancing**  
- **Cell Voltages**: During balancing, cell voltages converge, reducing SOC imbalances across the pack.  
- **Balancing Logic**: The BMS activates resistors for high-SOC cells, ensuring uniform charge utilization and prolonging battery life.  

### **5.2 Temperature Dynamics**  
- **Cell 6 vs. Cell 1**:  
  - **Cell 6 (Insulated)**: Reaches higher temperatures due to limited heat dissipation, leading to accelerated degradation.  
  - **Cell 1 (Exposed)**: Maintains lower temperatures due to better heat dissipation.  
  - **Implication**: Highlights the need for active thermal management solutions, such as cooling plates or liquid cooling systems.  

### **5.3 SOC Estimation Comparison**  
- **Coulomb Counting**: Fails to recover from an initial 80% SOC error due to the lack of feedback.  
- **EKF/UKF**: Both filters correct the SOC to the true value of 75% within 1 hour, with EKF being slightly faster.  

### **5.4 Fault Handling**  
- **Over-Voltage Protection**: The BMS limits charging current when cell voltage approaches 4.4V, preventing over-voltage conditions.  

---

## **6. Key Tools and Workflow**  
- **Simscape**: Used for multi-domain modeling, capturing electrical and thermal behaviors of the battery pack.  
- **Stateflow**: Enables the design of state machines for operational and fault modes.  
- **Control System Toolbox**: Implements Kalman filters for accurate SOC estimation.  
- **Simulation Workflow**:  
  1. **Define Test Scenarios**: Specify drive cycles, ambient conditions, and initial SOC levels.  
  2. **Simulate BMS Response**: Evaluate the system's performance under edge cases, such as high temperatures or low initial SOC.  
  3. **Validate Compliance**: Ensure the BMS meets safety and performance requirements under all tested conditions.  

---

## **Summary**  
The BMS model in Simulink provides a robust platform for:  
- **Risk-Free Testing**: Validating BMS algorithms without the need for physical hardware.  
- **Accurate SOC Estimation**: Combining Coulomb counting with advanced Kalman filters for precise SOC tracking.  
- **Thermal Insights**: Identifying design flaws, such as asymmetric heat dissipation, and guiding improvements.  
- **Scalability**: Supporting both small (6-cell) and large (96-cell) battery packs for comprehensive testing and validation.