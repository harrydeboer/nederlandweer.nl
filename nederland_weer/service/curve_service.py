from nederland_weer.repository.dawn_dusk_repository import DawnDuskRepository
from nederland_weer.repository.measurement_repository import MeasurementRepository
import numpy as np
import json
import locale
import datetime as dt
from nederland_weer.model.measurement import Measurement
from typing import Tuple


class CurveService:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.dawn_dusk_repository = DawnDuskRepository()

    def make_curve(self, station_id: int, type_graph: str, begin_year: int, end_year: int,
                   max_year: int) -> Tuple[str, str, str, str, str]:
        measurements = self.measurement_repository.find_all(station_id)
        text_output = ''
        if type_graph == 'temperature-day':
            locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
            x, y, y_smooth = self._get_curve(measurements, 'mean_temp', 1, begin_year, end_year)
            json_data = self._curve_to_json((x, y, y_smooth))
            text_output = 'Eerste zomerdag: ' + self._get_first_date_summer(y_smooth).strftime("%d %B") + '.'
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'dag'
        elif type_graph == 'temperature-year':
            x, y, y_smooth = self._get_curve(measurements, 'mean_temp', 0, begin_year, end_year)
            json_data = self._curve_to_json((x, y, y_smooth))
            text_output = 'Temperatuur stijging: ' + str(
                int((y_smooth[-1] - y_smooth[0]) * 10) / 10).replace('.', ',') + "°."
            title = 'Temperatuur'
            vertical = 'temperatuur °C'
            horizontal = 'jaar'
        elif type_graph == 'amount-rain':
            json_data = self._curve_to_json(self._get_curve(measurements, 'amount_rain', 1, begin_year, end_year))
            title = 'Regen hoeveelheid'
            vertical = 'regen hoeveelheid mm'
            horizontal = 'dag'
        elif type_graph == 'perc-rain':
            json_data = self._curve_to_json(self._get_curve(measurements, 'perc_rain', 1, begin_year, end_year))
            title = 'Regen percentage'
            vertical = 'regen percentage'
            horizontal = 'dag'
        elif type_graph == 'perc-sunshine':
            json_data = self._curve_to_json(self._get_curve(measurements, 'perc_sunshine',1, begin_year, end_year))
            title = 'Zonneschijn'
            vertical = 'percentage zon'
            horizontal = 'dag'
        elif type_graph == 'wind-speed':
            json_data = self._curve_to_json(self._get_curve(measurements, 'wind_speed', 1, begin_year, end_year))
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
            angle = self._mean_of_angle(speed_2d, angle_2d)

            json_data = self._curve_to_json(self._make_curve_data(angle, 1, begin_year, end_year))
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
            json_data = self._curve_to_json(self._make_curve_data(data_temp, 0,
                                             begin_year, end_year))
            title = 'Tropische dagen'
            vertical = 'aantal'
            horizontal = 'jaar'
        elif type_graph == 'extreme':
            rain_amounts = self.make_array(measurements, begin_year,
                                           max_year, 'amount_rain')
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
            json_data = self._curve_to_json(self._make_curve_data(data_rain, 0, begin_year, max_year))
            title = 'Maximaal neerslag tekort'
            vertical = 'tekort'
            horizontal = 'jaar'

        else:
            raise Exception('No valid type.')

        return json_data, title, vertical, horizontal, text_output

    def _get_curve(self, measurements: np.ndarray, column_name: str, axis: int,
                   first_year: int, last_year: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        array = self.make_array(measurements, first_year, last_year, column_name)
        y = array.mean(axis=axis)

        if column_name == 'perc_sunshine':
            dawn_dusks = self.dawn_dusk_repository.find_all()
            for index, day in enumerate(y):
                y[index] = y[index] / 2.4 * 24 / (dawn_dusks[index - 1].dusk - dawn_dusks[index - 1].dawn)

        return self._make_curve_data(y, axis, first_year, last_year)


    def _make_curve_data(self, y: np.ndarray, axis, first_year: int, last_year: int) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if bool(axis):
            x = np.arange(1, 366)
            box_points = 30

            # The start and end of a day curve should match. The data is tripled in order for the smoothing
            # to behave well at the endpoints.
            y_smooth = self._make_smooth_curve(np.append(y, [y, y]), box_points)

            # The middle part of the smooth curve is retrieved.
            length = int(y_smooth.size / 3)
            y_smooth = y_smooth[length: 2 * length]
        else:
            x = np.arange(first_year, last_year + 1)

            # The box_points is a fraction of the difference between lastYear and firstYear.
            box_points = int((last_year - first_year) / 120 * 30)

            y_smooth = self._make_smooth_curve_linear_extrapolate(y, box_points)

        return x, y, y_smooth

    def _curve_to_json(self, curves: Tuple[np.ndarray, np.ndarray, np.ndarray]):
        data_array = np.array(curves)
        return json.dumps(np.transpose(data_array).tolist())

        # Make a numpy array of weather values per day and per year.
    def make_array(self, measurements: np.ndarray, first_year: int, last_year: int, column_name: str) -> np.ndarray:

        dates = measurements[:, 1]

        column_number, factor = Measurement().__getattribute__(column_name)
        column = measurements[:, column_number]

        # The date array is initialized with zeros.
        day_year_array = np.zeros([365, last_year - first_year + 1])

        # Looping through all dates and placing the values in the dayYearArray.
        last_good_value = None
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

            if column[index] == '     ':
                if last_good_value is None:
                    last_good_value = column[index - 1]
                day_year_array[days_in_the_year, year - first_year] = float(last_good_value) * factor
            else:
                day_year_array[days_in_the_year, year - first_year] = float(column[index]) * factor

        return day_year_array

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
