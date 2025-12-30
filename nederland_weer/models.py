import numpy as np
import datetime as dt
from typing import Tuple
import csv
from enum import Enum


class DataColumn(Enum):

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


class KNMIData:

    def __init__(self):

        # Read txt file as list.
        txt_list = []
        with open('data/knmi.txt', newline='') as input_file:
            reader = csv.reader(input_file)
            last_good_row = None
            for row in reader:

                # During april 1945 a lot of data is not available. 31 March 1945 data is put over all days of april.
                if len(row) > 10 and row[4] == '     ' and row[1][:6] == '194504':
                    if last_good_row is None:
                        last_good_row = txt_list[-1:][0]
                    new_list = last_good_row
                    new_list[1] = row[1]
                    txt_list.append(new_list)

                else:
                    txt_list.append(row)

        self.array = np.asarray(txt_list)

        # Remove the days of the first years until most data is available.
        for index, row in enumerate(self.array):

            year = int(row[1][:4])

            # Most data is available from 1904 and onwards.
            if year == 1906:
                self.array = self.array[index:]
                break

        # Remove the days of the last year if it is not complete.
        year_to_delete = None
        for index, row in enumerate(reversed(self.array)):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '1231':
                year_to_delete = year
                continue

            if year_to_delete is not None:
                if year == year_to_delete - 1:
                    self.array = self.array[:-index]
                    break

        dates = self.array[:, 1]
        self.minYearFile = int(dates[1][:4])
        self.maxYearFile = int(dates[-1][:4])


class Curve:

    def __init__(self, y: np.ndarray, is_day_curve: bool, first_year: int, last_year: int):

        self.y = y

        if is_day_curve:
            self.x = np.arange(1, 366)
            box_points = 30

            # The start and end of a day curve should match. The data is tripled in order for the smoothing
            # to behave well at the endpoints.
            y_smooth = self.__make_smooth_curve(np.append(y, [y, y]), box_points)

            # The middle part of the smooth curve is retrieved.
            length = int(y_smooth.size / 3)
            self.y_smooth = y_smooth[length: 2 * length]
        else:
            self.x = np.arange(first_year, last_year + 1)

            # The box_points is a fraction of the difference between lastYear and firstYear.
            box_points = int((last_year - first_year) / 120 * 30)

            self.y_smooth = self.__make_smooth_curve_linear_extrapolate(y, box_points)

    @staticmethod
    def __make_smooth_curve(y, box_points) -> np.ndarray:

        box = np.ones(box_points) / box_points
        result = np.convolve(y, box, mode='same')

        return result

    # A moving average is used to smooth the curve. At the edges the data is extrapolated linearly with a regression.
    # That way the smoothing behaves well at the edges. After smoothing the extrapolated data is removed.
    @classmethod
    def __make_smooth_curve_linear_extrapolate(cls, y, box_points) -> np.ndarray:

        y_regress = y[:box_points]
        x_regress = np.arange(0, box_points)

        intercept, slope = cls.__calculate_intercept_and_slope(y_regress, x_regress)

        y_prepend = np.arange(box_points * (-1), 0) * slope + intercept

        y_regress = y[-box_points:]
        x_regress = np.arange(y.size - box_points, y.size)

        intercept, slope = cls.__calculate_intercept_and_slope(y_regress, x_regress)

        y_append = np.arange(y.size, y.size + box_points) * slope + intercept

        box = np.ones(box_points) / box_points
        result = np.convolve(np.append(np.append(y_prepend, y), y_append), box, mode='same')

        return result[box_points:-box_points]

    @staticmethod
    def __calculate_intercept_and_slope(y_regress: np.ndarray, x_regress: np.ndarray) -> Tuple[float, float]:

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
    def get_first_date_summer(self) -> dt.datetime:

        subtract = np.subtract(self.y_smooth[92:], self.y_smooth[:365 - 92])
        first_day_of_summer = int(np.where(np.absolute(subtract) == np.min(np.absolute(subtract)))[0][0])

        return dt.datetime(2019, 1, 1) + dt.timedelta(first_day_of_summer)

    @staticmethod
    def mean_of_angle(speed_2d: np.ndarray, angle_2d: np.ndarray) -> np.ndarray:

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
    @staticmethod
    def get_month_mean(y: np.ndarray, month: int, year: int) -> float:

        if y.size != 365:
            raise Exception('This stat can only be calculated for day curves.')

        day_number_begin = dt.datetime(year, month, 1).timetuple().tm_yday
        if month == 12:
            day_number_end = dt.datetime(year, month, 31).timetuple().tm_yday
        else:
            day_number_end = dt.datetime(year, month + 1, 1).timetuple().tm_yday - 1

        return y[day_number_begin - 1:day_number_end].mean(axis=0)
