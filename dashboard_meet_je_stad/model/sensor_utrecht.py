from dashboard_meet_je_stad.model.sensor import Sensor


class SensorUtrecht(Sensor):

    row_keys = [
        'mean_longitude',
        'mean_latitude',
        'start_date',
        'end_date',
        'start_date_utrecht',
        'end_date_utrecht',
        'is_particulate_matter'
    ]

    def __init__(self, row: list, id_sensor: int):
        super().__init__(id_sensor)
        for index, key in enumerate(Sensor.row_keys):
            self.__setattr__(key, row[index])

        self.mean_longitude = row[len(Sensor.row_keys)]
        self.mean_latitude = row[len(Sensor.row_keys) + 1]
        self.start_date = row[len(Sensor.row_keys) + 2]
        self.end_date = row[len(Sensor.row_keys) + 3]
        self.start_date_utrecht = row[len(Sensor.row_keys) + 4]
        self.end_date_utrecht = row[len(Sensor.row_keys) + 5]
        self.is_particulate_matter = row[len(Sensor.row_keys) + 6]
