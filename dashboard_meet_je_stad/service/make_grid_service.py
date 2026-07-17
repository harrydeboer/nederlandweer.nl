from typing import List
from dashboard_meet_je_stad.models import Measurement
import datetime


class MakeGridService:
    def make_grid(self, measurements_old: List[Measurement], days:float)  -> List[Measurement]:

        date_now = datetime.datetime.now(datetime.timezone.utc)
        measurements = []
        last_date = date_now - datetime.timedelta(minutes=date_now.minute % 15,
                                                  seconds=date_now.second,
                                                  microseconds=date_now.microsecond)
        last_date += datetime.timedelta(minutes=15)
        last_date -= datetime.timedelta(days=days)
        range_end = round(96 * days + 1)
        for index in range(0, range_end):
            measurement = Measurement()
            measurement.sensor_id = measurements_old[0].sensor_id
            measurement.timestamp = last_date
            measurement.extra = 'null'
            measurements.append(Measurement(row=measurement.to_list()))
            last_date += datetime.timedelta(minutes=15)
        if len(measurements_old) == 1:
            return measurements_old
        for index_measurement, measurement in enumerate(measurements_old):
            index = int(round((measurement.timestamp.timestamp()
                               - measurements[0].timestamp.timestamp()) / 60 / 15))
            if index < 0:
                continue
            if measurements[index].temperature is None:
                measurements[index] = measurement
            else:
                diff_current = abs(measurement.timestamp.timestamp() - measurements[index].timestamp.timestamp())
                if index_measurement - 1 in measurements_old:
                    diff_earlier = abs(measurements[index].timestamp.timestamp() -
                                       measurements_old[index_measurement - 1].timestamp.timestamp())
                    if diff_earlier > diff_current:
                        measurements[index] = measurement
        if measurements[-1].timestamp > date_now and measurements[-1].temperature is None:
            measurements = measurements[:-1]

        return measurements
