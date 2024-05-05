import georinex as gr
import numpy as np


def compare_rinex(file1, file2):
    # Load RINEX files
    rinex1 = gr.load(file1)
    rinex2 = gr.load(file2)

    # Count the number of rows (observations) in each file
    num_rows1 = rinex1.time.size
    num_rows2 = rinex2.time.size

    # Get unique satellites visible in each file
    satellites1 = np.unique(rinex1.sv.values)
    satellites2 = np.unique(rinex2.sv.values)

    print(f"File: {file1}")
    print(f"Number of observations: {num_rows1}")
    print(f"Satellites visible: {satellites1}\n")

    print(f"File: {file2}")
    print(f"Number of observations: {num_rows2}")
    print(f"Satellites visible: {satellites2}\n")

    # Compare the number of observations
    print("Comparison:")
    print(f"Difference in number of observations: {abs(num_rows1 - num_rows2)}")
    print(f"Satellites only in {file1}: {np.setdiff1d(satellites1, satellites2)}")
    print(f"Satellites only in {file2}: {np.setdiff1d(satellites2, satellites1)}")


# Example usage
compare_rinex('data/0_original/MTLD182A00.18n', 'data/1_filteredSV/MTLD182A00_modified.18n')
