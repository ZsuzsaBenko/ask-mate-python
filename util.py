# This module handles all the other functionalities.

from datetime import datetime
import time


def convert_timestamp_to_date(timestamp):
    date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
    return date


def convert_date_to_timestamp(date):
    dt = datetime(int(date[:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:]))
    timestamp = int(time.mktime(dt.timetuple()))
    return timestamp


def generate__id(content):
    if content:
        max_id = int(content[-1]['id'])
        id = max_id + 1
    else:
        id = 0
    return str(id)


def change_data(list_of_dictionaries):
    for item in list_of_dictionaries:
        item["submission_time"] = convert_date_to_timestamp(item["submission_time"])
    return list_of_dictionaries
