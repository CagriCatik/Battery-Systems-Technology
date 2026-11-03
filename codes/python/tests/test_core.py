import pytest
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.core.pack import BatteryPack, PackTopology
from battery_toolkit.core.units import kw_to_hp, hp_to_kw, celsius_to_kelvin


def test_battery_cell_properties():
    cell = BatteryCell(
        name="Test NMC Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.65,
        capacity_ah=5.0,
        mass_g=70.0,
        r0_mohm=20.0,
    )
    assert cell.nominal_energy_wh == pytest.approx(18.25, 0.01)
    assert cell.gravimetric_energy_density_wh_per_kg == pytest.approx(260.71, 0.1)
    assert cell.max_continuous_current_a == 10.0


def test_battery_pack_topology():
    cell = BatteryCell(
        name="Test Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.60,
        capacity_ah=5.0,
        r0_mohm=20.0,
        mass_g=70.0,
    )
    pack = BatteryPack(cell=cell, topology=PackTopology(num_series=96, num_parallel=2))

    assert pack.total_cells == 192
    assert pack.nominal_voltage_v == pytest.approx(345.6, 0.1)
    assert pack.capacity_ah == 10.0
    assert pack.nominal_energy_kwh == pytest.approx(3.456, 0.01)
    assert pack.cell_mass_kg == pytest.approx(13.44, 0.01)


def test_unit_conversions():
    assert kw_to_hp(100.0) == pytest.approx(134.10, 0.05)
    assert hp_to_kw(134.102209) == pytest.approx(100.0, 0.05)
    assert celsius_to_kelvin(25.0) == 298.15

