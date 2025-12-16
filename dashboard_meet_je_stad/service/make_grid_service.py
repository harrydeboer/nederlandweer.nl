from typing import Dict
from dashboard_meet_je_stad.model.measurement import Measurement
from dashboard_meet_je_stad.model.sensor import Sensor
import datetime


class MakeGridService:
    def make_grid(self, sensors:Dict[int, Sensor], days:float)  -> Dict[int, Sensor]:
        for id_sensor, sensor in sensors.items():
            measurements = []
            date_now = datetime.datetime.now(datetime.timezone.utc)
            last_date = date_now - datetime.timedelta(minutes=date_now.minute % 15,
                                                      seconds=date_now.second,
                                                      microseconds=date_now.microsecond)
            last_date += datetime.timedelta(minutes=15)

            last_date -= datetime.timedelta(days=days)
            range_end = round(96 * days + 1)
            for index in range(0, range_end):
                measurements.append(Measurement([last_date.strftime('%Y-%m-%d %H:%M:%S'),
                                                 sensor.measurements[-1].id, None, None, None, None, None,
                                                 None, None, None, None, None, None]))
                last_date += datetime.timedelta(minutes=15)
            if len(sensor.measurements) == 1:
                continue
            for index_measurement, measurement in enumerate(sensor.measurements):
                index = round((measurement.timestamp.timestamp() - measurements[0].timestamp.timestamp()) / 60 / 15)
                if index < 0:
                    continue
                if measurements[index].temperature is None:
                    measurements[index] = measurement
                else:
                    diff_current = abs(measurement.timestamp.timestamp() - measurements[index].timestamp.timestamp())
                    if index_measurement - 1 in sensor.measurements:
                        diff_earlier = abs(measurements[index].timestamp.timestamp() -
                                           sensor.measurements[index_measurement - 1].timestamp.timestamp())
                        if diff_earlier > diff_current:
                            measurements[index] = measurement
            if measurements[-1].timestamp > date_now and measurements[-1].temperature is None:
                measurements = measurements[:-1]
            sensors[id_sensor].set_measurements(measurements)
        return sensors
