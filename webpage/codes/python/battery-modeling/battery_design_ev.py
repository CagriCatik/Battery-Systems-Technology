# ev_battery_design.py

from dataclasses import dataclass
import math

@dataclass
class Cell:
    """
    Represents a single battery cell.
    """
    voltage: float   # Voltage of the cell in volts
    capacity: float  # Capacity of the cell in Ah

class BatteryPack:
    """
    Represents a battery pack composed of multiple cells in series and parallel.
    """
    def __init__(self, cell: Cell, desired_voltage: float, desired_capacity: float):
        """
        Initialize the battery pack design parameters.
        
        Parameters:
        - cell (Cell): The cell to use in the pack.
        - desired_voltage (float): Total desired pack voltage in volts.
        - desired_capacity (float): Total desired pack capacity in Ah.
        """
        self.cell = cell
        self.desired_voltage = desired_voltage
        self.desired_capacity = desired_capacity
        self.n_series = 0
        self.n_parallel = 0
        self.total_voltage = 0.0
        self.total_capacity = 0.0
        self.calculate_configuration()
        
    def calculate_configuration(self):
        """
        Calculate the number of series and parallel connections required.
        """
        # Calculate number of cells in series
        self.n_series = math.ceil(self.desired_voltage / self.cell.voltage)
        self.total_voltage = self.cell.voltage * self.n_series
        
        # Calculate number of parallel strings
        self.n_parallel = math.ceil(self.desired_capacity / self.cell.capacity)
        self.total_capacity = self.cell.capacity * self.n_parallel
        
        print(f"Calculated Configuration:")
        print(f"  Cells in Series: {self.n_series} (Total Voltage: {self.total_voltage} V)")
        print(f"  Cells in Parallel: {self.n_parallel} (Total Capacity: {self.total_capacity} Ah)")
        print(f"  Total Cells Required: {self.n_series * self.n_parallel}\n")
        
    def get_total_voltage(self) -> float:
        """
        Returns the total voltage of the battery pack.
        """
        return self.total_voltage
    
    def get_total_capacity(self) -> float:
        """
        Returns the total capacity of the battery pack.
        """
        return self.total_capacity
    
    def get_total_cells(self) -> int:
        """
        Returns the total number of cells in the battery pack.
        """
        return self.n_series * self.n_parallel
    
    def __str__(self) -> str:
        """
        String representation of the battery pack.
        """
        return (f"Battery Pack Configuration:\n"
                f"  Series Cells: {self.n_series}\n"
                f"  Parallel Strings: {self.n_parallel}\n"
                f"  Total Voltage: {self.total_voltage} V\n"
                f"  Total Capacity: {self.total_capacity} Ah\n"
                f"  Total Cells: {self.get_total_cells()}")

class EVBatteryDesign:
    """
    Represents the design process for an EV battery pack.
    """
    def __init__(self, cell: Cell, vehicle_range_km: float, vehicle_efficiency_km_per_kWh: float, 
                 max_voltage: float = None):
        """
        Initialize the EV battery design parameters.
        
        Parameters:
        - cell (Cell): The battery cell specifications.
        - vehicle_range_km (float): Desired range of the vehicle in kilometers.
        - vehicle_efficiency_km_per_kWh (float): Vehicle efficiency in km per kWh.
        - max_voltage (float, optional): Maximum allowable pack voltage. If None, calculated based on design.
        """
        self.cell = cell
        self.vehicle_range_km = vehicle_range_km
        self.vehicle_efficiency_km_per_kWh = vehicle_efficiency_km_per_kWh
        self.max_voltage = max_voltage  # Optional constraint
        self.required_energy_kWh = 0.0
        self.desired_voltage = 0.0
        self.desired_capacity = 0.0
        self.battery_pack = None
        self.calculate_requirements()
        
    def calculate_requirements(self):
        """
        Calculate the required energy, voltage, and capacity for the battery pack.
        """
        # Calculate required energy in kWh
        self.required_energy_kWh = self.vehicle_range_km / self.vehicle_efficiency_km_per_kWh
        print(f"Required Energy: {self.required_energy_kWh} kWh")
        
        # Convert kWh to Ah based on desired voltage
        # If max_voltage is provided, use it; otherwise, assume a typical EV voltage (e.g., 800 V)
        if self.max_voltage:
            self.desired_voltage = self.max_voltage
        else:
            self.desired_voltage = 800  # Typical high-voltage EV battery pack
        
        # Calculate desired capacity in Ah
        # Energy (Wh) = Voltage (V) * Capacity (Ah) => Capacity (Ah) = Energy (Wh) / Voltage (V)
        self.desired_capacity = (self.required_energy_kWh * 1000) / self.desired_voltage
        print(f"Desired Voltage: {self.desired_voltage} V")
        print(f"Desired Capacity: {self.desired_capacity:.2f} Ah\n")
        
        # Initialize BatteryPack
        self.battery_pack = BatteryPack(cell=self.cell, 
                                        desired_voltage=self.desired_voltage, 
                                        desired_capacity=self.desired_capacity)
        
    def get_battery_pack(self) -> BatteryPack:
        """
        Returns the designed battery pack.
        """
        return self.battery_pack
    
    def __str__(self) -> str:
        """
        String representation of the EV battery design.
        """
        return (f"EV Battery Design:\n"
                f"  Vehicle Range: {self.vehicle_range_km} km\n"
                f"  Vehicle Efficiency: {self.vehicle_efficiency_km_per_kWh} km/kWh\n"
                f"  Required Energy: {self.required_energy_kWh} kWh\n"
                f"  Desired Voltage: {self.desired_voltage} V\n"
                f"  Desired Capacity: {self.desired_capacity:.2f} Ah\n"
                f"{self.battery_pack}")

def main():
    """
    Main function to demonstrate EV battery pack design for a Porsche Taycan-like vehicle.
    """
    # Define cell specifications
    # Example: Using a cell with 3.6 V and 3.4 Ah (similar to your initial example)
    cell_voltage = 3.6  # volts
    cell_capacity = 3.4  # Ah
    cell = Cell(voltage=cell_voltage, capacity=cell_capacity)
    
    # Define EV specifications based on Porsche Taycan
    # Example values (approximate):
    # - Range: 500 km (varies by model and conditions)
    # - Efficiency: 6 km/kWh (depends on driving conditions and vehicle)
    vehicle_range_km = 500  # desired range in kilometers
    vehicle_efficiency_km_per_kWh = 6  # km per kWh
    
    # Optional: Define maximum pack voltage if needed
    # For high-performance EVs like Taycan, ~800 V is typical
    max_voltage = 800  # volts
    
    # Initialize EVBatteryDesign
    ev_battery_design = EVBatteryDesign(cell=cell, 
                                        vehicle_range_km=vehicle_range_km, 
                                        vehicle_efficiency_km_per_kWh=vehicle_efficiency_km_per_kWh,
                                        max_voltage=max_voltage)
    
    # Retrieve and display the battery pack configuration
    battery_pack = ev_battery_design.get_battery_pack()
    print(battery_pack)
    
    # Example Output:
    # Required Energy: 83.33333333333333 kWh
    # Desired Voltage: 800 V
    # Desired Capacity: 104.17 Ah
    #
    # Calculated Configuration:
    #   Cells in Series: 223 (Total Voltage: 802.8 V)
    #   Cells in Parallel: 31 (Total Capacity: 105.4 Ah)
    #   Total Cells Required: 6913
    #
    # Battery Pack Configuration:
    #   Series Cells: 223
    #   Parallel Strings: 31
    #   Total Voltage: 802.8 V
    #   Total Capacity: 105.4 Ah
    #   Total Cells: 6913

if __name__ == "__main__":
    main()
