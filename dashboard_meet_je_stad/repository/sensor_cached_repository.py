import sys
import os
import json
from dashboard_meet_je_stad.models import Sensor, Measurement
from typing import Dict
from django.apps import apps
from pathlib import Path


class SensorCachedRepository:

    def __init__(self):
        path = os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
        if sys.argv[1:2] == ['test']:
            self.path_data = path + '/tests/data/'
        else:
            self.path_data = path + '/data/'

    def find_all_as_string(self) -> str:
        try:
            with open(self.path_data + 'sensor_cached.json') as json_file:
                return json_file.read()
        except FileNotFoundError:

            return '{}'

    def find_all(self) -> Dict[int, Sensor]:

        try:
            with open(self.path_data + 'sensor_cached.json') as json_file:

                """ The sensor is loaded from json to a dictionary.
                The sensor gets measurements from the measurement fields in the dictionary.
                """
                sensors = json.load(json_file)
                sensors_cached = {}
                for sensor_id, sensor_cached in sensors.items():
                    measurements = []
                    sensor = Sensor()
                    for field in Sensor._meta.fields:
                        prop = field.attname
                        attribute = getattr(sensor, 'set_' + prop[1:])
                        attribute(sensor_cached[prop[1:]])
                    rows = []
                    for field in Measurement._meta.fields:
                        key = field.attname
                        if field.attname == '_id':
                            key = '_measurement_id'
                        rows.append(sensor_cached[key[1:]])
                    rows = [list(i) for i in zip(*rows)]
                    for row in rows:
                        measurements.append(Measurement(row=row))
                    sensor.set_measurements_cached(measurements)
                    sensors_cached[int(sensor_id)] = sensor
                return sensors_cached
        except FileNotFoundError:

            return {}

    def write(self, sensors: Dict[int, Sensor]):
        sensors_cached = {}
        for sensor_id, sensor in sensors.items():
            sensors_cached[sensor_id] = sensor.to_dict()
        if not os.path.exists(self.path_data):
            Path(self.path_data).mkdir(parents=True, exist_ok=True)
        with open(self.path_data + 'sensor_cached.json', 'w', encoding='utf-8') as f:
            json.dump(sensors_cached, f, ensure_ascii=False, indent=4)
