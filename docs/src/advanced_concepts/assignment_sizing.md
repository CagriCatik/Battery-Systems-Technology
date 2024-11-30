# Assignment of Battery Sizing

## Introduction

Battery Management Systems (BMS) are critical components in modern electrical systems, especially for electric vehicles (EVs). This documentation explores the design and calculation of batteries for applications like two-wheelers, emphasizing industry-oriented approaches that convert qualitative requirements into quantitative solutions. It integrates foundational understanding, practical steps, and essential formulas used in BMS design.

---

## Battery Basics

### What is a Battery?
A battery is an electrochemical device that stores energy and delivers it in the form of electricity. It consists of one or more cells, each having an anode, cathode, and electrolyte.

### Key Parameters:
- Voltage (V): The potential difference provided by the battery.
- Capacity (Ah): The amount of charge the battery can store.
- Energy (kWh): Total stored energy, calculated as \( \text{Energy} = \text{Voltage} \times \text{Capacity} \).
- Specific Energy (Wh/kg): Energy per unit weight.
- Cycle Life: The number of charge-discharge cycles a battery can undergo before its capacity drops significantly.
- Depth of Discharge (DoD): The percentage of the battery capacity that is used in a cycle.

---

## Battery Management Systems (BMS)

### Purpose of a BMS:
A BMS monitors and controls battery performance to ensure safety, longevity, and efficiency. Key functions include:
- Voltage and Current Monitoring
- State of Charge (SoC) Estimation
- Thermal Management
- Cell Balancing
- Fault Detection

---

## Designing a Battery for Two-Wheelers

### Problem Statement:
Design a battery pack for a two-wheeler with the following specifications:
- System Voltage: 48V
- Required Range: 50 km
- Specific Energy Consumption: 68 Wh/km
- Warranty Period: 5 years
- Average Daily Usage: 30 km

The goal is to calculate the battery capacity and ensure the design meets the warranty requirements while addressing real-world user behavior.

---

### Step-by-Step Design Approach:

#### 1. Understand the User Profile
- Daily Usage: 30 km/day
- Warranty Period: 5 years = \( 5 \times 365 = 1825 \) days
- Total Lifetime Distance: \( 30 \times 1825 = 54,750 \) km

#### 2. Determine Energy Requirements
The energy requirement for the two-wheeler is derived from specific energy consumption:
\[ \text{Energy Required (Wh)} = \text{Specific Energy Consumption} \times \text{Daily Distance} \]
\[ \text{Energy Required} = 68 \, \text{Wh/km} \times 30 \, \text{km} = 2040 \, \text{Wh (2.04 kWh)} \]

#### 3. Factor in Efficiency
Assume system efficiency (\( \eta \)) of 90% to account for losses in motor and BMS:
\[ \text{Effective Energy Required} = \frac{\text{Energy Required}}{\eta} \]
\[ \text{Effective Energy Required} = \frac{2040}{0.9} \approx 2267 \, \text{Wh (2.27 kWh)} \]

#### 4. Calculate Battery Capacity
Using a 48V system:
\[ \text{Capacity (Ah)} = \frac{\text{Energy (Wh)}}{\text{Voltage (V)}} \]
\[ \text{Capacity} = \frac{2267}{48} \approx 47.23 \, \text{Ah} \]

#### 5. Verify Against Range Requirements
For a range of 50 km:
\[ \text{Total Energy Required} = 68 \, \text{Wh/km} \times 50 \, \text{km} = 3400 \, \text{Wh (3.4 kWh)} \]
Using a 48V system:
\[ \text{Capacity for Full Range} = \frac{3400}{48} \approx 70.83 \, \text{Ah} \]

---

### Account for Degradation Over Time
Battery performance degrades over time, typically by 20% after 5 years. To account for degradation:
- Initial Capacity (C\_init): \( C\_init = \frac{C}{(1 - \text{Degradation})} \)
- For 20% degradation:
\[ C\_init = \frac{70.83}{0.8} \approx 88.54 \, \text{Ah} \]

---

## Design Summary

| Parameter                | Value           |
|-------------------------------|---------------------|
| System Voltage               | 48V                |
| Daily Energy Requirement     | 2.27 kWh           |
| Capacity for Daily Usage     | 47.23 Ah           |
| Capacity for Full Range      | 70.83 Ah           |
| Initial Capacity (5-year life)| 88.54 Ah           |

---

## Key Considerations for BMS Design

1. Thermal Management:
   - Implement cooling mechanisms to avoid overheating, which affects battery life.
   
2. Cell Balancing:
   - Ensure uniform charge across all cells to prevent overcharging and undercharging.

3. Safety Features:
   - Include protections for overcurrent, short-circuit, and thermal runaway.

4. SoC and SoH Monitoring:
   - Accurately estimate the State of Charge and State of Health for better performance and maintenance planning.

---

