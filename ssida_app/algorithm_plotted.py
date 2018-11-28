import time
import numpy as np
from datetime import datetime
from ssida_app.models import LiveData
import plotly as py
import plotly.graph_objs as go


time_out = 15.0
min_window_len = 10

normalise_min = 0.75
normalise_max = 1.25
epsilon = 0.0000001


# Compute Score for latitude-longitude geo-locations
def compute_geo_score(time_window, begin_timestamp=None, end_timestamp=None):
    time_window_size = time_window
    min_window_len = int(time_window_size * (2.0 / 3.0))
    if begin_timestamp is not None and end_timestamp is not None:
        begin_time = convert_to_seconds(str(begin_timestamp))
        end_time = convert_to_seconds(str(end_timestamp))
    else:
        begin_time = float("-inf")
        end_time = float("inf")

    scores = []
    score_times = []
    accelerations = []
    acceleration_times = []

    device_current_acceleration_window = {}
    device_current_acceleration_window_start_time = {}
    window_timestamp_starts = {}
    device_last_time_encountered = {}
    all_stored_data = LiveData.objects.all().order_by('id')
    for live_data in all_stored_data:
        device_id = live_data.device_id
        acceleration = live_data.accelerometer_x
        time_in_s = convert_to_seconds(str(live_data.timestamp))
        timestamp = live_data.timestamp
        latitude = live_data.latitude
        longitude = live_data.longitude
        if acceleration > epsilon and begin_time < time_in_s < end_time and latitude != 0.0 and longitude != 0.0:
            last_time_encountered = device_last_time_encountered.get(device_id, 0.0)
            if abs(time_in_s - last_time_encountered) > time_out:  # Current acceleration window no longer has contiguous data
                device_current_acceleration_window[device_id] = []  # Throw away old and create new acceleration window
                device_last_time_encountered[device_id] = time_in_s
            else:
                current_acceleration_window = device_current_acceleration_window.get(device_id, [])
                window_start_time = device_current_acceleration_window_start_time.get(device_id, time_in_s)
                if len(current_acceleration_window) > 0 and \
                        abs(time_in_s - window_start_time) > time_window_size:  # Calculate and save score for current window
                    if len(current_acceleration_window) > min_window_len:
                        score = normalised_coefficient_of_variation(current_acceleration_window)
                        scores.append(score * 100)
                        score_times.append(window_timestamp_starts.get(device_id))
                        scores.append(score * 100)
                        score_times.append(timestamp)

                    device_current_acceleration_window[device_id] = []  # Create new current acceleration window
                    device_last_time_encountered[device_id] = time_in_s
                else:  # Add acceleration reading onto current acceleration window
                    if len(current_acceleration_window) == 0:  # Count window start from when first value goes in
                        device_current_acceleration_window_start_time[device_id] = time_in_s
                        window_timestamp_starts[device_id] = timestamp
                        scores.append(0.0)
                        score_times.append(timestamp)

                    current_acceleration_window.append(abs(acceleration))
                    device_current_acceleration_window[device_id] = current_acceleration_window
                    device_last_time_encountered[device_id] = time_in_s
            accelerations.append(acceleration)
            acceleration_times.append(timestamp)

    trace0 = go.Scatter(x=acceleration_times, y=accelerations, name='Acceleration')
    trace1 = go.Scatter(x=score_times, y=scores, name='Distraction Value', yaxis='y2')

    data = [trace0, trace1]

    layout = go.Layout(
        title='Ernests Dublin Walk',
        yaxis=dict(
            title='Acceleration m/s/s',
            range=[-20, 130]
        ),
        yaxis2=dict(
            title='Distraction Value as %',
            overlaying='y',
            side='right',
            range=[-50, 100]
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='accelerometer_x.html')

    return True


def convert_to_seconds(timestamp):
    timestamp = timestamp[:-3]+timestamp[-2:]
    d = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
    time_in_s = time.mktime(d.timetuple())
    return time_in_s


def normalised_coefficient_of_variation(window):
    mean = np.mean(window)
    std = np.std(window)
    coefficient_of_variation = std / mean
    coefficient_of_variation_normalised = normalise(coefficient_of_variation)
    return coefficient_of_variation_normalised


def normalise(x):
    if x > normalise_max:
        x = normalise_max
    elif x < normalise_min:
        x = normalise_min
    return (x - normalise_min) / (normalise_max - normalise_min)
