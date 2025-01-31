# Initial SoC & SoH Estimation

The State of Charge (SoC) and State of Health (SoH) are fundamental parameters in Battery Management Systems (BMS). Accurate estimation of these metrics is crucial for ensuring the optimal performance, safety, and longevity of battery systems used in applications such as electric vehicles (EVs), renewable energy storage, and portable electronics. This chapter provides a comprehensive exploration of the methods and algorithms employed for initial SoC and SoH estimation, detailing the mathematical and logical processes involved.

---

## Overview of SoC and SoH Estimation

Understanding the State of Charge (SoC) and State of Health (SoH) is essential for effective battery management. These parameters provide insights into the battery's current capacity and its ability to perform over time.

### State of Charge (SoC)

**State of Charge (SoC)** represents the remaining capacity of the battery as a percentage of its maximum capacity. It indicates how much energy is left in the battery at any given time and is crucial for applications like EVs to predict driving range and manage charging cycles effectively.

### State of Health (SoH)

**State of Health (SoH)** reflects the overall condition of the battery, indicating its ability to store and deliver energy compared to its original capacity. SoH accounts for factors such as capacity loss, internal resistance increase, and overall degradation due to aging and usage patterns.

---

## Initial SoC Estimation

Accurate initial SoC estimation is vital for the BMS to provide reliable battery status from the outset. Various methods are employed to determine the initial SoC, each with its advantages and limitations.

### Open-Circuit Voltage (OCV) Method

The Open-Circuit Voltage (OCV) method estimates SoC based on the relationship between the battery's voltage and its SoC when the battery is at rest (i.e., no load or charge is applied). This method is straightforward but requires the battery to be in a rested state to obtain accurate readings.

#### Steps:

1. **Measure Open-Circuit Voltage**: Ensure the battery is at rest, then measure its voltage.
2. **Map OCV to SoC**: Use a pre-defined OCV-SoC curve or lookup table to estimate the SoC based on the measured OCV.

#### Example:

```c
// Function to estimate SoC using OCV Method
float estimate_SOC_OCV(float ocv) {
    // Example OCV-SoC lookup table
    float ocv_table[] = {3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2}; // Voltage in volts
    float soc_table[] = {0, 20, 40, 60, 80, 90, 100}; // SoC in percentage
    int table_size = sizeof(ocv_table) / sizeof(ocv_table[0]);

    // Find the closest OCV value in the table
    for(int i = 0; i < table_size - 1; i++) {
        if(ocv >= ocv_table[i] && ocv < ocv_table[i+1]) {
            // Linear interpolation
            float slope = (soc_table[i+1] - soc_table[i]) / (ocv_table[i+1] - ocv_table[i]);
            return soc_table[i] + slope * (ocv - ocv_table[i]);
        }
    }
    return soc_table[table_size - 1]; // Return 100% if OCV exceeds table
}
```

*Note: The OCV-SoC relationship varies with battery chemistry and temperature. Calibration is essential for accurate estimation.*

### Coulomb Counting Method

Coulomb counting estimates SoC by integrating the current flowing into or out of the battery over time. This method provides dynamic SoC estimation but requires an accurate initial SoC value and precise current measurements to minimize cumulative errors.

#### Steps:

1. **Measure Current Flow**: Continuously measure the current entering (charging) or leaving (discharging) the battery.
2. **Integrate Current Over Time**: Calculate the total charge added or removed by integrating the current over the elapsed time.
3. **Update SoC**: Adjust the initial SoC based on the integrated charge.

#### Example:

```c
// Function to estimate SoC using Coulomb Counting
float estimate_SOC(float current, float delta_time, float initial_SOC, float battery_capacity) {
    // current: Current in amperes (A)
    // delta_time: Time interval in seconds (s)
    // initial_SOC: SoC at the beginning of the interval (%)
    // battery_capacity: Total battery capacity in ampere-hours (Ah)

    // Convert battery capacity to coulombs (1 Ah = 3600 C)
    float battery_capacity_coulombs = battery_capacity * 3600.0;

    // Calculate charge change (Coulombs)
    float delta_charge = current * delta_time;

    // Update SoC
    float new_SOC = initial_SOC - (delta_charge / battery_capacity_coulombs) * 100.0;

    // Clamp SoC between 0% and 100%
    if (new_SOC > 100.0) new_SOC = 100.0;
    if (new_SOC < 0.0) new_SOC = 0.0;

    return new_SOC;
}
```

*Note: Accurate current measurement and minimal sensor drift are critical for reducing errors in Coulomb counting.*

---

## Initial SoH Estimation

State of Health (SoH) estimation evaluates the battery's condition and predicts its remaining useful life. Accurate SoH assessment helps in proactive maintenance and ensures reliability in applications.

