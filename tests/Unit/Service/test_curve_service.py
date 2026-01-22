import unittest
from nederland_weer.service.curve_service import CurveService
from nederland_weer.repository.station_repository import StationRepository


class TestCurveService(unittest.TestCase):

    def testFindAll(self) -> None:
        station_repository = StationRepository()
        stations = station_repository.find_all()
        station_de_bilt = stations['De Bilt']
        (json_data, title,
         vertical, horizontal, text_output) = CurveService().make_curves(
            station_de_bilt.station_id, 'temperature-day', station_de_bilt.begin_year, station_de_bilt.end_year)
        self.assertIsInstance(json_data, str)
        self.assertIsInstance(title, str)
        self.assertIsInstance(vertical, str)
        self.assertIsInstance(horizontal, str)
        self.assertIsInstance(text_output, str)