# This module handles all the other functionalities.

from datetime import datetime


def convert_timestamp_to_date(timestamp):
    date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
    return date


def generate__id(content):
    if content:
        max_id = int(content[-1]['id'])
        id = max_id + 1
    else:
        id = 0
    return str(id)
