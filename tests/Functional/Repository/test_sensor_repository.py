from django.test import TestCase

from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestSensorRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_repository = SensorRepository()

    def test_get_data(self) -> None:
        sensors = self.sensor_repository.find_all(False)
        self.assertEqual(len(sensors), 1)
        sensor_id = 1196
        sensor = self.sensor_repository.get(sensor_id)
        self.assertEqual(sensor.get_id(), sensor_id)
        sensor = Sensor()
        self.sensor_repository.create(sensor)
        sensor.set_is_lux(True)
        self.sensor_repository.update(sensor)
        sensor_updated = self.sensor_repository.get(sensor.get_id())
        self.assertTrue(sensor_updated.is_lux())
        self.sensor_repository.delete(sensor)
        self.assertIsNone(sensor.get_id())
