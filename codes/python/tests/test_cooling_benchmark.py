import pytest
from battery_toolkit.thermal.cooling_benchmark import CoolingTechnologyBenchmark


def test_cooling_technology_benchmark():
    bench = CoolingTechnologyBenchmark(
        pack_thermal_mass_j_per_k=100000.0,
        initial_temp_c=28.0,
        ambient_temp_c=25.0,
        heat_generation_w=800.0,
    )
    df = bench.run_full_benchmark(duration_s=1200.0)

    assert len(df) == 4
    # Liquid cooling must result in lower max temperature than Passive Air
    max_t_liquid = df.loc[df["System Type"] == "Liquid Cooling", "Maximum Battery Temperature (°C)"].values[0]
    max_t_passive = df.loc[df["System Type"] == "Passive Air", "Maximum Battery Temperature (°C)"].values[0]
    assert max_t_liquid < max_t_passive
