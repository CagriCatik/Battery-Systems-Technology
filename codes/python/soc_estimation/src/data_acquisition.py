import numpy as np
import pandas as pd
import os

def simulate_battery_data(total_time=3600, dt=1, initial_soc=1.0, battery_capacity=3600):
    """
    Simulates battery data for SoC estimation.
    
    Parameters:
        total_time (int): Total simulation time in seconds.
        dt (int): Time step in seconds.
        initial_soc (float): Initial SoC (0 to 1).
        battery_capacity (float): Battery capacity in Coulombs.
    
    Returns:
        data (DataFrame): Simulated battery data (time, current, voltage, soc_ground_truth).
    """
    time_steps = np.arange(0, total_time, dt)
    current = np.concatenate((-0.5 * np.ones(len(time_steps) // 2),
                              0.5 * np.ones(len(time_steps) // 2)))
    soc_ground_truth = initial_soc - (np.cumsum(current) * dt) / battery_capacity
    soc_ground_truth = np.clip(soc_ground_truth, 0, 1)
    voltage = 4.2 * soc_ground_truth + 0.05 * np.random.randn(len(soc_ground_truth))

    data = pd.DataFrame({
        'time': time_steps,
        'current': current,
        'voltage': voltage,
        'soc_ground_truth': soc_ground_truth
    })
    return data

# Save the simulated data to CSV
def save_simulated_data(data, filename="../data/battery_data.csv"):
    """
    Saves the simulated battery data to a CSV file.

    Parameters:
        data (DataFrame): The simulated battery data.
        filename (str): Path to save the file.
    """
    # Ensure the directory exists (though it should already exist)
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        print(f"Creating missing directory: {directory}")
        os.makedirs(directory)

    # Save the data to CSV
    data.to_csv(filename, index=False)
    print(f"Simulated data saved to {filename}")