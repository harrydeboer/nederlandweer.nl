from django.test import TestCase
from nederland_weer.models import Measurement
from nederland_weer.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def testFindAll(self) -> None:
        temp_array = MeasurementRepository().find_all(260)

        self.assertIsInstance(temp_array[0], Measurement)
#
