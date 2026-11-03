"""
main.py
Entry point to run and visualize the simulation for the BMS-HVAC integration.
"""

import random
import matplotlib.pyplot as plt
# If you haven't installed matplotlib, run: pip install matplotlib

from battery import Battery
from hvac import HVAC
from controller import ThermalController
from thermal_manager import ThermalManager

if __name__ == "__main__":
    # Create instances of each module
    battery = Battery(capacity_kWh=50.0, initial_temp=20.0, ambient_temp=25.0)
    hvac = HVAC(cabin_temp=30.0, ambient_temp=25.0)  # Suppose the cabin is initially hot
    controller = ThermalController()
    thermal_manager = ThermalManager(battery, hvac, controller)

    # Simulation parameters
    simulation_time_minutes = 60  # Run for 60 minutes
    dt = 1  # 1-minute steps

    # Lists to store data for plotting
    times = []
    battery_temps = []
    soc_values = []
    cabin_temps = []
    power_draws = []

    # Simulation loop
    for minute in range(simulation_time_minutes):
        # Generate a random power draw for each minute (0 to 50 kW)
        power_draw_kW = random.uniform(0, 50)

        # Step the thermal management system
        thermal_manager.step(power_draw_kW, dt=dt)

        # Store data
        times.append(minute)
        battery_temps.append(battery.temperature)
        soc_values.append(battery.soc)
        cabin_temps.append(hvac.cabin_temperature)
        power_draws.append(power_draw_kW)

        # Optional: print diagnostic info each loop iteration
        print(
            f"Minute: {minute+1:02d} | "
            f"Battery Temp: {battery.temperature:.2f}°C | "
            f"SOC: {battery.soc:.1f}% | "
            f"Cabin Temp: {hvac.cabin_temperature:.2f}°C | "
            f"Power Draw: {power_draw_kW:.1f} kW"
        )

    print("Simulation complete.")

    # ---------------------
    # PLOTTING THE RESULTS
    # ---------------------
    # Create a figure with multiple subplots
    plt.figure(figsize=(10, 6))

    # 1) Battery Temperature
    plt.subplot(2, 2, 1)
    plt.plot(times, battery_temps, label="Battery Temp (°C)", color="blue")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temperature (°C)")
    plt.title("Battery Temperature Over Time")
    plt.legend()
    plt.grid(True)

    # 2) Cabin Temperature
    plt.subplot(2, 2, 2)
    plt.plot(times, cabin_temps, label="Cabin Temp (°C)", color="orange")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temperature (°C)")
    plt.title("Cabin Temperature Over Time")
    plt.legend()
    plt.grid(True)

    # 3) Battery State of Charge (SoC)
    plt.subplot(2, 2, 3)
    plt.plot(times, soc_values, label="Battery SoC (%)", color="green")
    plt.xlabel("Time (minutes)")
    plt.ylabel("SoC (%)")
    plt.title("Battery SoC Over Time")
    plt.legend()
    plt.grid(True)

    # 4) Power Draw
    plt.subplot(2, 2, 4)
    plt.plot(times, power_draws, label="Power Draw (kW)", color="red")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Power (kW)")
    plt.title("Power Draw Over Time")
    plt.legend()
    plt.grid(True)

    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    # Show the plots
    plt.show()
