from typing import List
from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint
from typing import Any
import math
import json
import datetime


class Sensor(models.Model):

    id = models.AutoField(primary_key=True)
    is_particulate_matter = models.BooleanField()
    is_lux = models.BooleanField()
    is_active = False

    def get_measurements(self) -> List[Measurement]:
        return list(self.measurement_set.all())

    def set_measurements(self, measurements: List[Measurement]):
        self.measurement_set.set(measurements)

    def add_measurement(self, measurement: Measurement):
        self.measurement_set.add(measurement)

    def remove_measurement(self, measurement: Measurement):
        self.measurement_set.filter(id=measurement.id).delete()

    def to_dict(self):
        properties = {}
        measurements = []
        for measurement in self.get_measurements():
            measurements.append(measurement.to_list())
        properties['measurements'] = measurements
        for field in Sensor._meta.fields:
            prop = field.attname
            properties[prop] = self.__getattribute__(prop)
        properties['is_active'] = self.is_active

        return properties

class Measurement(models.Model):

    id = models.BigAutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    firmware_version = models.IntegerField(null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    lux = models.FloatField(null=True)
    supply = models.FloatField()
    battery = models.FloatField(null=True)
    pm25 = models.FloatField(null=True)
    pm10 = models.FloatField(null=True)
    extra = models.JSONField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("sensor", "timestamp"), name="unique_measurement"
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
        if row[0] == '' or row[0] is None:
            self.id = None
        else:
            self.id = int(row[0])
        self.sensor_id = int(row[1])
        self.timestamp = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        if row[3] == '' or row[3] is None:
            self.firmware_version = None
        else:
            self.firmware_version = int(row[3])
        self.longitude = self.set_float(row[4])
        self.latitude = self.set_float(row[5])
        self.temperature = self.set_float(row[6])
        self.humidity = self.set_float(row[7])
        self.lux = self.set_float(row[8])
        self.supply = self.set_float(row[9])
        self.battery = self.set_float(row[10])
        self.pm25 = self.set_float(row[11])
        self.pm10 = self.set_float(row[12])
        self.extra = json.dumps(row[13])

    def is_in_utrecht(self) -> bool:
        utrecht_center_lat_degrees = 52.085 * math.pi / 180
        utrecht_center_long_degrees = 5.085 * math.pi / 180
        radius = 9.46
        longitude = self.longitude
        latitude = self.latitude
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
            if prop == 'timestamp':
                row.append(self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                if prop == 'pm2.5':
                    row.append(self.pm25)
                else:
                    row.append(self.__getattribute__(prop))
        return row

    def set_float(self, value) -> float | None:
        if value == '' or value is None:
            return None
        return float(value)

class DashboardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
