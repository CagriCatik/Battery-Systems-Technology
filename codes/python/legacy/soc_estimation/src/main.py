import pandas as pd
from data_acquisition import simulate_battery_data, save_simulated_data
from coulomb_counting import coulomb_counting
from kalman_filter import kalman_filter_estimation
from machine_learning import train_ml_model, machine_learning_soc_estimation, load_ml_model
from visualization import plot_soc
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_PATH = "trained_model.pkl"

def main():
    try:
        # Step 1: Simulate Data
        logging.info("Simulating battery data...")
        data = simulate_battery_data()
        save_simulated_data(data)
        logging.info("Data simulation completed and saved as 'data/battery_data.csv'.")

        # Step 2: Coulomb Counting
        logging.info("Performing Coulomb Counting...")
        soc_cc = coulomb_counting(
            current=data['current'].values,
            initial_soc=1.0,
            battery_capacity=3600,
            dt=1
        )
        logging.info("Coulomb Counting completed.")

        # Step 3: Kalman Filter
        logging.info("Performing Kalman Filter estimation...")
        soc_kf = kalman_filter_estimation(
            current=data['current'].values,
            voltage=data['voltage'].values,
            initial_soc=1.0,
            battery_capacity=3600,
            dt=1
        )
        logging.info("Kalman Filter estimation completed.")

        # Step 4: Machine Learning
        logging.info("Preparing data for Machine Learning...")
        X = data[['current', 'voltage']].values
        y = data['soc_ground_truth'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        logging.info("Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        if os.path.exists(MODEL_PATH):
            logging.info(f"Loading trained model from {MODEL_PATH}...")
            model = load_ml_model(MODEL_PATH)
        else:
            logging.info("Training new Machine Learning model...")
            model = train_ml_model(X_train_scaled, y_train, MODEL_PATH)
            logging.info(f"Model trained and saved to {MODEL_PATH}.")

        logging.info("Predicting SoC using Machine Learning model...")
        soc_ml = machine_learning_soc_estimation(
            current=data['current'].values,
            voltage=data['voltage'].values,
            model=model,
            scaler=scaler
        )
        logging.info("Machine Learning prediction completed.")

        # Step 5: Visualization
        logging.info("Generating plots for SoC estimation...")
        plot_soc(
            time=data['time'].values,
            soc_cc=soc_cc,
            soc_kf=soc_kf,
            soc_ml=soc_ml,
            soc_gt=data['soc_ground_truth'].values
        )
        logging.info("Plots generated successfully. Program completed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
