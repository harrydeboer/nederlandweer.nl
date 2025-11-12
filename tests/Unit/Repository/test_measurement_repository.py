import unittest
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
import datetime


class TestMeasurementRepository(unittest.TestCase):

    def test_get_data(self) -> None:
        repository = MeasurementRepository()

        result = repository.get_small_last_24(
            datetime.datetime.strptime('2025-11-11 23:59:59',"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc))
        self.assertEqual(len(result), 1)