import matplotlib.pyplot as plt

class BatteryCell:
    def __init__(self, voltage, capacity):
        self.voltage = voltage  # Voltage in Volts
        self.capacity = capacity  # Capacity in mAh

def calculate_series_connection(cells):
    """Calculate total voltage and capacity for a series connection."""
    total_voltage = sum(cell.voltage for cell in cells)
    total_capacity = cells[0].capacity  # Capacity remains constant
    return total_voltage, total_capacity

def calculate_parallel_connection(cells):
    """Calculate total voltage and capacity for a parallel connection."""
    total_voltage = cells[0].voltage  # Voltage remains constant
    total_capacity = sum(cell.capacity for cell in cells)
    return total_voltage, total_capacity

def calculate_series_parallel_connection(series_count, parallel_count, cell):
    """Calculate total voltage and capacity for a series-parallel configuration."""
    total_voltage = series_count * cell.voltage
    total_capacity = parallel_count * cell.capacity
    return total_voltage, total_capacity

def display_results(configuration, voltage, capacity):
    """Print the configuration details."""
    print(f"Configuration: {configuration}")
    print(f"  Total Voltage: {voltage} V")
    print(f"  Total Capacity: {capacity} mAh\n")

def simulate_configurations():
    """Simulate multiple configurations and visualize results."""
    # Example battery cell: 3.7V, 3000mAh
    cell = BatteryCell(3.7, 3000)

    # Define configurations: [Series, Parallel]
    configurations = [
        {"series": 3, "parallel": 1},  # 3S1P
        {"series": 4, "parallel": 2},  # 4S2P
        {"series": 6, "parallel": 3},  # 6S3P
        {"series": 8, "parallel": 4},  # 8S4P
    ]

    labels = []
    voltages = []
    capacities = []

    # Simulate each configuration
    for config in configurations:
        series = config["series"]
        parallel = config["parallel"]
        total_voltage, total_capacity = calculate_series_parallel_connection(series, parallel, cell)
        configuration_label = f"{series}S{parallel}P"
        labels.append(configuration_label)
        voltages.append(total_voltage)
        capacities.append(total_capacity)
        display_results(configuration_label, total_voltage, total_capacity)

    # Plot Voltage Results
    plt.figure(figsize=(10, 6))
    plt.bar(labels, voltages, alpha=0.7, color="blue")
    plt.title("Voltage Across Configurations")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Configuration")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    # Plot Capacity Results
    plt.figure(figsize=(10, 6))
    plt.bar(labels, capacities, alpha=0.7, color="green")
    plt.title("Capacity Across Configurations")
    plt.ylabel("Capacity (mAh)")
    plt.xlabel("Configuration")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# Run simulation
simulate_configurations()
