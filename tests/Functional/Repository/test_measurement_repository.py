import numpy as np
from django.test import TestCase
from nederland_weer.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def testFindAll(self) -> None:
        temp_array = MeasurementRepository().find_all(260, 'mean_temp', 1906, 2025)

        self.assertIsInstance(temp_array[0], np.ndarray)
#
