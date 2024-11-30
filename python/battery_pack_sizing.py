# Constants
nominal_voltage_pack = 48  # Voltage of the pack in Volts
sec = 0.5  # Specific Energy Consumption in kWh/km
daily_distance = 30  # Distance traveled daily in km
max_range = 50  # Maximum range per full charge in km
soh_after_5_years = 0.75  # State of Health after 5 years
cell_nominal_voltage = 3.7  # Voltage of a single cell in Volts
cell_capacity_ah = 3.5  # Capacity of a single cell in Ah
energy_density_wh_per_kg = 250  # Energy density in Wh/kg
energy_density_wh_per_l = 700  # Energy density in Wh/L

# Calculations
# Energy requirement
daily_energy_kwh = sec * daily_distance
max_energy_kwh = sec * max_range

# Initial capacity required to meet the range requirement after 5 years
initial_capacity_kwh = max_energy_kwh / soh_after_5_years

# Total pack capacity in Ah
total_capacity_ah = (initial_capacity_kwh * 1000) / nominal_voltage_pack

# Number of cells in series
cells_in_series = round(nominal_voltage_pack / cell_nominal_voltage)

# Number of cells in parallel
cells_in_parallel = round(total_capacity_ah / cell_capacity_ah)

# Total number of cells
total_cells = cells_in_series * cells_in_parallel

# Weight and volume calculations
total_energy_wh = initial_capacity_kwh * 1000  # Convert kWh to Wh
total_weight_kg = total_energy_wh / energy_density_wh_per_kg
total_volume_l = total_energy_wh / energy_density_wh_per_l

# Results
results = {
    "Daily Energy Requirement (kWh)": daily_energy_kwh,
    "Maximum Energy Requirement (kWh)": max_energy_kwh,
    "Initial Capacity (kWh)": initial_capacity_kwh,
    "Total Capacity (Ah)": total_capacity_ah,
    "Cells in Series": cells_in_series,
    "Cells in Parallel": cells_in_parallel,
    "Total Cells": total_cells,
    "Battery Weight (kg)": total_weight_kg,
    "Battery Volume (L)": total_volume_l,
}

import pandas as pd

# Display results
results_df = pd.DataFrame.from_dict(results, orient="index", columns=["Value"])
print(results_df)
