from django.test import TestCase
from dashboard_meet_je_stad.models import Measurement
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository


class TestMeasurement(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()

    def test_get_data(self) -> None:
        measurement = self.measurement_repository.get(226785)
        self.assertEqual(len(measurement.to_list()), len(Measurement._meta.fields))
