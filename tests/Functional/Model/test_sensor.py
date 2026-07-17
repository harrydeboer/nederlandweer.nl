from django.test import TestCase
from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestSensor(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_repository = SensorRepository()

    def test_get_data(self) -> None:
        sensor = self.sensor_repository.get(1196)
        self.assertEqual(len(sensor.to_dict()), 1 + len(Sensor._meta.fields))
