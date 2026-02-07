from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    begin_year = models.IntegerField()
    end_year = models.IntegerField()
    begin_year_perc_rain = models.IntegerField()
    begin_year_amount_rain = models.IntegerField()

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