from django.db import models
from django.db.models.constraints import UniqueConstraint
from typing import Any
import math
import json
import datetime


class Measurement(models.Model):

    id = models.BigAutoField(primary_key=True)
    sensor = models.ForeignKey("dashboard_meet_je_stad.Sensor", on_delete=models.CASCADE)
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
