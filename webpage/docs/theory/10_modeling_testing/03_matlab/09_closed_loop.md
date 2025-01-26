# Closed-Loop Testing

## **1. Introduction to Closed-Loop Testing**

Closed-loop testing is a comprehensive validation approach that ensures the entire Battery Management System (BMS) Electronic Control Unit (ECU) operates correctly within its intended environment. By integrating the BMS ECU with a plant model—comprising components such as the battery pack, charger, and load—closed-loop testing simulates real-world interactions and scenarios. This method is pivotal for verifying system-level functionality, safety, and performance, particularly in safety-critical applications like electric vehicles and energy storage systems.

### **Key Objectives of Closed-Loop Testing**

1. **Test Interactions**:
   - **Function**: Validates the dynamic interactions between the BMS controller and physical components (e.g., battery cells, chargers).
   - **Importance**: Ensures that commands from the BMS lead to expected responses from the hardware, maintaining system stability and safety.

2. **Real-World Scenarios**:
   - **Function**: Simulates various operational scenarios such as charging, discharging, and fault conditions.
   - **Importance**: Tests the BMS's ability to handle typical and extreme conditions, ensuring robust performance under diverse circumstances.

3. **Non-Intrusive Monitoring**:
   - **Function**: Utilizes observers to monitor internal signals and states without altering the model's interfaces.
   - **Importance**: Allows for detailed inspection and validation of the system's internal logic and behavior without impacting its operational integrity.

By implementing closed-loop testing, developers can achieve a holistic validation of the BMS, ensuring that both the control algorithms and their interactions with physical components function seamlessly together.

---

## **2. Closed-Loop Test Harness Setup**

Creating an effective closed-loop test harness is fundamental to simulating the interaction between the BMS ECU and the plant model. This setup allows for the execution of comprehensive test scenarios that mimic real-world operations and fault conditions.

### **2.1 Creating the Test Harness**

Setting up a closed-loop test harness involves integrating the BMS ECU with the plant model and defining the necessary inputs and monitoring mechanisms. The following steps outline the process using Simulink Test:

1. **Isolate the Closed-Loop System**:
   - **Action**: Combine the BMS ECU with the plant components, such as the battery pack and pre-charge circuit, to form an integrated closed-loop system.
   - **Procedure**:
     - Open the Simulink model containing the BMS ECU and plant components.
     - Ensure that all connections between the ECU and plant components are correctly configured to enable two-way communication.

2. **Use Simulink Test to Create a Test Harness**:
   - **Action**: Utilize Simulink Test to generate a test harness that encapsulates the closed-loop system.
   - **Procedure**:
     - Navigate to *Apps > Simulink Test > Create Test Harness*.
     - Select the appropriate subsystem (e.g., BMS ECU and plant model) to include in the harness.
     - Configure the harness settings, specifying inputs and outputs as needed.
   - **Outcome**: A dedicated test harness that facilitates the injection of test inputs and the monitoring of system outputs without affecting the main model.

3. **Define Test Inputs**:
   - **Action**: Specify the inputs that drive the test scenarios, including state transitions and environmental conditions.
   - **Tools**:
     - **Test Sequence Block**: Defines temporal sequences of events and state transitions.
     - **Signal Builder**: Provides pre-recorded test scenarios for consistent and repeatable testing.

   **Test Sequence Block Example**:
   
   ```plaintext
   Step 1: Set State = STANDBY for 10 sec.
   Step 2: Transition to DRIVING when SOC > 30%.
   Step 3: Trigger FAULT if cell_temp > 45°C.
   ```
   
   **Signal Builder Example**:
   
   - **Purpose**: Injects complex and realistic drive cycles to test the BMS under various load conditions.
   - **Procedure**:
     - Open the Signal Builder block within the test harness.
     - Import or create drive cycle data representing aggressive acceleration, steady-state driving, and regenerative braking.
   
   **Code Snippet: Configuring Test Inputs Using Signal Builder**
   
   ```matlab
   % MATLAB Code Snippet: Configuring Test Inputs with Signal Builder
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Define test sequence steps
   testSequence = [
       struct('time', 0, 'State', 'STANDBY'),
       struct('time', 10, 'State', 'DRIVING', 'SOC', 31),
       struct('time', 20, 'State', 'FAULT', 'cell_temp', 46)
   ];
   
   % Configure Test Sequence Block
   set_param([testHarness, '/Test_Sequence'], 'Sequence', testSequence);
   
   disp('Test Sequence configured for closed-loop testing.');
   ```
   
   *Figure 1: Creating a Test Harness in Simulink Test*

### **2.2 Visualizing Results**

Effective visualization of test results is crucial for interpreting the behavior of the closed-loop system. Simulink provides various dashboard blocks that offer real-time monitoring and feedback during simulation runs.

1. **Add Dashboard Blocks**:
   - **Function**: Display key signals and states in an intuitive and interactive manner.
   - **Components**:
     - **Gauges**: Visual indicators for real-time values (e.g., cell temperatures, State of Charge (SOC)).
     - **Lamps**: Status indicators for critical flags (e.g., fault conditions).
     - **Displays**: Numerical displays for precise monitoring of signal values.

2. **Monitor Key Signals**:
   - **Examples**:
     - **Cell Temperatures**: Gauge displaying the temperature of individual battery cells.
     - **SOC**: Gauge indicating the current State of Charge of the battery pack.
     - **Pack Current/Voltage**: Gauges showing the overall current and voltage levels.
     - **Fault Indicators**: Lamps indicating the presence of over-temperature or over-voltage conditions.

   **Dashboard Configuration Example**:
   
   ```matlab
   % MATLAB Code Snippet: Configuring Dashboard Blocks
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Add a Gauge for SOC
   add_block('simulink/Commonly Used Blocks/Gauge', [testHarness, '/SOC_Gauge']);
   set_param([testHarness, '/SOC_Gauge'], 'GaugeFormat', 'Percentage', ...
             'Position', [100, 100, 150, 150]);
   
   % Add a Lamp for Fault Indicator
   add_block('simulink/Commonly Used Blocks/Lamp', [testHarness, '/Fault_Lamp']);
   set_param([testHarness, '/Fault_Lamp'], 'Position', [200, 100, 250, 150]);
   
   disp('Dashboard blocks added for result visualization.');
   ```
   
   *Figure 2: Adding Dashboard Blocks for Monitoring*

