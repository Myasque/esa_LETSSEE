import subprocess
from pathlib import Path
import csv
import shutil

def run_subprocess_command(command):
    """Executes a command as a subprocess."""
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return "Success"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


def process_rinex_file(input_file, output_dir, constellations):
    """Process a single RINEX file to include only specified constellations using teqc."""
    constellations = [c for c in ['G', 'R', 'E'] if c in constellations]
    teqc_location = "/home/george/tmp/teqc/teqc"
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    output_file = output_dir / f"{input_file.stem}_modified{input_file.suffix}"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build constellation flags string
    constellations_flags = " ".join([f"-{c}" for c in constellations])

    # Construct command
    command = f"{teqc_location} {constellations_flags} {input_file} > {output_file}"

    # Execute command
    try:
        subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Processed {input_file.name} successfully.")
        return output_file, constellations
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file.name}: {e}")
        return None, None


def generate_rtklib_command(input_file, output_dir, constellations):
    """Generates and runs RTKLIB command to process RINEX files."""
    rtklib_location = "/home/george/tmp/RTKLIB/app/rnx2rtkp/gcc/rnx2rtkp"
    constellations_suffix = '+'.join(constellations)
    output_file = output_dir / f"{input_file.stem}_{constellations_suffix}.nmea"
    command = f'{rtklib_location} -p 0 "{input_file.parent}/{input_file.stem}.*" -o {output_file}'

    if run_subprocess_command(command) == "Success":
        return output_file
    else:
        return None


def write_csv(entries, output_path):
    """Writes processed data entries to a CSV file."""
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'use_gps', 'use_glonass', 'use_galileo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


def process_directory(directory, teqc_output_dir, rtk_output_dir, constellations):
    """Processes all .18o and .18n RINEX files in the specified directory."""
    teqc_output_dir.mkdir(parents=True, exist_ok=True)
    rtk_output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for file_path in directory.glob('*.18*'):
        modified_file, used_constellations = process_rinex_file(file_path, teqc_output_dir, constellations)
        if modified_file:
            final_file = generate_rtklib_command(modified_file, rtk_output_dir, used_constellations)
            if final_file:
                entries.append({
                    'filename': final_file.name,
                    'use_gps': 'G' not in used_constellations,
                    'use_glonass': 'R' not in used_constellations,
                    'use_galileo': 'E' not in used_constellations
                })
    write_csv(entries, rtk_output_dir / 'processed_files.csv')


if __name__ == "__main__":
    source_dir = Path('data/0_original/')
    teqc_dir = Path('data/1_filteredSV/')
    rtk_dir = Path('data/2_rtk_to_nmea/')

    process_directory(source_dir, teqc_dir, rtk_dir, ['R'])
