from typing import List
from dashboard_meet_je_stad.models import Measurement
import datetime


"""This service makes a grid of every quarter and every hour of the given days. 
The measurements are put on this grid.
"""
class MakeGridService:

    def make_grid(self, measurements: List[Measurement], sensor_id: int, days:float)  -> List[Measurement]:

        date_now = datetime.datetime.now(datetime.timezone.utc)
        measurements_grid = []
        last_date = date_now - datetime.timedelta(minutes=date_now.minute % 15,
                                                  seconds=date_now.second,
                                                  microseconds=date_now.microsecond)
        last_date += datetime.timedelta(minutes=15)
        last_date -= datetime.timedelta(days=days)
        range_end = round(96 * days + 1)
        for index in range(0, range_end):
            measurement = Measurement()
            measurement.set_sensor_id(sensor_id)
            measurement.set_timestamp(last_date)
            measurement.set_extra(None)
            measurements_grid.append(Measurement(row=measurement.to_list()))
            last_date += datetime.timedelta(minutes=15)

        """When a measurement is from an inactive sensor it gets no grid."""
        if len(measurements) == 1 and measurements[0].get_timestamp() < date_now - datetime.timedelta(days=1):
            return measurements

        for index_measurement, measurement in enumerate(measurements):
            index = int(round((measurement.get_timestamp().timestamp()
                               - measurements_grid[0].get_timestamp().timestamp()) / 60 / 15))
            if index < 0:
                continue
            """A measurement always has supply, but the grid measurement supply can be None.
            The grid gets the measurement if it has not been set.
            If it was set the measurement that is nearest to the grid point is set.
            """
            if measurements_grid[index].get_supply() is None:
                measurements_grid[index] = measurement
            else:
                diff_current = abs(measurement.get_timestamp().timestamp() -
                                   measurements_grid[index].get_timestamp().timestamp())
                if index_measurement - 1 in measurements:
                    diff_earlier = abs(measurements_grid[index].timestamp.timestamp() -
                                       measurements[index_measurement - 1].get_timestamp().timestamp())
                    if diff_earlier > diff_current:
                        measurements_grid[index] = measurement

        """If the last grid point is not set and is in the future it is removed from the grid."""
        if measurements_grid[-1].get_timestamp() > date_now:
            measurements_grid = measurements_grid[:-1]

        return measurements_grid
