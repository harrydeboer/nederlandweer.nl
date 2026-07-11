from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.measurement_cached_repository import MeasurementCachedRepository


class TestMeasurementCachedRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        sensor_repository = SensorRepository()
        repository = MeasurementCachedRepository()

        result = repository.find_all(sensor_repository.find_all())
        self.assertEqual(len(result), 1)
