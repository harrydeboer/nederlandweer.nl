from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        repository = MeasurementRepository()
        measurement_id = 16683
        measurement = repository.get(measurement_id)
        self.assertEqual(measurement.id, measurement_id)