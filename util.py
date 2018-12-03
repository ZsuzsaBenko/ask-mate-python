# This module handles all the other functionalities.

from datetime import datetime


def convert_timestamp_to_date(timestamp):
    date = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
    return date
