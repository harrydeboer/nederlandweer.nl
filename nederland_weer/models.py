import datetime
from django.db import models
from typing import Any
from django.db.models.constraints import UniqueConstraint


class Station(models.Model):
    _id = models.AutoField(primary_key=True)
    _name = models.CharField(max_length=255, unique=True)
    _begin_year = models.IntegerField()
    _end_year = models.IntegerField()
    _begin_year_min_temp = models.IntegerField()
    _begin_year_mean_temp = models.IntegerField()
    _begin_year_max_temp = models.IntegerField()
    _begin_year_wind_direction = models.IntegerField()
    _begin_year_wind_speed_va = models.IntegerField()
    _begin_year_wind_speed = models.IntegerField()
    _begin_year_perc_sunshine = models.IntegerField()
    _begin_year_perc_rain = models.IntegerField()
    _begin_year_amount_rain = models.IntegerField()
    _longitude = models.FloatField()
    _latitude = models.FloatField()

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

    def get_begin_year_min_temp(self) -> int:
        return self._begin_year_min_temp

    def set_begin_year_min_temp(self, begin_year: int):
        self._begin_year_min_temp = begin_year

    def get_begin_year_mean_temp(self) -> int:
        return self._begin_year_mean_temp

    def set_begin_year_mean_temp(self, begin_year: int):
        self._begin_year_mean_temp = begin_year

    def get_begin_year_max_temp(self) -> int:
        return self._begin_year_max_temp

    def set_begin_year_max_temp(self, begin_year: int):
        self._begin_year_max_temp = begin_year

    def get_begin_year_wind_direction(self) -> int:
        return self._begin_year_wind_direction

    def set_begin_year_wind_direction(self, begin_year: int):
        self._begin_year_wind_direction = begin_year

    def get_begin_year_wind_speed(self) -> int:
        return self._begin_year_wind_speed

    def set_begin_year_wind_speed(self, begin_year: int):
        self._begin_year_wind_speed = begin_year

    def get_begin_year_wind_speed_va(self) -> int:
        return self._begin_year_wind_speed_va

    def set_begin_year_wind_speed_va(self, begin_year: int):
        self._begin_year_wind_speed_va = begin_year

    def get_begin_year_perc_sunshine(self) -> int:
        return self._begin_year_perc_sunshine

    def set_begin_year_perc_sunshine(self, begin_year: int):
        self._begin_year_perc_sunshine = begin_year

    def get_begin_year_perc_rain(self) -> int:
        return self._begin_year_perc_rain

    def set_begin_year_perc_rain(self, begin_year: int):
        self._begin_year_perc_rain = begin_year

    def get_begin_year_amount_rain(self) -> int:
        return self._begin_year_amount_rain

    def set_begin_year_amount_rain(self, begin_year: int):
        self._begin_year_amount_rain = begin_year

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

class Measurement(models.Model):
    _id = models.AutoField(primary_key=True)
    _station = models.ForeignKey(Station, on_delete=models.CASCADE)
    _timestamp = models.DateTimeField()
    _min_temp = models.FloatField(null=True)
    _mean_temp = models.FloatField(null=True)
    _max_temp = models.FloatField(null=True)
    _wind_direction = models.FloatField(null=True)
    _wind_speed_va = models.FloatField(null=True)
    _wind_speed = models.FloatField(null=True)
    _perc_sunshine = models.FloatField(null=True)
    _perc_rain = models.FloatField(null=True)
    _amount_rain = models.FloatField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("_station", "_timestamp"), name="unique_measurement"
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
        self.set_station_id(int(row[0]))
        self.set_timestamp(datetime.datetime.strptime(
            row[1],"%Y%m%d").replace(tzinfo=datetime.timezone.utc))
        self.set_min_temp(row[12])
        self.set_mean_temp(row[11])
        self.set_max_temp(row[14])
        self.set_wind_direction(row[2])
        self.set_wind_speed_va(row[3])
        self.set_wind_speed(row[4])
        self.set_perc_sunshine(row[19])
        self.set_perc_rain(row[21])
        self.set_amount_rain(row[22])

    def get_id(self) -> int:
        return self._id

    def set_id(self, measurement_id: int):
        self._id = measurement_id

    def get_timestamp(self) -> datetime.datetime:
        return self._timestamp

    def set_timestamp(self, value: datetime.datetime):
        self._timestamp = value

    def get_min_temp(self) -> float | None:
        return self._min_temp

    def set_min_temp(self, value: str|None):
        self._min_temp = self.set_float(value, 0.1)

    def get_mean_temp(self) -> float | None:
        return self._mean_temp

    def set_mean_temp(self, value: str|None):
        self._mean_temp = self.set_float(value, 0.1)

    def get_max_temp(self) -> float | None:
        return self._max_temp

    def set_max_temp(self, value: str|None):
        self._max_temp = self.set_float(value, 0.1)

    def get_wind_direction(self) -> float | None:
        return self._wind_direction

    def set_wind_direction(self, value: str|None):
        self._wind_direction = self.set_float(value)

    def get_wind_speed_va(self) -> float | None:
        return self._wind_speed_va

    def set_wind_speed_va(self, value: str|None):
        self._wind_speed_va = self.set_float(value, 0.1)

    def get_wind_speed(self) -> float | None:
        return self._wind_speed

    def set_wind_speed(self, value: str|None):
        self._wind_speed = self.set_float(value, 0.1)

    def get_perc_sunshine(self) -> float | None:
        return self._perc_sunshine

    def set_perc_sunshine(self, value: str|None):
        self._perc_sunshine = self.set_float(value)

    def get_perc_rain(self) -> float | None:
        return self._perc_rain

    def set_perc_rain(self, value: str|None):
        self._perc_rain = self.set_float(value, 0.416666666666)

    def get_amount_rain(self) -> float | None:
        return self._amount_rain

    def set_amount_rain(self, value: str|None):
        self._amount_rain = self.set_float(value, 0.1)

    def get_station_id(self):
        return self._station_id

    def set_station_id(self, value:int):
        self._station_id = value

    def get_station(self):
        return self._station

    def set_station(self, station: Station):
        self._station = station

    def set_float(self, value, factor: float = 1) -> float | None:
        if value == '' or value == '     ' or value is None:
            return None
        return float(value) * factor

class Page:
    title ='Nederland Weer'
    lastedit_date = datetime.datetime.strptime('2026-02-02', '%Y-%m-%d')

    def get_absolute_url(self):
        return ""
