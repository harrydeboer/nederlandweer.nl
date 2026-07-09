import os
import requests
from typing import Literal
import datetime
import csv
from dashboard_meet_je_stad.models import Measurement, Sensor
from typing import Dict

class MeetJeStadAPIService:

    cleanup = {'cutoff_temp': [True, -25, 70],
               'cutoff_pm25': [True, 0, 250],
               'cutoff_pm10': [True, 0, 250]}

    def get_data(self,
                 begin: str,
                 end: str,
                 type_api: Literal['sensors', 'flora', 'stories'],
                 format_output: Literal['csv', 'json'],
                 sensors: Dict[int, Sensor],
                 ids: str = 'Utrecht',
                 is_particulate_matter_only: bool = False,
                 limit: int = 100,
                 is_active_only: bool = False,
                 cleanup=None,
                 is_with_row = False) -> list:

        if cleanup is None:
            cleanup = self.cleanup
        date_begin = datetime.datetime.strptime(begin, "%Y-%m-%d,%H:%M:%S")
        date_end = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")

        if type_api not in ['sensors', 'flora', 'stories']:
            raise Exception('type must be sensors, flora or stories.')

        if format_output not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if ids == 'Utrecht':
            keys = {}
            for index, key in enumerate(Measurement._meta.fields):
                keys[key] = index
            ids = ''
            for index, sensor in sensors.items():
                last_measurement = datetime.datetime.strftime(sensor.measurements[0].timestamp, '%Y-%m-%d %H:%M:%S')
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

        # read from JSON
        results = []
        keys = []

        for field in Measurement._meta.fields:
            if field.attname == 'pm25':
                keys.append('pm2.5')
            elif field.attname == 'sensor_id':
                keys.append('id')
            else:
                keys.append(field.attname)
        if is_with_row:
            keys[0] = 'row'
        for row in response.json():
            result = []
            for key in row:
                if key not in keys and key != 'row':
                    print('Invalid key ' + key + ' in row.')
            for key in keys:
                if key in row:
                    result.append(row[key])
                else:
                    result.append(None)
            if not is_with_row:
                result[0] = None
            results.append(result)

        results.reverse()
        row_keys_flipped = {}
        for key, field in enumerate(Measurement._meta.fields):
            row_keys_flipped[field.attname] = key
        results.sort(key=lambda x: x[row_keys_flipped['sensor_id']])

        results = self._sanitize(results, row_keys_flipped, cleanup)

        if format_output == 'csv':
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            parent_path = os.path.dirname(path)
            file = open(parent_path + "/data/tmp/dataset.csv", "w", newline='')
            results = [Measurement._meta.fields] + results
            csv.writer(file).writerows(results)
            file.close()

            return []
        else:
            return results

    def _sanitize(self, raw_results: list, row_keys_flipped: dict, cleanup: dict) -> list:

        results = []
        for raw_row in raw_results:
            row = list(raw_row)
            if 'cutoff_temp' in cleanup and cleanup['cutoff_temp'][0]:
                if raw_row[row_keys_flipped['temperature']] is not None:
                    if (raw_row[row_keys_flipped['temperature']] < float(cleanup['cutoff_temp'][1])
                            or raw_row[row_keys_flipped['temperature']] > float(cleanup['cutoff_temp'][2])):
                        row[row_keys_flipped['temperature']] = None
            if 'cutoff_pm25' in cleanup and cleanup['cutoff_pm25'][0]:
                if raw_row[row_keys_flipped['pm25']] is not None:
                    if (raw_row[row_keys_flipped['pm25']] < float(cleanup['cutoff_pm25'][1])
                            or raw_row[row_keys_flipped['pm25']] > float(cleanup['cutoff_pm25'][2])):
                        row[row_keys_flipped['pm25']] = None
            if 'cutoff_pm10' in cleanup and cleanup['cutoff_pm10'][0]:
                if raw_row[row_keys_flipped['pm10']] is not None:
                    if (raw_row[row_keys_flipped['pm10']] < float(cleanup['cutoff_pm10'][1])
                            or raw_row[row_keys_flipped['pm10']] > float(cleanup['cutoff_pm10'][2])):
                        row[row_keys_flipped['pm10']] = None
            results += [row]

        return results
