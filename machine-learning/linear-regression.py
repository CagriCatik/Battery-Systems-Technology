import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Generate or Load Battery Data
# Simulating a dataset with voltage (V), current (A), temperature (°C), and State of Charge (SoC)
np.random.seed(42)
data_size = 1000

voltage = np.random.uniform(3.0, 4.2, data_size)  # Voltage range (typical for Li-ion)
current = np.random.uniform(-5, 5, data_size)  # Current range (charging/discharging)
temperature = np.random.uniform(15, 45, data_size)  # Temperature range in Celsius
soc = (voltage - 3.0) / (4.2 - 3.0) * 100  # Simplified SoC formula for simulation

# Create a DataFrame
battery_data = pd.DataFrame({
    'Voltage': voltage,
    'Current': current,
    'Temperature': temperature,
    'SoC': soc
})

# Step 2: Prepare Data for Training
X = battery_data[['Voltage', 'Current', 'Temperature']]  # Features
y = battery_data['SoC']  # Target (State of Charge)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: Test the Model
y_pred = model.predict(X_test)

# Step 5: Evaluate the Model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Step 6: Predict SoC for New Data
new_data = pd.DataFrame({
    'Voltage': [3.8, 3.5, 4.0],
    'Current': [0.5, -2.0, 1.2],
    'Temperature': [25, 35, 30]
})

soc_predictions = model.predict(new_data)
print("\nPredicted SoC for New Data:")
print(soc_predictions)

# Optional: Visualize Results
import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel("Actual SoC")
plt.ylabel("Predicted SoC")
plt.title("Actual vs Predicted SoC")
plt.grid(True)
plt.show()
