from django.test import TestCase
from nederland_weer.repository.station_repository import StationRepository
from nederland_weer.models import Station


class TestMeasurementRepository(TestCase):
    def setUp(self):
        StationRepository().create({'id': 260, 'name': "De Bilt", 'begin_year': 1906, 'end_year': 2025,
                               'begin_year_perc_rain': 1930, 'begin_year_amount_rain': 1906})

    def testFindAll(self) -> None:
        stations = StationRepository().find_all()

        self.assertIsInstance(stations, dict)
        self.assertIsInstance(stations['De Bilt'], Station)
