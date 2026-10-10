import datetime
from django.db import models


class Station(models.Model):
    _id = models.AutoField(primary_key=True)
    _name = models.CharField(max_length=255, unique=True)
    _begin_year = models.IntegerField()
    _end_year = models.IntegerField()
    _begin_year_perc_rain = models.IntegerField()
    _begin_year_amount_rain = models.IntegerField()
    _longitude = models.FloatField(null=True)
    _latitude = models.FloatField(null=True)

    def get_id(self) -> int:
        return self._id

    def set_id(self, station_id: int):
        self._id = station_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_begin_year(self) -> int:
        return self._begin_year

    def set_begin_year(self, begin_year: int):
        self._begin_year = begin_year

    def get_end_year(self) -> int:
        return self._end_year

    def set_end_year(self, end_year: int):
        self._end_year = end_year

    def get_begin_year_perc_rain(self) -> int:
        return self._begin_year_perc_rain

    def set_begin_year_perc_rain(self, begin_year: int):
        self._begin_year_perc_year = begin_year

    def get_begin_year_amount_rain(self) -> int:
        return self._begin_year_amount_rain

    def set_begin_year_amount_rain(self, begin_year: int):
        self._begin_year_amount_year = begin_year

    def get_longitude(self) -> float | None:
        return self._longitude

    def set_longitude(self, value: str|None):
        self._longitude = self.set_float(value)

    def get_latitude(self) -> float | None:
        return self._latitude

    def set_latitude(self, value: str|None):
        self._latitude = self.set_float(value)

    def set_float(self, value) -> float | None:
        if value == '' or value is None:
            return None
        return float(value)

    def to_dict(self) -> dict:
        properties = {}

        for field in Station._meta.fields:
            prop = field.attname
            try:
                attribute = getattr(self, 'get_' + prop[1:])
            except AttributeError:
                attribute = getattr(self, prop[1:])
            properties[prop[1:]] = attribute()

        return properties

class DawnDusk:

    def __init__(self, day: int, dawn: float, dusk: float):
        self.day = day
        self.dawn = dawn
        self.dusk = dusk

class Measurement:
    # (column_number, factor)
    min_temp = (12, 0.1)
    mean_temp = (11, 0.1)
    max_temp = (14, 0.1)
    wind_direction = (2, 1)
    wind_speed_va = (3, 0.1)
    wind_speed = (4, 0.1)
    perc_sunshine = (19, 1)
    perc_rain = (21, 0.416666666666)
    amount_rain = (22, 0.1)

class Page:
    title ='Nederland Weer'
    lastedit_date = datetime.datetime.strptime('2026-02-02', '%Y-%m-%d')

    def get_absolute_url(self):
        return ""
