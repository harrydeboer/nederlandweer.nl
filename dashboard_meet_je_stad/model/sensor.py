import datetime


class Sensor:

    measurement_keys = [
        'timestamp',
        'id',
        'temperature',
        'longitude',
        'latitude',
        'humidity',
        'supply',
        'battery',
        'firmware_version',
        'pm2.5',
        'pm10',
        'lux',
        'extra'
    ]

    def __init__(self, measurement: list):
        self.timestamp = []
        self.id = []
        self.temperature = []
        self.longitude = []
        self.latitude = []
        self.humidity = []
        self.supply = []
        self.battery = []
        self.firmware_version = []
        self.pm25 = []
        self.pm10 = []
        self.lux = []
        self.extra = []
        self.add_measurement(measurement)

    def add_measurement(self, measurement: list):
        for index, key in enumerate(Sensor.measurement_keys):
            if key == 'pm2.5':
                key = 'pm25'
            measurements = self.__getattribute__(key)
            if key == 'timestamp':
                measurements.append(datetime.datetime.strptime(measurement[index],"%Y-%m-%d %H:%M:%S")
                                    .replace(tzinfo=datetime.timezone.utc))
                self.timestamp = measurements
            elif key == 'id':
                self.id = int(measurement[index])
            else:
                if measurement[index] != '':
                    measurements.append(float(measurement[index]))
                else:
                    measurements.append(None)
                self.__setattr__(key, measurements)

    def dates_to_string(self) -> list:
        dates = []
        for date in self.timestamp:
            dates.append(date.strftime('%Y-%m-%d,%H:%M:%S'))
        return dates
