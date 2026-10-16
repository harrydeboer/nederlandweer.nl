from django.test import TestCase
from django.core.management import call_command
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.repository.station_repository import StationRepository


class TestUpdateDatasetCommand(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()
        self.station_repository = StationRepository()

    def test(self):
        call_command('update_dataset')
