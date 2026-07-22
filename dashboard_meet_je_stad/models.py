from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint
from typing import Any
import math
import json
import datetime


class Sensor(models.Model):

    def __init__(self, *args: Any, **kwargs: Any):
        self._measurements_cached = []
        super().__init__(*args, **kwargs)

    _id = models.AutoField(primary_key=True)
    _is_particulate_matter = models.BooleanField(default=False)
    _is_lux = models.BooleanField(default=False)
    _is_active_sensor = models.BooleanField(default=False)
    _measurements_cached = []

    def get_id(self) -> int:
        return self._id

    def set_id(self, sensor_id: int):
        self._id = sensor_id

    def is_particulate_matter(self) -> bool:
        return self._is_particulate_matter

    def set_is_particulate_matter(self, is_particulate_matter: bool):
        self._is_particulate_matter = is_particulate_matter

    def is_lux(self) -> bool:
        return self._is_lux

    def set_is_lux(self, is_lux: bool):
        self._is_lux = is_lux

    def is_active_sensor(self) -> bool:
        return self._is_active_sensor

    def set_is_active_sensor(self, is_active_sensor: bool):
        self._is_active_sensor = is_active_sensor

    def get_measurements(self):
        return list(self.measurement_set.all())

    def set_measurements(self, measurements):
        self.measurement_set.set(measurements)

    def get_measurements_cached(self):
        return self._measurements_cached

    def set_measurements_cached(self, measurements):
        self._measurements_cached = measurements

    def add_measurement_cached(self, measurement: Measurement):
        self._measurements_cached.append(measurement)

    def remove_measurement_cached(self, measurement: Measurement):
        self.get_measurements_cached().remove(measurement)

    # def to_dict(self) -> dict:
    #     properties = {}
    #     count = 0
    #     for field in Measurement._meta.fields:
    #         key = field.attname
    #         if field.attname == '_id':
    #             key = '_measurement_id'
    #         for index, measurement in enumerate(self.get_measurements_cached()):
    #             measurement = measurement.to_list()
    #             if key[1:] in properties:
    #                 properties[key[1:]].append(measurement[count])
    #             else:
    #                 properties[key[1:]] = [measurement[count]]
    #         count += 1
    #
    #     for field in Sensor._meta.fields:
    #         prop = field.attname
    #         try:
    #             attribute = getattr(self, 'get_' + prop[1:])
    #         except AttributeError:
    #             attribute = getattr(self, prop[1:])
    #         properties[prop[1:]] = attribute()
    #
    #     return properties

