import pytest
from battery_toolkit.data import (
    load_battery_dataset,
    load_btms_comparison_dataset,
    load_sizing_results_dataset,
    load_pretrained_soc_model,
)


def test_load_battery_dataset():
    df = load_battery_dataset()
    assert len(df) > 1000
    assert "current" in df.columns
    assert "voltage" in df.columns
    assert "soc_ground_truth" in df.columns


def test_load_btms_comparison_dataset():
    df = load_btms_comparison_dataset()
    assert len(df) >= 3
    assert "System Type" in df.columns


def test_load_sizing_results_dataset():
    df = load_sizing_results_dataset()
    assert len(df) >= 2


def test_load_pretrained_soc_model():
    model = load_pretrained_soc_model()
    assert model is not None

