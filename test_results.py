import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_gps_tracks(directory):
    # Path to the directory containing CSV files
    data_dir = Path(directory)
    files = list(data_dir.glob('NEWE*_R.csv'))  # List all CSV files in the directory

    # Set up the plot
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111)

    # Colors for each file
    colors = plt.cm.viridis(np.linspace(0, 1, len(files)))

    for file, color in zip(files, colors):
        # Read the CSV file
        df = pd.read_csv(file)

        # Plotting each track
        ax.plot(df['longitude'], df['latitude'], label=file.stem, color=color, marker='o', linestyle='-')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('GPS Tracks')
    ax.legend(loc='best', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.grid(True)

    # Show the plot
    plt.show()

# Example usage
plot_gps_tracks('data/3_processed_csv/')
