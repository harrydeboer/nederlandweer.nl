from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository


class TestSensorCachedRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        repository = SensorCachedRepository()

        result = repository.find_all()
        self.assertEqual(len(result), 1)
