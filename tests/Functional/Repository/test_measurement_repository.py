from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        repository = MeasurementRepository()

        result = repository.get_small_utrecht()
        self.assertEqual(len(result), 1)