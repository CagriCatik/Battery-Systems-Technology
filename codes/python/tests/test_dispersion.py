import pytest
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.core.pack import PackTopology
from battery_toolkit.core.dispersion import ConnectionSimulator


def test_topology_sweep():
    cell = BatteryCell(
        name="Test Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.7,
        capacity_ah=3.0,
    )
    configs = [(3, 1), (4, 2), (8, 4)]
    results = ConnectionSimulator.simulate_topology_sweep(cell, configs)
    assert len(results) == 3
    assert results[0]["nominal_voltage_v"] == pytest.approx(11.1, 0.05)
    assert results[1]["capacity_ah"] == pytest.approx(6.0, 0.05)


def test_statistical_dispersion():
    cell = BatteryCell(
        name="Test Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.7,
        capacity_ah=5.0,
        r0_mohm=20.0,
    )
    res = ConnectionSimulator.simulate_statistical_dispersion(
        cell=cell,
        topology=PackTopology(num_series=96, num_parallel=4),
        capacity_cov=0.015,
        resistance_cov=0.05,
    )
    assert res["nominal_capacity_ah"] == 20.0
    # Usable capacity should be slightly less than nominal due to dispersion
    assert res["usable_capacity_ah"] <= 20.0
    assert res["capacity_loss_from_dispersion_pct"] >= 0.0
    assert res["max_parallel_current_imbalance_a"] >= 0.0
