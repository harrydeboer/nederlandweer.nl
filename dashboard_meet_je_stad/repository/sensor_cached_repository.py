import sys
import os
import json
from dashboard_meet_je_stad.models import Sensor
from typing import Dict
from django.apps import apps


class SensorCachedRepository:

    def __init__(self):
        path = os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
        if sys.argv[1:2] == ['test']:
            self.path_data = path + '/tests/data/'
        else:
            self.path_data = path + '/data/'

    def find_all(self) -> Dict[str, dict]:

        try:
            with open(self.path_data + 'sensor_cached.json') as json_file:
                sensors = json.load(json_file)

                return sensors
        except FileNotFoundError:

            return {}

    def write(self, sensors: Dict[int, Sensor]):
        sensors_cached = {}
        for sensor_id, sensor in sensors.items():
            sensors_cached[sensor_id] = sensor.to_dict()
        with open(self.path_data + 'sensor_cached.json', 'w', encoding='utf-8') as f:
            json.dump(sensors_cached, f, ensure_ascii=False, indent=4)
