"""
Built-in datasets and trained model artifacts for battery systems technology.
"""

from pathlib import Path
import pandas as pd
import joblib

DATA_DIR = Path(__file__).parent


def get_data_path(filename: str) -> Path:
    """Returns absolute path to a packaged data file."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Data file '{filename}' not found in {DATA_DIR}")
    return path


def load_battery_dataset() -> pd.DataFrame:
    """
    Loads empirical battery cycling dataset containing:
    time (s), current (A), voltage (V), soc_ground_truth [0 to 1].
    """
    return pd.read_csv(get_data_path("battery_data.csv"))


def load_btms_comparison_dataset() -> pd.DataFrame:
    """Loads comparative BTMS cooling technology benchmark dataset."""
    return pd.read_csv(get_data_path("btms_performance_comparison.csv"))


def load_sizing_results_dataset() -> pd.DataFrame:
    """Loads reference EV pack sizing configuration results."""
    return pd.read_csv(get_data_path("results.csv"))


def load_pretrained_soc_model():
    """Loads pre-trained Random Forest SOC estimation model."""
    path = get_data_path("trained_model.pkl")
    return joblib.load(path)