By incorporating dashboard blocks, developers can gain real-time insights into the system's performance and promptly identify any anomalies or deviations from expected behavior during testing.

---

## **3. Observing Internal Signals Without Interface Changes**

A critical aspect of closed-loop testing is the ability to monitor internal signals and states within the BMS ECU without altering the model's external interfaces. This non-intrusive monitoring is achieved using observers, which provide visibility into the system's internal operations.

### **3.1 Using Observers**

Observers allow developers to monitor specific internal signals and states, facilitating detailed analysis and validation without impacting the system's functional interfaces.

1. **Add an Observer**:
   - **Action**: Incorporate an observer block into the test harness to monitor internal signals.
   - **Procedure**:
     - Right-click on the test harness canvas.
     - Select *Observers > Add Observer*.
     - Position the observer block appropriately within the harness.
   
   **Observer Addition Example**:
   
   ```matlab
   % MATLAB Code Snippet: Adding an Observer to the Test Harness
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Add Observer Block
   add_block('simulink/Commonly Used Blocks/Observer', [testHarness, '/Internal_Observer']);
   
   disp('Observer block added to the test harness.');
   ```
   
   *Figure 3: Adding an Observer Block*

2. **Select Internal Signals**:
   - **Action**: Specify which internal signals to monitor using the observer.
   - **Procedure**:
     - Click on the observer’s badge (🔍) to explore the model hierarchy.
     - Navigate through the model to locate desired internal signals.
     - Select signals such as `Charge_Current_Limit` and `Discharge_Current_Limit` within the BMS ECU.
     - Click the Wi-Fi icon (📶) to add the selected signals to the observer.
   
   **Signal Selection Example**:
   
   ```matlab
   % MATLAB Code Snippet: Selecting Internal Signals for Observation
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Define signal paths
   chargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Charge_Current_Limit';
   dischargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Discharge_Current_Limit';
   
   % Add signals to observer
   Simulink.Observer.addSignal(testHarness, 'Internal_Observer', chargeCurrentPath);
   Simulink.Observer.addSignal(testHarness, 'Internal_Observer', dischargeCurrentPath);
   
   disp('Internal signals added to the observer.');
   ```
   
   *Figure 4: Selecting Internal Signals for Observation*

### **3.2 Observer Output**

Observers capture and display the monitored internal signals, allowing developers to analyze system behavior in detail without altering the model's operational interfaces.

1. **Observer Outputs**:
   - **Function**: Provide non-intrusive access to internal signals, enabling comprehensive monitoring and validation.
   - **Example Outputs**:
     - `Charge_Current_Limit`: Tracks the maximum allowable charge current to prevent overcharging.
     - `Discharge_Current_Limit`: Monitors the minimum discharge current to avoid deep discharging.
   
   **Observer Output Configuration Example**:
   
   ```matlab
   % MATLAB Code Snippet: Configuring Observer Outputs
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Retrieve observed signals
   observedSignals = Simulink.Observer.getObservedSignals(testHarness, 'Internal_Observer');
   
   % Display observed signals
   disp('Observer Outputs:');
   disp(observedSignals);
   ```
   
   *Figure 5: Displaying Observer Outputs*

2. **Visualization**:
   - **Function**: Present observed signals in an organized and easily interpretable format within the test harness.
   - **Usage**:
     - Connect observer outputs to display blocks or logging mechanisms for real-time monitoring.
   
   **Observer Output Visualization Example**:
   
   ```matlab
   % MATLAB Code Snippet: Visualizing Observer Outputs
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Connect Charge_Current_Limit to a Display Block
   add_block('simulink/Commonly Used Blocks/Display', [testHarness, '/Charge_Current_Display']);
   add_line(testHarness, 'Internal_Observer/1', 'Charge_Current_Display/1');
   
   % Connect Discharge_Current_Limit to a Display Block
   add_block('simulink/Commonly Used Blocks/Display', [testHarness, '/Discharge_Current_Display']);
   add_line(testHarness, 'Internal_Observer/2', 'Discharge_Current_Display/1');
   
   disp('Observer outputs connected to display blocks for visualization.');
   ```
   
   *Figure 6: Connecting Observer Outputs to Display Blocks*

By utilizing observers, developers gain deep insights into the BMS's internal operations, enabling the identification and rectification of issues that may not be apparent through external monitoring alone.

---

## **4. Defining Test Assessments**

Test assessments are automated checks that validate whether the BMS operates within predefined safety and performance parameters. By integrating assessment blocks into the test harness, developers can enforce and verify critical system constraints.

### **4.1 Test Assessment Blocks**

Test assessment blocks allow for the automation of verification processes by defining logical conditions that system signals must satisfy during testing.

1. **Add Assessment Block**:
   - **Action**: Incorporate a Test Assessment block into the observer to define verification conditions.
   - **Procedure**:
     - From the *Simulink Test Library*, drag a **Test Assessment** block into the observer.
     - Connect the assessment block to the relevant observed signals.
   
   **Adding Assessment Block Example**:
   
   ```matlab
   % MATLAB Code Snippet: Adding a Test Assessment Block
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Add Test Assessment Block
   add_block('simulink/Commonly Used Blocks/Test Assessment', [testHarness, '/Current_Limits_Assessment']);
   
   % Connect assessment block to observer outputs
   add_line(testHarness, 'Internal_Observer/1', 'Current_Limits_Assessment/1');
   add_line(testHarness, 'Internal_Observer/2', 'Current_Limits_Assessment/2');
   
   disp('Test Assessment block added and connected to observer outputs.');
   ```
   
   *Figure 7: Adding a Test Assessment Block*

2. **Define Verify Statements**:
   - **Function**: Specify logical conditions that the monitored signals must satisfy.
   - **Procedure**:
     - Open the Test Assessment block's parameters.
     - Define `verify` statements that represent safety and performance constraints.
   
   **Define Verify Statements Example**:
   
   ```matlab
   % MATLAB Code Snippet: Defining Verify Statements in Test Assessment
   testHarness = 'BMS_ClosedLoop_Test_Harness';
   
   % Define verification conditions
   assessmentBlock = [testHarness, '/Current_Limits_Assessment'];
   
   % Add verify statements
   Simulink.Test.Assessment.addVerify(assessmentBlock, 'Charge_Current_Limit < 50', 'Must stay below 50A');
   Simulink.Test.Assessment.addVerify(assessmentBlock, 'Discharge_Current_Limit > 10', 'Must stay above 10A');
   
   disp('Verify statements defined in Test Assessment block.');
   ```
   
   *Figure 8: Defining Verify Statements in Test Assessment*

### **4.2 Analyzing Results**

Post-test analysis involves reviewing the outcomes of the assessment blocks to determine whether the BMS meets the defined safety and performance criteria.

1. **Diagnostic Viewer**:
   - **Function**: Provides a detailed view of the pass/fail status for each `verify` statement.
   - **Usage**:
     - Open the **Diagnostic Viewer** after test execution to inspect assessment results.
     - Identify any failed assessments and analyze the corresponding conditions.
   
   **Diagnostic Viewer Analysis Example**:
   
   ```matlab
   % MATLAB Code Snippet: Analyzing Assessment Results
   testSuite = 'BMS_ClosedLoop_Test_Suite';
   
   % Run the test suite
   Simulink.Test.TestManager.runTestSuite(testSuite);
   
   % Open Diagnostic Viewer
   Simulink.Test.TestManager.openDiagnosticViewer(testSuite);
   
   disp('Diagnostic Viewer opened for assessment result analysis.');
   ```
   
   *Figure 9: Opening Diagnostic Viewer for Assessment Results*

2. **Failure Diagnostics**:
   - **Function**: Highlights specific instances where `verify` conditions were not met.
   - **Example Failure**:
     ```plaintext
     FAIL: Charge_Current_Limit exceeded 50A at t=12.5s.
     ```
   - **Action**: Investigate the cause of the failure, which may involve reviewing the model logic, adjusting thresholds, or refining control algorithms.
   
   **Failure Diagnostics Example**:
   
   ```matlab
   % MATLAB Code Snippet: Retrieving Failure Diagnostics
   testSuite = 'BMS_ClosedLoop_Test_Suite';
   
   % Retrieve diagnostics
   diagnostics = Simulink.Test.TestManager.getDiagnosticReport(testSuite);
   
   % Display diagnostics
   disp('Diagnostics Report:');
   disp(diagnostics);
   ```
   
   *Figure 10: Retrieving and Displaying Diagnostics Report*

By systematically defining and analyzing test assessments, developers can ensure that the BMS operates within safe and efficient parameters, thereby enhancing system reliability and compliance with safety standards.

---

## **5. Workflow Summary**

A structured workflow is essential for conducting effective closed-loop testing. The following steps outline a comprehensive approach to validating the BMS ECU within a closed-loop environment.

1. **Simulate Closed-Loop System**:
   - **Action**: Execute the test harness with predefined state requests and test scenarios.
   - **Procedure**:
     - Run simulations that transition the system through various states (e.g., STANDBY, DRIVING, FAULT).
     - Ensure that test inputs are accurately defined to reflect real-world operational conditions.

2. **Monitor Signals**:
   - **Action**: Use dashboard blocks and observers to track critical signals and system states in real-time.
   - **Procedure**:
     - Observe key metrics such as cell temperatures, SOC, pack current/voltage, and fault indicators.
     - Utilize observers to monitor internal signals without altering the model's interfaces.

3. **Validate Internal Logic**:
   - **Action**: Employ test assessments and diagnostic tools to verify that internal logic adheres to safety and performance constraints.
   - **Procedure**:
     - Define `verify` statements to enforce conditions like charge/discharge limits.
     - Analyze assessment results using the Diagnostic Viewer to identify and rectify any violations.

4. **Iterate and Refine**:
   - **Action**: Based on test outcomes, refine the model and test scenarios to address identified issues.
   - **Procedure**:
     - Modify control algorithms or adjust thresholds as needed.
     - Re-run tests to validate the effectiveness of the refinements.

5. **Ensure Coverage**:
   - **Action**: Integrate Simulink Coverage to measure and enhance test completeness.
   - **Procedure**:
     - Enable coverage metrics (e.g., MCDC) within the test harness.
     - Analyze coverage reports to identify untested paths and develop additional test cases accordingly.

**Workflow Diagram**:

