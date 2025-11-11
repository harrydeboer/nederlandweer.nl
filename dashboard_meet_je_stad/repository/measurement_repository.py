import os
import csv
import datetime
from dashboard_meet_je_stad.model.measurement import Measurement


class MeasurementRepository:

    def __init__(self):
        self.path_data = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/'

    def add_to_full(self, id_sensor: int, rows: list):
        os.makedirs(self.path_data + "ids/" + str(id_sensor), exist_ok=True)
        file = open(self.path_data + "ids/" + str(id_sensor) + "/out.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def get_small_last_24(self, date_now: datetime.datetime) -> list:
        measurements = []
        with open(self.path_data + "dataset_small.csv") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                date_row = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
                if date_now - date_row < datetime.timedelta(hours=24):
                    measurements.append(row)
        return measurements

    def get_small_utrecht(self, sensors:dict) -> dict:
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
        for index, rows in measurements.items():
            sensors[index].set_measurements(rows)

        return sensors

    def add_to_small(self, rows: list):
        file = open(self.path_data + "dataset_small.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def write_to_small(self, rows: list):
        file = open(self.path_data + "dataset_small.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def write_to_small_utrecht(self, rows: list):
        file = open(self.path_data + "/dataset_small_utrecht.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()