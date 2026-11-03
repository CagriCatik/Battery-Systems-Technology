import matplotlib.pyplot as plt

def plot_soc(time, soc_cc, soc_kf, soc_ml, soc_gt):
    """
    Plots SoC estimations from different methods.
    
    Parameters:
        time (array): Time data in seconds.
        soc_cc (array): SoC from Coulomb Counting.
        soc_kf (array): SoC from Kalman Filter.
        soc_ml (array): SoC from Machine Learning.
        soc_gt (array): Ground Truth SoC.
    """
    plt.figure(figsize=(15, 8))
    plt.plot(time, soc_gt, label='Ground Truth SoC', linestyle='--', color='black')
    plt.plot(time, soc_cc, label='Coulomb Counting', alpha=0.7)
    plt.plot(time, soc_kf, label='Kalman Filter', alpha=0.7)
    plt.plot(time, soc_ml, label='Machine Learning Model', alpha=0.7)
    plt.xlabel('Time (s)')
    plt.ylabel('State of Charge (SoC)')
    plt.title('Battery State of Charge Estimation')
    plt.legend()
    plt.grid(True)
    plt.show()
