from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService


class Sensor:

    def __init__(self, id_sensor: int):
        service = MeetJeStadAPIService()
        self.id = id_sensor
        self.timestamp = []
        for key in service.row_keys:
            if key != 'id':
                self.__setattr__(key, [])
                test = self.__getattribute__(key)

    def add_row(self, row: list):
        service = MeetJeStadAPIService()
        for index, key in enumerate(service.row_keys):
            if key != 'id':
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
