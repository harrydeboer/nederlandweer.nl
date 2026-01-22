import unittest
from nederland_weer.repository.station_repository import StationRepository
from nederland_weer.model.station import Station


class TestMeasurementRepository(unittest.TestCase):

    def testFindAll(self) -> None:
        stations = StationRepository().find_all()

        self.assertIsInstance(stations, dict)
        self.assertIsInstance(stations['De Bilt'], Station)
#