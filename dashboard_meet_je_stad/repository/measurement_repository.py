import datetime
from django.db.utils import IntegrityError
from dashboard_meet_je_stad.models import Measurement
from typing import List
import pytz


class MeasurementRepository:

    def get(self, measurement_id: int) -> Measurement:

        return Measurement.objects.get(pk=measurement_id)

    def get_previous_month(self, sensor_id: int) -> List[Measurement]:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        first = datetime.datetime.now(pytz.timezone('Europe/Amsterdam')).replace(day=1)
        date_begin = first - datetime.timedelta(days=1)
        date_begin = date_begin.replace(day=date_now.day, hour=0, minute=0, second=0)
        diff = (datetime.datetime.now().timestamp() - date_begin.timestamp())
        date_begin = date_now - datetime.timedelta(seconds=diff)

        return list(Measurement.objects.filter(_sensor_id=sensor_id, _timestamp__range=(date_begin, date_now)))

    def create(self, measurement: Measurement):
        try:
            measurement.save()
        except IntegrityError:
            return

    def bulk_create(self, measurements: List[Measurement]):

        for measurement in measurements:
            self.create(measurement)

    def delete(self, measurement: Measurement) -> None:
        measurement.delete()
