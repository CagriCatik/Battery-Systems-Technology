"""
controller.py
Defines a high-level ThermalController class that decides
how much heating or cooling the battery needs.
"""

class ThermalController:
    """
    High-level controller that decides how much heating/cooling to allocate
    to the battery vs. the cabin, based on real-time conditions.
    """
    def __init__(self):
        # You might store or track data history, system states, or advanced algorithms here
        pass

    def decide_battery_hvac(self, battery, hvac):
        """
        Decide how much HVAC cooling or heating the battery needs, 
        given the cabin is also using HVAC resources.

        :param battery: Battery object
        :param hvac: HVAC object
        :return: (battery_cooling_power, battery_heating_power)
        """
        battery_diff = hvac.battery_target_temp - battery.temperature
        
        # Calculate the total "temperature difference" for cabin and battery
        cabin_diff = hvac.cabin_target_temp - hvac.cabin_temperature
        total_diff = abs(battery_diff) + abs(cabin_diff)

        if total_diff == 0:
            return (0.0, 0.0)

        # Fraction of HVAC power allocated to battery based on ratio of differences
        battery_ratio = abs(battery_diff) / total_diff

        # Decide if battery needs heating or cooling
        if battery_diff > 0:
            # Battery is too cold -> allocate heating
            desired_heating = battery_ratio * hvac.max_heating_power
            return (0.0, desired_heating)
        else:
            # Battery is too hot -> allocate cooling
            desired_cooling = battery_ratio * hvac.max_cooling_power
            return (desired_cooling, 0.0)
