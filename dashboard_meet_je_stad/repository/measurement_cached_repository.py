import csv
import sys
import os
from dashboard_meet_je_stad.models import Sensor, Measurement
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from typing import List, Dict
from django.apps import apps


class MeasurementCachedRepository:

    def __init__(self):
        path = os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
        if sys.argv[1:2] == ['test']:
            self.path_data = path + '/tests/data/'
        else:
            self.path_data = path + '/data/'
        self.measurement_repository = MeasurementRepository()

    def find_all(self, sensors: Dict[int, Sensor]) -> Dict[int, List[Measurement]]:
        measurements = {}
        try:
            with open(self.path_data + 'dataset_cached.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if int(row[1]) not in sensors:
                        continue
                    if int(row[1]) in measurements:
                        measurements[int(row[1])].append(Measurement(row=row))
                    else:
                        measurements[int(row[1])] = [Measurement(row=row)]

                return measurements
        except FileNotFoundError:

            return {}

    def write(self, measurements: list):
        rows = []
        for measurement in measurements:
            rows.append(measurement.to_list())
        file = open(self.path_data + "dataset_cached.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()