from typing import List
from nederland_weer.models import Measurement
import numpy as np
import datetime as dt


class MeasurementRepository:

    def find_all(self, station_id: int) -> List[Measurement]:
        return list(Measurement.objects.all().filter(_station_id=station_id).order_by('_timestamp'))

    def make_array(self, measurements: List[Measurement], component: str, begin_year: int, end_year: int) -> np.ndarray:
        first_year = measurements[0].get_timestamp().year
        last_year = measurements[-1].get_timestamp().year
        first_day = measurements[0].get_timestamp().day
        last_day = measurements[-1].get_timestamp().day
        first_month = measurements[0].get_timestamp().month
        last_month = measurements[-1].get_timestamp().month
        begin_year_array = begin_year
        end_year_array = end_year
        if first_day != 1 or first_month != 1:
            begin_year_array = begin_year + 1
        if last_day != 31 or last_month != 12:
            end_year_array = end_year - 1
        day_year_array = np.zeros([365, end_year_array - begin_year_array + 1])
        last_good_value = None
        for index, measurement in enumerate(measurements):
            year = int(measurement.get_timestamp().year)
            month = int(measurement.get_timestamp().month)
            day = int(measurement.get_timestamp().day)

            if year == first_year and (first_day != 1 or first_month != 1):
                continue

            if year == last_year and (last_day != 31 or last_month != 12):
                continue

            attribute = getattr(measurement, 'get_' + component)

            # The years outside the GUI range are neglected.
            if year < begin_year_array or year > end_year_array:
                continue

            # The year, month and day are converted into a day number of the year.
            days_in_the_year = (dt.date(year, month, day) - dt.date(year, 1, 1)).days

            # When the year is a leap year the day number is lowered after leap day.
            # This way there are 365 days used in the leap year also.
            if year % 4 == 0 and days_in_the_year > 59:
                days_in_the_year -= 1

            if attribute() is None:
                if last_good_value is None:
                    last_good_value = getattr(measurements[index - 1], 'get_' + component)()
                if last_good_value is None:
                    continue
                else:
                    day_year_array[days_in_the_year, year - begin_year_array] = float(last_good_value)
            else:
                day_year_array[days_in_the_year, year - begin_year_array] = float(attribute())

        return day_year_array

    def find_last(self, station_id: int) -> Measurement| None:
        return Measurement.objects.all().filter(_station_id=station_id).last()

    def create(self, measurement: Measurement):
        measurement.save()

    def delete(self, measurement: Measurement) -> None:
        measurement.delete()
