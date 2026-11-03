import tempfile
from pathlib import Path
import pytest
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.core.pack import BatteryPack, PackTopology
from battery_toolkit.sizing.pack_geometry import PackGeometryCalculator


def test_pack_geometry_dimensions():
    cell = BatteryCell(
        name="21700 Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.65,
        capacity_ah=5.0,
        diameter_mm=21.0,
        length_mm=70.0,
    )
    pack = BatteryPack(cell=cell, topology=PackTopology(num_series=96, num_parallel=4)) # 384 cells

    geo_hex = PackGeometryCalculator.calculate_cylindrical_layout(pack, hexagonal_packing=True)
    assert geo_hex.length_mm > 0.0
    assert geo_hex.width_mm > 0.0
    assert geo_hex.height_mm > 70.0
    assert geo_hex.enclosure_volume_liters > 0.0
    assert geo_hex.volumetric_packaging_efficiency > 0.3

    geo_ortho = PackGeometryCalculator.calculate_cylindrical_layout(pack, hexagonal_packing=False)
    # Hexagonal packing should be more compact than orthogonal grid
    assert geo_hex.enclosure_volume_liters <= geo_ortho.enclosure_volume_liters


def test_pack_geometry_csv_export():
    cell = BatteryCell(
        name="21700 Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=3.65,
        capacity_ah=5.0,
    )
    pack = BatteryPack(cell=cell, topology=PackTopology(num_series=96, num_parallel=4))
    with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
        PackGeometryCalculator.export_sizing_to_csv(pack, tmp.name)
        assert Path(tmp.name).stat().st_size > 50

