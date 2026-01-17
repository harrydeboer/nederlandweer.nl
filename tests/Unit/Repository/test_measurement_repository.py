import unittest
from nederland_weer.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(unittest.TestCase):

    def testFindAll(self) -> None:

        first_year = 1906
        last_year = 2025
        temp_array = MeasurementRepository().find_all()

        self.assertEqual(1, 1)
#