from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, mean_absolute_error


class MLSOCEstimator:
    """
    Machine Learning-based State of Charge (SOC) estimator.
    Uses multi-feature regression (current, voltage, moving averages)
    to predict instantaneous SOC.
    """
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state, n_jobs=-1)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def prepare_features(self, current: np.ndarray, voltage: np.ndarray) -> np.ndarray:
        """Constructs 2D feature matrix from electrical telemetry."""
        return np.column_stack((current, voltage))

    def fit(self, current: np.ndarray, voltage: np.ndarray, soc_ground_truth: np.ndarray) -> "MLSOCEstimator":
        """Fits scaler and Random Forest model on training telemetry."""
        X = self.prepare_features(current, voltage)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, soc_ground_truth)
        self.is_fitted = True
        return self

    def predict(self, current: np.ndarray, voltage: np.ndarray) -> np.ndarray:
        """Predicts SOC from current and voltage inputs."""
        if not self.is_fitted:
            raise RuntimeError("MLSOCEstimator must be fitted before predict.")
        X = self.prepare_features(current, voltage)
        X_scaled = self.scaler.transform(X)
        soc_pred = self.model.predict(X_scaled)
        return np.clip(soc_pred, 0.0, 1.0)

    def evaluate(self, current_test: np.ndarray, voltage_test: np.ndarray, soc_test: np.ndarray) -> Dict[str, float]:
        """Evaluates prediction accuracy returning RMSE and MAE."""
        preds = self.predict(current_test, voltage_test)
        rmse = float(root_mean_squared_error(soc_test, preds))
        mae = float(mean_absolute_error(soc_test, preds))
        return {"rmse": round(rmse, 4), "mae": round(mae, 4), "rmse_percentage": round(rmse * 100.0, 2)}

    def save(self, filepath: str | Path) -> None:
        """Serializes trained model and scaler to disk."""
        data = {"model": self.model, "scaler": self.scaler, "is_fitted": self.is_fitted}
        joblib.dump(data, filepath)

    @classmethod
    def load(cls, filepath: str | Path) -> "MLSOCEstimator":
        """Loads serialized model and scaler from disk."""
        data = joblib.load(filepath)
        # Check if saved artifact is dictionary or legacy pure model
        inst = cls()
        if isinstance(data, dict) and "model" in data:
            inst.model = data["model"]
            inst.scaler = data["scaler"]
            inst.is_fitted = data["is_fitted"]
        else:
            # Legacy raw model
            inst.model = data
            inst.is_fitted = True
        return inst

