import os
import csv
import datetime
from dashboard_meet_je_stad.model.measurement import Measurement
from dashboard_meet_je_stad.model.sensor import Sensor
import sys
from typing import List, Dict


class MeasurementRepository:

    def __init__(self):
        self.path_data = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if  sys.argv[1:2] == ['test']:
            self.path_data += '/tests/data/'
        else:
            self.path_data += '/data/'

    def add_to_full(self, id_sensor: int, rows: list):
        os.makedirs(self.path_data + "ids/" + str(id_sensor), exist_ok=True)
        file = open(self.path_data + "ids/" + str(id_sensor) + "/out.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def get(self, id_sensor: int) -> List[Measurement]:
        measurements = []
        date = datetime.datetime.now(datetime.timezone.utc)
        date -= datetime.timedelta(days=91)
        with open(self.path_data + "ids/" + str(id_sensor) + "/out.csv") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                measurement = Measurement(row)
                if measurement.timestamp > date:
                    measurements.append(measurement)
        return measurements

    def get_small_last_24(self, date_now: datetime.datetime) -> Dict[int, List[Measurement]]:
        measurements = {}
        with open(self.path_data + "dataset_small.csv") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                date_row = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
                if date_now - date_row < datetime.timedelta(hours=24):
                    if int(row[1]) in measurements:
                        measurements[int(row[1])].append(Measurement(row))
                    else:
                        measurements[int(row[1])] = [Measurement(row)]
        return measurements

    def get_small_utrecht(self, sensors: Dict[int, Sensor]) -> Dict[int, List[Measurement]]:
        measurements = {}
        with open(self.path_data + 'dataset_small_utrecht.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if int(row[1]) not in sensors:
                    continue
                if int(row[1]) in measurements:
                    measurements[int(row[1])].append(Measurement(row))
                else:
                    measurements[int(row[1])] = [Measurement(row)]
        return measurements

    def add_to_small(self, rows: list):
        file = open(self.path_data + "dataset_small.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def write_to_small(self, measurements_dict: dict):
        rows = []
        for index, measurements in measurements_dict.items():
            for measurement in measurements:
                rows.append(measurement.to_list())
        file = open(self.path_data + "dataset_small.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def write_to_small_utrecht(self, measurements_dict: dict):
        rows = []
        for index, measurements in measurements_dict.items():
            for measurement in measurements:
                rows.append(measurement.to_list())
        file = open(self.path_data + "/dataset_small_utrecht.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()