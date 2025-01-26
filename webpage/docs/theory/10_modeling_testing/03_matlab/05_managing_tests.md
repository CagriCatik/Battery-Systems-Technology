# Managing Tests in Simulink

## **1. Introduction to Test Management**  
Managing large-scale BMS test suites requires systematic organization, traceability to requirements, and automated reporting. **Simulink Test Manager** centralizes these tasks by:  
- Organizing test cases, iterations, and assessments.  
- Linking tests to requirements for compliance tracking.  
- Generating certification-ready documentation.  

---

## **2. Setting Up the Test Manager**  
### **2.1 Accessing the Test Manager**  
1. **Open Test Manager**:  
   - From the BMS model, click the *Simulink Test* badge (bottom-right corner).  
   - Select *Test Manager*.  
2. **Create a Test File**:  
   - Choose *Test File > New > Test File from Model*.  
   - Select the BMS model and specify the test type:  
     - **Baseline Test**: Compare outputs to a predefined baseline.  
     - **Equivalence Test**: Compare results across different test harnesses/conditions.  
     - **Simulation Test**: Validate behavior using logical/temporal assessments.  

---

## **3. Structuring Test Cases**  
### **3.1 Test Suites and Iterations**  
- **Test Suite**: Groups related test cases (e.g., `Dashboard_Tests`, `Signal_Editor_Tests`).  
- **Iterations**: Define scenarios within a test case (e.g., `Fault_Condition_1`, `Normal_Operation`).  
  - Example:  
    ```plaintext  
    Test Suite: Signal_Builder_Tests  
    ├─ Test Case: Over_Voltage_Scenarios  
    │  ├─ Iteration 1: Cell_Voltage_6V  
    │  └─ Iteration 2: Cell_Voltage_5.5V  
    └─ Test Case: Temperature_Faults  
    ```  

### **3.2 Acceleration with Fast Restart**  
- Enable *Fast Restart* to skip model recompilation between iterations.  

---

## **4. Defining Logical and Temporal Assessments**  
### **4.1 Trigger-Response Assessments**  
1. **Create Assessment**:  
   - In the *Logical and Temporal Assessments* pane, select *Add > Trigger-Response Assessment*.  
   - Example: Verify if the charger’s negative contactor opens when the pre-charge relay opens.  
2. **Configure Triggers**:  
   - **Trigger Condition**: `Charge_Relay_Open == true` AND `BMS_State != Charging`.  
   - **Trigger Duration**: `0.1 seconds` (must stay true for this duration).  
3. **Define Response**:  
   - **Expected Response**: `Negative_Contactor == Open` within a specified delay after the trigger.  

### **4.2 Signal Mapping**  
- Link assessment variables to Simulink signals (e.g., `BMS_State` → `State_Request` signal).  

---

## **5. Executing and Analyzing Tests**  
### **5.1 Running Tests**  
1. **Batch Execution**:  
   - Select test suites/cases and click *Run*.  
   - Results show **Pass/Fail** status for each iteration.  
2. **Debugging Failures**:  
   - Inspect logged signals (e.g., contactor states, voltages).  
   - Example: A test fails because a contactor did not open at `12.2 seconds` due to incorrect time units (seconds vs. milliseconds).  

### **5.2 Coverage Tracking**  
- Enable **Coverage Settings** to track code/model coverage during tests.  

---

## **6. Linking Tests to Requirements**  
### **6.1 Bi-Directional Traceability**  
1. **Add Requirements Column**:  
   - Right-click in the *Iterations Table* → *Add Column > Requirements*.  
2. **Link Tests to Requirements**:  
   - Select a test iteration → Link to a requirement (e.g., `Requirement 4.3: Fault Handling`).  
   - Verify bidirectional links in the *Requirements Browser*.  

### **6.2 Verification Status**  
- **Progress Tracking**:  
  - View verification status (e.g., `Implemented`, `Pending`) for each requirement.  
  - Example:  
    ```plaintext  
    Requirement 4.3 (Fault Handling) → 80% Verified  
    Requirement 2.1 (Input Ranges) → 100% Verified  
    ```  

---

## **7. Generating Certification-Ready Reports**  
### **7.1 Automated Documentation**  
1. **Generate Report**:  
   - In the Test Manager, click *Generate Report*.  
   - Customize content: Include plots, assessments, and pass/fail summaries.  
2. **Report Contents**:  
   - **Header**: Test title, date, and model version.  
   - **Summary**: Pass/fail status per iteration.  
   - **Plots**: Logged signals (e.g., contactor states, cell voltages).  
   - **Assessments**: Detailed results of trigger-response checks.  

### **7.2 Example Report (PDF)**  
```plaintext  
1. Test Summary  
   - Iterations: 11 (7 Passed, 4 Failed)  
2. Failed Tests  
   - Iteration 3: Negative_Contactor did not open at 12.2s (Unit error: seconds vs. milliseconds).  
3. Plots  
   - Figure 1: Contactor states during fault condition.  
   - Figure 2: Cell voltage vs. time.  
```  

---

## **8. Key Benefits**  
1. **Centralized Management**: Organize tests, requirements, and results in one interface.  
2. **Efficient Debugging**: Quickly identify issues via logged signals and failure explanations.  
3. **Certification Compliance**: IEC 61508, ISO 26262, and DO-178C require traceable test documentation.  

---

## **Summary**  
Managing BMS tests in Simulink involves:  
- Structuring test suites/iterations in the **Test Manager**.  
- Defining trigger-response assessments for fault detection.  
- Linking tests to requirements and generating audit-ready reports.  
