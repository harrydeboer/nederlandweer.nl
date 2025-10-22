import os
import requests
from typing import Literal
import datetime
import csv


class MeetJeStadAPIService:

    def __init__(self):
        self.row_keys = [
            'timestamp',
            'id',
            'temperature',
            'longitude',
            'latitude',
            'humidity',
            'supply',
            'battery',
            'firmware_version',
            'pm2.5',
            'pm10',
            'lux',
            'extra'
        ]

    def get_data(self,
                 begin: str,
                 end: str,
                 type_api: Literal['sensors', 'flora', 'stories'],
                 format_output: Literal['csv', 'json'],
                 ids: str = 'Utrecht',
                 is_particulate_matter_only: bool = False,
                 limit: int = 100,
                 is_active_only: bool = False) -> list:

        date_begin = datetime.datetime.strptime(begin, "%Y-%m-%d,%H:%M:%S")
        date_end = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")
        if date_end < date_begin:
            raise Exception('t1 must be later than t0.')

        if type_api not in ['sensors', 'flora', 'stories']:
            raise Exception('type must be sensors, flora or stories.')

        if format_output not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if ids == 'Utrecht':
            ids = ''
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/utrecht_ids.csv') as csvfile:
                reader = csv.reader(csvfile)
                for index, row in enumerate(reader):
                    if index == 0:
                        continue
                    if is_active_only and row[2] != '':
                        continue
                    if is_particulate_matter_only and row[5] == '0':
                        continue
                    ids += row[0] + ','
                ids = ids[:-1]
        else:
            for id_sensor in ids.split(','):
                if len(id_sensor.split('-')) > 1:
                    for id_underscore in id_sensor.split('-'):
                        if not id_underscore.isdigit():
                            raise Exception('Invalid IDs.')
                else:
                    if not id_sensor.isdigit():
                        raise Exception('Invalid IDs.')

        uri = 'https://meetjestad.net/data/?type='
        uri += (type_api + '&ids=' + ids + '&begin=' + date_begin.strftime('%Y-%m-%d,%H:%M:%S') + '&end=' +
                date_end.strftime('%Y-%m-%d,%H:%M:%S') + '&format=json&limit=' + str(limit))

        response = requests.get(uri)

        if response.status_code != 200:
            raise Exception(response.reason)

        # read from JSON
        results = []
        for row in response.json():
            result = []
            for key in row:
                if key not in self.row_keys and key != 'row':
                    print('Invalid key ' + key + ' in row.')
            for key in self.row_keys:
                if key in row:
                    result.append(row[key])
                else:
                    result.append(None)
            results.append(result)

        results.reverse()
        row_keys_flipped = {}
        for key, value in enumerate(self.row_keys):
            row_keys_flipped[value] = key
        results.sort(key=lambda x: x[row_keys_flipped['id']])

        results = self._sanitize(results, row_keys_flipped)

        if format_output == 'csv':
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            parent_path = os.path.dirname(path)
            grandparent_path = os.path.dirname(parent_path)
            if parent_path.endswith('vendor'):
                path = grandparent_path
            file = open(path + "/output/meet_je_stad/out.csv", "w", newline='')
            csv.writer(file).writerows(results)
            file.close()

            return []
        else:
            return results

    def _sanitize(self, raw_results: list, row_keys_flipped: dict) -> list:

        results = []
        for raw_row in raw_results:
            row = list(raw_row)
            if raw_row[row_keys_flipped['temperature']] is not None:
                if raw_row[row_keys_flipped['temperature']] < -25 or raw_row[row_keys_flipped['temperature']] > 70:
                    row[row_keys_flipped['temperature']] = None
            if raw_row[row_keys_flipped['pm2.5']] is not None:
                if raw_row[row_keys_flipped['pm2.5']] < 0 or raw_row[row_keys_flipped['pm2.5']] > 250:
                    row[row_keys_flipped['pm2.5']] = None
            if raw_row[row_keys_flipped['pm10']] is not None:
                if raw_row[row_keys_flipped['pm10']] < 0 or raw_row[row_keys_flipped['pm10']] > 250:
                    row[row_keys_flipped['pm10']] = None
            results += [row]

        return results
