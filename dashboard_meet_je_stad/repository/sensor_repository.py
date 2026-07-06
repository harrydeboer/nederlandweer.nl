from dashboard_meet_je_stad.models import Sensor
from typing import Dict


class SensorRepository:

    def create(self, sensor: Sensor):
        sensor.save()

    def update(self, sensor: Sensor):
        sensor.save()

    def find_all(self, pm:bool = False) -> Dict[int, Sensor]:
        sensors = Sensor.objects.all()
        sensors_return = {}
        for sensor in sensors:
            if pm and sensor.is_particulate_matter:
                sensors_return[sensor.id] = sensor
            elif not pm:
                sensors_return[sensor.id] = sensor

        return sensors_return

    def get(self, id_sensor: int) -> Sensor:
        sensor = self.find_all()[id_sensor]
        sensor.set_measurements(self.measurement_repository.get(id_sensor))
        return sensor

    def get_days(self, id_sensor: int, days:float) -> Sensor:
        sensor = self.find_all()[id_sensor]
        sensor.set_measurements(self.measurement_repository.get_days(id_sensor, days))
        return sensor

    def get_small_utrecht(self, sensors:Dict[int, Sensor], interval: str, id_sensor: int) -> Dict[int, Sensor]:
        measurements = self.measurement_repository.get_small_utrecht(sensors)
        for index, rows in measurements.items():
            sensors[index].set_measurements(rows)
            sensors[index].is_active = True

        sensors = self.make_grid_service.make_grid(sensors, 1)

        if id_sensor is not None and interval == '3month':
            is_active = False
            if sensors[id_sensor].is_active:
                is_active = True
            sensors[id_sensor] = self.get_days(id_sensor, 91)
            sensors_3month = {id_sensor: sensors[id_sensor]}
            sensors[id_sensor] = self.make_grid_service.make_grid(sensors_3month, 91)[id_sensor]
            sensors[id_sensor].is_active = is_active

        return dict(sorted(sensors.items()))

    def update_old(self, measurements: dict) -> dict:
        sensors = self.find_all()

        # Loop over all sensors
        rows_utrecht = {}
        values = []
        for index, measurements in measurements.items():

            # Set initial values of sensors
            particulate_matter = False
            if index in sensors:
                row = sensors[index]
                if row.is_particulate_matter:
                    particulate_matter = True
                if row.start_date is None:
                    start_date = None
                else:
                    start_date = row.start_date
                if row.start_date_utrecht is None:
                    start_date_utrecht = None
                else:
                    start_date_utrecht = row.start_date_utrecht
                if row.end_date_utrecht is None:
                    end_date_utrecht = None
                else:
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
            for key, measurement in enumerate(measurements):
                date = measurement.timestamp
                if key == 0 and start_date == '':
                    start_date = date
                latitude = measurement.latitude
                if latitude is None or latitude == '':
                    continue
                else:
                    latitude = float(latitude)
                longitude = measurement.longitude
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
                if measurement.pm25 is not None or measurement.pm10 is not None:
                    if measurement.pm25 != '' or measurement.pm10 != '':
                        particulate_matter = True
                values = measurement.to_list()

            # Determine if coordinates are in Utrecht and update start_date and set utrecht_city to true or false
            for date, latitude in latitudes.items():
                longitude = longitudes[date]


            # Write row to rows_utrecht
            if utrecht_city or (start_date_utrecht != '' and start_date_utrecht is not None):
                if not isinstance(end_date_utrecht, str) and end_date_utrecht is not None:
                    end_date_utrecht = end_date_utrecht.strftime('%Y-%m-%d')
                if not isinstance(start_date, str) and start_date is not None:
                    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
                if not isinstance(start_date_utrecht, str) and start_date_utrecht is not None:
                    start_date_utrecht = start_date_utrecht.strftime('%Y-%m-%d')
                if longitudes != {} and latitudes != {}:
                    longitude_file = longitudes[list(longitudes)[-1]]
                    latitude_file = latitudes[list(latitudes)[-1]]
                if particulate_matter:
                    particulate_matter = '1'
                else:
                    particulate_matter = '0'
                extra_row = [longitude_file, latitude_file, start_date,
                             start_date_utrecht, end_date_utrecht, particulate_matter]
                if values:
                    rows_utrecht[index] = Sensor(values.copy() + extra_row)

        # Update the sensors
        for index, row in rows_utrecht.items():
            sensors[index] = row
        if len(values) > 0:
            self.write(sensors)

        return sensors
