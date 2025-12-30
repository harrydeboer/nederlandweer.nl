import numpy as np
import datetime as dt
from nederland_weer.models import DataColumn


class DayYearArrayBuildService:

    # An array of weather values per day and per year is made.
    @staticmethod
    def make_array(knmi_data: np.ndarray, first_year: int, last_year: int, column_name: DataColumn) -> np.ndarray:

        dates = knmi_data[:, 1]

        column_number, factor = column_name.value
        column = knmi_data[:, column_number]

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
