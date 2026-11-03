import numpy as np
import pytest
from battery_toolkit.data import load_battery_dataset
from battery_toolkit.state_estimation.ml_estimator import MLSOCEstimator


def test_ml_estimator_training_and_prediction():
    df = load_battery_dataset().iloc[:300] # Use subset for fast test
    current = df["current"].values
    voltage = df["voltage"].values
    soc_gt = df["soc_ground_truth"].values

    estimator = MLSOCEstimator(n_estimators=10, random_state=42)
    estimator.fit(current, voltage, soc_gt)

    preds = estimator.predict(current, voltage)
    assert len(preds) == len(soc_gt)
    assert np.all(preds >= 0.0) and np.all(preds <= 1.0)

    metrics = estimator.evaluate(current, voltage, soc_gt)
    assert metrics["rmse"] < 0.15

