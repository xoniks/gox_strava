import gpxpy
import gpxpy.gpx
from datetime import timedelta

def adjust_speed_and_date(gpx, days_shift, speed_factor):
    """Adjusts speed by scaling intervals and shifts dates."""
    for track in gpx.tracks:
        for segment in track.segments:
            if len(segment.points) < 2:
                continue  # Need at least two points to adjust speed

            start_time = segment.points[0].time
            end_time = segment.points[-1].time
            original_duration = (end_time - start_time).total_seconds()

            # Calculate new total duration based on the speed factor
            new_total_duration = original_duration * speed_factor

            # Calculate time adjustment per point
            per_point_adjustment = new_total_duration / (len(segment.points) - 1)

            for i, point in enumerate(segment.points):
                if i == 0:
                    point.time += timedelta(days=days_shift)  # Apply date shift to the first point
                else:
                    # Apply adjusted time and date shift for subsequent points
                    point.time = start_time + timedelta(seconds=i * per_point_adjustment) + timedelta(days=days_shift)
def read_gpx_file(file_path):
    """Reads a GPX file and returns a GPX object."""
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx

def save_gpx_file(gpx, file_path):
    """Saves the GPX file."""
    with open(file_path, 'w') as file:
        file.write(gpx.to_xml())

# Load your GPX file
gpx_file_path = 'Morning_Ride (2).gpx'
gpx = read_gpx_file(gpx_file_path)

# Adjust the speed and date
days_shift = 0  # Days to shift
speed_factor = 0.2  # To double the speed (for example)
adjust_speed_and_date(gpx, days_shift, speed_factor)

# Save the modified GPX file
modified_gpx_file_path = 'skend_3.gpx'
save_gpx_file(gpx, modified_gpx_file_path)

print("GPX file has been modified.")
