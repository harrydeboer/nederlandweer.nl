import datetime
from dashboard_meet_je_stad.models import Measurement
from typing import List


class MeasurementRepository:

    def get(self, measurement_id: int) -> Measurement:

        return Measurement.objects.get(pk=measurement_id)

    def get_days(self, sensor_id: int, days:float) -> List[Measurement]:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_begin = date_now - datetime.timedelta(days=days)

        return list(Measurement.objects.filter(_sensor_id=sensor_id, _timestamp__range=(date_begin, date_now)))

    def create(self, measurement: Measurement):
        measurement.save()

    def bulk_create(self, measurements: List[Measurement]):

        for measurement in measurements:
            self.create(measurement)

    def delete(self, measurement: Measurement) -> None:
        measurement.delete()
