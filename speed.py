import gpxpy
import gpxpy.gpx
from datetime import timedelta

def read_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx

def adjust_speed(gpx, speed_factor):
    """
    Adjust the speed by modifying the timestamps in the track points.
    speed_factor: A factor by which the speed should be increased. 
                  A value of 2 would double the speed, 1.5 would increase it by 50%, etc.
    """
    if not gpx.tracks:
        print("No tracks found in the GPX file.")
        return

    for track in gpx.tracks:
        for segment in track.segments:
            previous_point_time = None
            for point in segment.points:
                if previous_point_time is not None:
                    time_diff = point.time - previous_point_time
                    new_time_diff = time_diff / speed_factor
                    point.time = previous_point_time + new_time_diff
                previous_point_time = point.time

def save_gpx_file(gpx, file_path):
    with open(file_path, 'w') as gpx_file:
        gpx_file.write(gpx.to_xml())

# Example usage
original_file_path = 'Morning_Ride (2).gpx'
modified_file_path = 'Morning_Ride_modified_2.gpx'
speed_factor = 2  # Increase speed by 50%

# Read the original GPX file
gpx = read_gpx_file(original_file_path)

# Adjust the speed
adjust_speed(gpx, speed_factor)

# Save the modified GPX file
save_gpx_file(gpx, modified_file_path)

print("Modified GPX file with increased speed saved.")
