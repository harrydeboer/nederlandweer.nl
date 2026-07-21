from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class TestMakeGridService(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()
        self.service = MakeGridService()

    def test(self):
        measurement = self.measurement_repository.get(226785)
        measurements = self.service.make_grid([measurement], measurement.get_sensor_id(), 1)
        self.assertTrue(len(measurements), 97)
