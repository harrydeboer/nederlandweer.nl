import datetime
from django.db.models import QuerySet
from dashboard_meet_je_stad.models import Measurement
from dashboard_meet_je_stad.models import Sensor
import json
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class MeasurementRepository:

    def __init__(self):
        self.sensor_repository = SensorRepository()

    def get(self, measurement_id: int) -> Measurement:

        return Measurement.objects.get(pk=measurement_id)

    def get_by_sensor_and_timestamp(self, sensor_id: int, timestamp: datetime.datetime) -> Measurement:

        return Measurement.objects.filter(sensor_id=sensor_id, timestamp=timestamp).get()

    def get_days(self, id_sensor: int, days:float) -> QuerySet[Measurement]:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_begin = date_now - datetime.timedelta(days=days)

        return Measurement.objects.filter(sensor_id=id_sensor, timestamp__range=(date_begin, date_now))

    def create(self, measurement: Measurement):
        measurement.save()

    def bulk_create(self, results: list):
        if len(results) == 0:
            return
        measurements = []
        sensors = self.sensor_repository.find_all()
        first_measurements = {}
        last_measurements = {}
        for row in results:
            measurement = self.row_to_measurement(row)
            if measurement.is_in_utrecht() and measurement.sensor_id not in sensors:
                measurements.append(measurement)
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
                first_measurements[measurement.sensor_id] = measurement
                last_measurements[sensor.id] = measurement
            elif measurement.is_in_utrecht() and measurement.sensor_id in sensors:
                sensor = sensors[measurement.sensor.id]
                measurements.append(measurement)
                last_measurements[sensor.id] = measurement
        Measurement.objects.bulk_create(measurements)
        sensors = self.sensor_repository.find_all()
        for sensor_id, sensor in sensors.items():
            if sensor_id in first_measurements:
                sensor.first_measurement = self.get_by_sensor_and_timestamp(sensor_id,
                                                                            first_measurements[sensor_id].timestamp).id
            if sensor_id in last_measurements:
                sensor.last_measurement = self.get_by_sensor_and_timestamp(sensor_id,
                                                                            last_measurements[sensor_id].timestamp).id
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
