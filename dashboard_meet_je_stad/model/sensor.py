from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService


class Sensor:

    def __init__(self, id_sensor: int):
        self.service = MeetJeStadAPIService()
        self.id = id_sensor
        self.timestamp = []
        for key in self.service.row_keys:
            if key != 'id':
                if key == 'pm2.5':
                    self.__setattr__('pm25', [])
                else:
                    self.__setattr__(key, [])

    def add_row(self, row: list):
        for index, key in enumerate(self.service.row_keys):
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
