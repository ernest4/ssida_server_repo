import time
import numpy as np
import pandas as pd
from datetime import datetime
from ssida_app.models import ScoreData


time_window_size = 60.0
time_out = 2.0
min_window_len = 40

normalise_min = 0.75
normalise_max = 1.25
epsilon = 0.0000001


# Compute Score for latitude-longitude geo-locations
def compute_geo_score(begin_timestamp=None, end_timestamp=None):
    if begin_timestamp is not None and end_timestamp is not None:
        begin_time = convert_to_seconds(str(begin_timestamp))
        end_time = convert_to_seconds(str(end_timestamp))
    else:
        begin_time = float("-inf")
        end_time = float("inf")

    device_current_acceleration_window = {}
    device_current_acceleration_window_start_time = {}
    device_last_time_encountered = {}
    all_stored_data = read_all_data_in()
    for live_data in all_stored_data:
        device_id = 0
        acceleration = live_data[0]
        time_in_s = convert_to_seconds(str(live_data[1]))
        latitude = live_data[2]
        longitude = live_data[3]
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
                        score_data = ScoreData()
                        score_data.latitude = latitude
                        score_data.longitude = longitude
                        score_data.score = score
                        score_data.save()

                    device_current_acceleration_window[device_id] = []  # Create new current acceleration window
                    device_last_time_encountered[device_id] = time_in_s
                else:  # Add acceleration reading onto current acceleration window
                    if len(current_acceleration_window) == 0:  # Count window start from when first value goes in
                        device_current_acceleration_window_start_time[device_id] = time_in_s

                    current_acceleration_window.append(abs(acceleration))
                    device_current_acceleration_window[device_id] = current_acceleration_window
                    device_last_time_encountered[device_id] = time_in_s
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


def read_all_data_in():
    df = pd.read_csv("./data.csv", usecols=['latitude', 'longitude', 'accelerometer_x', 'timestamp'])
    accelerometer_x = df.get('accelerometer_x')
    timestamps = df.get('timestamp')
    latitudes = df.get('latitude')
    longitudes = df.get('longitude')

    all_data = []
    for acceleration_x, timestamp_x, latitude_x, longitude_x in zip(accelerometer_x, timestamps, latitudes, longitudes):
        all_data.append((acceleration_x, timestamp_x, latitude_x, longitude_x))
    return all_data
