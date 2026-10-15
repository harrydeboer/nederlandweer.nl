from nederland_weer.models import Measurement
from typing import List


class MeasurementRepository:

    def find_all(self, station_id: int) -> List[Measurement]:
        return list(Measurement.objects.all().filter(_station_id=station_id))

    def find_last(self, station_id: int) -> Measurement| None:
        return Measurement.objects.all().filter(_station_id=station_id).last()

    def create(self, measurement: Measurement):
        measurement.save()

    def delete(self, measurement: Measurement) -> None:
        measurement.delete()
