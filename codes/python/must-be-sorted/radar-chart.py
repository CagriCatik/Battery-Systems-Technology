import matplotlib.pyplot as plt
import numpy as np

# Function to create a spider chart
def create_spider_chart(categories, values, title="Spider Chart", filename="spider_chart.png"):
    # Number of variables
    num_vars = len(categories)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    # Create figure and polar plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Add the values to the plot
    values += values[:1]  # Complete the loop for values
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)

    # Set categories as labels on the axes
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)

    # Add title
    ax.set_title(title, size=14, color="darkblue", pad=20)

    # Save the chart as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Spider chart saved as {filename}")

    # Show the chart
    plt.show()

# Example usage
categories = ["Speed", "Reliability", "Comfort", "Safety", "Efficiency"]
values = [8, 7, 9, 6, 7]  # Corresponding values for the categories

create_spider_chart(categories, values, title="Vehicle Performance", filename="vehicle_performance.png")