![Closed-Loop Testing Workflow](#)

*Figure 11: Structured Workflow for Closed-Loop Testing*

By following this workflow, developers can systematically validate the BMS ECU's performance and safety within a simulated operational environment, ensuring readiness for deployment in real-world applications.

---

## **6. Key Tools**

Simulink offers a suite of tools that facilitate the implementation and execution of closed-loop testing. These tools streamline the testing process, enhance monitoring capabilities, and ensure comprehensive validation of the BMS ECU.

| **Tool**                 | **Purpose**                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| **Test Sequence Block**  | Define state transitions and temporal logic for test scenarios.             |
| **Signal Builder**       | Inject pre-recorded test inputs (e.g., drive cycles, fault triggers).       |
| **Observers**            | Monitor internal signals without modifying model interfaces.                |
| **Test Assessment**      | Automate verification of signal conditions (e.g., thresholds, timing).      |
| **Diagnostic Viewer**    | Analyze pass/fail status of assessments and identify failure points.        |
| **Simulation Data Inspector** | Compare and visualize signals across different test runs (MIL, SIL, PIL).  |
| **Simulink Coverage**    | Measure and report test coverage metrics to ensure comprehensive testing.    |

### **6.1 Test Sequence Block**

- **Function**: Defines a sequence of events and state transitions to simulate various operational scenarios.
- **Usage**:
  - Create step-by-step test scenarios that transition the system through different states (e.g., STANDBY → DRIVING → FAULT).
  - Specify temporal conditions and triggers for state transitions.
  
  **Test Sequence Block Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Configuring Test Sequence Block
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define test sequence steps
  testSequence = [
      struct('time', 0, 'State', 'STANDBY'),
      struct('time', 10, 'State', 'DRIVING', 'SOC', 31),
      struct('time', 20, 'State', 'FAULT', 'cell_temp', 46)
  ];
  
  % Set Test Sequence parameters
  set_param([testHarness, '/Test_Sequence'], 'Sequence', testSequence);
  
  disp('Test Sequence configured with state transitions.');
  ```
  
  *Figure 12: Configuring Test Sequence Block*

### **6.2 Signal Builder**

- **Function**: Provides pre-recorded or custom-defined signal scenarios to simulate complex operational conditions.
- **Usage**:
  - Import drive cycle data that reflects realistic and aggressive driving patterns.
  - Define fault scenarios to test the BMS's response to abnormal conditions.
  
  **Signal Builder Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Configuring Signal Builder for Test Inputs
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Load drive cycle data
  load('Aggressive_Drive_Cycle.mat'); % Contains predefined signal data
  
  % Set Signal Builder parameters
  set_param([testHarness, '/Signal_Builder'], 'Data', driveCycleData);
  
  disp('Signal Builder configured with aggressive drive cycle data.');
  ```
  
  *Figure 13: Configuring Signal Builder with Drive Cycle Data*

### **6.3 Observers**

- **Function**: Monitor and log internal signals without altering the model's external interfaces.
- **Usage**:
  - Add observers to track critical internal variables like `Charge_Current_Limit` and `Discharge_Current_Limit`.
  - Configure observers to output data for real-time monitoring and post-test analysis.
  
  **Observer Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Configuring Observers
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define signal paths
  chargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Charge_Current_Limit';
  dischargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Discharge_Current_Limit';
  
  % Add signals to observer
  Simulink.Observer.addSignal(testHarness, 'Internal_Observer', chargeCurrentPath);
  Simulink.Observer.addSignal(testHarness, 'Internal_Observer', dischargeCurrentPath);
  
  disp('Internal signals added to observer for monitoring.');
  ```
  
  *Figure 14: Configuring Observers for Internal Signal Monitoring*

### **6.4 Test Assessment**

- **Function**: Automates the verification of signal conditions to enforce safety and performance constraints.
- **Usage**:
  - Define logical `verify` statements to ensure signals remain within specified limits.
  - Automatically evaluate these conditions during test execution and report pass/fail statuses.
  
  **Test Assessment Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Defining Test Assessments
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define assessment block
  assessmentBlock = [testHarness, '/Current_Limits_Assessment'];
  
  % Add verify statements
  Simulink.Test.Assessment.addVerify(assessmentBlock, 'Charge_Current_Limit < 50', 'Must stay below 50A');
  Simulink.Test.Assessment.addVerify(assessmentBlock, 'Discharge_Current_Limit > 10', 'Must stay above 10A');
  
  disp('Test Assessments defined for current limits.');
  ```
  
  *Figure 15: Defining Test Assessments for Current Limits*

### **6.5 Diagnostic Viewer**

- **Function**: Analyzes and displays the outcomes of test assessments, highlighting any failures or violations.
- **Usage**:
  - Open the Diagnostic Viewer after test execution to review assessment results.
  - Investigate specific failures to identify and rectify underlying issues.
  
  **Diagnostic Viewer Usage Example**:
  
  ```matlab
  % MATLAB Code Snippet: Opening Diagnostic Viewer
  testSuite = 'BMS_ClosedLoop_Test_Suite';
  
  % Run the test suite
  Simulink.Test.TestManager.runTestSuite(testSuite);
  
  % Open Diagnostic Viewer
  Simulink.Test.TestManager.openDiagnosticViewer(testSuite);
  
  disp('Diagnostic Viewer opened for result analysis.');
  ```
  
  *Figure 16: Opening Diagnostic Viewer for Test Analysis*

### **6.6 Simulation Data Inspector**

- **Function**: Facilitates the comparison and visualization of simulation data across different test runs (e.g., MIL, SIL, PIL).
- **Usage**:
  - Load and overlay signals from multiple test runs to detect discrepancies.
  - Analyze signal trajectories and timing to ensure consistency and correctness.
  
  **Simulation Data Inspector Example**:
  
  ```matlab
  % MATLAB Code Snippet: Using Simulation Data Inspector for Signal Comparison
  % Load MIL data
  milData = sdiCollection('BMS_MIL_Data.sdi');
  
  % Load SIL data
  silData = sdiCollection('BMS_SIL_Data.sdi');
  
  % Load PIL data
  pilData = sdiCollection('BMS_PIL_Data.sdi');
  
  % Open Simulation Data Inspector
  Simulink.sdi.view;
  
  % Compare specific signals across MIL, SIL, and PIL
  Simulink.sdi.compare(milData, silData, pilData, 'Error');
  
  disp('Signal comparison completed in Simulation Data Inspector.');
  ```
  
  *Figure 17: Comparing Signals in Simulation Data Inspector*

### **6.7 Simulink Coverage**

- **Function**: Measures and reports the extent to which the model has been exercised by the test cases.
- **Usage**:
  - Enable coverage metrics such as Decision Coverage, Condition Coverage, and MCDC.
  - Analyze coverage reports to identify untested paths and enhance test suites accordingly.
  
  **Simulink Coverage Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Enabling Simulink Coverage
  testSuite = 'BMS_ClosedLoop_Test_Suite';
  
  % Select the test suite
  Simulink.Test.TestManager.selectTestSuite(testSuite);
  
  % Enable coverage metrics
  Simulink.Test.TestManager.setCoverageSettings(testSuite, ...
      'Decision', true, 'Condition', true, 'MCDC', true);
  
  disp(['Coverage metrics enabled for test suite: ' testSuite]);
  
  % Run the test suite with coverage enabled
  Simulink.Test.TestManager.runTestSuite(testSuite);
  
  % Retrieve and display coverage results
  coverageResults = Simulink.Test.TestManager.getCoverage(testSuite);
  disp('Coverage Results:');
  disp(coverageResults);
  ```
  
  *Figure 18: Enabling and Running Simulink Coverage*

By leveraging these tools, developers can create a robust closed-loop testing environment that ensures comprehensive validation of the BMS ECU within its operational context.

---

## **7. Example: Validating Current Limits**

To illustrate the application of closed-loop testing, consider an example focused on validating the BMS's charge and discharge current limits. This example demonstrates how to set up test scenarios, monitor internal signals, define assessments, and analyze results to ensure that the BMS operates within safe and efficient parameters.

### **7.1 Test Scenario**

**Objective**: Ensure that the BMS maintains charge and discharge currents within specified safe limits during driving operations.

**Steps**:

1. **Inject a Drive Cycle with Aggressive Acceleration**:
   - **Action**: Use the Test Sequence Block to define a drive cycle that includes rapid acceleration phases to test the BMS's ability to handle high current demands.
   - **Procedure**:
     - Set the system state to `DRIVING` with SOC starting above 30%.
     - Simulate aggressive acceleration events that demand higher charge and discharge currents.
   
2. **Use Observers to Monitor Current Limits**:
   - **Action**: Observe the `Charge_Current_Limit` and `Discharge_Current_Limit` signals to ensure they remain within predefined thresholds.
   - **Procedure**:
     - Connect observers to the relevant internal signals within the BMS ECU.
     - Ensure that these signals are logged and available for assessment.
   
3. **Verify Limits via Test Assessment Blocks**:
   - **Action**: Define and execute `verify` statements to automatically check that current limits are not exceeded during the test run.
   - **Procedure**:
     - Configure Test Assessment blocks with conditions like `Charge_Current_Limit < 50A` and `Discharge_Current_Limit > 10A`.
     - Run the test harness and monitor assessment results for compliance.

**Test Scenario Configuration Example**:

```matlab
% MATLAB Code Snippet: Configuring Test Scenario for Current Limits
testHarness = 'BMS_ClosedLoop_Test_Harness';

% Define aggressive acceleration drive cycle
driveCycleData = [
    struct('time', 0, 'State', 'STANDBY', 'SOC', 35, 'cell_temp', 40),
    struct('time', 10, 'State', 'DRIVING', 'SOC', 35, 'cell_temp', 40),
    struct('time', 20, 'State', 'DRIVING', 'SOC', 34, 'cell_temp', 42),
    struct('time', 30, 'State', 'DRIVING', 'SOC', 33, 'cell_temp', 43),
    struct('time', 40, 'State', 'DRIVING', 'SOC', 32, 'cell_temp', 44),
    struct('time', 50, 'State', 'FAULT', 'SOC', 32, 'cell_temp', 46)
];

% Configure Test Sequence Block
set_param([testHarness, '/Test_Sequence'], 'Sequence', driveCycleData);

% Add Verify Statements for Current Limits
assessmentBlock = [testHarness, '/Current_Limits_Assessment'];
Simulink.Test.Assessment.addVerify(assessmentBlock, 'Charge_Current_Limit < 50', 'Must stay below 50A');
Simulink.Test.Assessment.addVerify(assessmentBlock, 'Discharge_Current_Limit > 10', 'Must stay above 10A');

disp('Test scenario configured for validating current limits.');
```

*Figure 19: Configuring Test Scenario for Current Limits*

### **7.2 Results**

Upon executing the test scenario, the following outcomes are observed:

1. **Pass Criteria**:
   - **Condition**: All `verify` statements are satisfied; `Charge_Current_Limit` remains below 50A and `Discharge_Current_Limit` stays above 10A.
   - **Outcome**: The BMS operates within safe current limits, passing the test case.
   
2. **Fail Criteria**:
   - **Condition**: Any `verify` statement fails (e.g., `Charge_Current_Limit` exceeds 50A).
   - **Outcome**: The test case fails, and the Diagnostic Viewer reports the specific condition violation.
   
**Test Results Overview**:

```plaintext
Test Results:
--------------
- Test Case: Validate Current Limits
  - Charge_Current_Limit: 48A (Pass)
  - Discharge_Current_Limit: 12A (Pass)
  - Overall Result: PASS
```

**Analysis**:

1. **Execution Time**:
   - **Observation**: The system maintained real-time performance, with control loops executing within the required time constraints.
   
2. **Signal Accuracy**:
   - **Observation**: All observed signals matched the expected values, indicating consistent behavior across MIL, SIL, and PIL testing stages.
   
3. **Coverage Achievement**:
   - **Observation**: The test scenario contributed to achieving full MCDC coverage, ensuring that all logical conditions within the current limit checks were thoroughly exercised.

**Example Diagnostic Report**:

```plaintext
Diagnostic Viewer Report
------------------------
Test Case: Validate Current Limits

1. Charge_Current_Limit Verification
   - Condition: Charge_Current_Limit < 50A
   - Actual Value: 48A
   - Status: PASS

2. Discharge_Current_Limit Verification
   - Condition: Discharge_Current_Limit > 10A
   - Actual Value: 12A
   - Status: PASS

Overall Test Result: PASS

Recommendations:
- Continue monitoring current limits during diverse operational scenarios.
- Consider testing additional fault conditions to further validate BMS robustness.
```

*Figure 20: Sample Diagnostic Viewer Report*

This example demonstrates how closed-loop testing effectively validates critical aspects of the BMS, ensuring that it operates safely and efficiently within its intended operational parameters.

---

## **8. Key Tools**

Implementing closed-loop testing effectively requires the integration of several specialized tools within the Simulink environment. These tools facilitate the creation of test harnesses, define test scenarios, monitor internal signals, automate assessments, and analyze results.

### **8.1 Test Sequence Block**

- **Function**: Defines a sequence of state transitions and temporal events to simulate various operational scenarios.
- **Usage**:
  - Create step-by-step test sequences that transition the system through different states (e.g., STANDBY → DRIVING → FAULT).
  - Specify timing and conditions for each state transition to mimic real-world operations.
  
  **Test Sequence Block Example**:
  
  ```matlab
  % MATLAB Code Snippet: Defining a Test Sequence for State Transitions
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define sequence steps
  testSequence = [
      struct('time', 0, 'State', 'STANDBY', 'SOC', 35, 'cell_temp', 40),
      struct('time', 10, 'State', 'DRIVING', 'SOC', 35, 'cell_temp', 40),
      struct('time', 20, 'State', 'DRIVING', 'SOC', 34, 'cell_temp', 42),
      struct('time', 30, 'State', 'DRIVING', 'SOC', 33, 'cell_temp', 43),
      struct('time', 40, 'State', 'DRIVING', 'SOC', 32, 'cell_temp', 44),
      struct('time', 50, 'State', 'FAULT', 'SOC', 32, 'cell_temp', 46)
  ];
  
  % Set Test Sequence parameters
  set_param([testHarness, '/Test_Sequence'], 'Sequence', testSequence);
  
  disp('Test Sequence defined for closed-loop testing.');
  ```
  
  *Figure 21: Defining Test Sequence for State Transitions*

### **8.2 Signal Builder**

- **Function**: Provides a mechanism to inject complex and pre-defined signal scenarios into the test harness.
- **Usage**:
  - Import or create drive cycle data that simulates realistic and aggressive driving patterns.
  - Define fault scenarios that trigger specific BMS responses, ensuring comprehensive testing of fault handling mechanisms.
  
  **Signal Builder Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Configuring Signal Builder with Drive Cycles
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Load predefined drive cycle data
  load('Aggressive_Drive_Cycle.mat'); % Contains driveCycleData structure
  
  % Configure Signal Builder block
  set_param([testHarness, '/Signal_Builder'], 'Data', driveCycleData);
  
  disp('Signal Builder configured with predefined drive cycles.');
  ```
  
  *Figure 22: Configuring Signal Builder with Drive Cycle Data*

### **8.3 Observers**

- **Function**: Monitor and log internal signals and states within the BMS ECU without altering external interfaces.
- **Usage**:
  - Add observers to track critical internal variables like `Charge_Current_Limit` and `Discharge_Current_Limit`.
  - Configure observers to output data for real-time monitoring and post-test analysis.
  
  **Observer Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Adding and Configuring Observers
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define signal paths for observation
  chargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Charge_Current_Limit';
  dischargeCurrentPath = 'BMS_ECU/Current_Power_Limits/Discharge_Current_Limit';
  
  % Add signals to observer
  Simulink.Observer.addSignal(testHarness, 'Internal_Observer', chargeCurrentPath);
  Simulink.Observer.addSignal(testHarness, 'Internal_Observer', dischargeCurrentPath);
  
  disp('Observers configured for monitoring internal current limits.');
  ```
  
  *Figure 23: Configuring Observers for Internal Signal Monitoring*

### **8.4 Test Assessment**

- **Function**: Automates the verification of signal conditions to ensure compliance with safety and performance standards.
- **Usage**:
  - Define logical conditions (`verify` statements) that system signals must satisfy during testing.
  - Automate the evaluation of these conditions to generate pass/fail outcomes.
  
  **Test Assessment Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Defining Verify Statements in Test Assessment
  testHarness = 'BMS_ClosedLoop_Test_Harness';
  
  % Define assessment block
  assessmentBlock = [testHarness, '/Current_Limits_Assessment'];
  
  % Add verify statements
  Simulink.Test.Assessment.addVerify(assessmentBlock, 'Charge_Current_Limit < 50', 'Must stay below 50A');
  Simulink.Test.Assessment.addVerify(assessmentBlock, 'Discharge_Current_Limit > 10', 'Must stay above 10A');
  
  disp('Verify statements defined in Test Assessment block.');
  ```
  
  *Figure 24: Defining Verify Statements in Test Assessment*

### **8.5 Diagnostic Viewer**

- **Function**: Analyzes and displays the outcomes of test assessments, highlighting any failures or violations.
- **Usage**:
  - Open the Diagnostic Viewer after test execution to review assessment results.
  - Investigate specific failures to identify and rectify underlying issues.
  
  **Diagnostic Viewer Usage Example**:
  
  ```matlab
  % MATLAB Code Snippet: Opening Diagnostic Viewer for Test Analysis
  testSuite = 'BMS_ClosedLoop_Test_Suite';
  
  % Run the test suite
  Simulink.Test.TestManager.runTestSuite(testSuite);
  
  % Open Diagnostic Viewer
  Simulink.Test.TestManager.openDiagnosticViewer(testSuite);
  
  disp('Diagnostic Viewer opened for assessment result analysis.');
  ```
  
  *Figure 25: Opening Diagnostic Viewer for Test Analysis*

### **8.6 Simulation Data Inspector**

- **Function**: Facilitates the comparison and visualization of simulation data from multiple test runs (e.g., MIL, SIL, PIL).
- **Usage**:
  - Load and overlay signals from different test runs to detect discrepancies and ensure consistency.
  - Analyze signal trajectories and timing to validate system behavior.
  
  **Simulation Data Inspector Example**:
  
  ```matlab
  % MATLAB Code Snippet: Using Simulation Data Inspector for Signal Comparison
  % Load MIL data
  milData = sdiCollection('BMS_MIL_Data.sdi');
  
  % Load SIL data
  silData = sdiCollection('BMS_SIL_Data.sdi');
  
  % Load PIL data
  pilData = sdiCollection('BMS_PIL_Data.sdi');
  
  % Open Simulation Data Inspector
  Simulink.sdi.view;
  
  % Compare specific signals across MIL, SIL, and PIL
  Simulink.sdi.compare(milData, silData, pilData, 'Error');
  
  disp('Signal comparison completed in Simulation Data Inspector.');
  ```
  
  *Figure 26: Comparing Signals in Simulation Data Inspector*

### **8.7 Simulink Coverage**

- **Function**: Measures and reports the extent to which the model has been exercised by the test cases.
- **Usage**:
  - Enable coverage metrics such as Decision Coverage, Condition Coverage, and Modified Condition/Decision Coverage (MCDC) within the test harness.
  - Analyze coverage reports to identify untested paths and enhance test suites accordingly.
  
  **Simulink Coverage Configuration Example**:
  
  ```matlab
  % MATLAB Code Snippet: Enabling and Running Simulink Coverage
  testSuite = 'BMS_ClosedLoop_Test_Suite';
  
  % Select the test suite
  Simulink.Test.TestManager.selectTestSuite(testSuite);
  
  % Enable coverage metrics
  Simulink.Test.TestManager.setCoverageSettings(testSuite, ...
      'Decision', true, 'Condition', true, 'MCDC', true);
  
  disp(['Coverage metrics enabled for test suite: ' testSuite]);
  
  % Run the test suite with coverage enabled
  Simulink.Test.TestManager.runTestSuite(testSuite);
  
  % Retrieve and display coverage results
  coverageResults = Simulink.Test.TestManager.getCoverage(testSuite);
  disp('Coverage Results:');
  disp(coverageResults);
  ```
  
  *Figure 27: Enabling and Running Simulink Coverage*

By effectively utilizing these tools, developers can create a robust closed-loop testing environment that ensures comprehensive validation of the BMS ECU within its operational context.

---

## **9. Example: Validating Current Limits**

To demonstrate the practical application of closed-loop testing, consider an example focused on validating the BMS's charge and discharge current limits. This example showcases how to set up test scenarios, monitor internal signals, define assessments, and analyze results to ensure that the BMS operates within safe and efficient parameters.

### **9.1 Test Scenario**

**Objective**: Ensure that the BMS maintains charge and discharge currents within specified safe limits during driving operations.

**Steps**:

1. **Inject a Drive Cycle with Aggressive Acceleration**:
   - **Action**: Use the Test Sequence Block to define a drive cycle that includes rapid acceleration phases to test the BMS's ability to handle high current demands.
   - **Procedure**:
     - Set the system state to `DRIVING` with SOC starting above 30%.
     - Simulate aggressive acceleration events that demand higher charge and discharge currents.
   
2. **Use Observers to Monitor Current Limits**:
   - **Action**: Observe the `Charge_Current_Limit` and `Discharge_Current_Limit` signals to ensure they remain within predefined thresholds.
   - **Procedure**:
     - Connect observers to the relevant internal signals within the BMS ECU.
     - Ensure that these signals are logged and available for assessment.
   
3. **Verify Limits via Test Assessment Blocks**:
   - **Action**: Define and execute `verify` statements to automatically check that current limits are not exceeded during the test run.
   - **Procedure**:
     - Configure Test Assessment blocks with conditions like `Charge_Current_Limit < 50A` and `Discharge_Current_Limit > 10A`.
     - Run the test harness and monitor assessment results for compliance.

**Test Scenario Configuration Example**:

```matlab
% MATLAB Code Snippet: Configuring Test Scenario for Current Limits
testHarness = 'BMS_ClosedLoop_Test_Harness';

% Define aggressive acceleration drive cycle
driveCycleData = [
    struct('time', 0, 'State', 'STANDBY', 'SOC', 35, 'cell_temp', 40),
    struct('time', 10, 'State', 'DRIVING', 'SOC', 35, 'cell_temp', 40),
    struct('time', 20, 'State', 'DRIVING', 'SOC', 34, 'cell_temp', 42),
    struct('time', 30, 'State', 'DRIVING', 'SOC', 33, 'cell_temp', 43),
    struct('time', 40, 'State', 'DRIVING', 'SOC', 32, 'cell_temp', 44),
    struct('time', 50, 'State', 'FAULT', 'SOC', 32, 'cell_temp', 46)
];

% Configure Test Sequence Block
set_param([testHarness, '/Test_Sequence'], 'Sequence', driveCycleData);

% Add Verify Statements for Current Limits
assessmentBlock = [testHarness, '/Current_Limits_Assessment'];
Simulink.Test.Assessment.addVerify(assessmentBlock, 'Charge_Current_Limit < 50', 'Must stay below 50A');
Simulink.Test.Assessment.addVerify(assessmentBlock, 'Discharge_Current_Limit > 10', 'Must stay above 10A');

disp('Test scenario configured for validating current limits.');
```

*Figure 28: Configuring Test Scenario for Current Limits*

### **9.2 Results**

Upon executing the test scenario, the following outcomes are observed:

1. **Pass Criteria**:
   - **Condition**: All `verify` statements are satisfied; `Charge_Current_Limit` remains below 50A and `Discharge_Current_Limit` stays above 10A.
   - **Outcome**: The BMS operates within safe current limits, passing the test case.
   
2. **Fail Criteria**:
   - **Condition**: Any `verify` statement fails (e.g., `Charge_Current_Limit` exceeds 50A).
   - **Outcome**: The test case fails, and the Diagnostic Viewer reports the specific condition violation.
   
**Test Results Overview**:

```plaintext
Test Results:
--------------
- Test Case: Validate Current Limits
  - Charge_Current_Limit: 48A (Pass)
  - Discharge_Current_Limit: 12A (Pass)
  - Overall Result: PASS
```

**Analysis**:

1. **Execution Time**:
   - **Observation**: The system maintained real-time performance, with control loops executing within the required time constraints.
   
2. **Signal Accuracy**:
   - **Observation**: All observed signals matched the expected values, indicating consistent behavior across MIL, SIL, and PIL testing stages.
   
3. **Coverage Achievement**:
   - **Observation**: The test scenario contributed to achieving full MCDC coverage, ensuring that all logical conditions within the current limit checks were thoroughly exercised.

**Example Diagnostic Report**:

```plaintext
Diagnostic Viewer Report
------------------------
Test Case: Validate Current Limits

1. Charge_Current_Limit Verification
   - Condition: Charge_Current_Limit < 50A
   - Actual Value: 48A
   - Status: PASS

2. Discharge_Current_Limit Verification
   - Condition: Discharge_Current_Limit > 10A
   - Actual Value: 12A
   - Status: PASS

Overall Test Result: PASS

Recommendations:
- Continue monitoring current limits during diverse operational scenarios.
- Consider testing additional fault conditions to further validate BMS robustness.
```

*Figure 29: Sample Diagnostic Viewer Report*

This example demonstrates how closed-loop testing effectively validates critical aspects of the BMS, ensuring that it operates safely and efficiently within its intended operational parameters.

---

## **9. Benefits of Closed-Loop Testing**

Implementing closed-loop testing for the BMS ECU offers numerous advantages that significantly enhance system validation, reliability, and compliance with safety standards. The key benefits include:

1. **System Validation**:
   - **Description**: Tests the interactions between the BMS controller and plant dynamics, ensuring that all components work harmoniously.
   - **Benefit**: Confirms that the integrated system functions as intended, maintaining stability and performance under various operational conditions.

2. **Non-Intrusive Monitoring**:
   - **Description**: Utilizes observers to monitor internal signals without modifying the model's external interfaces.
   - **Benefit**: Enables detailed inspection and validation of internal logic and behavior without impacting system functionality or introducing potential errors.

3. **Automated Checks**:
   - **Description**: Employs `verify` statements within Test Assessment blocks to enforce safety constraints and performance metrics.
   - **Benefit**: Automates the verification process, reducing manual oversight and ensuring consistent adherence to predefined conditions.

4. **Real-World Scenario Simulation**:
   - **Description**: Simulates real-world operational scenarios such as aggressive driving, charging, discharging, and fault conditions.
   - **Benefit**: Tests the BMS's ability to handle typical and extreme conditions, ensuring robust performance and safety in real-world applications.

5. **Comprehensive Coverage**:
   - **Description**: Integrates Simulink Coverage to measure and ensure that all critical execution paths are tested.
   - **Benefit**: Identifies untested areas within the model, allowing developers to enhance test suites for thorough validation.

6. **Enhanced Traceability**:
   - **Description**: Maintains clear bi-directional links between requirements, model elements, and test cases.
   - **Benefit**: Facilitates audits and compliance checks by ensuring that all requirements are adequately addressed and validated through testing.

7. **Risk Mitigation**:
   - **Description**: Identifies and addresses potential issues early in the development process through rigorous testing.
   - **Benefit**: Reduces the likelihood of system failures post-deployment, enhancing overall reliability and safety.

8. **Efficiency and Automation**:
   - **Description**: Streamlines the testing process by reusing test harnesses and automating verification checks.
   - **Benefit**: Saves time and resources, allowing developers to focus on optimizing system performance and addressing complex issues.

9. **Quality Assurance**:
   - **Description**: Provides a robust framework for validating both functional and performance aspects of the BMS.
   - **Benefit**: Ensures high-quality software delivery, fostering user confidence and system dependability.

**Summary of Benefits**:

- System Validation: Ensures integrated system functionality.
- Non-Intrusive Monitoring: Enables detailed internal signal observation.
- Automated Checks: Enforces safety and performance constraints automatically.
- Real-World Scenario Simulation: Tests system under typical and extreme conditions.
- Comprehensive Coverage: Identifies and addresses untested model areas.
- Enhanced Traceability: Facilitates audits and compliance through clear links.
- Risk Mitigation: Addresses potential issues early in development.
- Efficiency and Automation: Streamlines testing processes, saving time and resources.
- Quality Assurance: Guarantees high-quality, reliable software delivery.

By incorporating closed-loop testing into the BMS development workflow, developers can achieve a high level of confidence in the system's reliability, safety, and performance, ensuring its readiness for deployment in demanding and safety-critical environments.

---

## **10. Summary**

Closed-loop testing is an essential component of the Battery Management System (BMS) development lifecycle, providing a comprehensive framework for validating system-level functionality and safety. By integrating the BMS ECU with a plant model and leveraging specialized Simulink tools, developers can simulate real-world interactions, monitor internal signals, and enforce safety constraints effectively.

### **Key Actions for Effective Closed-Loop Testing**:

1. **Creating a Test Harness**:
   - **Purpose**: Integrate the BMS ECU with plant components to form a closed-loop system.
   - **Implementation**: Use Simulink Test to generate a dedicated test harness that encapsulates the entire system for testing purposes.

2. **Monitoring Signals**:
   - **Purpose**: Track critical system signals and internal states to ensure proper operation.
   - **Implementation**: Utilize dashboard blocks and observers to monitor signals such as cell temperatures, SOC, and current limits in real-time.

3. **Validating Internal Logic**:
   - **Purpose**: Ensure that the BMS's internal logic adheres to safety and performance requirements.
   - **Implementation**: Define and execute `verify` statements within Test Assessment blocks to automatically enforce and validate signal conditions.

4. **Automating Test Assessments**:
   - **Purpose**: Streamline the verification process by automating condition checks.
   - **Implementation**: Use Test Assessment blocks to define logical conditions that system signals must satisfy, automating pass/fail evaluations.

5. **Ensuring Comprehensive Coverage**:
   - **Purpose**: Measure and enhance test completeness to cover all critical execution paths.
   - **Implementation**: Enable and analyze Simulink Coverage metrics (Decision, Condition, MCDC) to identify and address untested model areas.

6. **Iterative Refinement**:
   - **Purpose**: Continuously improve system reliability by addressing identified issues and refining test scenarios.
   - **Implementation**: Modify the model and test harness based on test outcomes, re-running tests to validate enhancements.

7. **Generating and Utilizing Coverage Reports**:
   - **Purpose**: Document test effectiveness and support compliance with safety standards.
   - **Implementation**: Create detailed coverage reports that highlight tested and untested areas, guiding further testing efforts.

8. **Leveraging Diagnostic Tools**:
   - **Purpose**: Analyze test results and diagnose system issues effectively.
   - **Implementation**: Use the Diagnostic Viewer and Simulation Data Inspector to review assessment outcomes and signal comparisons.

9. **Integrating with Certification Processes**:
   - **Purpose**: Ensure that the BMS meets industry safety and reliability standards.
   - **Implementation**: Align closed-loop testing practices with standards like ISO 26262 and DO-178C, facilitating smooth certification and deployment.
