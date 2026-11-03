import pytest
from battery_toolkit.thermal.cabin_hvac import CabinHVACModel, IntegratedThermalManager


def test_cabin_hvac_cooling():
    cabin = CabinHVACModel(cabin_temp_c=35.0, target_temp_c=22.0)
    # Apply full cooling effort for 5 minutes
    new_t = cabin.step(ambient_temp_c=30.0, cooling_effort=1.0, dt_min=5.0)
    assert new_t < 35.0


def test_integrated_thermal_manager():
    itm = IntegratedThermalManager(battery_capacity_kwh=50.0, initial_battery_temp_c=25.0, initial_cabin_temp_c=35.0)
    state = itm.step(vehicle_traction_power_kw=20.0, dt_min=5.0)

    assert state.cabin_temp_c < 35.0
    assert state.battery_soc_percent < 100.0
    assert state.power_draw_kw > 20.0 # Traction + HVAC compressor

