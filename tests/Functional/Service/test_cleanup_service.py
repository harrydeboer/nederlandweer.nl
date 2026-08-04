from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.service.cleanup_service import CleanupService


class TestCleanupService(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()
        self.service = CleanupService()

    def test(self):
        measurement = self.measurement_repository.get(1)
        measurement.set_temperature(1000)
        measurements = self.service.clean([measurement])
        self.assertEqual(len(measurements), 1)
        self.assertIsNone(measurements[0].get_temperature())
