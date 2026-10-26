from nederland_weer.models import Measurement
from nederland_weer.repository.dawn_dusk_repository import DawnDuskRepository
from nederland_weer.repository.measurement_repository import MeasurementRepository
import numpy as np
import json
import locale
import datetime as dt
from typing import Tuple, List


class CurveService:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.dawn_dusk_repository = DawnDuskRepository()
        self.y_smooth = None
        self.begin_year = None
        self.end_year = None

    def make_curves(self, component: str, measurements: List[Measurement]) -> Tuple[str, str, str, str, str]:
        first_day = measurements[0].get_timestamp().day
        last_day = measurements[-1].get_timestamp().day
        first_month = measurements[0].get_timestamp().month
        last_month = measurements[-1].get_timestamp().month
        begin_year = measurements[0].get_timestamp().year
        end_year = measurements[-1].get_timestamp().year
        self.begin_year = begin_year
        self.end_year = end_year
        if first_day != 1 or first_month != 1:
            self.begin_year = begin_year + 1
        if last_day != 31 or last_month != 12:
            self.end_year = end_year - 1
        text_output = ''
        if component == 'temperature-day':
            locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                   'mean_temp',
                                                                                   begin_year,
                                                                                   end_year).mean(axis=1), True)
            text_output = 'Eerste zomerdag: ' + self._get_first_date_summer(self.y_smooth).strftime("%d %B") + '.'
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'dag'
        elif component == 'temperature-year':
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                   'mean_temp',
                                                                                   begin_year,
                                                                                   end_year).mean(axis=0), False)
            text_output = 'Temperatuur stijging: ' + str(
                int((self.y_smooth[-1] - self.y_smooth[0]) * 10) / 10).replace('.', ',') + "°."
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'jaar'
        elif component == 'amount-rain':
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                 'amount_rain', begin_year,
                                                                                 end_year).mean(axis=1), True)
            title = 'Regen hoeveelheid'
            vertical = 'regen hoeveelheid mm'
            horizontal = 'dag'
        elif component == 'perc-rain':
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                 'perc_rain', begin_year,
                                                                                 end_year).mean(axis=1), True)
            title = 'Regen percentage'
            vertical = 'regen percentage'
            horizontal = 'dag'
        elif component == 'perc-sunshine':
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                 'perc_sunshine', begin_year,
                                                                                 end_year).mean(axis=1),
                                            True, 'perc_sunshine')
            title = 'Zonneschijn'
            vertical = 'percentage zon'
            horizontal = 'dag'
        elif component == 'wind-speed':
            json_data = self._curve_to_json(self.measurement_repository.make_array(measurements,
                                                                                 'wind_speed', begin_year,
                                                                                 end_year).mean(axis=1), True)
            title = 'Wind snelheid'
            vertical = 'snelheid m/s'
            horizontal = 'dag'
        elif component == 'wind-speed-va':
            # The vector average speed and direction are retrieved as a 2-dimensional day year array.
            speed_2d = self.measurement_repository.make_array(measurements,
                                                            'wind_speed_va', begin_year,
                                                            end_year)
            angle_2d = self.measurement_repository.make_array(measurements,
                                                            'wind_direction', begin_year,
                                                            end_year)

            # The 2-dimensional angle and speed are averaged over the years.
            angle = self._mean_of_angle(speed_2d, angle_2d)

            json_data = self._curve_to_json(angle, True)
            title = 'Wind richting'
            vertical = 'hoek'
            horizontal = 'dag'
        elif component == 'tropical':
            temperatures = self.measurement_repository.make_array(measurements,
                                                                'max_temp', begin_year,
                                                                end_year)
            data_temp = np.zeros(temperatures.shape[1])
            index_year = 0
            for year in np.transpose(temperatures):
                for temp in year:
                    if temp >= 30:
                        data_temp[index_year] += 1
                index_year += 1
            json_data = self._curve_to_json(data_temp, False)
            title = 'Tropische dagen'
            vertical = 'aantal'
            horizontal = 'jaar'
        elif component == 'extreme':
            rain_amounts = self.measurement_repository.make_array(measurements,
                                                                'amount_rain', begin_year,
                                                                end_year)
            data_rain = np.zeros(rain_amounts.shape[1])
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
                data_rain[index_year] = np.max(deficit_days)
                index_year += 1
            json_data = self._curve_to_json(data_rain, False)
            title = 'Maximaal neerslag tekort'
            vertical = 'tekort'
            horizontal = 'jaar'

        else:
            raise Exception('No valid component.')

        return json_data, title, vertical, horizontal, text_output

    def _curve_to_json(self, y: np.ndarray, is_day: bool, column_name: str|None = None) -> str:
        if column_name == 'perc_sunshine':
            dawn_dusks = self.dawn_dusk_repository.find_all()
            for index, day in enumerate(y):
                y[index] = y[index] / 2.4 * 24 / (dawn_dusks[index - 1].dusk - dawn_dusks[index - 1].dawn)

        if is_day:
            x = np.arange(1, 366)
            box_points = 30

            # The start and end of a day curve should match. The data is tripled in order for the smoothing
            # to behave well at the endpoints.
            self.y_smooth = self._make_smooth_curve(np.append(y, [y, y]), box_points)

            # The middle part of the smooth curve is retrieved.
            length = int(self.y_smooth.size / 3)
            self.y_smooth = self.y_smooth[length: 2 * length]
        else:
            x = np.arange(self.begin_year, self.end_year + 1)

            # The box_points is a fraction of the difference between end year and begin year.
            box_points = int((self.end_year - self.begin_year) / 120 * 30)

            self.y_smooth = self._make_smooth_curve_linear_extrapolate(y, box_points)

        data_array = np.array((x, y, self.y_smooth))

        return json.dumps(np.transpose(data_array).tolist())

    def _make_smooth_curve(self, y, box_points) -> np.ndarray:

        box = np.ones(box_points) / box_points
        result = np.convolve(y, box, mode='same')

        return result

    # A moving average is used to smooth the curve. At the edges the data is extrapolated linearly with a regression.
    # That way the smoothing behaves well at the edges. After smoothing the extrapolated data is removed.
    def _make_smooth_curve_linear_extrapolate(self, y, box_points) -> np.ndarray:

        y_regress = y[:box_points]
        x_regress = np.arange(0, box_points)

        intercept, slope = self._calculate_intercept_and_slope(y_regress, x_regress)

        y_prepend = np.arange(box_points * (-1), 0) * slope + intercept

        y_regress = y[-box_points:]
        x_regress = np.arange(y.size - box_points, y.size)

        intercept, slope = self._calculate_intercept_and_slope(y_regress, x_regress)

        y_append = np.arange(y.size, y.size + box_points) * slope + intercept

        box = np.ones(box_points) / box_points
        result = np.convolve(np.append(np.append(y_prepend, y), y_append), box, mode='same')

        return result[box_points:-box_points]

    def _calculate_intercept_and_slope(self, y_regress: np.ndarray, x_regress: np.ndarray) -> Tuple[float, float]:

        y_mean = y_regress.mean()
        x_mean = x_regress.mean()

        slope = float(np.sum((x_regress - x_mean) * (y_regress - y_mean))) \
                / float(np.sum((x_regress - x_mean) * (x_regress - x_mean)))
        intercept = y_mean - slope * x_mean

        return intercept, slope

    # The first day of summer is the point where the temperature is equal to the temperature 92 days later.
    # On average a season has 92 days. The smooth curves are subtracted with 92 days interval.
    # Then the absolute value is taken.
    # Then the first day of summer is the point where these absolute values are minimal.
    # Then the first day is translated into a date object.
    def _get_first_date_summer(self, y_smooth: np.ndarray) -> dt.datetime:

        subtract = np.subtract(y_smooth[92:], y_smooth[:365 - 92])
        first_day_of_summer = int(np.where(np.absolute(subtract) == np.min(np.absolute(subtract)))[0][0])

        return dt.datetime(2025, 1, 1) + dt.timedelta(first_day_of_summer)

    def _mean_of_angle(self, speed_2d: np.ndarray, angle_2d: np.ndarray) -> np.ndarray:

        # The KNMI angle starts at 0 (north) and goes clockwise to 360 degrees.
        # The x and y coordinates are calculated because a mean can only be taken from x and y coordinates.
        x = speed_2d * np.sin(angle_2d / 360 * 2 * np.pi)
        y = speed_2d * np.cos(angle_2d / 360 * 2 * np.pi)
        x_mean = x.mean(1)
        y_mean = y.mean(1)

        angle = np.zeros(365)

        for index, value in enumerate(x_mean):
            angle[index] = np.arctan2(y_mean[index], x_mean[index]) / np.pi * 180

            # The arctan2 function start at -Pi (west) and goes counterclockwise to Pi.
            # The angle starts at 0 (east) and goes to 360.
            # There is a gap of 2 Pi in the west point and this gap is closed
            # by adding 360 degrees when y < 0 (y changes sign in the west point).
            if y_mean[index] < 0:
                angle[index] += 360

        return angle

    # The curve can have a mean per month if it is a day curve.
    def _get_month_mean(self, y: np.ndarray, month: int, year: int) -> float:

        if y.size != 365:
            raise Exception('This stat can only be calculated for day curves.')

        day_number_begin = dt.datetime(year, month, 1).timetuple().tm_yday
        if month == 12:
            day_number_end = dt.datetime(year, month, 31).timetuple().tm_yday
        else:
            day_number_end = dt.datetime(year, month + 1, 1).timetuple().tm_yday - 1

        return y[day_number_begin - 1:day_number_end].mean(axis=0)
