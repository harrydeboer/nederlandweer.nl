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

    def get_days(self, id_sensor: int, days:float) -> Sensor:
        sensor = self.find_all()[id_sensor]
        sensor.set_measurements(self.measurement_repository.get_days(id_sensor, days))
        return sensor

    def dress_with_measurements(self, sensors: Dict[int, Sensor], pm: bool, interval: str, inactive: bool,
                  id_sensor: int|None) -> Dict[int, Sensor]:
        measurements = self.measurement_cached_repository.find_all(sensors)
        earlier_day = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=1)
        for index, rows in measurements.items():
            if pm and not sensors[index].is_particulate_matter:
                sensors.pop(index)
                continue
            if not inactive and len(rows) == 1 and rows[0].timestamp < earlier_day:
                sensors.pop(index)
                continue
            else:
                if rows[-1].timestamp > earlier_day:
                    sensors[index].is_active = True
            sensors[index].set_measurements(rows)

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

    def delete(self, sensor: Sensor) -> None:
        for measurement in sensor.measurements:
            self.measurement_repository.delete(measurement)
        sensor.delete()
