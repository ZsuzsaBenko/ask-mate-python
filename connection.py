# This module handles the csv files.

import csv


def read_csv_file(filename):
    with open(filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)



def write_csv_file(filename):
    pass
