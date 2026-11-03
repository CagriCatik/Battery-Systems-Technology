from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import joblib

def train_ml_model(X_train, y_train, model_path=None):
    """
    Trains a Machine Learning model for SoC prediction and optionally saves it.

    Parameters:
        X_train (array): Training features.
        y_train (array): Training target (SoC).
        model_path (str, optional): Path to save the trained model. If None, the model is not saved.

    Returns:
        model (RandomForestRegressor): Trained ML model.
    """
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model if a path is provided
    if model_path:
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")

    return model

def machine_learning_soc_estimation(current, voltage, model, scaler):
    """
    Estimates SoC using a trained ML model.
    
    Parameters:
        current (array): Current data in Amperes.
        voltage (array): Voltage data in Volts.
        model: Trained Machine Learning model.
        scaler: Scaler for feature normalization.
    
    Returns:
        soc (array): Predicted SoC over time.
    """
    X = np.column_stack((current, voltage))
    X_scaled = scaler.transform(X)
    soc_pred = model.predict(X_scaled)
    return np.clip(soc_pred, 0, 1)

def load_ml_model(model_path="trained_model.pkl"):
    """
    Loads a trained Machine Learning model from a file.

    Parameters:
        model_path (str): Path to the saved model.

    Returns:
        model: Loaded ML model.
    """
    try:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        return model
    except FileNotFoundError:
        print(f"Model file not found at {model_path}. Train the model first.")
        return None