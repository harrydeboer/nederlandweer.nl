from django.test import TestCase
from django.core.management import call_command
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
import dotenv
import os


class TestUpdateDatasetCommand(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_cached_repository = SensorCachedRepository()

    def test(self):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        last_sensor_id = os.getenv('LAST_SENSOR_ID')
        end_date = os.getenv('END_DATE')
        self.sensor_cached_repository.move('sensor_cached.json', 'sensor_cached_temp.json')
        call_command('update_dataset')
        self.assertTrue(isinstance(self.sensor_cached_repository.find_all(), dict))
        self.sensor_cached_repository.move('sensor_cached_temp.json', 'sensor_cached.json')
        if not last_sensor_id is None:
            dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        if not end_date is None:
            dotenv.set_key(dotenv_file, "END_DATE", end_date, quote_mode='never')
