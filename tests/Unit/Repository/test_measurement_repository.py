import unittest
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
import datetime


class TestMeasurementRepository(unittest.TestCase):

    def test_get_data(self) -> None:
        repository = MeasurementRepository()

        result = repository.get_small_last_24(datetime.datetime.now(datetime.timezone.utc))
        self.assertEqual(result, {})