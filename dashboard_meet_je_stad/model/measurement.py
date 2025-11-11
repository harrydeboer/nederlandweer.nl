import datetime


class Measurement:

    properties = [
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
        properties_flipped = {}
        for index, prop in enumerate(self.properties):
            properties_flipped[prop] = index
        self.timestamp = datetime.datetime.strptime(measurement[properties_flipped['timestamp']],
                                                    "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        self.id = int(measurement[properties_flipped['id']])
        self.temperature = self.set_float(measurement[properties_flipped['temperature']])
        self.longitude = self.set_float(measurement[properties_flipped['longitude']])
        self.latitude = self.set_float(measurement[properties_flipped['latitude']])
        self.humidity = self.set_float(measurement[properties_flipped['humidity']])
        self.supply = self.set_float(measurement[properties_flipped['supply']])
        self.battery = self.set_float(measurement[properties_flipped['battery']])
        self.firmware_version = self.set_float(measurement[properties_flipped['firmware_version']])
        self.pm25 = self.set_float(measurement[properties_flipped['pm2.5']])
        self.pm10 = self.set_float(measurement[properties_flipped['pm10']])
        self.lux = self.set_float(measurement[properties_flipped['lux']])
        self.extra = measurement[properties_flipped['extra']]

    def to_list(self):
        row = []
        for prop in self.properties:
            if prop == 'timestamp':
                row.append(self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                if prop == 'pm2.5':
                    row.append(self.pm25)
                else:
                    row.append(self.__getattribute__(prop))
        return row

    def set_float(self, value) -> float | None:
        if value == '' or value is None:
            return None
        return float(value)
