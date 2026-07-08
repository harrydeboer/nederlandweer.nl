import datetime
from dashboard_meet_je_stad.models import Measurement
import json
from typing import List


class MeasurementRepository:

    def get(self, measurement_id: int) -> Measurement:

        return Measurement.objects.get(pk=measurement_id)

    def get_from_sensor(self, sensor_id: int) -> List[Measurement]:

        return list(Measurement.objects.filter(sensor_id=sensor_id))

    def get_by_sensor_and_timestamp(self, sensor_id: int, timestamp: datetime.datetime) -> Measurement:

        return Measurement.objects.filter(sensor_id=sensor_id, timestamp=timestamp).get()

    def get_days(self, id_sensor: int, days:float) -> List[Measurement]:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_begin = date_now - datetime.timedelta(days=days)

        return list(Measurement.objects.filter(sensor_id=id_sensor, timestamp__range=(date_begin, date_now)))

    def create(self, measurement: Measurement):
        measurement.save()

    def bulk_create(self, measurements: List[Measurement]):

        Measurement.objects.bulk_create(measurements)
