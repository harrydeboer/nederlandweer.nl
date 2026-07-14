from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from typing import Dict
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class SensorRepository:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.make_grid_service = MakeGridService()

    def get(self, sensor_id: int) -> Sensor:

        return Sensor.objects.get(pk=sensor_id)

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

    def delete(self, sensor: Sensor) -> None:
        for measurement in sensor.get_measurements():
            self.measurement_repository.delete(measurement)
        sensor.delete()