To comprehensively size the battery pack for this two-wheeler, let's break the problem into steps:

---

### 1. **Understanding the Requirements**

- **Daily energy requirement:** \(30 \, \text{km/day}\), with a consumption of \(0.5 \, \text{kWh/km}\).  
  - **Daily energy = \( 30 \times 0.5 = 15 \, \text{kWh/day}\).**
- **Maximum range requirement (Full Charge):** 50 km.  
  - **Energy for maximum range = \( 50 \times 0.5 = 25 \, \text{kWh}\).**
- **SoH after 5 years:** Battery will retain 75% of its original capacity.  

Thus, we must ensure that the battery delivers 25 kWh after 5 years, even at 75% SoH.

---

### 2. **Battery Sizing**

#### 2.1. **Determine the Initial Battery Capacity**
- The capacity must account for degradation over 5 years:
  \[
  \text{Initial capacity} = \frac{\text{Required capacity after 5 years}}{\text{SoH after 5 years}} = \frac{25 \, \text{kWh}}{0.75} = 33.33 \, \text{kWh}.
  \]

#### 2.2. **Nominal Voltage of the Pack**
- Nominal voltage is \(48 \, \text{V}\), typical for two-wheelers.

---

### 3. **Battery Cell Configuration**

#### 3.1. **Choose a Battery Cell Type**
- Assume lithium-ion cells with:
  - **Nominal voltage per cell:** \(3.7 \, \text{V}\),
  - **Capacity per cell:** \(3.5 \, \text{Ah}\) (typical for 18650 cells).

#### 3.2. **Determine the Series Configuration**
- To achieve \(48 \, \text{V}\), calculate the number of cells in series:
  \[
  \text{Number of cells in series} = \frac{\text{Nominal voltage of the pack}}{\text{Nominal voltage per cell}} = \frac{48}{3.7} \approx 13 \, \text{cells in series}.
  \]

#### 3.3. **Determine the Parallel Configuration**
- Calculate the pack's total capacity in ampere-hours (Ah):
  \[
  \text{Total capacity (Ah)} = \frac{\text{Total energy (kWh)}}{\text{Voltage (V)}} = \frac{33.33}{48} = 694.44 \, \text{Ah}.
  \]
- Each cell has \(3.5 \, \text{Ah}\). The number of parallel connections is:
  \[
  \text{Cells in parallel} = \frac{\text{Total pack capacity (Ah)}}{\text{Capacity per cell (Ah)}} = \frac{694.44}{3.5} \approx 199 \, \text{cells in parallel}.
  \]

#### 3.4. **Total Number of Cells**
- Total cells in the pack:
  \[
  \text{Total cells} = \text{Cells in series} \times \text{Cells in parallel} = 13 \times 199 = 2587 \, \text{cells}.
  \]

---

### 4. **Verification of Design**

#### 4.1. **Energy Check**
- Energy provided by the pack:
  \[
  \text{Total energy} = \text{Voltage} \times \text{Capacity} = 48 \, \text{V} \times 694.44 \, \text{Ah} = 33.33 \, \text{kWh}.
  \]
- After 5 years at 75% SoH:
  \[
  \text{Remaining energy} = 33.33 \, \text{kWh} \times 0.75 = 25 \, \text{kWh}.
  \]
  This meets the maximum range requirement.

#### 4.2. **Daily Energy Check**
- Energy used daily = \(15 \, \text{kWh/day}\).  
- Energy available after 5 years = \(25 \, \text{kWh}\).  
- Even with a daily usage of \(15 \, \text{kWh}\), the battery provides sufficient energy for \(25/15 = 1.67 \, \text{days}\), ensuring the user can travel daily without exceeding the capacity.

---

### 5. **Weight and Volume Estimate**
The weight and volume depend on the cell type:
- **Energy density (18650 cells):** \(250 \, \text{Wh/kg}\),
- **Battery weight:**
  \[
  \text{Weight} = \frac{\text{Total energy (Wh)}}{\text{Energy density}} = \frac{33,333}{250} \approx 133.33 \, \text{kg}.
  \]
- **Volume (energy density = \(700 \, \text{Wh/L}\)):**
  \[
  \text{Volume} = \frac{\text{Total energy (Wh)}}{\text{Energy density (Wh/L)}} = \frac{33,333}{700} \approx 47.6 \, \text{L}.
  \]

---

### Final Design Summary:

| **Parameter**            | **Value**                      |
|--------------------------|--------------------------------|
| Nominal Voltage          | 48V                           |
| Total Capacity           | 33.33 kWh                     |
| SoH after 5 years        | 75%                           |
| Cells in Series          | 13                            |
| Cells in Parallel        | 199                           |
| Total Cells              | 2587                          |
| Weight                   | ~133 kg                       |
| Volume                   | ~48 L                         |

This battery pack meets the range, warranty, and SoH requirements for the two-wheeler.