import os
import csv
from dashboard_meet_je_stad.model.sensor import Sensor
import math
import datetime


class SensorUtrechtRepository:

    def __init__(self):
        self.path_data = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/'
        self.row_keys = Sensor.row_keys
        self.utrecht_center_lat_degrees = 52.085 * math.pi / 180
        self.utrecht_center_long_degrees = 5.085 * math.pi / 180
        self.radius = 9.46

    def write(self, rows: list):
        file = open(self.path_data + "utrecht_ids.csv", "w", newline='')
        csv.writer(file).writerows(rows)
        file.close()

    def get(self, pm:bool = False) -> dict:
        rows = {}
        with open(self.path_data + 'utrecht_ids.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if pm and row[15] == '1':
                    rows[int(row[1])] = row
                elif not pm:
                    rows[int(row[1])] = row
        return rows

    def update(self, last_date: str, rows_new_list: list) -> list:
        rows_old = self.get()

        #Make dictionary of the new rows
        rows_new = {}
        for row in rows_new_list:
            if row[1] not in rows_new:
                rows_new[row[1]] = [row]
            else:
                rows_new[row[1]] += [row]

        # Loop over all ids
        rows_utrecht = {}
        values = []
        for index, rows in rows_new.items():

            # Set initial values of utrecht_ids
            end_date = ''
            particulate_matter = 0
            if index in rows_old:
                row = rows_old[index]
                if row[len(self.row_keys) + 6] == '1':
                    particulate_matter = 1
                start_date = row[len(self.row_keys) + 2]
                start_date_utrecht = row[len(self.row_keys) + 4]
                end_date_utrecht = row[len(self.row_keys) + 5]
                utrecht_city = True
                longitude_file = row[len(self.row_keys)]
                latitude_file = row[len(self.row_keys) + 1]
            else:
                start_date = ''
                start_date_utrecht = ''
                end_date_utrecht = ''
                utrecht_city = False
                longitude_file = ''
                latitude_file = ''

            #Calculate the mean longitudes and latitudes per day
            latitudes = {}
            longitudes = {}
            count_latitude = 0
            count_longitude = 0
            for key, row in enumerate(rows):
                date_object = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                date = date_object.strftime('%Y-%m-%d')
                end_date = date
                if key == 0 and start_date == '':
                    start_date = date
                latitude = row[4]
                if latitude is None or latitude == '':
                    continue
                else:
                    latitude = float(latitude)
                longitude = row[3]
                if longitude is None or longitude == '':
                    continue
                else:
                    longitude = float(longitude)
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

            # Determine if coordinates are in Utrecht and update start_date and set utrecht_city to true or false
            for date, latitude in latitudes.items():
                longitude = longitudes[date]
                degrees_lat = math.pi / 180 * latitude
                degrees_lon = math.pi / 180 * longitude
                if longitude > 180 or longitude < -180 or latitude > 90 or latitude < -90:
                    continue
                distance = 2 * math.asin(math.sqrt(((1 - math.cos(degrees_lat - self.utrecht_center_lat_degrees)) +
                                                    math.cos(degrees_lat) * math.cos(self.utrecht_center_lat_degrees) *
                                                    (1 - math.cos(
                                                        degrees_lon - self.utrecht_center_long_degrees))) / 2)) * 6371
                if distance < self.radius:
                    end_date_utrecht = date
                    if not utrecht_city and start_date_utrecht == '':
                        start_date_utrecht = date
                    utrecht_city = True
                else:
                    utrecht_city = False

            # Write row to rows_utrecht
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

        # Update the utrecht_ids
        ids = []
        output = []
        for index, row in rows_utrecht.items():
            rows_old[index] = row
            ids.append(int(row[1]))
        for index, row in rows_old.items():
            output.append(row)
            if index not in ids:
                ids.append(int(index))
        if len(values) > 0:
            self.write(output)

        return sorted(ids)
