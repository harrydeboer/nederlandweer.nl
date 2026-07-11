from django.db import models
from typing import List
import datetime
from .measurement import Measurement


class Sensor(models.Model):

    id = models.AutoField(primary_key=True)
    is_particulate_matter = models.BooleanField()
    is_lux = models.BooleanField()
    is_active = False
    measurements = []

    def get_measurements(self) -> List[Measurement]:
        return self.measurements

    def set_measurements(self, measurements: List[Measurement]):
        self.measurements = measurements

    def to_dict(self):
        properties = {}
        for field in Measurement._meta.fields:
            prop = field.attname
            if prop == 'id':
                continue
            properties[prop] = []
            for measurement in self.measurements:
                value = measurement.__getattribute__(prop)
                if isinstance(value, datetime.datetime):
                    properties[prop].append(value.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    properties[prop].append(value)
        for field in Sensor._meta.fields:
            prop = field.attname
            value = self.__getattribute__(prop)
            if isinstance(value, datetime.datetime):
                properties[prop] = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                properties[prop] = value
        properties['is_active'] = self.is_active
        return properties
