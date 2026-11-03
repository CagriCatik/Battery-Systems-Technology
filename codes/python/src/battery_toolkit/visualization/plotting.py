from typing import List, Optional
import numpy as np
import matplotlib.pyplot as plt


def plot_soc_comparison(
    time_s: np.ndarray,
    soc_ground_truth: np.ndarray,
    soc_coulomb_counting: Optional[np.ndarray] = None,
    soc_kalman_filter: Optional[np.ndarray] = None,
    soc_machine_learning: Optional[np.ndarray] = None,
    title: str = "Battery State of Charge Estimation Benchmark",
    filename: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """
    Plots multi-estimator SOC tracking comparison against ground truth.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    ax1.plot(time_s, soc_ground_truth * 100.0, label="Ground Truth SOC", color="black", linestyle="--", linewidth=2)

    if soc_coulomb_counting is not None:
        ax1.plot(time_s, soc_coulomb_counting * 100.0, label="Coulomb Counting", color="#1f77b4", alpha=0.8)
        err_cc = (soc_coulomb_counting - soc_ground_truth) * 100.0
        ax2.plot(time_s, err_cc, label="CC Error", color="#1f77b4", alpha=0.7)

    if soc_kalman_filter is not None:
        ax1.plot(time_s, soc_kalman_filter * 100.0, label="Kalman Filter (EKF/UKF)", color="#2ca02c", linewidth=1.5)
        err_kf = (soc_kalman_filter - soc_ground_truth) * 100.0
        ax2.plot(time_s, err_kf, label="KF Error", color="#2ca02c", linewidth=1.5)

    if soc_machine_learning is not None:
        ax1.plot(time_s, soc_machine_learning * 100.0, label="Machine Learning", color="#d62728", alpha=0.8)
        err_ml = (soc_machine_learning - soc_ground_truth) * 100.0
        ax2.plot(time_s, err_ml, label="ML Error", color="#d62728", alpha=0.8)

    ax1.set_ylabel("SOC (%)", fontsize=11)
    ax1.set_title(title, fontsize=13)
    ax1.legend(loc="best")
    ax1.grid(True, linestyle="--", alpha=0.6)

    ax2.set_xlabel("Time (seconds)", fontsize=11)
    ax2.set_ylabel("Error (%)", fontsize=11)
    ax2.axhline(0, color="gray", linestyle=":")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(loc="best")

    fig.tight_layout()

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_configurations_bar_chart(
    configurations: List[str],
    voltages: List[float],
    capacities_ah: List[float],
    filename: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """
    Plots comparative bar charts across battery pack series-parallel configurations.
    """
    x = np.arange(len(configurations))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    rects1 = ax1.bar(x - width / 2, voltages, width, label="Pack Voltage (V)", color="#1f77b4", alpha=0.85)
    rects2 = ax2.bar(x + width / 2, capacities_ah, width, label="Capacity (Ah)", color="#2ca02c", alpha=0.85)

    ax1.set_xlabel("Configuration Topology", fontsize=11)
    ax1.set_ylabel("Voltage (V)", color="#1f77b4", fontsize=11)
    ax2.set_ylabel("Capacity (Ah)", color="#2ca02c", fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(configurations, fontsize=10)
    ax1.set_title("Voltage & Capacity Across Pack Topologies", fontsize=13)
    ax1.grid(axis="y", linestyle="--", alpha=0.6)

    fig.tight_layout()

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_thermal_profiles(
    time_minutes: np.ndarray,
    battery_temp_c: np.ndarray,
    cabin_temp_c: np.ndarray,
    power_draw_kw: np.ndarray,
    filename: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """
    Plots coupled battery and cabin HVAC thermal profiles.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.plot(time_minutes, battery_temp_c, label="Battery Temp (°C)", color="#d62728", linewidth=2)
    ax1.plot(time_minutes, cabin_temp_c, label="Cabin Temp (°C)", color="#1f77b4", linewidth=2)
    ax1.axhline(35.0, color="orange", linestyle="--", label="Cooling Threshold (35°C)")
    ax1.axhline(22.0, color="green", linestyle=":", label="Comfort Setpoint (22°C)")
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.set_title("Coupled BMS & Cabin Thermal Dynamics", fontsize=13)
    ax1.legend(loc="best")
    ax1.grid(True, linestyle="--", alpha=0.6)

    ax2.plot(time_minutes, power_draw_kw, label="Electrical Power Draw (kW)", color="#2ca02c", alpha=0.8)
    ax2.set_xlabel("Time (minutes)", fontsize=11)
    ax2.set_ylabel("Power (kW)", fontsize=11)
    ax2.legend(loc="best")
    ax2.grid(True, linestyle="--", alpha=0.6)

    fig.tight_layout()

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig
