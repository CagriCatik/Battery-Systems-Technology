# Automated Battery Pack Sizing via Python

Sizing an electric vehicle battery pack is an iterative, coupled optimization problem. Sizing cannot be performed via static single-variable division: the mass of the battery pack constitutes a substantial fraction ($20\% - 30\%$) of the vehicle's total curb weight. Adding cells to increase vehicle range increases overall mass, which increases rolling resistance and inertial acceleration power demand, requiring yet more battery capacity to achieve the target range[^Ehsani2018].

To resolve this circular dependency, automotive engineers utilize **Iterative Mass-Convergence Algorithms** coupled with longitudinal vehicle physics[^Gao2007]. This chapter details the physical formulation, mathematical convergence equations, and automated Python implementation utilizing the `battery_toolkit` package.

---

## 1. Longitudinal Vehicle Dynamics and Energy Demand

The electrical energy $E_{\text{net}}$ required to propel a vehicle over distance $D$ across a defined velocity profile $v(t)$ is determined by the integral of the instantaneous tractive power at the battery pack terminals[^Ehsani2018].

```mermaid
flowchart LR
    subgraph Forces["Longitudinal Resistance Forces"]
        AERO["F_aero = 0.5 * rho * Cd * Af * v^2"]
        ROLL["F_roll = m_total * g * Crr * cos(theta)"]
        GRADE["F_grade = m_total * g * sin(theta)"]
        ACCEL["F_accel = m_total * a(t)"]
    end

    subgraph Power_Train["Drivetrain Coupling"]
        SUM(( + ))
        F_TRACT["Total Wheel Force F_t"]
        P_MECH["Mechanical Power P_mech = F_t * v"]
        ETA_DRIVE["Drivetrain Efficiency eta_drive (~90%)"]
        AUX["Auxiliary Electrical Load P_aux (~800 W)"]
        P_ELEC["Battery Terminal Power P_batt"]
    end

    Forces --> SUM
    SUM --> F_TRACT
    F_TRACT --> P_MECH
    P_MECH --> ETA_DRIVE
    ETA_DRIVE --> P_ELEC
    AUX --> P_ELEC
```

### 1.1 Fundamental Governing Equations

1. **Total Tractive Force ($F_{\text{total}}$)**:

$$
F_{\text{total}}(t) = \frac{1}{2} \rho_{\text{air}} C_d A_f v(t)^2 + m_{\text{total}} g C_{rr} \cos(\theta) + m_{\text{total}} g \sin(\theta) + m_{\text{total}} \frac{dv(t)}{dt}
$$

where:
- $\rho_{\text{air}}$ is ambient air density ($1.225\,\text{kg/m}^3$ at sea level),
- $C_d$ is the aerodynamic drag coefficient ($0.20 - 0.28$ for modern aerodynamic EVs),
- $A_f$ is frontal cross-sectional area ($2.0 - 2.4\,\text{m}^2$),
- $m_{\text{total}} = m_{\text{glider}} + m_{\text{payload}} + m_{\text{pack}}$ is the total vehicle mass ($\text{kg}$),
- $C_{rr}$ is the tire rolling resistance coefficient ($0.008 - 0.010$).

2. **Electrical Power Demand at Battery Terminals ($P_{\text{batt}}$)**:
   - During traction ($F_{\text{total}} \ge 0$):

$$
P_{\text{batt}}(t) = \frac{F_{\text{total}}(t) \cdot v(t)}{\eta_{\text{drivetrain}}} + P_{\text{aux}}
$$

   - During regenerative braking ($F_{\text{total}} < 0$):

$$
P_{\text{batt}}(t) = F_{\text{total}}(t) \cdot v(t) \cdot \eta_{\text{regen}} + P_{\text{aux}}
$$

3. **Steady-State Specific Consumption ($E_{\text{spec}}$ in $\text{Wh/km}$)** at constant speed $v$:

$$
E_{\text{spec}}(v) = \frac{P_{\text{batt}}(v)}{v} \cdot 1000 = \left( \frac{\frac{1}{2} \rho C_d A_f v^2 + m_{\text{total}} g C_{rr}}{\eta_{\text{drivetrain}}} + \frac{P_{\text{aux}}}{v} \right) \cdot 1000
$$

---

## 2. The Iterative Mass-Convergence Algorithm

Because $m_{\text{total}}$ depends directly on the pack mass $m_{\text{pack}}$, which itself depends on $E_{\text{spec}}$, the system must be solved via a fixed-point iteration loop[^Gao2007].

```mermaid
flowchart TD
    START([Start Sizing]) --> INIT_MASS[1. Initialize Vehicle Mass: m_total = m_curb + m_pack_guess]
    INIT_MASS --> CALC_CONS[2. Compute Energy Consumption E_spec Wh/km via Road Load]
    CALC_CONS --> CALC_NET[3. Compute Required Net Energy: E_net = Range * E_spec]
    CALC_NET --> CALC_GROSS[4. Apply Safety Buffers: E_gross = E_net / (1 - Buffer%)]
    CALC_GROSS --> SIZE_TOPO[5. Solve Topology: Ns = ceil(V_sys / V_cell), Np = ceil(Ah / C_cell)]
    SIZE_TOPO --> CALC_PACK_M[6. Compute Actual Pack Mass: m_pack = Ns * Np * m_cell * (1 + Overhead%)]
    CALC_PACK_M --> CONV_CHECK{"7. |m_pack_new - m_pack_old| < 1.0 kg?"}
    CONV_CHECK -- No --> UPDATE_M[Update m_total = m_curb + m_pack_new]
    UPDATE_M --> CALC_CONS
    CONV_CHECK -- Yes --> FINISH([Convergence Reached: Optimal Pack Output])
```

