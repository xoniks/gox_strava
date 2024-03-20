import streamlit as st
import gpxpy
import gpxpy.gpx
from datetime import timedelta
import io

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

def app():
    st.title("Strava Average Speed Hack tool :sunglasses:")
    st.write("This app is designed by Egezon Baruti. It allows you to hack your average speed by modifying your GPX file.")
    st.write("You need to download your GPX file of your activity, modify it here :point_down: ,download it and import it again to Strava,Relive,Komot,...")



    uploaded_file = st.file_uploader("Choose a GPX file", type="gpx")
    if uploaded_file is not None:
        # Read the uploaded GPX file
        gpx = gpxpy.parse(uploaded_file.getvalue())

        # Input for days to shift and speed factor
        days_shift = 0
        speed_factor = st.number_input("Speed factor (e.g. 2 to double your average speed) ", min_value=0.1, value=1.0, format="%.1f")
        speed_factor = 1/speed_factor
        if st.button("Modify GPX File"):
            # Adjust the speed and date of the GPX file
            adjust_speed_and_date(gpx, days_shift, speed_factor)

            # Save the modified GPX to a temporary buffer
            # Save the modified GPX to a temporary buffer
            gpx_string = gpx.to_xml()  # Get the GPX file as a string
            gpx_bytes = gpx_string.encode('utf-8')  # Convert the string to bytes

            # Create the download button to provide the modified GPX file
            original_file_name = uploaded_file.name.rsplit(".", 1)[0]
            modified_file_name = f"{original_file_name}_hacked.gpx"
            st.download_button(label="Download modified GPX file",
                               data=gpx_bytes,
                               file_name=modified_file_name,
                               mime="application/gpx+xml")

if __name__ == "__main__":
    app()
