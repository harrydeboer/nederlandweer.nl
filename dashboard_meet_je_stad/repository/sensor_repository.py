import os
import csv
import datetime
from dashboard_meet_je_stad.model.sensor import Sensor


class SensorRepository:

    def __init__(self):
        self.path_data = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/'

    def add_to_full(self, id_sensor: int, rows: list):
        os.makedirs(self.path_data + "ids/" + str(id_sensor), exist_ok=True)
        file = open(self.path_data + "ids/" + str(id_sensor) + "/out.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def get_small_last_24(self, date_now: datetime.datetime) -> list:
        rows = []
        with open(self.path_data + "dataset_small.csv") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                date_row = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
                if date_now - date_row < datetime.timedelta(hours=24):
                    rows.append(row)
        return rows

    def get_small_utrecht(self, sensors_utrecht:dict) -> dict:
        sensors = {}
        with open(self.path_data + 'dataset_small_utrecht.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if int(row[1]) not in sensors_utrecht:
                    continue
                if int(row[1]) not in sensors:
                    sensors[int(row[1])] = Sensor(row)
                else:
                    sensors[int(row[1])].add_measurement(row)
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