### Capacity Loss Calculation

Capacity loss quantifies the reduction in the battery's ability to store energy compared to its original capacity. It is influenced by factors like the number of charge-discharge cycles, depth of discharge, and operating temperatures.

#### Steps:

1. **Determine Charge-Discharge Cycles**: Track the number of complete and partial charge-discharge cycles the battery has undergone.
2. **Estimate Capacity Loss**: Use empirical models or lookup tables to estimate capacity loss based on the cycle count.
3. **Calculate Current Capacity**: Subtract the estimated capacity loss from the original capacity.
4. **Compute SoH**: Express SoH as the ratio of current capacity to original capacity.

#### Formula:

$$
\text{SoH} = \left( \frac{\text{Current Capacity}}{\text{Original Capacity}} \right) \times 100\%
$$

#### Example:

```c
// Function to estimate SoH based on capacity loss
float estimate_SOH(float current_capacity, float original_capacity) {
    return (current_capacity / original_capacity) * 100.0;
}
```

### Cycle Counting

Cycle counting involves tracking the number of charge-discharge cycles a battery has experienced. Each cycle contributes to the gradual degradation of the battery's capacity and overall health.

#### Steps:

1. **Measure Depth of Discharge (DoD)**: For each cycle, determine how deeply the battery was discharged.
2. **Accumulate Partial Cycles**: Account for partial cycles by normalizing DoD to equivalent full cycles.
3. **Estimate Total Cycles**: Sum the equivalent full cycles to determine the total cycle count.
4. **Map Cycles to Capacity Loss**: Use a predefined model or lookup table to estimate capacity loss based on total cycles.

#### Example:

```c
// Function to estimate SoH based on cycle counting
float estimate_SOH_cycles(int total_cycles, float capacity_loss_per_cycle) {
    float total_capacity_loss = total_cycles * capacity_loss_per_cycle;
    float soh = 100.0 - total_capacity_loss;
    if (soh < 0.0) soh = 0.0;
    return soh;
}
```

*Note: The capacity loss per cycle varies with battery chemistry and operating conditions.*

---

## Mathematical and Logical Steps for SoC and SoH Estimation

Accurate SoC and SoH estimation involves a systematic approach that integrates data collection, processing, and algorithmic analysis.

### Data Collection

Effective estimation begins with the acquisition of accurate and reliable data from the battery system.

- **Terminal Voltage**: Measure the voltage across the battery terminals using voltage sensors.
- **Current**: Monitor the current flowing into or out of the battery using current sensors.
- **Temperature**: Track the battery temperature using temperature sensors.
- **Open-Circuit Voltage (OCV)**: Measure OCV when the battery is at rest for the OCV-based SoC estimation.

### Cycle Counting and Capacity Loss Estimation

1. **Calculate Depth of Discharge (DoD)**:
   
   $$
   \text{DoD} = \frac{\text{Energy Discharged}}{\text{Battery Capacity}} \times 100\%
   $$

2. **Accumulate DoD Values**:
   
   Normalize partial cycles to equivalent full cycles.

   $$
   \text{Equivalent Full Cycles} = \frac{\text{DoD}}{100\%}
   $$

3. **Estimate Capacity Loss**:
   
   Use the total number of equivalent full cycles to determine capacity loss.

4. **Compute SoH**:
   
   Apply the capacity loss to calculate SoH.

### 4.3 SoC Estimation

1. **Initial SoC Estimation**:
   
   Utilize the OCV method to establish the initial SoC when the battery is at rest.

2. **Dynamic SoC Update**:
   
   Implement Coulomb counting to update SoC in real-time during battery operation.

   ```c
   // Combined SoC Estimation Process
   float initial_SOC = estimate_SOC_OCV(measured_ocv);
   float updated_SOC = initial_SOC;

   void update_SOC(float current, float delta_time, float battery_capacity) {
       updated_SOC = estimate_SOC(current, delta_time, updated_SOC, battery_capacity);
   }
   ```

### SoH Estimation

1. **Calculate Current Capacity**:
   
   Subtract the estimated capacity loss from the original capacity.

2. **Compute SoH**:
   
   Use the SoH formula to determine the battery's health status.

   ```c
   // Combined SoH Estimation Process
   float current_capacity = original_capacity - (total_cycles * capacity_loss_per_cycle);
   float soh = estimate_SOH(current_capacity, original_capacity);
   ```

---

## Practical Implementation in BMS

Implementing SoC and SoH estimation within a BMS involves integrating the aforementioned algorithms into the system's software architecture. The following steps outline the practical workflow:

1. **Data Acquisition**: Continuously collect sensor data (voltage, current, temperature) from the battery modules via slave units.

