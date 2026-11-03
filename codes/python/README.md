# Battery Toolkit (`battery_toolkit`) 🔋⚡

An industrial-grade, academic-depth Python package for **Battery Systems Technology**: covering cell characterization, series-parallel pack design, equivalent circuit modeling (ECM), non-linear state estimation (EKF/UKF/RLS), BMS supervisory logic, thermal management, and HIL test automation.

---

## Architecture Overview

```
battery_toolkit/
├── core/               # BatteryCell, BatteryPack topology, units, and dispersion simulator
├── sizing/             # Vehicle longitudinal physics, geometry calculators, & sizing optimizer
├── modeling/           # 1-RC/2-RC Thevenin ECM, OCV-SOC mapping, HPPC parameter extraction
├── state_estimation/   # Coulomb Counting, Extended Kalman Filter (EKF), UKF, RLS, and ML Regressor
├── bms/                # ASIL-D State Machine, Active/Passive Balancing, ASTM E1049 Rainflow counting
├── thermal/            # 2-node electro-thermal network, BTMS control, and cabin HVAC co-simulation
├── visualization/      # Chemistry radar spider charts, SOC comparison, and thermal profiling
├── testing/            # Virtual ASAM XIL test automation and safety assertion framework
├── data/               # Embedded battery cycle datasets and pretrained ML estimation models
└── cli.py              # Command-line interface (`battery-toolkit`)
```

---

## Installation

Install in editable development mode:

```bash
cd codes/python
pip install -e .
```

Or install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Unit Tests

```bash
pytest
```

---

## Module Overview & Examples

### 1. Battery Pack Sizing
```python
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.sizing.vehicle import VehicleParameters
from battery_toolkit.sizing.optimizer import PackSizingOptimizer

cell = BatteryCell(
    name="LG M50T",
    chemistry=CellChemistry.NMC,
    nominal_voltage=3.63,
    capacity_ah=5.0,
    r0_mohm=25.0,
    mass_g=70.0
)

vehicle = VehicleParameters(
    curb_weight_kg=1850.0,
    drag_coefficient=0.24,
    frontal_area_m2=2.22
)

optimizer = PackSizingOptimizer(cell, vehicle)
pack = optimizer.size_pack(
    desired_energy_kwh=75.0,
    system_voltage=400.0,
    buffer_percentage=15.0
)
print(pack.summary())
```

### 2. Equivalent Circuit Modeling & EKF State Estimation
```python
from battery_toolkit.modeling.ecm import DualPolarizationECM
from battery_toolkit.state_estimation.ekf import ExtendedKalmanFilter

ecm = DualPolarizationECM(r0=0.015, r1=0.010, c1=2500.0, r2=0.020, c2=15000.0)
ekf = ExtendedKalmanFilter(ecm=ecm, nominal_capacity_ah=50.0)

# Online measurement update in 10 ms cyclic task
estimated_soc = ekf.step(current_a=35.0, voltage_v=3.82, dt_s=0.01)
```

### 3. ASTM E1049 Rainflow Cycle Counting
```python
from battery_toolkit.bms.rainflow import RainflowCounter

counter = RainflowCounter()
cycles = counter.count_cycles(soc_time_series)
damage = counter.compute_palmgren_miner_damage(cycles)
```

---

## Command Line Interface (CLI)

The package installs an executable CLI command `battery-toolkit`:

```bash
# Size a pack to 400V / 75kWh:
battery-toolkit size --voltage 400 --energy 75 --cell-cap 5.0 --cell-volt 3.65

# Convert units (e.g., 200 kW to HP):
battery-toolkit convert kw-to-hp 200

# Benchmark thermal management systems:
battery-toolkit benchmark

# Run full simulation pipeline & generate all publication-grade plots, logs, and reports:
battery-toolkit simulate --output-dir outputs
```

---

## Master Simulation Pipeline & Generated Artifacts

Run all 5 engineering simulation domains at once:

```bash
python run_all_simulations.py
```

This generates:

### 1. High-Resolution Plots (`outputs/plots/`):
- `01_pack_sizing_tradeoffs.png`: Speed vs tractive road loads, consumption (Wh/km), range sensitivity, and pack mass distribution.
- `02_ecm_hppc_identification.png`: 40A HPPC pulse, experimental vs 2-RC model voltage, and residual error in mV.
- `03_soc_estimation_benchmark.png`: Ground truth SOC vs Coulomb Counting vs EKF vs UKF vs ML with $\pm 3\sigma$ covariance envelope.
- `04_cell_balancing_dynamics.png`: 16-channel series string equalization under cell dispersion and PCB thermal heat dissipation.
- `05_state_machine_execution.png`: ASIL-D contactor sequencing, precharge capacitor inrush ramp, and emergency HVIL trip.
- `06_electro_thermal_btms_simulation.png`: Fast-charging 150A cell thermal response ($T_{\text{core}}, T_{\text{case}}, T_{\text{cool}}$) and closed-loop BTMS chiller control.
- `07_btms_cooling_technology_benchmark.png`: Comparison of Passive Air, Active Air, Liquid Cooling, and Heat Recovery across maximum temperature, auxiliary energy, and COP.
- `08_battery_chemistry_radar.png`: Multivariate trade-off radar chart for NMC-811, LFP, LTO, and NCA.

### 2. Time-Series Engineering Datasets (`outputs/logs/`):
- `01_sizing_tradeoffs.csv`: Road-load power and driving range across vehicle speeds.
- `02_ecm_hppc_identification.csv`: High-frequency millisecond voltage/current HPPC telemetry.
- `03_soc_benchmark_timeseries.csv`: Complete state estimation logs and tracking error metrics.
- `04_cell_balancing_timeseries.csv`: Multi-channel cell voltage convergence traces.
- `05_state_machine_trace.json`: Chronological event and contactor state transition logs.
- `06_thermal_transients.csv`: Core, casing, and coolant temperatures and heat rate breakdown.
- `07_cooling_technology_benchmark.csv`: Performance metrics for all 4 BTMS topologies.

### 3. Automated Executive Reports (`outputs/reports/`):
- `executive_report.md`: Complete engineering summary with performance KPIs, model parameters, and algorithm RMSE scores.
- `simulation_summary.json`: Structured machine-readable metrics for automated CI/CD validation.


