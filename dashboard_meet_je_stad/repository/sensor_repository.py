import datetime
from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.measurement_cached_repository import MeasurementCachedRepository
from typing import Dict
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class SensorRepository:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.measurement_cached_repository = MeasurementCachedRepository()
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

    def get_days(self, sensor_id: int, days:float) -> Sensor:
        sensor = self.find_all()[sensor_id]
        sensor.set_measurements(self.measurement_repository.get_days(sensor_id, days))
        return sensor

    def filter_and_dress_with_measurements(self, sensors: Dict[int, Sensor], pm: bool, interval: str, inactive: bool,
                  sensor_id: int|None) -> Dict[int, Sensor]:
        measurements = self.measurement_cached_repository.find_all(sensors)
        earlier_day = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=1)
        for index, rows in measurements.items():
            if pm and not sensors[index].is_particulate_matter:
                sensors.pop(index)
                continue
            if not inactive and rows[-1].timestamp < earlier_day:
                sensors.pop(index)
                continue
            else:
                if rows[-1].timestamp > earlier_day:
                    sensors[index].is_active = True
            sensors[index].set_measurements(rows)

        sensors = self.make_grid_service.make_grid(sensors, 1)

        if sensor_id is not None and interval == '3month':
            if sensor_id in sensors:
                is_active = False
                if sensors[sensor_id].is_active:
                    is_active = True
                sensors[sensor_id] = self.get_days(sensor_id, 91)
                sensors_3month = {sensor_id: sensors[sensor_id]}
                sensors[sensor_id] = self.make_grid_service.make_grid(sensors_3month, 91)[sensor_id]
                sensors[sensor_id].is_active = is_active

        return dict(sorted(sensors.items()))

    def delete(self, sensor: Sensor) -> None:
        for measurement in sensor.get_measurements():
            self.measurement_repository.delete(measurement)
        sensor.delete()
