import csv
import datetime
import math
import os
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService

class UpdateUtrechtIdsService:

    def __init__(self):
        self.utrecht_center_lat_degrees = 52.085 * math.pi / 180
        self.utrecht_center_long_degrees = 5.085 * math.pi / 180
        self.radius = 9.46

    def update(self, ids: dict, last_date: str, rows: list) ->  list:
        service = MeetJeStadAPIService()
        rows_dataset = {}
        rows_old = {}
        with open(os.path.dirname(os.getcwd()) + "/utrecht_ids.csv", newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for key, row in enumerate(reader):
                rows_old[row[1]] = row
        for row in rows:
            if row[1] not in rows_dataset:
                rows_dataset[row[1]] = [row]
            else:
                rows_dataset[row[1]] += [row]
        rows_utrecht = {}
        values = []
        for index, rows in ids.items():
            if str(index) in rows_dataset:
                rows += rows_dataset[str(index)]
            utrecht = []
            latitudes = {}
            longitudes = {}
            start_date = ''
            end_date = ''
            count_latitude = 0
            count_longitude = 0
            utrecht_city = False
            start_date_utrecht = ''
            end_date_utrecht = ''
            particulate_matter = 0
            longitude_file = ''
            latitude_file = ''
            if str(index) in rows_old:
                row = rows_old[str(index)]
                if row[len(service.row_keys) + 6] == '1':
                    particulate_matter = 1
                start_date = row[len(service.row_keys) + 2]
                utrecht_city = True
                start_date_utrecht = row[len(service.row_keys) + 4]
                end_date_utrecht = row[len(service.row_keys) + 5]
                longitude_file = row[len(service.row_keys)]
                latitude_file = row[len(service.row_keys) + 1]
            for key, row in enumerate(rows):
                date_object = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                date = date_object.strftime('%Y-%m-%d')
                end_date = date
                if key == 0:
                    start_date = date
                latitude = row[4]
                if latitude is None or latitude == '':
                    continue
                else:
                    latitude = float(latitude)
                longitude = row[3]
                if longitude is None or latitude == '':
                    continue
                else:
                    longitude = float(longitude)
                latitudes[date] = latitude
                if date in latitudes:
                    count_latitude += 1
                    latitudes[date] = (latitude + latitudes[date] * (count_latitude - 1)) / count_latitude
                else:
                    latitudes[date] = latitude
                    count_latitude = 1
                if date in longitudes:
                    count_longitude += 1
                    longitudes[date] = (longitude + longitudes[date] * (count_longitude - 1)) / count_longitude
                else:
                    longitudes[date] = longitude
                    count_longitude = 1
                if row[9] is not None or row[10] is not None:
                    particulate_matter = 1
                values = row
            for key, latitude in latitudes.items():
                longitude = longitudes[key]
                utrecht_row = [key]
                end_date_utrecht = key
                degrees_lat = math.pi / 180 * latitude
                degrees_lon = math.pi / 180 * longitude
                if longitude > 180 or longitude < -180 or latitude > 90 or latitude < -90:
                    continue
                distance = 2 * math.asin(math.sqrt(((1 - math.cos(degrees_lat - self.utrecht_center_lat_degrees)) +
                                           math.cos(degrees_lat) * math.cos(self.utrecht_center_lat_degrees) *
                                           (1 - math.cos(degrees_lon - self.utrecht_center_long_degrees))) / 2)) * 6371
                if distance < self.radius:
                    utrecht_row.append(1)
                    if not utrecht_city and start_date_utrecht == '':
                        start_date_utrecht = key
                        utrecht_city = True
                    else:
                        utrecht_row.append(0)
                        utrecht_city = False
                    utrecht.append(utrecht_row)
            if utrecht_city or start_date_utrecht != '':
                if end_date == last_date:
                    end_date = ''
                if end_date_utrecht == last_date:
                    end_date_utrecht = ''
                rows_utrecht[index] = values.copy()

                if longitudes != {} and latitudes != {}:
                    longitude_file = longitudes[list(longitudes)[-1]]
                    latitude_file = latitudes[list(latitudes)[-1]]
                rows_utrecht[index] += [longitude_file, latitude_file, start_date, end_date,
                                        start_date_utrecht, end_date_utrecht, particulate_matter]
        rows_new = []
        ids = []
        for index, row in rows_utrecht.items():
            rows_old[str(index)] = row
            ids.append(int(row[1]))
        for index, row in rows_old.items():
            rows_new.append(row)
            if row[1] not in ids:
                ids.append(int(row[1]))
        if len(values) > 0:
            file = open(os.path.dirname(os.getcwd()) + "/utrecht_ids.csv", "w", newline='')
            csv.writer(file).writerows(rows_new)
            file.close()

        return sorted(ids)
