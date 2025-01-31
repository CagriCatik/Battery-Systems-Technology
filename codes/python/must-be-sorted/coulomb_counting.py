import time
import random
import matplotlib.pyplot as plt

class CoulombCounter:
    def __init__(self, capacity_ah, initial_soc=100.0):
        """
        Initialize the Coulomb Counter.
        
        :param capacity_ah: Nominal capacity of the battery in Ampere-hours (Ah).
        :param initial_soc: Initial State of Charge (SOC) in percentage.
        """
        self.capacity_ah = capacity_ah
        self.soc = initial_soc
        self.previous_time = None  # Initialized as None to set on first update
    
    def update(self, current_a, current_time):
        """
        Update the SOC based on the current and elapsed time.
        
        :param current_a: Current in Amperes (A). Positive for discharge, negative for charge.
        :param current_time: Current timestamp in seconds.
        """
        if self.previous_time is None:
            # First update call
            self.previous_time = current_time
            return  # No SOC change on first call
        
        delta_time_sec = current_time - self.previous_time
        delta_time_h = delta_time_sec / 3600  # Convert seconds to hours
        delta_soc = (current_a * delta_time_h) / self.capacity_ah * 100  # SOC change in percentage
        self.soc -= delta_soc  # Subtract because discharge decreases SOC
        self.soc = max(0.0, min(100.0, self.soc))  # Clamp SOC between 0% and 100%
        self.previous_time = current_time
    
    def get_soc(self):
        """
        Get the current State of Charge.
        
        :return: SOC in percentage.
        """
        return self.soc

def simulate_current():
    """
    Simulate current measurements.
    For demonstration, random currents between -2A (charging) and 2A (discharging).
    
    :return: Simulated current in Amperes.
    """
    return random.uniform(-2.0, 2.0)

def main():
    # Initialize Coulomb Counter with a 100 Ah battery, starting at 100% SOC
    bms = CoulombCounter(capacity_ah=100.0, initial_soc=100.0)
    
    # Simulation parameters
    simulation_duration = 60  # seconds
    start_time = time.time()
    current_time = start_time
    end_time = start_time + simulation_duration
    interval = 1  # seconds
    
    # Data storage for plotting
    time_data = []
    soc_data = []
    current_data = []
    
    print("Starting Coulomb Counting Simulation")
    print(f"Initial SOC: {bms.get_soc():.2f}%\n")
    
    while current_time < end_time:
        current = simulate_current()
        bms.update(current_a=current, current_time=current_time)
        soc = bms.get_soc()
        
        elapsed_time = current_time - start_time
        time_data.append(elapsed_time)
        soc_data.append(soc)
        current_data.append(current)
        
        print(f"Time: {int(elapsed_time)}s | Current: {current:.2f}A | SOC: {soc:.2f}%")
        
        time.sleep(interval)  # Wait for the next interval
        current_time = time.time()
    
    print(f"\nFinal SOC after {simulation_duration} seconds: {bms.get_soc():.2f}%")
    
    # Plotting the results
    plot_results(time_data, soc_data, current_data)

def plot_results(time_data, soc_data, current_data):
    """
    Plot SOC and current over time.
    
    :param time_data: List of elapsed time in seconds.
    :param soc_data: List of SOC percentages.
    :param current_data: List of current measurements in Amperes.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('State of Charge (%)', color=color)
    ax1.plot(time_data, soc_data, color=color, label='SOC')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 100)
    
    ax2 = ax1.twinx()  # Instantiate a second axes that shares the same x-axis
    
    color = 'tab:red'
    ax2.set_ylabel('Current (A)', color=color)  # We already handled the x-label with ax1
    ax2.plot(time_data, current_data, color=color, label='Current')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Add legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    
    plt.title('Coulomb Counting: SOC and Current Over Time')
    fig.tight_layout()  # To prevent label cutoff
    plt.show()

if __name__ == "__main__":
    main()
