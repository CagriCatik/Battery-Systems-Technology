# battery_design.py

from dataclasses import dataclass

@dataclass
class Cell:
    """
    Represents a single battery cell.
    """
    voltage: float   # Voltage of the cell in volts
    capacity: float  # Capacity of the cell in mAh or Ah

class BatteryPack:
    """
    Represents a battery pack composed of multiple cells in various configurations.
    """
    def __init__(self, connection_type: str, cell: Cell, n_series: int = 1, n_parallel: int = 1):
        """
        Initialize the battery pack.
        
        Parameters:
        - connection_type (str): 'series', 'parallel', or 'series-parallel'.
        - cell (Cell): The cell to use in the pack.
        - n_series (int): Number of cells in series (applicable for 'series' and 'series-parallel').
        - n_parallel (int): Number of parallel strings (applicable for 'parallel' and 'series-parallel').
        """
        self.connection_type = connection_type.lower()
        self.cell = cell
        self.n_series = n_series
        self.n_parallel = n_parallel
        self.total_voltage = 0.0
        self.total_capacity = 0.0
        self.calculate()
        
    def calculate(self):
        """
        Calculate total voltage and capacity based on connection type.
        """
        if self.connection_type == 'series':
            self.total_voltage = self.cell.voltage * self.n_series
            self.total_capacity = self.cell.capacity
            print(f"Calculating Series Connection: {self.n_series} cells in series.")
        elif self.connection_type == 'parallel':
            self.total_voltage = self.cell.voltage
            self.total_capacity = self.cell.capacity * self.n_parallel
            print(f"Calculating Parallel Connection: {self.n_parallel} cells in parallel.")
        elif self.connection_type == 'series-parallel':
            self.total_voltage = self.cell.voltage * self.n_series
            self.total_capacity = self.cell.capacity * self.n_parallel
            print(f"Calculating Series-Parallel Connection: {self.n_series} cells in series and {self.n_parallel} parallel strings.")
        else:
            raise ValueError("Invalid connection type. Choose 'series', 'parallel', or 'series-parallel'.")
        
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
    
    def __str__(self) -> str:
        """
        String representation of the battery pack.
        """
        return (f"Battery Pack Configuration: {self.connection_type.capitalize()} Connection\n"
                f"Total Voltage: {self.total_voltage} V\n"
                f"Total Capacity: {self.total_capacity} mAh\n")

def main():
    """
    Main function to demonstrate battery pack configurations.
    """
    # Define a single cell
    cell_voltage = 3.6  # volts
    cell_capacity = 3400  # mAh
    cell = Cell(voltage=cell_voltage, capacity=cell_capacity)
    
    # 1. Series Connection Example
    n_series = 4
    series_pack = BatteryPack(connection_type='series', cell=cell, n_series=n_series)
    print(series_pack)
    # Expected Output:
    # Total Voltage: 14.4 V
    # Total Capacity: 3400 mAh
    
    # 2. Parallel Connection Example
    n_parallel = 3
    parallel_pack = BatteryPack(connection_type='parallel', cell=cell, n_parallel=n_parallel)
    print(parallel_pack)
    # Expected Output:
    # Total Voltage: 3.6 V
    # Total Capacity: 10200 mAh
    
    # 3. Series-Parallel Connection Example
    n_series_sp = 3
    n_parallel_sp = 2
    series_parallel_pack = BatteryPack(connection_type='series-parallel', cell=cell, n_series=n_series_sp, n_parallel=n_parallel_sp)
    print(series_parallel_pack)
    # Expected Output:
    # Total Voltage: 10.8 V
    # Total Capacity: 6800 mAh

if __name__ == "__main__":
    main()
