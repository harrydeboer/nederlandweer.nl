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
        sensor_id = 1085
        measurements = self.service.get_measurements('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  sensor_repository.find_all(),
                                  str(sensor_id))
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))
        self.assertEqual(measurements[0].get_sensor_id(), sensor_id)

        measurements = self.service.get_measurements('2017-11-16,0:00:00',
                                  '2017-11-17,00:00:00',
                                  'sensors',
                                  sensor_repository.find_all())
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))
