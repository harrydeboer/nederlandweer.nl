import requests
from typing import Literal, List, Dict
import datetime
import csv
from dashboard_meet_je_stad.models import Sensor, Measurement
from django.apps import apps
import os


class MeetJeStadAPIService:

    def get_measurements(self,
                 begin: str,
                 end: str,
                 type_api: Literal['sensors', 'flora', 'stories'],
                 format_output: Literal['csv', 'json'],
                 sensors: Dict[int, Sensor],
                 ids: str = 'Utrecht',
                 is_particulate_matter_only: bool = False,
                 limit: int = 100,
                 is_active_only: bool = False,
                 is_with_row = False) -> List[Measurement]:

        if limit > 1000000:
            raise Exception('Aantal rijen mag niet meer zijn dan 1000000.')

        date_begin = datetime.datetime.strptime(begin, "%Y-%m-%d,%H:%M:%S")
        date_end = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")

        if type_api not in ['sensors', 'flora', 'stories']:
            raise Exception('type must be sensors, flora or stories.')

        if format_output not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if ids == 'Utrecht':
            ids = ''
            for index, sensor in sensors.items():
                last_measurement = datetime.datetime.strftime(
                    sensor.get_measurements()[-1].timestamp, '%Y-%m-%d %H:%M:%S')
                delta = date_end - datetime.datetime.strptime(last_measurement, "%Y-%m-%d %H:%M:%S")
                if index == 0:
                    continue
                if is_active_only and delta.days > 0:
                    continue
                if is_particulate_matter_only and sensor.is_particulate_matter == '0':
                    continue
                ids += str(index) + ','
            ids = ids[:-1]

        uri = 'https://meetjestad.net/data/?type='
        uri += (type_api + '&ids=' + ids + '&begin=' + date_begin.strftime('%Y-%m-%d,%H:%M:%S') + '&end=' +
                date_end.strftime('%Y-%m-%d,%H:%M:%S') + '&format=json&limit=' + str(limit))

        response = requests.get(uri)

        if response.status_code != 200:
            raise Exception(response.reason)

        try:
            response.json()
        except Exception:
            raise Exception(response.content.decode("utf-8"))

        row_keys = []
        for field in Measurement._meta.fields:
            if field.attname == 'pm25':
                row_keys.append('pm2.5')
            elif field.attname == 'id':
                row_keys.append('row')
            elif field.attname == 'sensor_id':
                row_keys.append('id')
            else:
                row_keys.append(field.attname)

        rows = []
        for row in response.json():
            result = []
            for key in row:
                if key not in row_keys:
                    print('Invalid key ' + key + ' in row.')
            for key in row_keys:
                if key in row:
                    result.append(row[key])
                else:
                    result.append(None)
            if not is_with_row:
                result[0] = None
            rows.append(result)

        if not is_with_row:
            rows.reverse()

        measurements = []
        for row in rows:
            measurements.append(Measurement(row=row))

        if format_output == 'csv':
            path = apps.get_app_config('dashboard_meet_je_stad').path
            file = open(os.path.dirname(path) + "/data/tmp/dataset.csv", "w", newline='')
            rows = [row_keys] + rows
            csv.writer(file).writerows(rows)
            file.close()

        return measurements
