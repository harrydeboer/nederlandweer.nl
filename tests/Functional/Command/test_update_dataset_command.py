from django.test import TestCase
from django.core.management import call_command
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
import dotenv
import os
import datetime

class TestUpdateDatasetCommand(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_cached_repository = SensorCachedRepository()

    def test(self):
        dotenv_file = dotenv.find_dotenv('.env.test')
        end_date = os.getenv('END_DATE')
        if not end_date is None:
            end_date_object = datetime.datetime.now(datetime.timezone.utc)
            end_date_object = end_date_object - datetime.timedelta(hours=1)
            dotenv.set_key(dotenv_file, "END_DATE",
                           datetime.datetime.strftime(end_date_object, '%Y-%m-%d,%H:%M:%S'), quote_mode='never')
        dotenv.load_dotenv(dotenv_file, override=True)
        call_command('update_dataset')
        self.assertTrue(isinstance(self.sensor_cached_repository.find_all(), dict))
