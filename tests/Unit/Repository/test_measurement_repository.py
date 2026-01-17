import unittest
import numpy as np
from nederland_weer.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(unittest.TestCase):

    def testFindAll(self) -> None:
        temp_array = MeasurementRepository().find_all()

        self.assertIsInstance(temp_array, np.ndarray)
#