import unittest
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestSensorRepository(unittest.TestCase):

    def test_get_data(self) -> None:
        repository = SensorRepository()

        result = repository.get(False)
        self.assertEqual(len(result), 1)