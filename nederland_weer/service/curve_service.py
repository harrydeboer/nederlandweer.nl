from nederland_weer.model.curve import Curve
from nederland_weer.repository.measurement_repository import MeasurementRepository
import numpy as np
import json
import locale
import datetime as dt
from nederland_weer.model.measurement import Measurement


class CurveService:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()

    def make_curve(self, type_graph: str, begin_year: int, end_year: int,
                   max_year: int, begin_year_rain_perc: int) -> tuple:
        measurements = self.measurement_repository.find_all()
        text_output = ''
        if type_graph == 'temperature-day':
            curve = self._get_curve(measurements, 'mean_temp', 1, begin_year, end_year)
            locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
            json_data = self._curve_to_json(curve)
            text_output = 'Eerste zomer dag: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'dag'
        elif type_graph == 'temperature-year':
            curve = self._get_curve(measurements, 'mean_temp', 0, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            text_output = 'Temperatuur stijging: ' + str(
                int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'jaar'
        elif type_graph == 'amount-rain':
            curve = self._get_curve(measurements, 'amount_rain', 1, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            title = 'Regen hoeveelheid'
            vertical = 'regen hoeveelheid mm'
            horizontal = 'dag'
        elif type_graph == 'perc-rain':
            curve = self._get_curve(measurements, 'perc_rain', 1, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            title = 'Regen percentage'
            vertical = 'regen percentage'
            horizontal = 'dag'
        elif type_graph == 'perc-sunshine':
            curve = self._get_curve(measurements, 'perc_sunshine', 1, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            title = 'Zonneschijn'
            vertical = 'percentage zon'
            horizontal = 'dag'
        elif type_graph == 'wind-speed':
            curve = self._get_curve(measurements, 'wind_speed', 1, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            title = 'Wind snelheid'
            vertical = 'snelheid m/s'
            horizontal = 'dag'
        elif type_graph == 'wind-speed-va':
            # The vector average speed and direction are retrieved as a 2-dimensional day year array.
            speed_2d = self.make_array(measurements, begin_year,
                                                       end_year, 'wind_speed_va')
            angle_2d = self.make_array(measurements,
                                                       begin_year, end_year, 'wind_direction')

            # The 2-dimensional angle and speed are averaged over the years.
            angle = Curve.mean_of_angle(speed_2d, angle_2d)

            curve = Curve(angle, True, begin_year, end_year)
            json_data = self._curve_to_json(curve)
            title = 'Wind richting'
            vertical = 'hoek'
            horizontal = 'dag'
        elif type_graph == 'tropical':
            temperatures = self.make_array(measurements, begin_year, end_year, 'max_temp')
            data_temp = np.zeros(temperatures.shape[1])
            index_year = 0
            for year in np.transpose(temperatures):
                for temp in year:
                    if temp >= 30:
                        data_temp[index_year] += 1
                index_year += 1
            json_data = self._curve_to_json(Curve(data_temp, False, begin_year, end_year))
            title = 'Tropische dagen'
            vertical = 'aantal'
            horizontal = 'jaar'
        elif type_graph == 'extreme':
            rain_amounts = self.make_array(measurements, begin_year_rain_perc,
                                                           max_year, 'amount_rain')
            data_temp = np.zeros(rain_amounts.shape[1])
            index_year = 0
            rain_amount_average = 0
            for year in np.transpose(rain_amounts):
                for amount in year:
                    rain_amount_average += amount
            rain_amount_average = rain_amount_average / len(np.transpose(rain_amounts))
            for year in np.transpose(rain_amounts):
                index_day = 0
                rain_amount_realized = 0
                deficit_days = np.zeros(len(year))
                for amount in year:
                    rain_amount_average_day = rain_amount_average / 365.24 * (index_day + 1)
                    rain_amount_realized += amount
                    deficit_days[index_day] = rain_amount_realized - rain_amount_average_day
                    index_day += 1
                data_temp[index_year] = np.max(deficit_days)
                index_year += 1
            json_data = self._curve_to_json(
                Curve(data_temp, False, begin_year_rain_perc, max_year))
            title = 'Maximaal neerslag tekort'
            vertical = 'tekort'
            horizontal = 'jaar'

        else:
            raise Exception('No valid type.')

        return json_data, title, vertical, horizontal, text_output

    def _get_curve(self, measurements: np.ndarray, column_name: str, axis: int, first_year: int, last_year: int) \
            -> Curve:
        array = self.make_array(measurements, first_year, last_year, column_name)
        y = array.mean(axis=axis)
        return Curve(y, bool(axis), first_year, last_year)

    def _curve_to_json(self, curve: Curve) -> str:
        data_array = np.array([curve.x, curve.y, curve.y_smooth])
        return json.dumps(np.transpose(data_array).tolist())

        # Make a numpy array of weather values per day and per year.
    def make_array(self, measurements: np.ndarray, first_year: int, last_year: int, column_name: str) -> np.ndarray:

        dates = measurements[:, 1]

        column_number, factor = Measurement().__getattribute__(column_name)
        column = measurements[:, column_number]

        # The date array is initialized with zeros.
        day_year_array = np.zeros([365, last_year - first_year + 1])

        # Looping through all dates and placing the values in the dayYearArray.
        for index, date in enumerate(dates):

            # The KNMI txt file has dateformat YYYYMMDD and this is split into a year, month and day.
            year = int(date[:4])
            month = int(date[4:6])
            day = int(date[6:8])

            # The years outside the GUI range are neglected.
            if year < first_year or year > last_year:
                continue

            # The year, month and day are converted into a day number of the year.
            days_in_the_year = (dt.date(year, month, day) - dt.date(year, 1, 1)).days

            # When the year is a leap year the day number is lowered after leap day.
            # This way there are 365 days used in the leap year also.
            if year % 4 == 0 and days_in_the_year > 59:
                days_in_the_year -= 1

            day_year_array[days_in_the_year, year - first_year] = float(column[index]) * factor

        return day_year_array