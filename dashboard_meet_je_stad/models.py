from django.db import models
from django.db.models.constraints import UniqueConstraint
import math


class Sensor(models.Model):

    id = models.AutoField(primary_key=True)
    is_particulate_matter = models.BooleanField()
    is_lux = models.BooleanField()
    first_measurement = models.IntegerField(null=True)
    last_measurement = models.IntegerField(null=True)
    measurements = []

    def add_measurement(self, measurement: Measurement):
        self.measurements.append(measurement)

    def set_measurements(self, measurements: list):
        self.measurements = measurements

class Measurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    firmware_version = models.IntegerField(null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
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
        for prop, field in Measurement._meta.fields:
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
