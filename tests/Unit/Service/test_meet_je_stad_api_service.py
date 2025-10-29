import unittest
from dashboard_meet_je_stad.service import meet_je_stad_api_service


class TestMeetJeStadAPIService(unittest.TestCase):

    def test_get_data(self) -> None:
        service = meet_je_stad_api_service.MeetJeStadAPIService()

        result = service.get_data('2024-11-16,12:00:00',
                                  '2024-11-17,12:00:00',
                                  'sensors',
                                  'csv')
        self.assertListEqual(result, [])

        result = service.get_data('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  'json',
                                  '1085')
        self.assertEqual(len(result[0]), len(service.row_keys))

        result = service.get_data('2025-06-20,0:00:00',
                                  '2025-06-30,23:59:00',
                                  'sensors',
                                  'json')
        self.assertEqual(len(result[0]), len(service.row_keys))