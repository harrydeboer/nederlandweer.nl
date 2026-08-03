from django.test import TestCase
from django.core.management import call_command
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
import dotenv
import os
import datetime


class TestUpdateDatasetCommand(TestCase):

    def setUp(self):
        self.measurement_repository = MeasurementRepository()
        self.sensor_repository = SensorRepository()
        self.sensor_cached_repository = SensorCachedRepository()

    def test(self):
        dotenv_file = dotenv.find_dotenv('.env.test')
        end_date = os.getenv('END_DATE')
        earlier_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
        if (not end_date is None and end_date != '' and datetime.datetime.strptime(
                end_date, '%Y-%m-%d,%H:%M:%S').replace(tzinfo=datetime.timezone.utc) < earlier_date):
            dotenv.set_key(dotenv_file, "END_DATE",
                           datetime.datetime.strftime(earlier_date, '%Y-%m-%d,%H:%M:%S'), quote_mode='never')
            dotenv.load_dotenv(dotenv_file, override=True)
        elif end_date == '':
            dotenv.set_key(dotenv_file, "END_DATE", datetime.datetime.strftime(earlier_date,
                                                                               '%Y-%m-%d,%H:%M:%S'), quote_mode='never')
            dotenv.load_dotenv(dotenv_file, override=True)
        sensors = self.sensor_cached_repository.find_all()
        for sensor_id, sensor in sensors.items():
            self.sensor_repository.create(sensor)
            measurements = sensor.get_measurements_cached()
            for measurement in measurements:
                if not measurement.get_supply() is None:
                    self.measurement_repository.create(measurement)
        call_command('update_dataset')
        self.assertTrue(isinstance(self.sensor_cached_repository.find_all(), dict))
