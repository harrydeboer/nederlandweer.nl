import datetime
from dashboard_meet_je_stad.models import Measurement
import json
from typing import List, Dict


class MeasurementRepository:

    def get(self, measurement_id: int) -> Measurement:

        return Measurement.objects.get(pk=measurement_id)

    def get_from_sensor(self, sensor_id: int) -> List[Measurement]:

        return list(Measurement.objects.filter(sensor_id=sensor_id))

    def get_by_sensor_and_timestamp(self, sensor_id: int, timestamp: datetime.datetime) -> Measurement:

        return Measurement.objects.filter(sensor_id=sensor_id, timestamp=timestamp).get()

    def get_small(self) -> Dict[int, List[Measurement]]:
        measurements = {}
        for measurement in Measurement.objects.all():
            if measurement.sensor_id not in measurements:
                measurements[measurement.sensor_id] = [measurement]
            else:
                measurements[measurement.sensor_id].append(measurement)

        return measurements

    def get_days(self, id_sensor: int, days:float) -> List[Measurement]:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_begin = date_now - datetime.timedelta(days=days)

        return list(Measurement.objects.filter(sensor_id=id_sensor, timestamp__range=(date_begin, date_now)))

    def create(self, measurement: Measurement):
        measurement.save()

    def bulk_create(self, measurements: List[Measurement]):

        Measurement.objects.bulk_create(measurements)

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
