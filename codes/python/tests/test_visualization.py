import numpy as np
import pytest
from battery_toolkit.visualization.radar import create_spider_chart, plot_chemistry_radar_comparison
from battery_toolkit.visualization.plotting import (
    plot_soc_comparison,
    plot_configurations_bar_chart,
    plot_thermal_profiles,
)


def test_spider_chart_creation():
    fig = create_spider_chart(
        categories=["Energy", "Power", "Safety", "Life", "Cost"],
        values=[8, 7, 9, 6, 8],
        title="Test Radar",
        show=False,
    )
    assert fig is not None


def test_chemistry_radar_comparison():
    fig = plot_chemistry_radar_comparison(show=False)
    assert fig is not None


def test_plot_soc_comparison():
    t = np.linspace(0, 100, 101)
    gt = np.linspace(1.0, 0.5, 101)
    est = gt + 0.02
    fig = plot_soc_comparison(t, gt, soc_kalman_filter=est, show=False)
    assert fig is not None


def test_plot_configurations_bar_chart():
    fig = plot_configurations_bar_chart(
        configurations=["3S1P", "4S2P", "8S4P"],
        voltages=[11.1, 14.8, 29.6],
        capacities_ah=[3.0, 6.0, 12.0],
        show=False,
    )
    assert fig is not None


def test_plot_thermal_profiles():
    t = np.linspace(0, 60, 61)
    t_batt = np.linspace(25, 38, 61)
    t_cab = np.linspace(35, 22, 61)
    p = np.full_like(t, 25.0)
    fig = plot_thermal_profiles(t, t_batt, t_cab, p, show=False)
    assert fig is not None
