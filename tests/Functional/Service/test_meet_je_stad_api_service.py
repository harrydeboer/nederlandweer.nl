import unittest
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.service import meet_je_stad_api_service
from dashboard_meet_je_stad.models import Measurement


class TestMeetJeStadAPIService(unittest.TestCase):

    def test_get_data(self) -> None:
        service = meet_je_stad_api_service.MeetJeStadAPIService()
        sensor_repository = SensorRepository()

        measurements = service.get_measurements('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  'json',
                                  sensor_repository.find_all(),
                                  '1085')
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))

        measurements = service.get_measurements('2017-11-16,0:00:00',
                                  '2025-11-16,23:59:00',
                                  'sensors',
                                  'json',
                                  sensor_repository.find_all())
        self.assertTrue(isinstance(measurements, list))
        self.assertTrue(isinstance(measurements[0], Measurement))
