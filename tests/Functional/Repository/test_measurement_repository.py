import datetime
from django.test import TestCase
from nederland_weer.models import Measurement
from nederland_weer.repository.measurement_repository import MeasurementRepository


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def testFindAll(self) -> None:
        temp_array = MeasurementRepository().find_all(260,
                                                      datetime.datetime.strptime('01-01-1901',
                                                                                 '%d-%m-%Y')
                                                      .replace(tzinfo=datetime.timezone.utc),
                                                      datetime.datetime.strptime('01-01-2026', '%d-%m-%Y')
                                                      .replace(tzinfo=datetime.timezone.utc))

        self.assertIsInstance(temp_array[0], Measurement)
#
