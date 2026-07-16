from django.test import TestCase
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.models import Measurement
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService


class TestMeetJeStadAPIService(TestCase):
    fixtures = ['fixture.json']

    def setUp(self) -> None:
        self.sensor_repository = SensorRepository()
        self.service = MeetJeStadAPIService()

    def test_get_data(self) -> None:
        sensor_repository = SensorRepository()

        measurements = self.service.get_measurements('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  'json',
                                  sensor_repository.find_all(),
                                  '1085')
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))

        measurements = self.service.get_measurements('2017-11-16,0:00:00',
                                  '2026-07-15,23:59:00',
                                  'sensors',
                                  'json',
                                  sensor_repository.find_all())
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))
