from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository


class TestSensorCachedRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self) -> None:
        self.sensor_cached_repository = SensorCachedRepository()

    def test_get_data(self) -> None:

        sensors_cached = self.sensor_cached_repository.find_all()
        self.assertTrue(isinstance(sensors_cached, dict))
        self.sensor_cached_repository.write({})
        sensors_cached_empty = self.sensor_cached_repository.find_all()
        self.assertEqual(sensors_cached_empty, {})
        self.sensor_cached_repository.write(sensors_cached)
