from django.test import TestCase
from nederland_weer.repository.station_repository import StationRepository
from nederland_weer.models import Station


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def testFindAll(self) -> None:
        stations = StationRepository().find_all()

        self.assertIsInstance(stations, dict)
        self.assertIsInstance(stations['De Bilt'], Station)
