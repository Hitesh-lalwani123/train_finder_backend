import matplotlib.pyplot as plt

def visualize_connections(connections, stations):
    """
    Visualizes station-to-station connections using arrows on separate lines.

    Parameters:
    - connections: List of (start_index, end_index) tuples
    - stations: List of station codes (index-mapped)
    """
    if not connections or not stations:
        print("No connections or stations provided.")
        return

    max_index = max(max(start, end) for start, end in connections)
    if max_index >= len(stations):
        print("Error: Connection index exceeds station list.")
        return

    array = list(range(len(stations)))

    fig, ax = plt.subplots(figsize=(max(len(array) / 1.5, 10), len(connections)))

    # Plot station dots and labels
    ax.plot(array, [0] * len(array), 'ko')
    for i, code in enumerate(stations):
        ax.text(i, 0.3, code, ha='center', fontsize=8, rotation=45)

    # Draw each connection on its own y-level
    for idx, (start, end) in enumerate(connections):
        y = -idx - 1
        ax.annotate("",
                    xy=(end, y), xytext=(start, y),
                    arrowprops=dict(arrowstyle="->", color="blue"))
        label = f"{stations[start]} → {stations[end]}"
        ax.text((start + end) / 2, y + 0.2, label, ha='center', fontsize=8)

    # Style
    ax.set_ylim(-len(connections) - 1, 2)
    ax.axis('off')
    plt.title("Station-to-Station Connections")
    plt.tight_layout()
    plt.show()
