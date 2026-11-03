# battery_sizing.py

"""
Battery Sizing Tool
===================

This script automates the battery sizing process, determining the optimal configuration
of battery cells required to meet specific energy and voltage requirements. It calculates
the number of series and parallel connections needed based on cell specifications and
design parameters, ensuring efficient and reliable battery system design.

Features:
- Supports multiple battery cell types.
- Accepts user input via command-line interface (CLI).
- Validates input parameters to prevent invalid configurations.
- Provides detailed output and optionally exports results to a CSV file.
- Includes logging for tracking the calculation process.

"""

import argparse
import csv
import logging
from math import ceil
from dataclasses import dataclass
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    filename='battery_sizing.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class BatteryCell:
    """
    Represents the characteristics of a single battery cell.
    
    Attributes:
        name (str): Identifier for the battery cell type.
        nominal_voltage (float): Voltage per cell in volts (V).
        usable_capacity (float): Usable capacity per cell in ampere-hours (Ah).
    """
    name: str
    nominal_voltage: float  # Voltage per cell in volts (V)
    usable_capacity: float  # Usable capacity per cell in ampere-hours (Ah)

@dataclass
class BatteryDesignParameters:
    """
    Encapsulates the design requirements for the battery system.
    
    Attributes:
        desired_energy_kwh (float): Desired energy in kilowatt-hours (kWh).
        system_voltage (float): Desired system voltage in volts (V).
        buffer_percentage (float): Depth of discharge as a percentage (e.g., 80 for 80%).
        cell_type (str): Identifier for the battery cell type to use.
    """
    desired_energy_kwh: float     # Desired energy in kilowatt-hours (kWh)
    system_voltage: float         # Desired system voltage in volts (V)
    buffer_percentage: float      # Depth of discharge (e.g., 80 for 80%)
    cell_type: str                # Battery cell type identifier

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments provided by the user.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Battery Sizing Tool: Calculate optimal battery configurations.'
    )
    
    parser.add_argument(
        '--cell',
        action='append',
        nargs=3,
        metavar=('NAME', 'VOLTAGE', 'CAPACITY'),
        required=True,
        help='Define a battery cell type with NAME, nominal voltage (V), and usable capacity (Ah). Can be used multiple times for multiple cell types.'
    )
    
    parser.add_argument(
        '--design',
        action='append',
        nargs=4,
        metavar=('ENERGY_kWh', 'VOLTAGE', 'BUFFER_%', 'CELL_NAME'),
        required=True,
        help='Define a battery design with desired energy (kWh), system voltage (V), buffer percentage (%), and cell type name.'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        default=None,
        help='Optional: Path to export the results as a CSV file.'
    )
    
    return parser.parse_args()

def create_battery_cells(cell_args: List[List[str]]) -> Dict[str, BatteryCell]:
    """
    Creates a dictionary of BatteryCell instances from parsed arguments.
    
    Parameters:
        cell_args (List[List[str]]): List of battery cell definitions.
    
    Returns:
        Dict[str, BatteryCell]: Dictionary mapping cell names to BatteryCell instances.
    """
    cells = {}
    for cell in cell_args:
        name, voltage, capacity = cell
        try:
            voltage = float(voltage)
            capacity = float(capacity)
            if voltage <= 0 or capacity <= 0:
                raise ValueError
            cells[name] = BatteryCell(name=name, nominal_voltage=voltage, usable_capacity=capacity)
            logging.info(f"Defined Battery Cell - Name: {name}, Voltage: {voltage}V, Capacity: {capacity}Ah")
        except ValueError:
            logging.error(f"Invalid cell parameters: {cell}. Voltage and Capacity must be positive numbers.")
            raise argparse.ArgumentTypeError(f"Invalid cell parameters: {cell}. Voltage and Capacity must be positive numbers.")
    return cells

