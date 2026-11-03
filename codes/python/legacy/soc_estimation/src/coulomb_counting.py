import numpy as np

def coulomb_counting(current, initial_soc, battery_capacity, dt):
    """
    Estimates State of Charge (SoC) using Coulomb Counting.
    
    Parameters:
        current (array): Current data in Amperes.
        initial_soc (float): Initial SoC (0 to 1).
        battery_capacity (float): Battery capacity in Coulombs (Ah * 3600).
        dt (float): Time step in seconds.
    
    Returns:
        soc (array): Estimated SoC over time.
    """
    soc = np.zeros_like(current)
    soc[0] = initial_soc
    for t in range(1, len(current)):
        soc[t] = soc[t-1] - (current[t-1] * dt) / battery_capacity
        soc[t] = np.clip(soc[t], 0, 1)
    return soc
