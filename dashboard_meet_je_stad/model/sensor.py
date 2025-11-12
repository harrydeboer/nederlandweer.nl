from dashboard_meet_je_stad.model.measurement import Measurement
import datetime


class Sensor:

    properties = [
        'mean_longitude',
        'mean_latitude',
        'start_date',
        'end_date',
        'start_date_utrecht',
        'end_date_utrecht',
        'is_particulate_matter',
        'is_active',
    ]

    def __init__(self, measurement: list):
        properties_flipped = {}
        for index, prop in enumerate(self.properties):
            properties_flipped[prop] = index
        mean_longitude = measurement[len(Measurement.properties) + properties_flipped['mean_longitude']]
        if mean_longitude == '' or mean_longitude is None:
            self.mean_longitude = None
        else:
            self.mean_longitude = float(mean_longitude)
        mean_latitude = measurement[len(Measurement.properties) + properties_flipped['mean_latitude']]
        if mean_latitude == '' or mean_longitude is None:
            self.mean_latitude = None
        else:
            self.mean_latitude = float(mean_latitude)
        self.start_date = self.set_date(measurement[len(Measurement.properties) + properties_flipped['start_date']])
        self.end_date = self.set_date(measurement[len(Measurement.properties) + properties_flipped['end_date']])
        self.start_date_utrecht = self.set_date(measurement[len(Measurement.properties) +
                                                            properties_flipped['start_date_utrecht']])
        self.end_date_utrecht = self.set_date(measurement[len(Measurement.properties) +
                                                          properties_flipped['end_date_utrecht']])
        if measurement[len(Measurement.properties) + properties_flipped['is_particulate_matter']] == '1':
            self.is_particulate_matter = True
        else:
            self.is_particulate_matter = False
        self.is_active = False
        self.measurements = []
        self.add_measurement(Measurement(measurement))

    def set_date(self, date:str):
        if date == '' or date is None:
            return None
        else:
            return datetime.datetime.strptime(
                date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)

    def add_measurement(self, measurement: Measurement):
        self.measurements.append(measurement)

    def set_measurements(self, measurements: list):
        self.measurements = measurements

    def get_dates(self)-> list:
        dates = []
        for measurement in self.measurements:
            dates.append(measurement.timestamp)
        return dates

    def to_dict(self):
        properties = {}
        for prop in Measurement.properties:
            if prop == 'pm2.5':
                prop = 'pm25'
            properties[prop] = []
            for measurement in self.measurements:
                value = measurement.__getattribute__(prop)
                if isinstance(value, datetime.datetime):
                    properties[prop].append(value.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    properties[prop].append(value)
        for prop in self.properties:
            value = self.__getattribute__(prop)
            if isinstance(value, datetime.datetime):
                properties[prop] = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                properties[prop] = value
        return properties
