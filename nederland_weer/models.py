import datetime
from django.db import models
from typing import Any
from django.db.models.constraints import UniqueConstraint


class Station(models.Model):
    _id = models.AutoField(primary_key=True)
    _name = models.CharField(max_length=255, unique=True)
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
    _wind_direction = models.IntegerField(null=True)
    _wind_speed_va = models.IntegerField(null=True)
    _mean_wind_speed = models.IntegerField(null=True)
    _max_wind_speed = models.IntegerField(null=True)
    _max_wind_speed_hour = models.IntegerField(null=True)
    _min_wind_speed = models.IntegerField(null=True)
    _min_wind_speed_hour = models.IntegerField(null=True)
    _wind_gust = models.IntegerField(null=True)
    _wind_gust_hour = models.IntegerField(null=True)
    _min_temp = models.IntegerField(null=True)
    _min_temp_hour = models.IntegerField(null=True)
    _mean_temp = models.IntegerField(null=True)
    _max_temp = models.IntegerField(null=True)
    _max_temp_hour = models.IntegerField(null=True)
    _min_temp_10 = models.IntegerField(null=True)
    _min_temp_hour_10 = models.IntegerField(null=True)
    _amount_sunshine = models.IntegerField(null=True)
    _perc_sunshine = models.IntegerField(null=True)
    _radiation = models.IntegerField(null=True)
    _perc_rain = models.IntegerField(null=True)
    _amount_rain = models.IntegerField(null=True)
    _max_rain = models.IntegerField(null=True)
    _max_rain_hour = models.IntegerField(null=True)
    _mean_air_pressure = models.IntegerField(null=True)
    _max_air_pressure = models.IntegerField(null=True)
    _max_air_pressure_hour = models.IntegerField(null=True)
    _min_air_pressure = models.IntegerField(null=True)
    _min_air_pressure_hour = models.IntegerField(null=True)
    _min_visibility = models.IntegerField(null=True)
    _min_visibility_hour = models.IntegerField(null=True)
    _max_visibility = models.IntegerField(null=True)
    _max_visibility_hour = models.IntegerField(null=True)
    _cloudiness = models.IntegerField(null=True)
    _mean_humidity = models.IntegerField(null=True)
    _max_humidity = models.IntegerField(null=True)
    _max_humidity_hour = models.IntegerField(null=True)
    _min_humidity = models.IntegerField(null=True)
    _min_humidity_hour = models.IntegerField(null=True)
    _evapotranspiration = models.IntegerField(null=True)

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
        self.set_wind_direction(row[2])
        self.set_wind_speed_va(row[3])
        self.set_mean_wind_speed(row[4])
        self.set_max_wind_speed(row[5])
        self.set_max_wind_speed_hour(row[6])
        self.set_min_wind_speed(row[7])
        self.set_min_wind_speed_hour(row[8])
        self.set_wind_gust(row[9])
        self.set_wind_gust_hour(row[10])
        self.set_mean_temp(row[11])
        self.set_min_temp(row[12])
        self.set_min_temp_hour(row[13])
        self.set_max_temp(row[14])
        self.set_max_temp_hour(row[15])
        self.set_min_temp_10(row[16])
        self.set_min_temp_hour_10(row[17])
        self.set_amount_sunshine(row[18])
        self.set_perc_sunshine(row[19])
        self.set_radiation(row[20])
        self.set_perc_rain(row[21])
        self.set_amount_rain(row[22])
        self.set_max_rain(row[23])
        self.set_max_rain_hour(row[24])
        self.set_mean_air_pressure(row[25])
        self.set_max_air_pressure(row[26])
        self.set_max_air_pressure_hour(row[27])
        self.set_min_air_pressure(row[28])
        self.set_min_air_pressure_hour(row[29])
        self.set_min_visibility(row[30])
        self.set_min_visibility_hour(row[31])
        self.set_max_visibility(row[32])
        self.set_max_visibility_hour(row[33])
        self.set_cloudiness(row[34])
        self.set_mean_humidity(row[35])
        self.set_max_humidity(row[36])
        self.set_max_humidity_hour(row[37])
        self.set_min_humidity(row[38])
        self.set_min_humidity_hour(row[39])
        self.set_evapotranspiration(row[40])

    def get_id(self) -> int:
        return self._id

    def set_id(self, measurement_id: int):
        self._id = measurement_id

    def get_timestamp(self) -> datetime.datetime:
        return self._timestamp

    def set_timestamp(self, value: datetime.datetime):
        self._timestamp = value

    def get_wind_direction(self) -> int | None:
        return self._wind_direction

    def set_wind_direction(self, value: str|None):
        self._wind_direction = self.set_int(value)

    def get_wind_speed_va(self) -> float | None:
        return self.get_float(self._wind_speed_va, 0.1)

    def set_wind_speed_va(self, value: str|None):
        self._wind_speed_va = self.set_int(value)

    def get_mean_wind_speed(self) -> float | None:
        return self.get_float(self._mean_wind_speed, 0.1)

    def set_mean_wind_speed(self, value: str|None):
        self._mean_wind_speed = self.set_int(value)

    def get_max_wind_speed(self) -> float | None:
        return self.get_float(self._max_wind_speed, 0.1)

    def set_max_wind_speed(self, value: str|None):
        self._max_wind_speed = self.set_int(value)

    def get_max_wind_speed_hour(self) -> int | None:
        return self._max_wind_speed_hour

    def set_max_wind_speed_hour(self, value: str|None):
        self._max_wind_speed_hour = self.set_int(value)

    def get_min_wind_speed(self) -> float | None:
        return self.get_float(self._min_wind_speed, 0.1)

    def set_min_wind_speed(self, value: str|None):
        self._min_wind_speed = self.set_int(value)

    def get_min_wind_speed_hour(self) -> int | None:
        return self._min_wind_speed_hour

    def set_min_wind_speed_hour(self, value: str|None):
        self._min_wind_speed_hour = self.set_int(value)

    def get_wind_gust(self) -> float | None:
        return self.get_float(self._wind_gust, 0.1)

    def set_wind_gust(self, value: str|None):
        self._wind_gust = self.set_int(value)

    def get_wind_gust_hour(self) -> int | None:
        return self._wind_gust_hour

    def set_wind_gust_hour(self, value: str|None):
        self._wind_gust_hour = self.set_int(value)

    def get_min_temp(self) -> float | None:
        return self.get_float(self._min_temp, 0.1)

    def set_min_temp(self, value: str|None):
        self._min_temp = self.set_int(value)

    def get_min_temp_hour(self) -> int | None:
        return self._min_temp_hour

    def set_min_temp_hour(self, value: str|None):
        self._min_temp_hour = self.set_int(value)

    def get_mean_temp(self) -> float | None:
        return self.get_float(self._mean_temp, 0.1)

    def set_mean_temp(self, value: str|None):
        self._mean_temp = self.set_int(value)

    def get_max_temp(self) -> float | None:
        return self.get_float(self._max_temp, 0.1)

    def set_max_temp(self, value: str|None):
        self._max_temp = self.set_int(value)

    def get_max_temp_hour(self) -> int | None:
        return self._max_temp_hour

    def set_max_temp_hour(self, value: str|None):
        self._max_temp_hour = self.set_int(value)

    def get_min_temp_10(self) -> float | None:
        return self.get_float(self._min_temp_10, 0.1)

    def set_min_temp_10(self, value: str|None):
        self._min_temp_10 = self.set_int(value)

    def get_min_temp_hour_10(self) -> int | None:
        return self._min_temp_10_hour

    def set_min_temp_hour_10(self, value: str | None):
        self._min_temp_10_hour = self.set_int(value)

    def get_amount_sunshine(self) -> float | None:
        return self.get_float(self._amount_sunshine, 0.1)

    def set_amount_sunshine(self, value: str|None):
        self._amount_sunshine = self.set_int(value)

    def get_perc_sunshine(self) -> int | None:
        return self._perc_sunshine

    def set_perc_sunshine(self, value: str|None):
        self._perc_sunshine = self.set_int(value)

    def get_radiation(self) -> int | None:
        return self._radiation

    def set_radiation(self, value: str|None):
        self._radiation = self.set_int(value)

    def get_perc_rain(self) -> float | None:
        return self.get_float(self._perc_rain, 0.416666666666)

    def set_perc_rain(self, value: str|None):
        self._perc_rain = self.set_int(value)

    def get_amount_rain(self) -> float | None:
        return self.get_float(self._amount_rain, 0.1)

    def set_amount_rain(self, value: str|None):
        self._amount_rain = self.set_int(value)

    def get_max_rain(self) -> float | None:
        return self.get_float(self._max_rain, 0.1)

    def set_max_rain(self, value: str|None):
        self._max_rain = self.set_int(value)

    def get_max_rain_hour(self) -> int | None:
        return self._max_rain_hour

    def set_max_rain_hour(self, value: str|None):
        self._max_rain_hour = self.set_int(value)

    def get_mean_air_pressure(self) -> float | None:
        return self.get_float(self._mean_air_pressure, 0.1)

    def set_mean_air_pressure(self, value: str|None):
        self._mean_air_pressure = self.set_int(value)

    def get_max_air_pressure(self) -> float | None:
        return self.get_float(self._max_air_pressure, 0.1)

    def set_max_air_pressure(self, value: str|None):
        self._max_air_pressure = self.set_int(value)

    def get_max_air_pressure_hour(self) -> int | None:
        return self._max_air_pressure_hour

    def set_max_air_pressure_hour(self, value: str|None):
        self._max_air_pressure_hour = self.set_int(value)

    def get_min_air_pressure(self) -> float | None:
        return self.get_float(self._min_air_pressure, 0.1)

    def set_min_air_pressure(self, value: str | None):
        self._min_air_pressure = self.set_int(value)

    def get_min_air_pressure_hour(self) -> int | None:
        return self._min_air_pressure_hour

    def set_min_air_pressure_hour(self, value: str | None):
        self._min_air_pressure_hour = self.set_int(value)

    def get_min_visibility(self) -> int | None:
        return self._min_visibility

    def set_min_visibility(self, value: str|None):
        self._min_visibility = self.set_int(value)

    def get_min_visibility_hour(self) -> int | None:
        return self._min_visibility_hour

    def set_min_visibility_hour(self, value: str|None):
        self._min_visibility_hour = self.set_int(value)

    def get_max_visibility(self) -> int | None:
        return self._max_visibility

    def set_max_visibility(self, value: str | None):
        self._max_visibility = self.set_int(value)

    def get_max_visibility_hour(self) -> int | None:
        return self._max_visibility_hour

    def set_max_visibility_hour(self, value: str | None):
        self._max_visibility_hour = self.set_int(value)

    def get_cloudiness(self) -> int | None:
        return self._cloudiness

    def set_cloudiness(self, value: str | None):
        self._cloudiness = self.set_int(value)

    def get_mean_humidity(self) -> int | None:
        return self._mean_humidity

    def set_mean_humidity(self, value: str | None):
        self._mean_humidity = self.set_int(value)

    def get_max_humidity(self) -> int | None:
        return self._max_humidity

    def set_max_humidity(self, value: str | None):
        self._max_humidity = self.set_int(value)

    def get_max_humidity_hour(self) -> int | None:
        return self._max_humidity_hour

    def set_max_humidity_hour(self, value: str | None):
        self._max_humidity_hour = self.set_int(value)

    def get_min_humidity(self) -> int | None:
        return self._min_humidity

    def set_min_humidity(self, value: str | None):
        self._min_humidity = self.set_int(value)

    def get_min_humidity_hour(self) -> int | None:
        return  self._min_humidity_hour

    def set_min_humidity_hour(self, value: str | None):
        self._min_humidity_hour = self.set_int(value)

    def get_evapotranspiration(self) -> float | None:
        return self.get_float(self._evapotranspiration, 0.1)

    def set_evapotranspiration(self, value: str | None):
        self._evapotranspiration = self.set_int(value)

    def get_station_id(self):
        return self._station_id

    def set_station_id(self, value:int):
        self._station_id = value

    def get_station(self):
        return self._station

    def set_station(self, station: Station):
        self._station = station

    def get_float(self, value: int|None, factor: float):
        if value is None:
            return None
        return value * factor

    def set_int(self, value) -> int | None:
        if value == '' or value == '     ' or value is None:
            return None
        return int(value)

class Page:
    title ='Nederland Weer'
    lastedit_date = datetime.datetime.strptime('2026-02-02', '%Y-%m-%d')

    def get_absolute_url(self):
        return ""
