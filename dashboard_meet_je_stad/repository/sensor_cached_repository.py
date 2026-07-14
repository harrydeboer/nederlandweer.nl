import sys
import os
import json
from dashboard_meet_je_stad.models import Sensor, Measurement
from typing import Dict
from django.apps import apps


class SensorCachedRepository:

    def __init__(self):
        path = os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
        if sys.argv[1:2] == ['test']:
            self.path_data = path + '/tests/data/'
        else:
            self.path_data = path + '/data/'

    def find_all(self) -> Dict[int, Sensor]:

        try:
            with open(self.path_data + 'sensor_cached.json') as json_file:
                sensors = json.load(json_file)
                sensors_cached = {}
                for sensor_id, sensor_cached in sensors.items():
                    measurements = []
                    sensor = Sensor()
                    sensor.is_active = sensor_cached['is_active']
                    for field in Sensor._meta.fields:
                        prop = field.attname
                        sensor.__setattr__(prop, sensor_cached[prop])
                    for row in sensor_cached['measurements']:
                        measurements.append(Measurement(row=row))
                    sensor.set_measurements_cached(measurements)
                    sensors_cached[int(sensor_id)] = sensor
                return sensors_cached
        except FileNotFoundError:

            return {}

    def transpose_measurements(self, sensors: Dict[int, Sensor]) -> Dict[int, Sensor]:
        sensors_transposed = {}
        for sensor_id, sensor in sensors.items():
            sensor = sensor.to_dict(True)
            sensors_transposed[int(sensor_id)] = sensor

        return sensors_transposed

    def write(self, sensors: Dict[int, Sensor]):
        sensors_cached = {}
        for sensor_id, sensor in sensors.items():
            sensors_cached[sensor_id] = sensor.to_dict()
        with open(self.path_data + 'sensor_cached.json', 'w', encoding='utf-8') as f:
            json.dump(sensors_cached, f, ensure_ascii=False, indent=4)
