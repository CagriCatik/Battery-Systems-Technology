"""
thermal_manager.py
Orchestrates updates between Battery, HVAC, and the Controller.
"""

class ThermalManager:
    """
    Orchestrates the updates between Battery, HVAC, and the Controller.
    """
    def __init__(self, battery, hvac, controller):
        self.battery = battery
        self.hvac = hvac
        self.controller = controller

    def step(self, power_draw_kW, dt=1.0):
        """
        Simulate one time step of the integrated thermal management.

        :param power_draw_kW: Power usage by the drivetrain 
                              (+ for discharging, - for charging)
        :param dt: Duration of the timestep in minutes
        """
        # 1. Update cabin temperature passively
        self.hvac.update_cabin_temperature(dt)

        # 2. Determine how much HVAC power goes to heating/cooling the cabin
        self.hvac.apply_hvac_to_cabin(dt)

        # 3. Use the controller to decide how much HVAC to allocate to the battery
        battery_cooling_power, battery_heating_power = self.controller.decide_battery_hvac(
            self.battery, 
            self.hvac
        )

        # 4. Update the battery temperature using the allocated HVAC power
        self.battery.update(power_draw_kW, battery_cooling_power, battery_heating_power, dt)

        # (Optional) Update ambient conditions or other factors
        self.hvac.ambient_temperature = self.battery.ambient_temp
        # You could implement additional logic here to reflect external temperature changes
