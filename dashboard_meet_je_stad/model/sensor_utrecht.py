from sensor import Sensor


class SensorUtrecht(Sensor):

    def __init__(self, id_sensor: int):
        super().__init__(id_sensor)
        self.longitude_mean = None
        self.latitude_mean = None
        self.start_date = ''
        self.end_date = ''
        self.start_date_utrecht = ''
        self.end_date_utrecht = ''
        self.particulate_matter = None

    def add_row(self, row: list):
        super().add_row(row)
        offset = len(self.service.row_keys)
        self.longitude_mean = row[offset]
        self.latitude_mean = row[offset + 1]
        self.start_date = row[offset + 2]
        self.end_date = row[offset + 3]
        self.start_date_utrecht = row[offset + 4]
        self.end_date_utrecht = row[offset + 5]
        self.particulate_matter = row[offset + 6]
