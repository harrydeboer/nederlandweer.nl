import datetime
from dashboard_meet_je_stad.models import Measurement
from dashboard_meet_je_stad.models import Sensor
from typing import List
import json
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class MeasurementRepository:

    def __init__(self):
        self.sensor_repository = SensorRepository()

    def get(self, id_sensor: int) -> List[Measurement]:
        measurements = []

        return measurements

    def get_days(self, id_sensor: int, days:float) -> List[Measurement]:
        measurements = []
        date = datetime.datetime.now(datetime.timezone.utc)
        date -= datetime.timedelta(days=days)

        return measurements

    def create(self, measurement: Measurement):
        measurement.save()

    def bulk_create(self, results: list):
        if len(results) == 0:
            return
        measurements = []
        sensors = self.sensor_repository.find_all()
        for row in results:
            measurement = self.row_to_measurement(row)
            if measurement.sensor_id not in sensors:
                sensor = Sensor()
                if measurement.pm25 is not None or measurement.pm10 is not None:
                    sensor.is_particulate_matter = True
                else:
                    sensor.is_particulate_matter = False
                if measurement.lux is not None:
                    sensor.is_lux = True
                else:
                    sensor.is_lux = False
                sensor.id = measurement.sensor_id
                self.sensor_repository.create(sensor)
                sensor.first_measurement_object = measurement
            else:
                sensor = sensors[measurement.sensor_id]
            sensor.last_measurement_object = measurement
            if measurement.is_in_utrecht():
                measurements.append(measurement)
        Measurement.objects.bulk_create(measurements)
        for sensor_id, sensor in sensors.items():
            if sensor.first_measurement_object:
                sensor.first_measurement = sensor.first_measurement_object.id
            if sensor.last_measurement_object:
                sensor.last_measurement = sensor.last_measurement_object.id
            self.sensor_repository.update(sensor)

    def row_to_measurement(self, row: list) -> Measurement:
        measurement = Measurement()
        measurement.timestamp = (datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                                 .astimezone(datetime.timezone.utc))
        measurement.sensor_id = row[0]
        measurement.firmware_version = row[3]
        measurement.longitude = row[4]
        measurement.latitude = row[5]
        measurement.temperature = row[6]
        measurement.humidity = row[7]
        measurement.lux = row[8]
        measurement.supply = row[9]
        measurement.battery = row[10]
        measurement.pm25 = row[11]
        measurement.pm10 = row[12]
        measurement.extra = json.dumps(row[13])

        return measurement
