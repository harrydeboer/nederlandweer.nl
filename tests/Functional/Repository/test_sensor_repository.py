from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestSensorRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        repository = SensorRepository()

        result = repository.find_all(False)
        self.assertEqual(len(result), 1)
