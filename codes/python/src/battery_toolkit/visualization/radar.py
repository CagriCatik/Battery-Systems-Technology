from typing import List, Dict, Optional
import numpy as np
import matplotlib.pyplot as plt


def create_spider_chart(
    categories: List[str],
    values: List[float],
    title: str = "Battery Performance Radar",
    filename: Optional[str] = None,
    color: str = "blue",
    show: bool = False,
) -> plt.Figure:
    """
    Creates and optionally saves a spider/radar chart for multivariate evaluation.
    """
    num_vars = len(categories)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1] # Close polygon

    val_plot = list(values)
    val_plot += val_plot[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.fill(angles, val_plot, color=color, alpha=0.25)
    ax.plot(angles, val_plot, color=color, linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_title(title, size=14, color="darkblue", pad=20)

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_chemistry_radar_comparison(
    filename: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """
    Plots a multi-chemistry comparative spider chart across 6 key metrics:
    Specific Energy, Specific Power, Safety, Lifespan, Performance, Cost.
    """
    categories = ["Specific Energy", "Specific Power", "Safety", "Cycle Life", "Cold Performance", "Cost"]
    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Scores normalized 1 to 10
    chemistries = {
        "NMC-811": [9.0, 8.5, 6.0, 7.0, 7.5, 7.0],
        "LFP":     [6.0, 7.0, 9.5, 9.5, 5.0, 9.0],
        "LTO":     [4.0, 9.5, 10.0, 10.0, 9.0, 4.0],
        "NCA":     [9.5, 8.5, 5.5, 6.5, 7.0, 6.5],
    }

    colors = {"NMC-811": "#1f77b4", "LFP": "#2ca02c", "LTO": "#9467bd", "NCA": "#ff7f0e"}

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    for name, vals in chemistries.items():
        v = vals + vals[:1]
        ax.plot(angles, v, label=name, color=colors[name], linewidth=2)
        ax.fill(angles, v, color=colors[name], alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_rgrids([2, 4, 6, 8, 10], angle=0, fontsize=8)
    ax.set_title("Lithium-Ion Chemistry Trade-off Analysis", size=14, pad=25)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig

