import math
from dataclasses import dataclass


@dataclass
class VehicleParameters:
    """
    Longitudinal vehicle dynamics parameters for tractive energy estimation.
    """
    curb_weight_kg: float = 1900.0        # Mass of vehicle without battery pack (or baseline)
    drag_coefficient: float = 0.23        # Aerodynamic drag coefficient Cd
    frontal_area_m2: float = 2.20         # Frontal cross-sectional area Af (m^2)
    rolling_resistance_coeff: float = 0.009 # Crr (low-resistance EV tires)
    air_density_kg_per_m3: float = 1.225  # Air density at sea level, 15°C
    gravity_m_per_s2: float = 9.80665     # Gravitational acceleration
    drivetrain_efficiency: float = 0.90   # Inverter + Motor + Transmission combined efficiency
    regen_braking_efficiency: float = 0.70# Fraction of kinetic deceleration energy recaptured
    auxiliary_load_kw: float = 0.80       # Continuous HVAC + 12V electronics electrical load

    def tractive_force_n(
        self,
        velocity_kmh: float,
        acceleration_m_per_s2: float = 0.0,
        grade_rad: float = 0.0,
        total_mass_kg: float = 2200.0,
    ) -> float:
        """
        Calculates total longitudinal tractive resistance force at the wheels:
        F_total = F_aero + F_rolling + F_grade + F_acceleration
        """
        v_ms = velocity_kmh / 3.6

        # Aerodynamic Drag Force: 0.5 * rho * Cd * Af * v^2
        f_aero = 0.5 * self.air_density_kg_per_m3 * self.drag_coefficient * self.frontal_area_m2 * (v_ms ** 2)

        # Rolling Resistance Force: m * g * Crr * cos(theta)
        f_rolling = total_mass_kg * self.gravity_m_per_s2 * self.rolling_resistance_coeff * math.cos(grade_rad)

        # Gradient / Gravity Climbing Force: m * g * sin(theta)
        f_grade = total_mass_kg * self.gravity_m_per_s2 * math.sin(grade_rad)

        # Inertial Acceleration Force: m * a
        f_accel = total_mass_kg * acceleration_m_per_s2

        return f_aero + f_rolling + f_grade + f_accel

    def mechanical_power_demand_kw(
        self,
        velocity_kmh: float,
        acceleration_m_per_s2: float = 0.0,
        total_mass_kg: float = 2200.0,
    ) -> float:
        """Mechanical power required at the wheels (kW)."""
        v_ms = velocity_kmh / 3.6
        force_n = self.tractive_force_n(velocity_kmh, acceleration_m_per_s2, total_mass_kg=total_mass_kg)
        return (force_n * v_ms) / 1000.0

    def electrical_power_demand_kw(
        self,
        velocity_kmh: float,
        acceleration_m_per_s2: float = 0.0,
        total_mass_kg: float = 2200.0,
    ) -> float:
        """
        Electrical power required from the high-voltage battery pack (kW),
        including drivetrain losses and auxiliary HVAC load.
        """
        p_mech = self.mechanical_power_demand_kw(velocity_kmh, acceleration_m_per_s2, total_mass_kg)
        if p_mech >= 0.0:
            # Traction mode
            return (p_mech / self.drivetrain_efficiency) + self.auxiliary_load_kw
        else:
            # Regenerative braking mode
            return (p_mech * self.regen_braking_efficiency) + self.auxiliary_load_kw

    def steady_state_consumption_wh_per_km(
        self,
        velocity_kmh: float,
        total_mass_kg: float = 2200.0,
    ) -> float:
        """Steady-state electrical consumption in Wh/km at a constant speed."""
        p_elec_kw = self.electrical_power_demand_kw(velocity_kmh, 0.0, total_mass_kg)
        # Time to travel 1 km = 1 / v_kmh (hours)
        hours_per_km = 1.0 / max(velocity_kmh, 1e-3)
        return p_elec_kw * 1000.0 * hours_per_km
