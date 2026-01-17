import numpy as np
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
