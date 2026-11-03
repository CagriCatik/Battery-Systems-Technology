import pytest
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.sizing.vehicle import VehicleParameters
from battery_toolkit.sizing.optimizer import PackSizingOptimizer, SizingRequirements


def test_vehicle_longitudinal_force():
    veh = VehicleParameters(
        curb_weight_kg=1800.0,
        drag_coefficient=0.23,
        frontal_area_m2=2.2,
    )
    # At zero velocity and zero acceleration, tractive force is purely rolling resistance
    f_roll = veh.tractive_force_n(velocity_kmh=0.0, acceleration_m_per_s2=0.0, total_mass_kg=2000.0)
    expected_f = 2000.0 * 9.80665 * 0.009
    assert f_roll == pytest.approx(expected_f, 0.1)

    # Power demand at 100 km/h
    p_elec = veh.electrical_power_demand_kw(velocity_kmh=100.0, total_mass_kg=2000.0)
    assert p_elec > 5.0 and p_elec < 30.0


def test_pack_sizing_optimizer():
    cell = BatteryCell(
        name="High Energy Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.7,
        capacity_ah=5.0,
        mass_g=70.0,
    )
    veh = VehicleParameters()
    opt = PackSizingOptimizer(cell, veh)

    pack = opt.size_pack(desired_energy_kwh=60.0, system_voltage=400.0, buffer_percentage=10.0)
    assert pack.topology.num_series == 109 # ceil(400 / 3.7)
    assert pack.nominal_energy_kwh >= 60.0
    assert pack.v_max_v > 400.0
