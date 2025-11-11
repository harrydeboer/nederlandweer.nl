import os
import csv
from dashboard_meet_je_stad.model.measurement import Measurement
from dashboard_meet_je_stad.model.sensor import Sensor
import math
import datetime


class SensorRepository:

    def __init__(self):
        self.path_data = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/'
        self.utrecht_center_lat_degrees = 52.085 * math.pi / 180
        self.utrecht_center_long_degrees = 5.085 * math.pi / 180
        self.radius = 9.46

    def write(self, sensors: dict):
        file = open(self.path_data + "utrecht_ids.csv", "w", newline='')
        rows_out = []
        for index, sensor in sensors.items():
            row = []
            for key in Measurement.properties:
                row.append(sensor.measurements[0].__getattribute__(key))
            for key in Sensor.properties:
                row.append(sensor.__getattribute__(key))
            rows_out.append(row)
        csv.writer(file).writerows(rows_out)
        file.close()

    def get(self, pm:bool = False) -> dict:
        sensors = {}
        with open(self.path_data + 'utrecht_ids.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                sensor_utrecht = Sensor(row)
                if pm and sensor_utrecht.is_particulate_matter:
                    sensors[int(row[1])] = sensor_utrecht
                elif not pm:
                    sensors[int(row[1])] = sensor_utrecht
        return sensors

    def update(self, date_now: datetime.datetime, sensors_list: list) -> dict:
        sensors_utrecht = self.get()

        #Make dictionary of sensors
        sensors = {}
        for row in sensors_list:
            if row[1] not in sensors:
                sensors[int(row[1])] = [row]
            else:
                sensors[int(row[1])] += [row]

        # Loop over all sensors
        rows_utrecht = {}
        values = []
        row_keys = {}
        for index_key, key in enumerate(Measurement.properties):
            row_keys[key] = index_key
        for index, sensor in sensors.items():

            # Set initial values of sensors_utrecht
            end_date = None
            particulate_matter = False
            if index in sensors_utrecht:
                row = sensors_utrecht[index]
                if row.is_particulate_matter:
                    particulate_matter = True
                start_date = row.start_date
                start_date_utrecht = row.start_date_utrecht
                end_date_utrecht = row.end_date_utrecht
                utrecht_city = True
                longitude_file = row.mean_longitude
                latitude_file = row.mean_latitude
            else:
                start_date = None
                start_date_utrecht = None
                end_date_utrecht = None
                utrecht_city = False
                longitude_file = None
                latitude_file = None

            #Calculate the mean longitudes and latitudes per day
            latitudes = {}
            longitudes = {}
            count_latitude = 0
            count_longitude = 0
            for key, row in enumerate(sensor):
                date_object = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                date = date_object.strftime('%Y-%m-%d')
                end_date = date
                if key == 0 and start_date == '':
                    start_date = date
                latitude = row[row_keys['latitude']]
                if latitude is None or latitude == '':
                    continue
                else:
                    latitude = float(latitude)
                longitude = row[row_keys['longitude']]
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
                if row[row_keys['pm2.5']] is not None or row[row_keys['pm10']] is not None:
                    if row[row_keys['pm2.5']] != '' or row[row_keys['pm10']] != '':
                        particulate_matter = True
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
                if end_date == date_now:
                    end_date = ''
                if end_date_utrecht == date_now:
                    end_date_utrecht = ''
                if longitudes != {} and latitudes != {}:
                    longitude_file = longitudes[list(longitudes)[-1]]
                    latitude_file = latitudes[list(latitudes)[-1]]
                extra_row = [longitude_file, latitude_file, start_date, end_date,
                             start_date_utrecht, end_date_utrecht, particulate_matter]
                rows_utrecht[index] = Sensor(values.copy() + extra_row)

        # Update the sensors utrecht
        for index, row in rows_utrecht.items():
            sensors_utrecht[index] = row
        if len(values) > 0:
            self.write(sensors_utrecht)

        return sensors_utrecht
