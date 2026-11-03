from dataclasses import dataclass
from typing import Dict, Any
from battery_toolkit.core.cell import BatteryCell


@dataclass
class PackTopology:
    """Topology descriptor defining series and parallel connections."""
    num_series: int      # N_s
    num_parallel: int    # N_p

    @property
    def total_cells(self) -> int:
        return self.num_series * self.num_parallel

    def __str__(self) -> str:
        return f"{self.num_series}S{self.num_parallel}P"


class BatteryPack:
    """
    Representation of an integrated battery pack composed of series-parallel cell strings,
    interconnect resistance, and structural overhead.
    """
    def __init__(
        self,
        cell: BatteryCell,
        topology: PackTopology,
        busbar_resistance_mohm: float = 0.5,
        structural_mass_overhead_ratio: float = 0.25, # Enclosure, cooling, BMS adds 25% mass
    ):
        self.cell = cell
        self.topology = topology
        self.busbar_resistance_mohm = busbar_resistance_mohm
        self.structural_mass_overhead_ratio = structural_mass_overhead_ratio

    @property
    def total_cells(self) -> int:
        return self.topology.total_cells

    @property
    def nominal_voltage_v(self) -> float:
        """Nominal pack terminal voltage: V_pack = N_s * V_cell."""
        return self.topology.num_series * self.cell.nominal_voltage

    @property
    def v_max_v(self) -> float:
        """Pack maximum voltage cutoff."""
        return self.topology.num_series * self.cell.v_max

    @property
    def v_min_v(self) -> float:
        """Pack minimum voltage cutoff."""
        return self.topology.num_series * self.cell.v_min

    @property
    def capacity_ah(self) -> float:
        """Total pack capacity: C_pack = N_p * C_cell."""
        return self.topology.num_parallel * self.cell.capacity_ah

    @property
    def nominal_energy_kwh(self) -> float:
        """Total nominal pack energy in kWh."""
        return (self.nominal_voltage_v * self.capacity_ah) / 1000.0

    @property
    def cell_mass_kg(self) -> float:
        """Total mass of all individual cells in kg."""
        return (self.total_cells * self.cell.mass_g) / 1000.0

    @property
    def total_pack_mass_kg(self) -> float:
        """Total pack mass including enclosure, busbars, and BTMS cold plates."""
        return self.cell_mass_kg * (1.0 + self.structural_mass_overhead_ratio)

    @property
    def total_resistance_mohm(self) -> float:
        """
        Total DC equivalent internal resistance of the pack string:
        R_pack = N_s * (R_cell / N_p) + R_busbar_total
        """
        cell_matrix_r = self.topology.num_series * (self.cell.r0_mohm / self.topology.num_parallel)
        total_busbar_r = (self.topology.num_series - 1) * self.busbar_resistance_mohm
        return cell_matrix_r + total_busbar_r

    @property
    def gravimetric_energy_density_wh_per_kg(self) -> float:
        """Pack-level gravimetric energy density."""
        return (self.nominal_energy_kwh * 1000.0) / self.total_pack_mass_kg

    def calculate_voltage_drop(self, current_a: float) -> float:
        """Instantaneous ohmic IR voltage drop across the pack under load."""
        return current_a * (self.total_resistance_mohm / 1000.0)

    def summary(self) -> Dict[str, Any]:
        """Returns structured diagnostic dictionary of pack metrics."""
        return {
            "topology": str(self.topology),
            "total_cells": self.total_cells,
            "nominal_voltage_v": round(self.nominal_voltage_v, 2),
            "voltage_range_v": f"{round(self.v_min_v, 1)}V - {round(self.v_max_v, 1)}V",
            "capacity_ah": round(self.capacity_ah, 2),
            "nominal_energy_kwh": round(self.nominal_energy_kwh, 2),
            "cell_mass_kg": round(self.cell_mass_kg, 2),
            "total_pack_mass_kg": round(self.total_pack_mass_kg, 2),
            "total_pack_r0_mohm": round(self.total_resistance_mohm, 2),
            "gravimetric_energy_density_wh_per_kg": round(self.gravimetric_energy_density_wh_per_kg, 2),
        }

