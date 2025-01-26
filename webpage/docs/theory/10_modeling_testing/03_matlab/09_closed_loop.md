# Closed-Loop Testing

## **1. Introduction to Closed-Loop Testing**  
Closed-loop testing validates the **entire BMS ECU** against the plant model (e.g., battery pack, charger, load) to ensure system-level functionality and safety. This approach:  
- **Tests Interactions**: Validates the interactions between the BMS controller and physical components.  
- **Real-World Scenarios**: Simulates real-world scenarios such as charging, discharging, and fault handling.  
- **Non-Intrusive Monitoring**: Uses **observers** to monitor internal signals without modifying model interfaces.  

---

## **2. Closed-Loop Test Harness Setup**  
### **2.1 Creating the Test Harness**  
1. **Isolate the Closed-Loop System**:  
   - Combine the BMS ECU and plant model (battery pack, pre-charge circuit).  
   - Use **Simulink Test** to create a test harness:  
     - Navigate to *Apps > Simulink Test > Create Test Harness*.  
2. **Define Test Inputs**:  
   - **Test Sequence Block**: Inject state requests (e.g., `DRIVING`, `CHARGING`, `BALANCING`).  
     - Example:  
       ```plaintext  
       Step 1: Set State = STANDBY for 10 sec.  
       Step 2: Transition to DRIVING when SOC > 30%.  
       Step 3: Trigger FAULT if cell_temp > 45°C.  
       ```  
   - **Signal Builder**: Use pre-recorded test scenarios (e.g., aggressive drive cycles) for consistent testing.  

### **2.2 Visualizing Results**  
- **Dashboard Blocks**:  
  - Add gauges, lamps, and displays to monitor:  
    - Cell temperatures, SOC, pack current/voltage.  
    - Fault indicators (e.g., over-temperature, over-voltage).  

---

## **3. Observing Internal Signals Without Interface Changes**  
### **3.1 Using Observers**  
1. **Add an Observer**:  
   - Right-click the test harness canvas → *Observers > Add Observer*.  
2. **Select Internal Signals**:  
   - Click the observer’s badge (🔍) to explore the model hierarchy.  
   - Example: Monitor `Charge_Current_Limit` and `Discharge_Current_Limit` within the BMS ECU.  
     ```plaintext  
     Path: BMS_ECU → Current_Power_Limits → Charge_Current_Limit  
     Path: BMS_ECU → Current_Power_Limits → Discharge_Current_Limit  
     ```  
   - Click the Wi-Fi icon (📶) to add signals to the observer.  

### **3.2 Observer Output**  
- Observer outputs appear as non-intrusive signals in the test harness.  
- Example:  
  ```plaintext  
  Observer_Outputs:  
    - Charge_Current_Limit  
    - Discharge_Current_Limit  
  ```  

---

## **4. Defining Test Assessments**  
### **4.1 Test Assessment Blocks**  
1. **Add Assessment Block**:  
   - From the *Simulink Test Library*, drag a **Test Assessment** block into the observer.  
2. **Define Verify Statements**:  
   - Use logical conditions to validate signals.  
   - Example:  
     ```matlab  
     % Check charge/discharge limits  
     verify(Charge_Current_Limit < 50);  % Must stay below 50A  
     verify(Discharge_Current_Limit > 10); % Must stay above 10A  
     ```  

### **4.2 Analyzing Results**  
- **Diagnostic Viewer**:  
  - Displays pass/fail status for each `verify` statement.  
  - Example failure:  
    ```plaintext  
    FAIL: Charge_Current_Limit exceeded 50A at t=12.5s.  
    ```  

---

## **5. Workflow Summary**  
1. **Simulate Closed-Loop System**:  
   - Run the test harness with state requests (e.g., charging → driving → fault).  
2. **Monitor Signals**:  
   - Use dashboard blocks for high-level visualization.  
3. **Validate Internal Logic**:  
   - Leverage observers and test assessments to check hidden signals.  

---

## **6. Key Tools**  
| **Tool**               | **Purpose**                                                                 |  
|-------------------------|-----------------------------------------------------------------------------|  
| **Test Sequence Block** | Define state transitions and temporal logic for test scenarios.             |  
| **Signal Builder**      | Inject pre-recorded test inputs (e.g., drive cycles, fault triggers).       |  
| **Observers**           | Monitor internal signals without modifying model interfaces.                |  
| **Test Assessment**     | Automate verification of signal conditions (e.g., thresholds, timing).      |  

---

## **7. Example: Validating Current Limits**  
### **7.1 Test Scenario**  
- **Objective**: Ensure charge/discharge currents stay within safe limits during driving.  
- **Steps**:  
  1. Inject a drive cycle with aggressive acceleration.  
  2. Use observers to monitor `Charge_Current_Limit` and `Discharge_Current_Limit`.  
  3. Verify limits via test assessment blocks.  

### **7.2 Results**  
- **Pass**: Currents stay within bounds (e.g., charge < 50A, discharge > 10A).  
- **Fail**: Diagnostic Viewer reports violations (e.g., over-current during acceleration).  

---

## **8. Benefits of Closed-Loop Testing**  
1. **System Validation**: Test interactions between BMS logic and plant dynamics, ensuring system-level functionality.  
2. **Non-Intrusive Monitoring**: Observe internal signals without redesigning models, reducing development time.  
3. **Automated Checks**: Use `verify` statements to enforce safety constraints, ensuring compliance with design requirements.  

---

## **Summary**  
Closed-loop testing for BMS involves:  
1. **Creating a Test Harness**: Use **Test Sequence** or **Signal Builder** blocks to define test scenarios.  
2. **Monitoring Signals**: Use **observers** to monitor internal signals (e.g., current limits) without modifying the model.  
3. **Validating Behavior**: Use **Test Assessment** blocks and the **Diagnostic Viewer** to enforce safety constraints and validate system behavior.  

For advanced workflows, integrate **Simulink Coverage** to measure test completeness and ensure compliance with standards like ISO 26262. This approach ensures robust and reliable BMS software, ready for real-world deployment.