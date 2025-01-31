from filterpy.kalman import KalmanFilter
import numpy as np

def kalman_filter_estimation(current, voltage, initial_soc, battery_capacity, dt):
    """
    Estimates SoC using Kalman Filter (with FilterPy).
    
    Parameters:
        current (array): Current data in Amperes.
        voltage (array): Voltage data in Volts.
        initial_soc (float): Initial SoC (0 to 1).
        battery_capacity (float): Battery capacity in Coulombs.
        dt (float): Time step in seconds.
    
    Returns:
        soc (array): Estimated SoC over time.
    """
    # Initialize Kalman Filter
    kf = KalmanFilter(dim_x=1, dim_z=1)
    
    # Define initial state and matrices
    kf.x = np.array([initial_soc])  # Initial SoC
    kf.F = np.array([[1]])  # State transition matrix
    kf.H = np.array([[1]])  # Measurement function
    kf.P = np.array([[1]])  # Initial uncertainty
    kf.R = np.array([[1]])  # Measurement noise
    kf.Q = np.array([[0.01]])  # Process noise

    # Measurements: Voltage normalized to max voltage (assume linear relation)
    measurements = voltage / 4.2
    soc = []

    for i in range(len(measurements)):
        # Predict phase
        kf.predict()
        
        # Update phase with measurement
        kf.update(measurements[i])
        
        # Adjust SoC using current and store result
        state = kf.x[0]
        if i > 0:
            state -= (current[i-1] * dt) / battery_capacity
        soc.append(np.clip(state, 0, 1))
    
    return np.array(soc)
