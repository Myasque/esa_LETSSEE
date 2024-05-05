import csv
from datetime import datetime
from pathlib import Path
import os

def read_metadata(metadata_path):
    """Reads metadata from a CSV file to map filenames to constellation usage."""
    metadata = {}
    with open(metadata_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = row['filename']
            metadata[filename] = {
                'use_gps': row['use_gps'] == 'True',
                'use_glonass': row['use_glonass'] == 'True',
                'use_galileo': row['use_galileo'] == 'True'
            }
    return metadata

def convert_coordinate(value):
    """Convert NMEA coordinate to decimal degrees."""
    degrees = int(float(value) // 100)
    minutes = float(value) % 100
    return degrees + (minutes / 60)

def convert_latitude(lat, direction):
    """Convert latitude to decimal degrees."""
    decimal_lat = convert_coordinate(lat)
    return -decimal_lat if direction == 'S' else decimal_lat

def convert_longitude(lon, direction):
    """Convert longitude to decimal degrees."""
    decimal_lon = convert_coordinate(lon)
    return -decimal_lon if direction == 'W' else decimal_lon

def convert_time(time_str, date_str):
    """Convert NMEA time and date to ISO datetime string."""
    time = datetime.strptime(time_str, "%H%M%S.%f")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    full_datetime = datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond)
    return full_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + 'Z'

def strip_units(value):
    """Strip unit characters and convert to float."""
    return float(value[:-1]) if value[-1].upper() == 'M' else float(value)

def load_metadata(metadata_file):
    """Loads metadata about constellation usage from a CSV file."""
    metadata = {}
    with open(metadata_file, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for rows in reader:
            if len(rows) >= 4:
                metadata[rows[0]] = {
                    'use_gps': rows[1].lower() == 'true',
                    'use_glonass': rows[2].lower() == 'true',
                    'use_galileo': rows[3].lower() == 'true'
                }
    return metadata

def convert_nmea_to_csv(input_dir, output_dir):
    input_dir = Path('data/' + input_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    metadata = load_metadata(input_dir / 'processed_files.csv')

    input_files = [x for x in os.listdir(input_dir) if x != 'processed_files.csv']
    for input_file in input_files:
        if input_file.endswith('.nmea'):
            data = []
            with open(input_dir / input_file, 'r') as file:
                lines = file.readlines()

            file_metadata = metadata.get(input_file, {'use_gps': False, 'use_glonass': False, 'use_galileo': False})

            for i in range(0, len(lines), 2):  # Process two lines at a time
                rmc_parts = lines[i].strip().split(',')
                gga_parts = lines[i + 1].strip().split(',') if i + 1 < len(lines) else None

                if rmc_parts[0].startswith('$GPRMC') and gga_parts and gga_parts[0].startswith('$GPGGA'):
                    entry = {
                        'timestamp': convert_time(rmc_parts[1], datetime.strptime(rmc_parts[9], "%d%m%y").strftime("%Y-%m-%d")),
                        'latitude': convert_latitude(rmc_parts[3], rmc_parts[4]),
                        'longitude': convert_longitude(rmc_parts[5], rmc_parts[6]),
                        'speed_over_ground': float(rmc_parts[7]),
                        'status': rmc_parts[2],
                        'fix_quality': int(gga_parts[6]),
                        'number_of_satellites': int(gga_parts[7]),
                        'hdop': float(gga_parts[8]),
                        'altitude': strip_units(gga_parts[9]),
                        'geoidal_separation': strip_units(gga_parts[11]),
                        **file_metadata
                    }
                    data.append(entry)

            output_fn = output_dir / f"{input_file[:-4]}csv"
            with open(output_fn, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'latitude', 'longitude', 'speed_over_ground', 'status', 'fix_quality',
                              'number_of_satellites', 'hdop', 'altitude', 'geoidal_separation',
                              'use_gps', 'use_glonass', 'use_galileo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for entry in data:
                    writer.writerow(entry)


convert_nmea_to_csv('2_rtk_to_nmea', 'data/3_processed_csv')