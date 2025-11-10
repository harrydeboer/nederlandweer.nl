from dashboard_meet_je_stad.model.sensor import Sensor
import datetime


class SensorUtrecht(Sensor):

    keys = [
        'mean_longitude',
        'mean_latitude',
        'start_date',
        'end_date',
        'start_date_utrecht',
        'end_date_utrecht',
        'is_particulate_matter'
    ]

    def __init__(self, measurement: list):
        super().__init__(measurement)
        keys = {}
        for index, key in enumerate(self.keys):
            keys[key] = index
        mean_longitude = measurement[len(Sensor.measurement_keys) + keys['mean_longitude']]
        if mean_longitude == '':
            self.mean_longitude = None
        else:
            self.mean_longitude = float(mean_longitude)
        mean_latitude = measurement[len(Sensor.measurement_keys) + keys['mean_latitude']]
        if mean_latitude == '':
            self.mean_latitude = None
        else:
            self.mean_latitude = float(mean_latitude)
        self.start_date = self.set_date(measurement[len(Sensor.measurement_keys) + keys['start_date']])
        self.end_date = self.set_date(measurement[len(Sensor.measurement_keys) + keys['end_date']])
        self.start_date_utrecht = self.set_date(measurement[len(Sensor.measurement_keys) + keys['start_date_utrecht']])
        self.end_date_utrecht = self.set_date(measurement[len(Sensor.measurement_keys) + keys['end_date_utrecht']])
        if measurement[len(Sensor.measurement_keys) + keys['is_particulate_matter']] == '1':
            self.is_particulate_matter = True
        else:
            self.is_particulate_matter = False

    def set_date(self, date:str):
        if date == '':
            return None
        else:
            return datetime.datetime.strptime(
                date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)

    def to_dict(self):
        properties = {}
        for key in Sensor.measurement_keys + self.keys:
            if key == 'pm2.5':
                key = 'pm25'
            value = self.__getattribute__(key)
            if isinstance(value, list):
                properties[key] = []
                for item in value:
                    if isinstance(item, datetime.datetime):
                        properties[key].append(item.strftime('%Y-%m-%d,%H:%M:%S'))
                    else:
                        properties[key].append(item)
            else:
                if isinstance(value, datetime.datetime):
                    properties[key] = value.strftime('%Y-%m-%d,%H:%M:%S')
                else:
                    properties[key] = value
        return properties
