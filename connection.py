# This module handles the csv files.

import csv


def read_csv_file(filename, headers):
    with open(filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        content = []
        for row in reader:
            data = {}
            for item in headers:
                data[item] = row[item]
            content.append(data)
        return content


def write_csv_file(filename, content, headers):
    with open(filename, mode="w", encoding="utf-8") as csv_file:
        fieldnames = headers
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in content:
            writer.writerow(row)
