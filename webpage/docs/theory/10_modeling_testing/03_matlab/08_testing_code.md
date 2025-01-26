# Testing Generated Code

## **1. Introduction to Code Validation**  
After generating code from a Battery Management System (BMS) model, validation ensures the code behaves identically to the original Simulink design. Two key methods are used:  
- **Software-in-the-Loop (SIL)**: Executes generated code on a host PC, validating functional correctness.  
- **Processor-in-the-Loop (PIL)**: Runs code on the target embedded hardware (e.g., BeagleBone Black), measuring performance and real-time behavior.  

---

## **2. Software-in-the-Loop (SIL) Testing**  
### **2.1 Workflow**  
1. **Generate Code**: Use Embedded Coder to produce `.c` and `.h` files from the BMS model.  
2. **Reuse Existing Tests**: Leverage test harnesses created for the Simulink model to validate the generated code.  
3. **Configure SIL Mode**:  
   - In **Simulink Test Manager**, select *Simulation Mode > Software-in-the-Loop*.  
   - This replaces the Simulink model with the compiled object code during simulation.  

### **2.2 Equivalence Testing**  
- **Objective**: Compare results from **Model-in-the-Loop (MIL)** and **SIL** simulations to ensure the generated code matches the model behavior.  
- **Steps**:  
  1. Run MIL tests (original Simulink model).  
  2. Run SIL tests (generated code).  
  3. Use **Simulink Test Manager** to validate equivalence (pass/fail).  

### **2.3 Analyzing Results**  
- **Simulation Data Inspector**:  
  - Compare logged signals (e.g., contactor states, fault flags) between MIL and SIL runs.  
  - Example: `Error = 0` indicates identical behavior.  
- **Code Coverage**:  
  - Enable coverage metrics (e.g., MCDC) in SIL mode to validate code execution paths and ensure comprehensive testing.  

---

## **3. Processor-in-the-Loop (PIL) Testing**  
### **3.1 PIL Setup**  
1. **Target Configuration**:  
   - Select the embedded hardware (e.g., BeagleBone Black) in *Simulink > Hardware Settings*.  
   - Cross-compile code for the target processor.  
2. **Configure PIL Mode**:  
   - In the **SIL/PIL Manager**, enable *Processor-in-the-Loop*.  

### **3.2 Execution Time Measurement**  
- **Task Execution Time**:  
  - Measure how long the BMS code takes to execute on the target hardware.  
  - Example: `3.9 µs` per cycle (as reported in the **Simulation Data Inspector**).  

### **3.3 Workflow**  
1. **Run PIL Tests**:  
   - Execute tests on the target hardware via the **SIL/PIL Manager**.  
2. **Compare Results**:  
   - Validate equivalence between MIL, SIL, and PIL outputs to ensure consistency across all testing stages.  
3. **Generate Report**:  
   - Includes task execution time, memory usage, and signal comparisons for detailed analysis.  

---

## **4. Key Tools and Workflow**  
### **4.1 Simulink Test Manager**  
- **Equivalence Tests**: Automate MIL vs. SIL/PIL comparisons to ensure functional correctness.  
- **Batch Execution**: Run multiple iterations (e.g., 11 test scenarios) to validate edge cases.  
- **Coverage Integration**: Track code coverage metrics during SIL/PIL runs to ensure comprehensive testing.  

### **4.2 SIL/PIL Manager**  
- **Hardware Integration**:  
  - Supports BeagleBone Black, Arduino, and custom targets for flexible testing.  
- **Automated Back-to-Back Testing**:  
  - Validate code against the model without manual intervention, reducing errors and saving time.  

### **4.3 Simulation Data Inspector**  
- **Signal Comparison**: Overlay MIL, SIL, and PIL signals to detect discrepancies and ensure consistency.  
- **Execution Time Profiling**: Visualize task timing for performance optimization and real-time compliance.  

---

## **5. Benefits**  
1. **Functional Correctness**: Ensure the generated code matches the model behavior, reducing the risk of errors.  
2. **Performance Metrics**: Measure execution time and memory usage to validate real-time performance.  
3. **Certification Readiness**: SIL/PIL tests align with safety standards like ISO 26262 and DO-178C, ensuring compliance.  

---

## **6. Example: BeagleBone Black PIL Test**  
### **6.1 Setup**  
- **Target**: BeagleBone Black board.  
- **Test Harness**: Reuse signal editor scenarios (e.g., fault conditions) for consistent testing.  
- **Metrics**:  
  - **Execution Time**: 3 µs per cycle.  
  - **Signal Accuracy**: Matches MIL/SIL results, ensuring consistency across testing stages.  

### **6.2 Results**  
- **Pass Criteria**: All 11 iterations pass with `Error = 0`, indicating identical behavior across MIL, SIL, and PIL tests.  
- **Coverage**: 100% MCDC achieved via hybrid MIL/SIL/PIL testing, ensuring comprehensive validation.  

---

## **Summary**  
Testing BMS-generated code involves:  
1. **SIL Testing**: Validate code on a host PC against Simulink results to ensure functional correctness.  
2. **PIL Testing**: Measure performance on target hardware (e.g., BeagleBone) to validate real-time behavior.  
3. **Equivalence Checks**: Use the **Simulink Test Manager** for automated comparisons between MIL, SIL, and PIL results.  

For advanced workflows, leverage **Simulink Coverage** and **Embedded Coder** to meet safety-critical standards like ISO 26262 ASIL-D, ensuring robust and compliant BMS software.