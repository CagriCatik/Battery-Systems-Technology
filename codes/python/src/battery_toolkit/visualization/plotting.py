from typing import List, Optional, Dict, Any
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def set_engineering_style():
    """Applies clean engineering styling to matplotlib figures."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 14,
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
    })


def plot_sizing_tradeoffs(
    speeds_kmh: np.ndarray,
    powers_kw: np.ndarray,
    consumptions_wh_per_km: np.ndarray,
    ranges_km: Dict[str, np.ndarray],
    pack_breakdown: Dict[str, float],
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots vehicle longitudinal power requirements, energy consumption, and pack mass distribution.
    """
    set_engineering_style()
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

    # Subplot 1: Speed vs Tractive Power
    ax1.plot(speeds_kmh, powers_kw, color="#1f77b4", linewidth=2.2, label="Total Tractive Power")
    ax1.set_xlabel("Cruising Speed (km/h)")
    ax1.set_ylabel("Power Demand (kW)")
    ax1.set_title("Longitudinal Road-Load Power", fontweight="bold")
    ax1.grid(True)
    ax1.legend(loc="upper left")

    # Subplot 2: Speed vs Energy Consumption & Range
    ax2.plot(speeds_kmh, consumptions_wh_per_km, color="#d62728", linewidth=2.2, label="Consumption (Wh/km)")
    ax2.set_xlabel("Cruising Speed (km/h)")
    ax2.set_ylabel("Consumption (Wh/km)", color="#d62728")
    ax2.tick_params(axis="y", labelcolor="#d62728")

    ax2_twin = ax2.twinx()
    colors = ["#2ca02c", "#ff7f0e", "#9467bd"]
    for idx, (label, range_arr) in enumerate(ranges_km.items()):
        ax2_twin.plot(speeds_kmh, range_arr, linestyle="--", color=colors[idx % len(colors)], label=label)
    ax2_twin.set_ylabel("Driving Range (km)", color="#2ca02c")
    ax2_twin.tick_params(axis="y", labelcolor="#2ca02c")
    ax2.set_title("Consumption & Range Sensitivity", fontweight="bold")
    ax2_twin.legend(loc="lower left", fontsize=8)

    # Subplot 3: Pack Mass Breakdown Pie/Donut Chart
    labels = list(pack_breakdown.keys())
    masses = list(pack_breakdown.values())
    pie_colors = ["#3366cc", "#dc3912", "#ff9900", "#109618"]
    wedges, texts, autotexts = ax3.pie(
        masses,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=pie_colors[:len(labels)],
        wedgeprops=dict(width=0.45, edgecolor="w", linewidth=1.5),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_weight("bold")
    ax3.set_title("Pack Mass Breakdown", fontweight="bold")

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_ecm_hppc_fit(
    time_s: np.ndarray,
    current_a: np.ndarray,
    voltage_true: np.ndarray,
    voltage_model: np.ndarray,
    r0_m_ohm: float,
    r1_m_ohm: float,
    c1_f: float,
    r2_m_ohm: float,
    c2_f: float,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots HPPC pulse excitation, true vs model voltage response, and residual error.
    """
    set_engineering_style()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=True, gridspec_kw={"height_ratios": [1, 2, 1]})

    # 1. Current Profile
    ax1.plot(time_s, current_a, color="#1f77b4", linewidth=1.8, label="Current Pulse (A)")
    ax1.set_ylabel("Current (A)")
    ax1.set_title("HPPC Pulse Response & 2-RC Dual Polarization Parameter Identification", fontweight="bold")
    ax1.grid(True)
    ax1.legend(loc="upper right")

    # 2. Voltage Response
    ax2.plot(time_s, voltage_true, color="black", linewidth=2.0, label="Experimental Cell Voltage")
    ax2.plot(time_s, voltage_model, color="#ff7f0e", linestyle="--", linewidth=2.0, label="Identified 2-RC Model")
    ax2.set_ylabel("Terminal Voltage (V)")
    ax2.grid(True)
    param_text = (
        f"$R_0 = {r0_m_ohm:.2f}\\,\\mathrm{{m\\Omega}}$\n"
        f"$R_1 = {r1_m_ohm:.2f}\\,\\mathrm{{m\\Omega}},\\; C_1 = {c1_f:.0f}\\,\\mathrm{{F}}\\; (\\tau_1 = {r1_m_ohm*c1_f/1000:.1f}\\,\\mathrm{{s}})$\n"
        f"$R_2 = {r2_m_ohm:.2f}\\,\\mathrm{{m\\Omega}},\\; C_2 = {c2_f:.0f}\\,\\mathrm{{F}}\\; (\\tau_2 = {r2_m_ohm*c2_f/1000:.1f}\\,\\mathrm{{s}})$"
    )
    ax2.text(0.02, 0.15, param_text, transform=ax2.transAxes, fontsize=9,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="gray"))
    ax2.legend(loc="upper right")

    # 3. Residual Error (mV)
    residual_mv = (voltage_model - voltage_true) * 1000.0
    ax3.plot(time_s, residual_mv, color="#d62728", linewidth=1.5, label="Residual Error ($V_{model} - V_{exp}$)")
    ax3.axhline(0.0, color="gray", linestyle=":")
    ax3.set_xlabel("Time (seconds)")
    ax3.set_ylabel("Error (mV)")
    ax3.grid(True)
    ax3.legend(loc="upper right")

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_soc_estimation_benchmark(
    time_s: np.ndarray,
    current_a: np.ndarray,
    soc_ground_truth: np.ndarray,
    soc_coulomb_counting: Optional[np.ndarray] = None,
    soc_ekf: Optional[np.ndarray] = None,
    soc_ukf: Optional[np.ndarray] = None,
    soc_ml: Optional[np.ndarray] = None,
    ekf_sigma_bounds: Optional[np.ndarray] = None,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots multi-algorithm SOC tracking benchmark: True SOC, Estimator Tracks, Residual Errors, and Kalman Covariance Bounds.
    """
    set_engineering_style()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True, gridspec_kw={"height_ratios": [1, 2.5, 1.5]})

    # 1. Drive Current
    ax1.plot(time_s, current_a, color="#333333", linewidth=1.2, label="Dynamic Pack Current (A)")
    ax1.set_ylabel("Current (A)")
    ax1.set_title("Nonlinear State of Charge Estimation Benchmark (EKF vs UKF vs CC vs ML)", fontweight="bold")
    ax1.grid(True)
    ax1.legend(loc="upper right")

    # 2. State of Charge Tracks
    ax2.plot(time_s, soc_ground_truth * 100.0, label="Ground Truth SOC", color="black", linestyle="--", linewidth=2.2)

    if soc_coulomb_counting is not None:
        ax2.plot(time_s, soc_coulomb_counting * 100.0, label="Coulomb Counting (Drift)", color="#1f77b4", alpha=0.85, linewidth=1.6)

    if soc_ekf is not None:
        ax2.plot(time_s, soc_ekf * 100.0, label="Extended Kalman Filter (EKF)", color="#2ca02c", linewidth=2.0)
        if ekf_sigma_bounds is not None:
            upper = (soc_ekf + 3 * ekf_sigma_bounds) * 100.0
            lower = (soc_ekf - 3 * ekf_sigma_bounds) * 100.0
            ax2.fill_between(time_s, lower, upper, color="#2ca02c", alpha=0.15, label=r"EKF $\pm 3\sigma$ Bounds")

    if soc_ukf is not None:
        ax2.plot(time_s, soc_ukf * 100.0, label="Unscented Kalman Filter (UKF)", color="#9467bd", linestyle="-.", linewidth=1.8)

    if soc_ml is not None:
        ax2.plot(time_s, soc_ml * 100.0, label="Random Forest ML Estimator", color="#ff7f0e", linestyle=":", linewidth=2.0)

    ax2.set_ylabel("State of Charge (%)")
    ax2.grid(True)
    ax2.legend(loc="upper right", fontsize=9)

    # 3. Residual Tracking Error (%)
    if soc_coulomb_counting is not None:
        err_cc = (soc_coulomb_counting - soc_ground_truth) * 100.0
        ax3.plot(time_s, err_cc, color="#1f77b4", label=f"CC (Final Err: {err_cc[-1]:.2f}%)", alpha=0.85)

    if soc_ekf is not None:
        err_ekf = (soc_ekf - soc_ground_truth) * 100.0
        rmse_ekf = np.sqrt(np.mean(err_ekf ** 2))
        ax3.plot(time_s, err_ekf, color="#2ca02c", linewidth=1.8, label=f"EKF (RMSE: {rmse_ekf:.2f}%)")

    if soc_ukf is not None:
        err_ukf = (soc_ukf - soc_ground_truth) * 100.0
        rmse_ukf = np.sqrt(np.mean(err_ukf ** 2))
        ax3.plot(time_s, err_ukf, color="#9467bd", linestyle="-.", label=f"UKF (RMSE: {rmse_ukf:.2f}%)")

    if soc_ml is not None:
        err_ml = (soc_ml - soc_ground_truth) * 100.0
        rmse_ml = np.sqrt(np.mean(err_ml ** 2))
        ax3.plot(time_s, err_ml, color="#ff7f0e", linestyle=":", label=f"ML (RMSE: {rmse_ml:.2f}%)")

    ax3.axhline(0.0, color="black", linestyle="--", linewidth=0.8)
    ax3.set_xlabel("Time (seconds)")
    ax3.set_ylabel("Estimation Error (%)")
    ax3.grid(True)
    ax3.legend(loc="lower right", fontsize=8)

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_cell_balancing_dynamics(
    time_s: np.ndarray,
    cell_voltages_v: np.ndarray,
    active_channels_count: np.ndarray,
    total_pcb_dissipation_w: np.ndarray,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots multi-cell voltage balancing equalization and PCB thermal power dissipation.
    """
    set_engineering_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [2.5, 1.2]})

    num_cells = cell_voltages_v.shape[1]
    cmap = matplotlib.colormaps["viridis"].resampled(num_cells)

    for c in range(num_cells):
        ax1.plot(time_s, cell_voltages_v[:, c], color=cmap(c), alpha=0.75, linewidth=1.2)

    ax1.set_ylabel("Cell Voltage (V)")
    ax1.set_title("Multi-Channel Passive Cell Balancing Dynamics (16S Pack)", fontweight="bold")
    ax1.grid(True)

    # Subplot 2: Active balancing channels & Dissipation
    color_bar = "#d62728"
    ax2.plot(time_s, total_pcb_dissipation_w, color=color_bar, linewidth=2.0, label="PCB Thermal Dissipation (W)")
    ax2.set_xlabel("Balancing Time (seconds)")
    ax2.set_ylabel("Power Loss (W)", color=color_bar)
    ax2.tick_params(axis="y", labelcolor=color_bar)
    ax2.grid(True)

    ax2_twin = ax2.twinx()
    color_chan = "#1f77b4"
    ax2_twin.step(time_s, active_channels_count, color=color_chan, where="post", linewidth=1.5, label="Active Bleed Channels")
    ax2_twin.set_ylabel("Active Channels", color=color_chan)
    ax2_twin.tick_params(axis="y", labelcolor=color_chan)

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_btms_thermal_simulation(
    time_s: np.ndarray,
    current_a: np.ndarray,
    t_core_c: np.ndarray,
    t_casing_c: np.ndarray,
    t_coolant_c: np.ndarray,
    q_joule_w: np.ndarray,
    q_entropic_w: np.ndarray,
    btms_flow_lpm: np.ndarray,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots fast-charging electro-thermal cell response with BTMS closed-loop cooling.
    """
    set_engineering_style()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=True, gridspec_kw={"height_ratios": [1, 2, 1.2]})

    # 1. Fast Charging Current
    ax1.plot(time_s, current_a, color="#333333", linewidth=1.8, label="Fast-Charging Current (A)")
    ax1.set_ylabel("Current (A)")
    ax1.set_title("Fast-Charging Coupled Electro-Thermal Cell Response & BTMS Regulation", fontweight="bold")
    ax1.grid(True)
    ax1.legend(loc="upper right")

    # 2. Temperature Transients
    ax2.plot(time_s, t_core_c, color="#d62728", linewidth=2.2, label=r"Core Temperature $T_{\mathrm{core}}$")
    ax2.plot(time_s, t_casing_c, color="#ff7f0e", linewidth=1.8, label=r"Casing Temperature $T_{\mathrm{case}}$")
    ax2.plot(time_s, t_coolant_c, color="#1f77b4", linestyle="--", linewidth=1.6, label=r"Coolant Temperature $T_{\mathrm{cool}}$")
    ax2.axhline(45.0, color="darkred", linestyle=":", linewidth=1.5, label="Safety Limit ($45^{\\circ}\\mathrm{C}$)")
    ax2.set_ylabel("Temperature (°C)")
    ax2.grid(True)
    ax2.legend(loc="upper left")

    # 3. Heat Generation Breakdown & Flow Rate
    ax3.plot(time_s, q_joule_w, color="#e377c2", label=r"Joule Heat ($I^2 R_0$)", linewidth=1.5)
    ax3.plot(time_s, q_entropic_w, color="#8c564b", label=r"Reversible Entropic ($I T \frac{\partial U}{\partial T}$)", linewidth=1.5)
    ax3.plot(time_s, q_joule_w + q_entropic_w, color="#2ca02c", linewidth=2.0, label="Total Heat Generated")
    ax3.set_xlabel("Time (seconds)")
    ax3.set_ylabel("Heat Rate (W)")
    ax3.grid(True)
    ax3.legend(loc="upper left")

    ax3_twin = ax3.twinx()
    ax3_twin.plot(time_s, btms_flow_lpm, color="#17becf", linestyle="-.", linewidth=1.6, label="Coolant Flow (L/min)")
    ax3_twin.set_ylabel("Coolant Flow (L/min)", color="#17becf")
    ax3_twin.tick_params(axis="y", labelcolor="#17becf")
    ax3_twin.legend(loc="upper right")

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_cooling_technology_comparison(
    benchmark_df: Any,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots BTMS comparative technology metrics: Maximum Battery Temp, Energy Consumed, and COP Ratio.
    """
    set_engineering_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    system_types = benchmark_df["System Type"].tolist()
    max_temps = benchmark_df["Maximum Battery Temperature (°C)"].tolist()
    energies_kj = (benchmark_df["Total Energy Consumed (J)"] / 1000.0).tolist()
    cop_values = benchmark_df["COP Efficiency Ratio"].tolist()

    x = np.arange(len(system_types))
    colors = ["#7f7f7f", "#1f77b4", "#2ca02c", "#ff7f0e"]

    # Bar chart: Maximum Battery Temperature
    bars1 = ax1.bar(x, max_temps, color=colors, alpha=0.85, width=0.55, edgecolor="black")
    ax1.axhline(35.0, color="red", linestyle="--", linewidth=1.2, label="Optimal Upper Limit ($35^{\\circ}\\mathrm{C}$)")
    ax1.set_ylabel("Maximum Battery Temperature (°C)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(system_types, rotation=15, ha="right")
    ax1.set_title("Thermal Dissipation Performance", fontweight="bold")
    ax1.grid(axis="y")
    ax1.legend(loc="upper right")
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval + 0.3, f"{yval:.1f}°C", ha="center", va="bottom", fontsize=9, fontweight="bold")

    # Bar chart: Energy Consumed vs COP
    width = 0.35
    bars2 = ax2.bar(x - width / 2, energies_kj, width, label="Parasitic Energy (kJ)", color="#e377c2", alpha=0.85)
    ax2.set_ylabel("Energy Consumed (kJ)", color="#e377c2")
    ax2.tick_params(axis="y", labelcolor="#e377c2")
    ax2.set_xticks(x)
    ax2.set_xticklabels(system_types, rotation=15, ha="right")
    ax2.set_title("Auxiliary Energy & System COP", fontweight="bold")
    ax2.grid(axis="y")

    ax2_twin = ax2.twinx()
    cop_display = [min(c, 10.0) for c in cop_values]
    bars3 = ax2_twin.bar(x + width / 2, cop_display, width, label="System COP", color="#17becf", alpha=0.85)
    ax2_twin.set_ylabel("COP Efficiency Ratio", color="#17becf")
    ax2_twin.tick_params(axis="y", labelcolor="#17becf")

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


def plot_state_machine_execution(
    time_s: np.ndarray,
    v_pack_v: np.ndarray,
    v_link_v: np.ndarray,
    states: List[str],
    k_minus: np.ndarray,
    k_pre: np.ndarray,
    k_plus: np.ndarray,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Plots ASIL-D Precharge State Machine sequence: Link Voltage Ramp and Contactor Statuses.
    """
    set_engineering_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True, gridspec_kw={"height_ratios": [2, 1.2]})

    # 1. Voltage curves
    ax1.plot(time_s, v_pack_v, color="black", linestyle="--", linewidth=1.8, label="Battery Pack Voltage ($V_{pack}$)")
    ax1.plot(time_s, v_link_v, color="#1f77b4", linewidth=2.2, label="DC Link Inverter Voltage ($V_{link}$)")
    ax1.axhline(0.95 * v_pack_v[0], color="#2ca02c", linestyle=":", label="95% Precharge Threshold")
    ax1.set_ylabel("Voltage (V)")
    ax1.set_title("ASIL-D Contactor Precharge Sequencing & State Transitions", fontweight="bold")
    ax1.grid(True)
    ax1.legend(loc="center right")

    # 2. Contactor Logic States
    ax2.step(time_s, k_minus + 2.4, label="Negative Contactor ($K_-$)", color="#333333", where="post", linewidth=1.8)
    ax2.step(time_s, k_pre + 1.2, label="Precharge Contactor ($K_{pre}$)", color="#ff7f0e", where="post", linewidth=1.8)
    ax2.step(time_s, k_plus, label="Main Positive Contactor ($K_+$)", color="#2ca02c", where="post", linewidth=1.8)

    ax2.set_xlabel("Time (seconds)")
    ax2.set_yticks([0, 1, 1.2, 2.2, 2.4, 3.4])
    ax2.set_yticklabels(["OPEN", "CLOSED", "OPEN", "CLOSED", "OPEN", "CLOSED"], fontsize=8)
    ax2.set_ylabel("Contactor States")
    ax2.grid(True)
    ax2.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig


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
