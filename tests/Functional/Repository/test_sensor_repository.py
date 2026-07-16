from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestSensorRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_repository = SensorRepository()

    def test_get_data(self) -> None:
        result = self.sensor_repository.find_all(False)
        self.assertEqual(len(result), 1)
