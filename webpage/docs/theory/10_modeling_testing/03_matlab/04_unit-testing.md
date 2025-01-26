# Unit Testing

## **1. Introduction to Unit Testing**  
Unit testing is a critical step in validating individual components of a Battery Management System (BMS), such as the state machine or balancing logic, to ensure they meet specified requirements. Key objectives of unit testing include:  
- **Isolate Components**: Test specific logic without external dependencies to ensure accurate results.  
- **Inject Test Inputs**: Simulate real-world scenarios (e.g., voltage spikes, temperature faults) to evaluate component behavior.  
- **Verify Outputs**: Validate responses against expected behavior to confirm compliance with design requirements.  

---

## **2. Creating a Test Harness in Simulink**  
### **2.1 Test Harness Setup**  
1. **Navigate to Simulink Test**:  
   - Open the BMS model (e.g., the state machine component).  
   - Go to the *Simulink Toolstrip > Apps > Simulink Test*.  
2. **Generate Test Harness**:  
   - Click *Add Test Harness*.  
   - Name the harness (e.g., `StateMachine_Test`) and specify its storage location.  
3. **Configure Inputs/Outputs**:  
   - **Input Sources**: Use Signal Builder, Signal Editor, or workspace variables to define test inputs.  
   - **Output Sinks**: Log results using scopes, MATLAB workspace, or files for analysis.  

### **2.2 Example: Signal Builder for Inputs**  
- **Define Test Scenarios**:  
  - Use Signal Builder to create custom input waveforms (e.g., step changes in voltage or temperature).  
  - Example: Inject `cell_voltage = 6V` to simulate a fault condition.  
- **Output Configuration**:  
  - Log results to the workspace using `To Workspace` blocks or visualize outputs in real time using scopes.  

---

## **3. Manual Testing with Dashboards**  
### **3.1 Dashboard Block Integration**  
1. **Add Dashboard Components**:  
   - Insert interactive components such as switches, knobs, and gauges into the test harness.  
   - Example: Use a **Slider** to dynamically adjust cell voltage during simulation.  
2. **Run Interactive Simulations**:  
   - Start the simulation and manually adjust inputs (e.g., set `cell_voltage = 6V`).  
   - Observe outputs in real time (e.g., fault activation) to validate component behavior.  

### **3.2 Saving Simulation Data**  
- **Export to Workspace**:  
  - After stopping the simulation, access logged data in the MATLAB workspace.  
  - Save the dataset for future use (e.g., `fault_scenario.mat`).  
  ```matlab  
  save('fault_scenario.mat', 'simulation_output');  
  ```  

---

## **4. Automating Tests with Recorded Data**  
### **4.1 Replay Test Scenarios**  
1. **Use Signal Editor**:  
   - Replace Signal Builder with **Signal Editor** in the test harness.  
   - Load saved datasets (e.g., `fault_scenario.mat`) to replay specific test scenarios.  
2. **Modify Scenarios**:  
   - Duplicate or edit datasets to create new test cases (e.g., adjust voltage thresholds or temperature profiles).  

### **4.2 Batch Execution**  
- **Automate Simulations**:  
  - Use the `sim` function in MATLAB to run multiple test scenarios programmatically.  
  ```matlab  
  testScenarios = {'fault_scenario.mat', 'normal_operation.mat'};  
  for i = 1:length(testScenarios)  
      load(testScenarios{i});  
      sim('StateMachine_Test');  
  end  
  ```  

---

## **5. Key Tools and Workflow**  
### **5.1 Simulink Test Features**  
- **Test Harness Navigation**:  
  - Use badges (🔗) to toggle between the component under test and its harness.  
- **Input/Output Blocks**:  
  - **Signal Builder**: Design custom input waveforms for specific test cases.  
  - **Signal Editor**: Replay pre-recorded datasets for regression testing.  
  - **Scope**: Visualize outputs in real time during simulation.  

### **5.2 Workflow Summary**  
1. **Isolate Component**: Select the BMS logic (e.g., state machine) to be tested.  
2. **Create Harness**: Define inputs and outputs using Simulink Test.  
3. **Test Manually**: Use dashboards for interactive validation of component behavior.  
4. **Automate**: Reuse saved datasets for regression testing and batch execution.  

---

## **6. Benefits of Unit Testing in Simulink**  
- **Early Fault Detection**: Identify issues such as over-voltage or over-temperature conditions before hardware deployment.  
- **Reproducibility**: Replay edge cases (e.g., 40°C ambient temperature, 30% initial SOC) to ensure consistent behavior.  
- **Certification Readiness**: Align with standards like ISO 26262 by documenting test coverage and ensuring compliance.  

---

## **Summary**  
Unit testing BMS software in Simulink involves:  
- **Creating Test Harnesses**: Isolate components (e.g., state machines) for focused testing.  
- **Injecting Inputs**: Use dashboards or pre-recorded datasets to simulate real-world scenarios.  
- **Automating Validation**: Leverage Signal Editor and batch scripts for efficient regression testing.  