def create_design_parameters(design_args: List[List[str]], cells: Dict[str, BatteryCell]) -> List[BatteryDesignParameters]:
    """
    Creates a list of BatteryDesignParameters instances from parsed arguments.
    
    Parameters:
        design_args (List[List[str]]): List of battery design definitions.
        cells (Dict[str, BatteryCell]): Dictionary of available battery cells.
    
    Returns:
        List[BatteryDesignParameters]: List of design parameters.
    """
    designs = []
    for design in design_args:
        energy, voltage, buffer, cell_name = design
        try:
            energy = float(energy)
            voltage = float(voltage)
            buffer = float(buffer)
            if energy <= 0 or voltage <= 0 or not (0 < buffer <= 100):
                raise ValueError
            if cell_name not in cells:
                logging.error(f"Cell type '{cell_name}' not defined.")
                raise ValueError(f"Cell type '{cell_name}' not defined.")
            designs.append(BatteryDesignParameters(
                desired_energy_kwh=energy,
                system_voltage=voltage,
                buffer_percentage=buffer,
                cell_type=cell_name
            ))
            logging.info(f"Defined Battery Design - Energy: {energy}kWh, Voltage: {voltage}V, Buffer: {buffer}%, Cell Type: {cell_name}")
        except ValueError as ve:
            logging.error(f"Invalid design parameters: {design}. Ensure energy, voltage are positive and buffer is between 0 and 100.")
            raise argparse.ArgumentTypeError(f"Invalid design parameters: {design}. Ensure energy, voltage are positive and buffer is between 0 and 100.")
    return designs

def calculate_battery_configuration(cell: BatteryCell, design: BatteryDesignParameters) -> Optional[Dict[str, float]]:
    """
    Calculates the battery configuration based on cell specifications and design parameters.
    
    Parameters:
        cell (BatteryCell): The characteristics of a single battery cell.
        design (BatteryDesignParameters): The design requirements for the battery system.
    
    Returns:
        Optional[Dict[str, float]]: Dictionary containing configuration details or None if invalid.
    """
    logging.debug(f"Calculating configuration for Design - Energy: {design.desired_energy_kwh}kWh, Voltage: {design.system_voltage}V, Buffer: {design.buffer_percentage}%, Cell Type: {cell.name}")
    
    # Adjust usable capacity based on buffer percentage to prevent full discharge
    usable_capacity = cell.usable_capacity * (design.buffer_percentage / 100)
    logging.debug(f"Adjusted Usable Capacity per Cell: {usable_capacity}Ah")
    
    # Calculate total ampere-hours needed
    total_ah_needed = (design.desired_energy_kwh * 1000) / design.system_voltage
    logging.debug(f"Total Ampere-Hours Needed: {total_ah_needed}Ah")
    
    # Calculate number of series cells required (rounded up to the nearest integer)
    num_series = ceil(design.system_voltage / cell.nominal_voltage)
    actual_system_voltage = num_series * cell.nominal_voltage
    logging.debug(f"Number of Series Cells: {num_series}, Actual System Voltage: {actual_system_voltage}V")
    
    # Ensure that actual system voltage is within acceptable range (e.g., within 5% of desired)
    voltage_tolerance = 0.05 * design.system_voltage
    if abs(actual_system_voltage - design.system_voltage) > voltage_tolerance:
        logging.warning(f"Actual system voltage {actual_system_voltage}V deviates more than 5% from desired {design.system_voltage}V.")
    
    # Calculate number of parallel cells required (rounded up to the nearest integer)
    num_parallel = ceil(total_ah_needed / usable_capacity)
    logging.debug(f"Number of Parallel Cells: {num_parallel}")
    
    # Total number of cells is the product of series and parallel cells
    total_cells = num_series * num_parallel
    logging.debug(f"Total Cells Required: {total_cells}")
    
    # Total capacity in ampere-hours
    total_capacity_ah = num_parallel * usable_capacity
    logging.debug(f"Total Capacity: {total_capacity_ah}Ah")
    
    # Total energy in kilowatt-hours
    total_energy_kwh = (actual_system_voltage * total_capacity_ah) / 1000
    logging.debug(f"Total Energy: {total_energy_kwh}kWh")
    
    return {
        'number_of_series_cells': num_series,
        'number_of_parallel_cells': num_parallel,
        'total_cells': total_cells,
        'actual_system_voltage': actual_system_voltage,
        'total_capacity_ah': total_capacity_ah,
        'total_energy_kwh': total_energy_kwh
    }

