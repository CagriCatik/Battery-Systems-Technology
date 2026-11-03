from typing import List, Dict, Any
import numpy as np


class PassiveBalancingSimulator:
    """
    Simulation of multi-channel dissipative passive balancing across a series cell string.
    """
    def __init__(self, bleed_resistor_ohms: float = 33.0, threshold_voltage_v: float = 0.010):
        self.r_bleed = bleed_resistor_ohms
        self.v_threshold = threshold_voltage_v # Voltage delta trigger (e.g. 10 mV)

    def evaluate_balancing_channels(self, cell_voltages: np.ndarray) -> np.ndarray:
        """
        Determines which cells require balancing based on deviation from the minimum cell:
        Balance channel k if V_k - min(V) >= v_threshold.
        Returns boolean mask array.
        """
        v_min = np.min(cell_voltages)
        return (cell_voltages - v_min) >= self.v_threshold

    def compute_dissipation(self, cell_voltages: np.ndarray) -> Dict[str, Any]:
        """
        Calculates instantaneous balancing currents and heat dissipation per channel:
        I_bal = V_cell / R_bleed
        P_diss = V_cell^2 / R_bleed
        """
        active_mask = self.evaluate_balancing_channels(cell_voltages)
        currents_a = np.where(active_mask, cell_voltages / self.r_bleed, 0.0)
        power_w = np.where(active_mask, (cell_voltages ** 2) / self.r_bleed, 0.0)

        return {
            "active_channels_count": int(np.sum(active_mask)),
            "active_mask": active_mask.tolist(),
            "balancing_currents_ma": np.round(currents_a * 1000.0, 1).tolist(),
            "channel_power_w": np.round(power_w, 3).tolist(),
            "total_pcb_dissipation_w": float(np.round(np.sum(power_w), 2)),
        }


class ActiveBalancingSimulator:
    """
    Simulation of non-dissipative active balancing using switched-capacitor
    or inductive bidirectional energy transfer.
    """
    def __init__(self, efficiency: float = 0.88, max_transfer_current_a: float = 2.0):
        self.efficiency = efficiency
        self.max_current = max_transfer_current_a

    def transfer_energy(
        self,
        source_cell_voltage: float,
        target_cell_voltage: float,
        duration_s: float,
    ) -> Dict[str, float]:
        """
        Calculates energy extracted from high-voltage cell and transferred into low-voltage cell:
        E_extracted = V_source * I * dt
        E_delivered = E_extracted * efficiency
        """
        if source_cell_voltage <= target_cell_voltage:
            return {"energy_extracted_j": 0.0, "energy_delivered_j": 0.0, "heat_loss_j": 0.0}

        energy_extracted_j = source_cell_voltage * self.max_current * duration_s
        energy_delivered_j = energy_extracted_j * self.efficiency
        heat_loss_j = energy_extracted_j - energy_delivered_j

        return {
            "energy_extracted_j": round(energy_extracted_j, 2),
            "energy_delivered_j": round(energy_delivered_j, 2),
            "heat_loss_j": round(heat_loss_j, 2),
        }

