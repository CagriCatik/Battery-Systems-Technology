"""
battery.py
Defines the Battery class for a simplified EV battery model.
"""

class Battery:
    """
    Represents a simplified EV Battery model.
    """
    def __init__(self, capacity_kWh=50.0, initial_temp=25.0, ambient_temp=25.0):
        self.capacity_kWh = capacity_kWh
        self.temperature = initial_temp     # in Celsius
        self.soc = 100.0                   # State of Charge in %
        self.ambient_temp = ambient_temp   # Environmental temperature in Celsius

        # For simulation: how quickly the battery temperature changes (deg C per minute)
        self.cooling_rate = -0.05
        self.heating_rate = 0.05

    def update(self, power_draw_kW, hvac_cooling_power, hvac_heating_power, dt):
        """
        Update battery temperature based on power draw and HVAC effects.

        :param power_draw_kW: Power drawn from or supplied to the battery (kW)
        :param hvac_cooling_power: Cooling power in kW applied to the battery
        :param hvac_heating_power: Heating power in kW applied to the battery
        :param dt: time step in minutes
        """
        # Very simplified heat generation based on power draw
        heat_generated = 0.01 * power_draw_kW  # arbitrary ratio

        # Net heating/cooling = internal heat - hvac cooling + hvac heating
        net_temp_change = (
            heat_generated
            + (hvac_heating_power * self.heating_rate)
            + (hvac_cooling_power * self.cooling_rate)
        )

        # Multiply by dt (in minutes) to get the actual temperature change
        self.temperature += net_temp_change * dt
        
        # Battery cools or warms passively toward ambient (optional realism)
        ambient_diff = self.ambient_temp - self.temperature
        passive_transfer = 0.001 * ambient_diff  # small factor for passive heat exchange
        self.temperature += passive_transfer * dt

        # Update State of Charge (SoC) - simplified
        self.soc -= (power_draw_kW * dt / 60.0) / self.capacity_kWh * 100.0
        self.soc = max(0, min(100, self.soc))  # clamp between 0% and 100%