def batch_calculate_configurations(cells: Dict[str, BatteryCell], designs: List[BatteryDesignParameters]) -> Dict[str, Dict[str, float]]:
    """
    Calculates battery configurations for a batch of design parameters.
    
    Parameters:
        cells (Dict[str, BatteryCell]): Dictionary of available battery cells.
        designs (List[BatteryDesignParameters]): List of design parameters.
    
    Returns:
        Dict[str, Dict[str, float]]: Dictionary where each key is a model name and the value is the corresponding configuration.
    """
    configurations = {}
    for design in designs:
        cell = cells.get(design.cell_type)
        if not cell:
            logging.error(f"Cell type '{design.cell_type}' not found. Skipping design.")
            continue
        config = calculate_battery_configuration(cell, design)
        if config:
            model_name = f"{design.system_voltage}V_{design.desired_energy_kwh}kWh_{cell.name}"
            configurations[model_name] = config
            logging.info(f"Configuration calculated for Model: {model_name}")
    return configurations

def export_to_csv(configurations: Dict[str, Dict[str, float]], filepath: str):
    """
    Exports the battery configurations to a CSV file.
    
    Parameters:
        configurations (Dict[str, Dict[str, float]]): Battery configurations.
        filepath (str): Path to the output CSV file.
    """
    fieldnames = [
        'Model',
        'Number of Series Cells',
        'Number of Parallel Cells',
        'Total Cells Required',
        'Actual System Voltage (V)',
        'Total Capacity (Ah)',
        'Total Energy (kWh)'
    ]
    
    try:
        with open(filepath, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for model, config in configurations.items():
                writer.writerow({
                    'Model': model,
                    'Number of Series Cells': config['number_of_series_cells'],
                    'Number of Parallel Cells': config['number_of_parallel_cells'],
                    'Total Cells Required': config['total_cells'],
                    'Actual System Voltage (V)': config['actual_system_voltage'],
                    'Total Capacity (Ah)': config['total_capacity_ah'],
                    'Total Energy (kWh)': config['total_energy_kwh']
                })
        logging.info(f"Configurations exported to {filepath}")
    except Exception as e:
        logging.error(f"Failed to export configurations to CSV: {e}")
        print(f"Error: Failed to export configurations to CSV: {e}")

def display_configurations(configurations: Dict[str, Dict[str, float]]):
    """
    Displays the battery configurations in a readable format.
    
    Parameters:
        configurations (Dict[str, Dict[str, float]]): Battery configurations.
    """
    if not configurations:
        print("No valid configurations to display.")
        return
    
    for model, config in configurations.items():
        print(f"Model: {model}")
        print(f"  Number of Series Cells     : {config['number_of_series_cells']}")
        print(f"  Number of Parallel Cells   : {config['number_of_parallel_cells']}")
        print(f"  Total Cells Required      : {config['total_cells']}")
        print(f"  Actual System Voltage     : {config['actual_system_voltage']} V")
        print(f"  Total Capacity            : {config['total_capacity_ah']} Ah")
        print(f"  Total Energy              : {config['total_energy_kwh']} kWh\n")

def main():
    """
    Main function to execute the battery sizing tool.
    
    Parses command-line arguments, defines battery cells and design parameters,
    calculates configurations, displays results, and optionally exports to CSV.
    """
    args = parse_arguments()
    
    # Create battery cells
    try:
        cells = create_battery_cells(args.cell)
    except argparse.ArgumentTypeError as e:
        print(f"Error defining battery cells: {e}")
        return
    
    # Create design parameters
    try:
        designs = create_design_parameters(args.design, cells)
    except argparse.ArgumentTypeError as e:
        print(f"Error defining battery designs: {e}")
        return
    
    # Calculate configurations
    configurations = batch_calculate_configurations(cells, designs)
    
    # Display configurations
    display_configurations(configurations)
    
    # Export to CSV if requested
    if args.export:
        export_to_csv(configurations, args.export)
        print(f"Configurations have been exported to {args.export}")
    
    print("Battery sizing calculations completed. Check 'battery_sizing.log' for detailed logs.")

if __name__ == "__main__":
    main()
