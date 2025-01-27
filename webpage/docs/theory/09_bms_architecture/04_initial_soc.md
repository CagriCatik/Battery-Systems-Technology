# Initial SoC & SoH Estimation

The State of Charge (SoC) and State of Health (SoH) are two critical parameters in Battery Management Systems (BMS). Accurate estimation of these parameters is essential for ensuring the optimal performance, safety, and longevity of battery systems. This section provides a detailed explanation of the methods and algorithms used for initial SoC and SoH estimation, including the mathematical and logical steps involved.

---

## 1. **Overview of SoC and SoH Estimation**

### 1.1 **State of Charge (SoC)**
SoC represents the remaining capacity of the battery as a percentage of its maximum capacity. It indicates how much energy is left in the battery at any given time.

### 1.2 **State of Health (SoH)**
SoH reflects the overall condition of the battery, indicating its ability to store and deliver energy compared to its original capacity. It accounts for factors such as capacity loss and aging.

---

## 2. **Initial SoC Estimation**

The initial SoC estimation is typically based on the open-circuit voltage (OCV) of the battery. However, other methods, such as coulomb counting, are also used for more accurate and dynamic estimation.

### 2.1 **Open-Circuit Voltage (OCV) Method**
- The OCV method relies on the relationship between the battery's voltage and its SoC when the battery is at rest (no load or charge).
- A lookup table or curve is used to map the measured OCV to the corresponding SoC.

#### Steps:
1. Measure the battery's open-circuit voltage.
2. Use a pre-defined OCV-SoC curve or lookup table to estimate the SoC.

### 2.2 **Coulomb Counting Method**
- Coulomb counting involves integrating the current flowing in or out of the battery over time to estimate the SoC.
- This method is more accurate during dynamic operation but requires an initial SoC value to start the integration.

#### Steps:
1. Measure the current flowing into or out of the battery.
2. Integrate the current over time to calculate the charge added or removed.
3. Update the SoC based on the initial SoC and the calculated charge.

---

## 3. **Initial SoH Estimation**

SoH estimation is based on the battery's capacity loss over time, which is influenced by factors such as the number of charge-discharge cycles and operating conditions.

### 3.1 **Capacity Loss Calculation**
- The capacity loss is calculated by comparing the current capacity of the battery with its original (rated) capacity.
- The number of charge-discharge cycles is a key factor in determining capacity loss.

#### Steps:
1. Determine the number of charge-discharge cycles completed by the battery.
2. Use a lookup table or model to estimate the capacity loss corresponding to the number of cycles.
3. Calculate the current capacity by subtracting the capacity loss from the original capacity.
4. Compute the SoH as the ratio of the current capacity to the original capacity.

#### Formula:
$$
\text{SoH} = \frac{\text{Current Capacity}}{\text{Original Capacity}} \times 100\%
$$

### 3.2 **Cycle Counting**
- Cycle counting involves tracking the number of charge-discharge cycles the battery has undergone.
- A cycle is typically defined as a full charge followed by a full discharge, but partial cycles are also accounted for.

#### Steps:
1. Measure the depth of discharge (DoD) for each charge-discharge event.
2. Accumulate the partial cycles to estimate the total number of equivalent full cycles.
3. Use the total number of cycles to estimate capacity loss and SoH.

---

## 4. **Mathematical and Logical Steps for SoC and SoH Estimation**

### 4.1 **Data Collection**
- Collect terminal voltage, current, and temperature data from the battery.
- Measure the open-circuit voltage (OCV) when the battery is at rest.

### 4.2 **Cycle Counting and Capacity Loss Estimation**
1. Calculate the difference between the charge and discharge voltages for each cycle.
2. Divide the difference by the rated voltage to determine the depth of discharge (DoD).
3. Accumulate the DoD values to estimate the total number of equivalent full cycles.
4. Use a lookup table or model to estimate the capacity loss based on the number of cycles.

### 4.3 **SoC Estimation**
1. Use the OCV method to estimate the initial SoC.
2. Apply coulomb counting to update the SoC during operation.

### 4.4 **SoH Estimation**
1. Calculate the current capacity by subtracting the estimated capacity loss from the original capacity.
2. Compute the SoH as the ratio of the current capacity to the original capacity.

---

## 5. **Practical Implementation in BMS**

In a BMS, the SoC and SoH estimation algorithms are implemented in software and executed by the microcontroller. The following steps outline the practical implementation:

1. **Data Acquisition**: Collect sensor data (voltage, current, temperature) from the battery.
2. **Initial SoC Estimation**: Use the OCV method to estimate the initial SoC.
3. **Cycle Counting**: Track the number of charge-discharge cycles and calculate the depth of discharge (DoD).
4. **Capacity Loss Estimation**: Use a lookup table or model to estimate capacity loss based on the number of cycles.
5. **SoH Calculation**: Compute the SoH using the current and original capacity values.
6. **Dynamic SoC Update**: Use coulomb counting to update the SoC during operation.

---

## 6. **Summary of SoC and SoH Estimation**

| **Parameter**       | **Method**                          | **Key Steps**                                                                 |
|----------------------|-------------------------------------|-------------------------------------------------------------------------------|
| **State of Charge (SoC)** | Open-Circuit Voltage (OCV) Method  | Measure OCV, use lookup table to estimate SoC.                                |
|                      | Coulomb Counting Method            | Integrate current over time, update SoC based on initial value.               |
| **State of Health (SoH)** | Capacity Loss Estimation           | Track cycles, estimate capacity loss, compute SoH as current/original capacity.|

---

## 7. **Challenges and Future Directions**

- **Accuracy**: Improving the accuracy of SoC and SoH estimation algorithms is a key challenge, especially under varying operating conditions.
- **Aging Effects**: Accounting for battery aging and its impact on capacity loss requires advanced models and algorithms.
- **Real-Time Implementation**: Ensuring real-time performance of estimation algorithms on embedded systems with limited computational resources.

---

This documentation provides a comprehensive overview of the methods and algorithms used for initial SoC and SoH estimation in BMS. By understanding these concepts, engineers can design more accurate and reliable battery management systems, ensuring optimal performance and longevity of battery systems.