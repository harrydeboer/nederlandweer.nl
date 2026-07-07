from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from typing import Dict
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class SensorRepository:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.make_grid_service = MakeGridService()

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
        sensor.set_measurements(self.measurement_repository.get_from_sensor(id_sensor))
        return sensor

    def get_days(self, id_sensor: int, days:float) -> Sensor:
        sensor = self.find_all()[id_sensor]
        sensor.set_measurements(self.measurement_repository.get_days(id_sensor, days))
        return sensor

    def get_small_utrecht(self, sensors:Dict[int, Sensor], interval: str, id_sensor: int) -> Dict[int, Sensor]:
        measurements = self.measurement_repository.get_small_utrecht()
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