class Measurement(models.Model):

    _id = models.BigAutoField(primary_key=True)
    _sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    _timestamp = models.DateTimeField()
    _firmware_version = models.IntegerField(null=True)
    _longitude = models.FloatField(null=True)
    _latitude = models.FloatField(null=True)
    _temperature = models.FloatField(null=True)
    _humidity = models.FloatField(null=True)
    _lux = models.FloatField(null=True)
    _supply = models.FloatField()
    _battery = models.FloatField(null=True)
    _pm25 = models.FloatField(null=True)
    _pm10 = models.FloatField(null=True)
    _extra = models.JSONField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("_sensor", "_timestamp"), name="unique_measurement"
            ),
        ]

    def __init__(self, *args: Any, **kwargs: Any):
        if 'row' in kwargs:
            row = kwargs['row']
            kwargs.pop('row')
        else:
            row = []
        super().__init__(*args, **kwargs)
        if len(row) == 0:
            return
        self.set_id(row[0])
        self.set_sensor_id(int(row[1]))
        self.set_timestamp(datetime.datetime.strptime(row[2],
                                                      "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc))
        self.set_firmware_version(row[3])
        self.set_longitude(row[4])
        self.set_latitude(row[5])
        self.set_temperature(row[6])
        self.set_humidity(row[7])
        self.set_lux(row[8])
        self.set_supply(row[9])
        self.set_battery(row[10])
        self.set_pm25(row[11])
        self.set_pm10(row[12])
        self.set_extra(row[13])

    def get_id(self) -> int|None:
        return self._id

    def set_id(self, value: int|str|None):
        if value is None:
            self._id = None
        else:
            self._id = int(value)

    def get_timestamp(self) -> datetime.datetime:
        return self._timestamp

    def set_timestamp(self, value: datetime.datetime):
        self._timestamp = value

    def get_firmware_version(self) -> int|None:
        return self._firmware_version

    def set_firmware_version(self, value: int|None):
        self._firmware_version = value

    def get_longitude(self) -> float | None:
        return self._longitude

    def set_longitude(self, value: str|None):
        self._longitude = self.set_float(value)

    def get_latitude(self) -> float | None:
        return self._latitude

    def set_latitude(self, value: str|None):
        self._latitude = self.set_float(value)

    def get_temperature(self) -> float | None:
        return self._temperature

    def set_temperature(self, value: float|None):
        self._temperature = self.set_float(value)

    def get_humidity(self) -> float | None:
        return self._humidity

    def set_humidity(self, value: float|None):
        self._humidity = self.set_float(value)

    def get_lux(self) -> float|None:
        return self._lux

    def set_lux(self, value: float|None):
        self._lux = self.set_float(value)

    def get_supply(self) -> float|None:
        return self._supply

    def set_supply(self, value: float|None):
        self._supply = self.set_float(value)

    def get_battery(self) -> float|None:
        return self._battery

    def set_battery(self, value: float|None):
        self._battery = self.set_float(value)

    def get_pm25(self) -> float|None:
        return self._pm25

    def set_pm25(self, value: float|None):
        return self.set_float(value)

    def get_pm10(self) -> float|None:
        return self._pm10

    def set_pm10(self, value: float|None):
        self._pm10 = self.set_float(value)

    def get_sensor_id(self):
        return self._sensor_id

    def set_sensor_id(self, value:int):
        self._sensor_id = value

    def get_sensor(self):
        return self._sensor

    def set_sensor(self, sensor: Sensor):
        self._sensor = sensor

    def get_extra(self) -> str:
        return json.loads(self._extra)

    def set_extra(self, extra: list|None):
        self._extra = json.dumps(extra)

    def is_in_utrecht(self) -> bool:
        utrecht_center_lat_degrees = 52.085 * math.pi / 180
        utrecht_center_long_degrees = 5.085 * math.pi / 180
        radius = 9.46
        longitude = self.get_longitude()
        latitude = self.get_latitude()
        if longitude is None or latitude is None:
            return False

        degrees_lat = math.pi / 180 * latitude
        degrees_lon = math.pi / 180 * longitude
        if longitude > 180 or longitude < -180 or latitude > 90 or latitude < -90:
            return False

        distance = 2 * math.asin(math.sqrt(((1 - math.cos(degrees_lat - utrecht_center_lat_degrees)) +
                                            math.cos(degrees_lat) * math.cos(utrecht_center_lat_degrees) *
                                            (1 - math.cos(
                                                degrees_lon - utrecht_center_long_degrees))) / 2)) * 6371
        if distance < radius:
            return True

        return False

    def to_list(self):
        row = []
        for field in Measurement._meta.fields:
            prop = field.attname
            if prop == '_timestamp':
                row.append(self.get_timestamp().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                attribute = getattr(self, 'get_' + prop[1:])
                row.append(attribute())
        return row

    def set_float(self, value) -> float | None:
        if value == '' or value is None:
            return None
        return float(value)

class DashboardUser(models.Model):
    _id = models.AutoField(primary_key=True)
    _user = models.OneToOneField(User, on_delete=models.CASCADE)
    _sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)

    def get_id(self) -> int:
        return self._id

    def set_id(self, value:int):
        self._id = value

    def get_user(self) -> User:
        return self._user

    def set_user(self, user: User):
        self._user = user

    def get_sensor(self) -> Sensor:
        return self._sensor

    def set_sensor(self, sensor: Sensor):
        self._sensor = sensor

