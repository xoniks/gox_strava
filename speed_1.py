import gpxpy
import gpxpy.gpx
from datetime import timedelta

def read_gpx_file(file_path):
    """Reads a GPX file and returns a GPX object."""
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx

def shift_dates(gpx, days=1):
    """Shifts all dates in the GPX object by a specified number of days."""
    if hasattr(gpx, 'metadata') and gpx.metadata and gpx.metadata.time:
        gpx.metadata.time += timedelta(days=days)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.time:
                    point.time += timedelta(days=days)

def adjust_speed(gpx, speed_factor):
    """Adjusts the speed by scaling time intervals between points.
    To increase speed, speed_factor should be less than 1.
    For example, a speed_factor of 0.5 will double the speed."""
    for track in gpx.tracks:
        for segment in track.segments:
            previous_point_time = None
            for i, point in enumerate(segment.points):
                if i == 0:  # Skip the first point
                    previous_point_time = point.time
                    continue
                if point.time and previous_point_time:
                    # Scale the time interval between the current point and the previous point
                    time_diff = point.time - previous_point_time
                    # Apply speed factor
                    new_time_diff = timedelta(seconds=time_diff.total_seconds() * speed_factor)
                    point.time = previous_point_time + new_time_diff
                    previous_point_time = point.time

def save_gpx_file(gpx, file_path):
    """Saves the modified GPX object to a new file."""
    with open(file_path, 'w') as gpx_file:
        gpx_file.write(gpx.to_xml())

# Specify the path to your original GPX file and the output file
original_file_path = 'Morning_Ride (2).gpx'
modified_file_path = 'skenderaj_5.gpx'
days_to_shift = 5  # Number of days to shift
speed_factor = 0.1  # Example speed factor to increase speed by 50%

# Process the GPX file
gpx = read_gpx_file(original_file_path)
shift_dates(gpx, days=days_to_shift)  # Shift dates first
adjust_speed(gpx, speed_factor)  # Then adjust speed
save_gpx_file(gpx, modified_file_path)

print("The GPX file dates have been shifted and speed increased consistently.")
