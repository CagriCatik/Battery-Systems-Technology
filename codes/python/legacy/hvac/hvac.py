"""
hvac.py
Defines the HVAC class for managing the cabin's heating and cooling
while also providing resources to the battery.
"""

class HVAC:
    """
    Simulated HVAC system that can provide both heating and cooling
    for cabin and battery in an integrated manner.
    """
    def __init__(self, cabin_temp=25.0, ambient_temp=25.0):
        self.cabin_temperature = cabin_temp
        self.ambient_temperature = ambient_temp
        self.cabin_target_temp = 22.0
        self.battery_target_temp = 25.0
        
        # Heating/Cooling power constraints (kW), simplified
        self.max_cooling_power = 5.0
        self.max_heating_power = 5.0

        # Track current HVAC usage
        self.current_cooling_power = 0.0
        self.current_heating_power = 0.0

    def update_cabin_temperature(self, dt):
        """
        Simplistic model of cabin temperature drifting towards ambient without HVAC.
        :param dt: time step in minutes
        """
        diff = self.ambient_temperature - self.cabin_temperature
        self.cabin_temperature += 0.005 * diff * dt  # small factor for passive movement

    def apply_hvac_to_cabin(self, dt):
        """
        Simple proportional control to heat or cool the cabin.
        """
        cabin_diff = self.cabin_target_temp - self.cabin_temperature
        
        if cabin_diff > 0:
            # Need heating
            self.current_heating_power = min(self.max_heating_power, abs(cabin_diff))
            self.cabin_temperature += 0.1 * self.current_heating_power * dt
            self.current_cooling_power = 0.0
        else:
            # Need cooling
            self.current_cooling_power = min(self.max_cooling_power, abs(cabin_diff))
            self.cabin_temperature -= 0.1 * self.current_cooling_power * dt
            self.current_heating_power = 0.0
