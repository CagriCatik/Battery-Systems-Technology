import math
from dataclasses import dataclass
from typing import Dict, Any
from battery_toolkit.core.cell import BatteryCell
from battery_toolkit.core.pack import BatteryPack, PackTopology
from battery_toolkit.sizing.vehicle import VehicleParameters


@dataclass
class SizingRequirements:
    """Input requirements for sizing a battery pack."""
    target_range_km: float = 450.0             # Desired vehicle range (km)
    target_system_voltage_v: float = 400.0     # Nominal DC bus operating voltage (V)
    buffer_percentage: float = 15.0            # Unusable safety buffer (e.g. 5% top, 10% bottom)
    avg_speed_kmh: float = 100.0               # Representative driving speed for sizing
    ambient_temp_celsius: float = 20.0         # Operating temperature


class PackSizingOptimizer:
    """
    Automated optimization engine to size battery packs matching range, voltage,
    and power specifications.
    """
    def __init__(self, cell: BatteryCell, vehicle: VehicleParameters):
        self.cell = cell
        self.vehicle = vehicle

    def size_pack(
        self,
        desired_energy_kwh: float,
        system_voltage: float,
        buffer_percentage: float = 15.0,
    ) -> BatteryPack:
        """
        Calculates the required N_s and N_p cell topology to deliver the target
        net energy and nominal voltage within buffer constraints.
        """
        # 1. Series count based on nominal voltage
        num_series = math.ceil(system_voltage / self.cell.nominal_voltage)

        # 2. Total gross energy needed including unusable safety buffers
        usable_fraction = 1.0 - (buffer_percentage / 100.0)
        gross_energy_kwh_needed = desired_energy_kwh / usable_fraction

        # 3. Total Ah capacity needed at this nominal voltage
        pack_nominal_v = num_series * self.cell.nominal_voltage
        total_ah_needed = (gross_energy_kwh_needed * 1000.0) / pack_nominal_v

        # 4. Parallel cell count
        num_parallel = math.ceil(total_ah_needed / self.cell.capacity_ah)

        topology = PackTopology(num_series=num_series, num_parallel=num_parallel)
        return BatteryPack(cell=self.cell, topology=topology)

    def size_for_range(self, requirements: SizingRequirements) -> Dict[str, Any]:
        """
        Solves vehicle longitudinal dynamics to determine consumption (Wh/km),
        energy demand, and sized pack specifications.
        """
        # Initial estimate for total mass: vehicle curb weight + estimated 450 kg pack
        estimated_mass = self.vehicle.curb_weight_kg + 450.0

        # Iterative mass convergence (pack mass adds to vehicle consumption)
        for _ in range(5):
            consumption_wh_per_km = self.vehicle.steady_state_consumption_wh_per_km(
                velocity_kmh=requirements.avg_speed_kmh,
                total_mass_kg=estimated_mass,
            )
            net_energy_kwh = (consumption_wh_per_km * requirements.target_range_km) / 1000.0

            pack = self.size_pack(
                desired_energy_kwh=net_energy_kwh,
                system_voltage=requirements.target_system_voltage_v,
                buffer_percentage=requirements.buffer_percentage,
            )
            new_total_mass = self.vehicle.curb_weight_kg + pack.total_pack_mass_kg
            if abs(new_total_mass - estimated_mass) < 1.0:
                break
            estimated_mass = new_total_mass

        # Final range check
        usable_pack_kwh = pack.nominal_energy_kwh * (1.0 - requirements.buffer_percentage / 100.0)
        achieved_range_km = (usable_pack_kwh * 1000.0) / consumption_wh_per_km

        return {
            "requirements": requirements,
            "consumption_wh_per_km": round(consumption_wh_per_km, 1),
            "net_energy_kwh": round(net_energy_kwh, 2),
            "achieved_range_km": round(achieved_range_km, 1),
            "total_vehicle_mass_kg": round(estimated_mass, 1),
            "pack_summary": pack.summary(),
            "pack_object": pack,
        }

