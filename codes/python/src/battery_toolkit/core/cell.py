from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CellChemistry(str, Enum):
    NMC = "Lithium Nickel Manganese Cobalt Oxide (NMC)"
    LFP = "Lithium Iron Phosphate (LiFePO4)"
    NCA = "Lithium Nickel Cobalt Aluminum Oxide (NCA)"
    LTO = "Lithium Titanate Oxide (LTO)"
    SOLID_STATE = "All-Solid-State Lithium (ASSB)"


@dataclass
class BatteryCell:
    """
    Physical and electrical specification model of an individual battery cell.
    """
    name: str
    chemistry: CellChemistry
    nominal_voltage: float       # Volts (V)
    capacity_ah: float           # Rated capacity in Ampere-hours (Ah)
    v_max: float = 4.20          # Maximum charge voltage cutoff (V)
    v_min: float = 2.80          # Minimum discharge voltage cutoff (V)
    r0_mohm: float = 20.0        # Ohmic internal resistance (milli-Ohms)
    mass_g: float = 70.0         # Individual cell mass (grams)
    length_mm: float = 65.0      # Length or height (mm)
    diameter_mm: float = 21.0    # Diameter for cylindrical cell (mm)
    c_rate_continuous: float = 2.0  # Max continuous discharge C-rate
    c_rate_peak: float = 5.0        # Max peak 10s pulse discharge C-rate
    c_th_joules_per_k: float = 65.0 # Thermal mass / heat capacity (J/K)
    r_th_k_per_w: float = 12.0      # Thermal resistance casing-to-ambient (K/W)

    @property
    def nominal_energy_wh(self) -> float:
        """Nominal energy of the cell in Watt-hours (Wh)."""
        return self.nominal_voltage * self.capacity_ah

    @property
    def gravimetric_energy_density_wh_per_kg(self) -> float:
        """Gravimetric energy density in Wh/kg."""
        return (self.nominal_energy_wh / self.mass_g) * 1000.0

    @property
    def volume_liters(self) -> float:
        """Approximated cylindrical volume in Liters."""
        import math
        radius_m = (self.diameter_mm / 2.0) / 1000.0
        length_m = self.length_mm / 1000.0
        return (math.pi * (radius_m ** 2) * length_m) * 1000.0

    @property
    def volumetric_energy_density_wh_per_l(self) -> float:
        """Volumetric energy density in Wh/L."""
        return self.nominal_energy_wh / self.volume_liters

    @property
    def max_continuous_current_a(self) -> float:
        """Maximum continuous discharge current in Amperes."""
        return self.capacity_ah * self.c_rate_continuous

