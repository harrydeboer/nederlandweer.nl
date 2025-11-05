from dashboard_meet_je_stad.model.sensor import Sensor


class SensorUtrecht:

    row_keys = [
        'mean_longitude',
        'mean_latitude',
        'start_date',
        'end_date',
        'start_date_utrecht',
        'end_date_utrecht',
        'is_particulate_matter'
    ]

    def __init__(self, row: list):
        for index, key in enumerate(Sensor.row_keys):
            self.__setattr__(key, row[index])
        for index, key in enumerate(self.row_keys):
            self.__setattr__(key, len(Sensor.row_keys) + row[index])