---

## 3. Production Python Sizing Implementation

Using the modular `battery_toolkit` Python package, the complete sizing pipeline is executed concisely with full mathematical convergence:

```python
"""
Automated Battery Pack Sizing Pipeline
Target: 500 km WLTP Highway Cruising Range at 105 km/h
"""

from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.sizing.vehicle import VehicleParameters
from battery_toolkit.sizing.optimizer import PackSizingOptimizer, SizingRequirements

# 1. Select Cell Specifications from Datasheet
cell = BatteryCell(
    name="Automotive NMC-811 21700",
    chemistry=CellChemistry.NMC,
    nominal_voltage=3.65,        # V
    capacity_ah=5.0,             # Ah
    r0_mohm=22.0,                # mOhm
    mass_g=69.0,                 # g
)

# 2. Define Vehicle Glider & Aerodynamic Parameters
vehicle = VehicleParameters(
    curb_weight_kg=1850.0,       # Mass without pack
    drag_coefficient=0.23,       # Cd
    frontal_area_m2=2.22,        # Af
    rolling_resistance_coeff=0.009, # Crr
    drivetrain_efficiency=0.90,  # 90% combined motor + inverter efficiency
    auxiliary_load_kw=0.75,      # 750 W HVAC + electronics
)

# 3. Specify Design Requirements
requirements = SizingRequirements(
    target_range_km=500.0,
    target_system_voltage_v=400.0,
    buffer_percentage=12.0,      # 12% total buffer (5% top, 7% bottom reserve)
    avg_speed_kmh=105.0,         # Constant highway speed
)

# 4. Execute Iterative Convergence Optimization
optimizer = PackSizingOptimizer(cell=cell, vehicle=vehicle)
results = optimizer.size_for_range(requirements)

# 5. Output Sizing Architecture
pack = results["pack_object"]
print(f"Vehicle Specific Consumption: {results['consumption_wh_per_km']} Wh/km")
print(f"Gross Pack Energy:            {pack.nominal_energy_kwh:.2f} kWh")
print(f"Pack Architecture Topology:   {pack.topology}")
print(f"Total Series Cells (Ns):      {pack.topology.num_series}")
print(f"Total Parallel Strings (Np):  {pack.topology.num_parallel}")
print(f"Total Cell Count:             {pack.total_cells}")
print(f"Total Pack Mass:              {pack.total_pack_mass_kg:.1f} kg")
print(f"Pack Gravimetric Density:     {pack.gravimetric_energy_density_wh_per_kg:.1f} Wh/kg")
```

---

## 4. Sensitivity Analysis: Impact of Vehicle Aerodynamics vs. Pack Mass

To guide engineering trade-offs, sensitivity analysis quantifies the relative impact of aerodynamic drag reduction vs. cell gravimetric density improvements on total pack weight:

```mermaid
xychart-beta
    title "Vehicle Energy Consumption (Wh/km) vs. Highway Speed"
    x-axis [60, 80, 100, 120, 140]
    y-axis "Consumption (Wh/km)" 80 --> 260
    line [95, 115, 142, 185, 245]
```

### 4.1 Engineering Takeaways
- **Aerodynamic Dominance at High Speed**: Because aerodynamic drag scales with the square of velocity ($F_{\text{aero}} \propto v^2$) and power with the cube ($P_{\text{aero}} \propto v^3$), reducing drag coefficient $C_d$ from $0.28$ to $0.23$ saves $\approx 14\,\text{kWh}$ of required battery energy for a $500\,\text{km}$ range, eliminating over $80\,\text{kg}$ of pack mass.
- **Mass Overhead Ratio**: Pack enclosures, thermal interface gap pads, and liquid cold plates add $20\% - 30\%$ non-cell structural mass. High cell-to-pack (CTP) structural integration directly reduces the iterative mass feedback penalty.

For complete source code and unit tests, see:
- [codes/python/src/battery_toolkit/sizing/vehicle.py](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/sizing/vehicle.py)
- [codes/python/src/battery_toolkit/sizing/optimizer.py](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/src/battery_toolkit/sizing/optimizer.py)
- [codes/python/examples/01_pack_sizing_pipeline.py](file:///Users/cc/Desktop/Battery-Systems-Technology/codes/python/examples/01_pack_sizing_pipeline.py)

---

## 5. References

[^Ehsani2018]: M. Ehsani, Y. Gao, S. Longo, and K. M. Ebrahimi, *Modern Electric, Hybrid Electric, and Fuel Cell Vehicles*, 3rd ed., CRC Press, 2018.
[^Gao2007]: Y. Gao, M. Ehsani, and J. M. Miller, "Hybrid Electric Vehicle System Architecture and Component Sizing," *IEEE Transactions on Vehicular Technology*, vol. 56, no. 5, pp. 2392–2399, 2007. [DOI: 10.1109/TVT.2007.896977](https://doi.org/10.1109/TVT.2007.896977)
