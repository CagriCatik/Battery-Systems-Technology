from typing import List, Dict, Any, Tuple
import numpy as np
from battery_toolkit.core.cell import BatteryCell
from battery_toolkit.core.pack import BatteryPack, PackTopology


class ConnectionSimulator:
    """
    Simulates multi-configuration topology sweeps and statistical cell-to-cell
    manufacturing dispersion (Gaussian capacity and internal resistance variations).
    """
    @staticmethod
    def simulate_topology_sweep(
        cell: BatteryCell,
        configurations: List[Tuple[int, int]], # List of (Ns, Np) tuples
    ) -> List[Dict[str, Any]]:
        """
        Evaluates a list of (series_count, parallel_count) topologies.
        """
        results = []
        for ns, np_count in configurations:
            topology = PackTopology(num_series=ns, num_parallel=np_count)
            pack = BatteryPack(cell=cell, topology=topology)
            results.append({
                "label": str(topology),
                "num_series": ns,
                "num_parallel": np_count,
                "total_cells": pack.total_cells,
                "nominal_voltage_v": pack.nominal_voltage_v,
                "capacity_ah": pack.capacity_ah,
                "nominal_energy_kwh": pack.nominal_energy_kwh,
            })
        return results

    @staticmethod
    def simulate_statistical_dispersion(
        cell: BatteryCell,
        topology: PackTopology,
        capacity_cov: float = 0.015, # 1.5% Coefficient of Variation
        resistance_cov: float = 0.050, # 5.0% Coefficient of Variation
        seed: int = 42,
    ) -> Dict[str, Any]:
        """
        Monte Carlo simulation of Ns * Np cells with Gaussian dispersion:
        C_i ~ N(mu_C, sigma_C^2), R_0,i ~ N(mu_R, sigma_R^2).
        Calculates usable string capacity and parallel current sharing mismatch.
        """
        rng = np.random.default_rng(seed)
        n_cells = topology.total_cells

        # Sample cell capacities and resistances
        mu_c = cell.capacity_ah
        sigma_c = mu_c * capacity_cov
        capacities = rng.normal(mu_c, sigma_c, size=(topology.num_series, topology.num_parallel))

        mu_r = cell.r0_mohm / 1000.0
        sigma_r = mu_r * resistance_cov
        resistances = np.maximum(1e-4, rng.normal(mu_r, sigma_r, size=(topology.num_series, topology.num_parallel)))

        # In a parallel-first (NpS) brick, parallel capacities sum together
        brick_capacities = np.sum(capacities, axis=1) # Sum across Np for each series brick

        # Bottleneck capacity is constrained by the weakest series brick
        usable_pack_capacity_ah = float(np.min(brick_capacities))
        nominal_ideal_capacity_ah = topology.num_parallel * mu_c
        capacity_loss_percent = ((nominal_ideal_capacity_ah - usable_pack_capacity_ah) / nominal_ideal_capacity_ah) * 100.0

        # Current sharing imbalance in parallel branches during pack discharge at 1C
        pack_current_a = nominal_ideal_capacity_ah
        # In a parallel branch of 1 brick: I_j = I_total * (1/R_j) / sum(1/R)
        conductances = 1.0 / resistances[0, :]
        branch_currents = pack_current_a * (conductances / np.sum(conductances))
        current_imbalance_max_a = float(np.max(branch_currents) - np.min(branch_currents))

        return {
            "topology": str(topology),
            "nominal_capacity_ah": round(nominal_ideal_capacity_ah, 2),
            "usable_capacity_ah": round(usable_pack_capacity_ah, 2),
            "capacity_loss_from_dispersion_pct": round(capacity_loss_percent, 2),
            "weakest_brick_capacity_ah": round(float(np.min(brick_capacities)), 2),
            "strongest_brick_capacity_ah": round(float(np.max(brick_capacities)), 2),
            "max_parallel_current_imbalance_a": round(current_imbalance_max_a, 2),
        }

