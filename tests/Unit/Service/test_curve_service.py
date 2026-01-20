import unittest
from nederland_weer.service.curve_service import CurveService
import csv


class TestCurveService(unittest.TestCase):

    def testFindAll(self) -> None:
        stations = []
        station_de_bilt = []
        with open('data/station.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                stations.append(row)
                if row[0] == '260':
                    station_de_bilt = row
        (json_data, title,
         vertical, horizontal, text_output) = CurveService().make_curve(
            260, 'temperature-day', int(station_de_bilt[2]), int(station_de_bilt[3]),
            int(station_de_bilt[3]), int(station_de_bilt[4]))
        self.assertIsInstance(json_data, str)
        self.assertIsInstance(title, str)
        self.assertIsInstance(vertical, str)
        self.assertIsInstance(horizontal, str)
        self.assertIsInstance(text_output, str)