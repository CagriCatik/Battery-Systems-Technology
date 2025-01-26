# Unit Testing 

## **1. Introduction to Unit Testing**  
Unit testing validates individual components (e.g., BMS state machine, balancing logic) to ensure they meet requirements. Key objectives include:  
- **Isolate Components**: Test specific logic without external dependencies.  
- **Inject Test Inputs**: Simulate scenarios (e.g., voltage spikes, temperature faults).  
- **Verify Outputs**: Validate responses against expected behavior.  

---

## **2. Creating a Test Harness in Simulink**  
### **2.1 Test Harness Setup**  
1. **Navigate to Simulink Test**:  
   - Open the BMS model (e.g., state machine component).  
   - Go to the *Simulink Toolstrip > Apps > Simulink Test*.  
2. **Generate Test Harness**:  
   - Click *Add Test Harness*.  
   - Name the harness (e.g., `StateMachine_Test`) and specify its storage location.  
3. **Configure Inputs/Outputs**:  
   - **Input Sources**: Signal Builder, Signal Editor, or workspace variables.  
   - **Output Sinks**: Scopes, MATLAB workspace, or files.  

### **2.2 Example: Signal Builder for Inputs**  
- **Define Test Scenarios**:  
  - Use Signal Builder to create input waveforms (e.g., step changes in voltage, temperature).  
  - Example: Inject `cell_voltage = 6V` to trigger a fault.  
- **Output Configuration**:  
  - Log results to the workspace using `To Workspace` blocks or visualize via scopes.  

---

## **3. Manual Testing with Dashboards**  
### **3.1 Dashboard Block Integration**  
1. **Add Dashboard Components**:  
   - Insert switches, knobs, and gauges into the test harness.  
   - Example: Use a **Slider** to dynamically adjust cell voltage during simulation.  
2. **Run Interactive Simulations**:  
   - Start simulation and manually adjust inputs (e.g., set `cell_voltage = 6V`).  
   - Observe outputs in real time (e.g., fault activation).  

### **3.2 Saving Simulation Data**  
- **Export to Workspace**:  
  - After stopping the simulation, access logged data in the MATLAB workspace.  
  - Save as a dataset (e.g., `fault_scenario.mat`).  
  ```matlab  
  save('fault_scenario.mat', 'simulation_output');  
  ```  

---

## **4. Automating Tests with Recorded Data**  
### **4.1 Replay Test Scenarios**  
1. **Use Signal Editor**:  
   - Replace Signal Builder with **Signal Editor** in the test harness.  
   - Load saved datasets (e.g., `fault_scenario.mat`).  
2. **Modify Scenarios**:  
   - Duplicate or edit datasets to create new test cases (e.g., adjust voltage thresholds).  

### **4.2 Batch Execution**  
- **Automate Simulations**:  
  - Use `sim` function in MATLAB to run multiple test scenarios programmatically.  
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
  - **Signal Builder**: Design custom input waveforms.  
  - **Signal Editor**: Replay pre-recorded datasets.  
  - **Scope**: Visualize outputs in real time.  

### **5.2 Workflow Summary**  
1. **Isolate Component**: Select the BMS logic (e.g., state machine).  
2. **Create Harness**: Define inputs/outputs via Simulink Test.  
3. **Test Manually**: Use dashboards for interactive validation.  
4. **Automate**: Reuse saved datasets for regression testing.  

---

## **6. Benefits of Unit Testing in Simulink**  
- **Early Fault Detection**: Identify issues like over-voltage conditions before hardware deployment.  
- **Reproducibility**: Replay edge cases (e.g., 40°C ambient, 30% SOC).  
- **Certification Readiness**: Align with ISO 26262 by documenting test coverage.  

---

## **Summary**  
Unit testing BMS software in Simulink involves:  
- Creating test harnesses to isolate components (e.g., state machines).  
- Injecting inputs via dashboards or pre-recorded datasets.  
- Automating validation with Signal Editor and batch scripts.  

For advanced workflows, leverage **Simulink Test Manager** to generate compliance reports and trace tests to requirements.