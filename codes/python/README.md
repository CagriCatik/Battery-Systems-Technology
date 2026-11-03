# Battery Toolkit (`battery_toolkit`) 🔋⚡

An industrial-grade, academic-depth Python package for **Battery Systems Technology**: covering cell characterization, series-parallel pack design, equivalent circuit modeling (ECM), non-linear state estimation (EKF/UKF/RLS), BMS supervisory logic, thermal management, and HIL test automation.

---

## Architecture Overview

```
battery_toolkit/
├── core/               # BatteryCell, BatteryPack topology, and engineering units
├── sizing/             # Vehicle longitudinal physics & automated pack sizing optimizer
├── modeling/           # 1-RC/2-RC Thevenin ECM, OCV-SOC mapping, HPPC parameter extraction
├── state_estimation/   # Coulomb Counting, Extended Kalman Filter (EKF), UKF, and RLS
├── bms/                # ASIL-D State Machine, Cell Balancing, ASTM E1049 Rainflow cycle counting
├── thermal/            # 2-node electro-thermal network and BTMS chiller/heater control
└── testing/            # Virtual ASAM XIL test automation and safety assertion framework
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
