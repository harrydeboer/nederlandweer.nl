import os
import csv


class SensorUtrechtRepository:

    def __init__(self):
        self.path_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def write(self, rows: list):
        file = open(os.path.dirname(os.getcwd()) + "/utrecht_ids.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def get(self) -> dict:
        rows = {}
        with open(self.path_app + '/utrecht_ids.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows[row[1]] = row
        return rows