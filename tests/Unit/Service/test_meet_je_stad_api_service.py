import unittest
from dashboard_meet_je_stad.service import meet_je_stad_api_service
from dashboard_meet_je_stad.model.measurement import Measurement


class TestMeetJeStadAPIService(unittest.TestCase):

    def test_get_data(self) -> None:
        service = meet_je_stad_api_service.MeetJeStadAPIService()

        result = service.get_data('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  'json',
                                  '1085')
        self.assertEqual(len(result[0]), len(Measurement.properties))

        result = service.get_data('2017-11-16,0:00:00',
                                  '2025-11-16,23:59:00',
                                  'sensors',
                                  'json')
        self.assertEqual(len(result[0]), len(Measurement.properties))