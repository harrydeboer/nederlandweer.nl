class Sensor:

    row_keys = [
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

    def __init__(self, id_sensor: int):
        self.id = id_sensor
        self.timestamp = []
        for key in self.row_keys:
            if key != 'id':
                if key == 'pm2.5':
                    self.__setattr__('pm25', [])
                else:
                    self.__setattr__(key, [])

    def add_row(self, row: list):
        for index, key in enumerate(self.row_keys):
            if key != 'id':
                if key == 'pm2.5':
                    key = 'pm25'
                values = self.__getattribute__(key)
                if key == 'timestamp':
                    values.append(row[index])
                    self.timestamp = values
                else:
                    if row[index] != '':
                        values.append(float(row[index]))
                        self.__setattr__(key, values)
                    else:
                        values.append(None)
                        self.__setattr__(key, values)
