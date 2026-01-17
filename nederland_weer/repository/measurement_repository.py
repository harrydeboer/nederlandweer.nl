import numpy as np
import datetime as dt
from nederland_weer.model.measurement import Measurement
import csv


class MeasurementRepository:

    def find_all(self) -> np.ndarray:

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

        measurements = np.asarray(txt_list)

        # Remove the days of the first years until most data is available.
        for index, row in enumerate(measurements):

            year = int(row[1][:4])

            # Most data is available from 1904 and onwards.
            if year == 1906:
                measurements = measurements[index:]
                break

        # Remove the days of the last year if it is not complete.
        year_to_delete = None
        for index, row in enumerate(reversed(measurements)):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '1231':
                year_to_delete = year
                continue

            if year_to_delete is not None:
                if year == year_to_delete - 1:
                    measurements = measurements[:-index]
                    break

        return measurements

    # Make a numpy array of weather values per day and per year.
    def get(self, measurements: np.ndarray, first_year: int, last_year: int, column_name: str) -> np.ndarray:

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
