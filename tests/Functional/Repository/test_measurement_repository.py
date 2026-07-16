from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()

    def test_get_data(self) -> None:
        measurement_id = 226785
        measurement = self.measurement_repository.get(measurement_id)
        self.assertEqual(measurement.id, measurement_id)