2. **Initial SoC Estimation**:
   - When the battery is at rest, measure the OCV.
   - Use the OCV-SoC lookup table or curve to estimate the initial SoC.

3. **Cycle Counting**:
   - Track each charge-discharge cycle and calculate the DoD.
   - Accumulate partial cycles to estimate the total number of equivalent full cycles.

4. **Capacity Loss Estimation**:
   - Utilize a lookup table or empirical model to determine capacity loss based on the total cycle count.

5. **SoH Calculation**:
   - Calculate the current capacity by subtracting the capacity loss from the original capacity.
   - Compute SoH using the current and original capacity values.

6. **Dynamic SoC Update**:
   - During operation, employ Coulomb counting to update SoC based on real-time current measurements.

7. **Integration and Communication**:
   - Integrate SoC and SoH estimates into the BMS's overall monitoring and control logic.
   - Communicate the estimated SoC and SoH to the Vehicle Control Unit (VCU) and other relevant systems for informed decision-making.

#### Example Workflow:

```c
// Initialize BMS Parameters
float original_capacity = 100.0; // in Ah
float capacity_loss_per_cycle = 0.05; // in Ah
int total_cycles = 0;

// Initial SoC Estimation
float measured_ocv = readOCV();
float initial_SOC = estimate_SOC_OCV(measured_ocv);
float current_SOC = initial_SOC;

// Main Control Loop
void loop() {
    // Data Acquisition
    float current = readCurrentSensor();
    float voltage = readVoltageSensor();
    float temperature = readTemperatureSensor();
    float delta_time = getDeltaTime(); // Time since last update

    // Update SoC
    current_SOC = estimate_SOC(current, delta_time, current_SOC, original_capacity);

    // Cycle Counting
    float dod = calculate_DoD(voltage, original_capacity);
    total_cycles += calculate_equivalent_cycles(dod);

    // Capacity Loss Estimation
    float capacity_loss = total_cycles * capacity_loss_per_cycle;
    float current_capacity = original_capacity - capacity_loss;

    // SoH Calculation
    float soh = estimate_SOH(current_capacity, original_capacity);

    // Communication with VCU
    send_SOC_SoH_to_VCU(current_SOC, soh);

    // Safety and Control Actions
    enforceSafetyLimits(voltage, current, temperature);

    delay(1000); // Update interval (e.g., 1 second)
}
```

*Note: The above example is a simplified representation. Actual implementations may require more sophisticated error handling and calibration mechanisms.*

---

## Summary of SoC and SoH Estimation

Understanding and accurately estimating SoC and SoH are pivotal for effective battery management. The methods outlined ensure that the BMS can provide reliable information for optimal battery operation and longevity.

| **Parameter**       | **Method**                          | **Key Steps**                                                                 |
|---------------------|-------------------------------------|-------------------------------------------------------------------------------|
| **State of Charge (SoC)** | Open-Circuit Voltage (OCV) Method  | Measure OCV, use lookup table to estimate SoC.                                |
|                     | Coulomb Counting Method            | Integrate current over time, update SoC based on initial value.               |
| **State of Health (SoH)** | Capacity Loss Estimation           | Track cycles, estimate capacity loss, compute SoH as current/original capacity.|
|                     | Cycle Counting                      | Measure DoD, accumulate equivalent cycles, map to capacity loss.             |

---

## Challenges and Future Directions

While significant advancements have been made in SoC and SoH estimation, several challenges persist that require ongoing research and development.

### Accuracy

- **Sensor Precision**: High-precision sensors are essential for minimizing errors in voltage and current measurements.
- **Algorithm Calibration**: Continuous calibration of estimation algorithms is necessary to account for changes in battery behavior over time and under varying conditions.

### Aging Effects

- **Dynamic Modeling**: Developing models that accurately reflect the aging process of batteries to improve SoH estimation.
- **Adaptive Algorithms**: Implementing algorithms that adapt to the changing characteristics of the battery as it ages.

### Real-Time Implementation

- **Computational Efficiency**: Designing algorithms that can run efficiently on embedded systems with limited processing power.
- **Latency Reduction**: Ensuring that SoC and SoH estimations are updated promptly to reflect real-time battery states.

### Environmental Factors

- **Temperature Variations**: Accounting for the impact of temperature on battery performance and measurement accuracy.
- **Load Fluctuations**: Managing rapid changes in load conditions to maintain accurate SoC and SoH estimates.

### Integration with Advanced Technologies

- **Machine Learning and AI**: Leveraging advanced machine learning techniques to enhance the accuracy and adaptability of SoC and SoH estimation algorithms.
- **IoT Integration**: Utilizing IoT platforms for remote monitoring and data analysis to improve estimation accuracy and enable predictive maintenance.
