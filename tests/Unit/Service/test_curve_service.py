import unittest
from nederland_weer.service.curve_service import CurveService
from dotenv import load_dotenv
import os


class TestCurveService(unittest.TestCase):

    def testFindAll(self) -> None:
        load_dotenv()
        first_year = int(os.getenv('BEGIN_YEAR'))
        last_year = int(os.getenv('END_YEAR'))
        begin_year_rain_perc = int(os.getenv('BEGIN_YEAR_RAIN_PERCENTAGE'))
        (json_data, title,
         vertical, horizontal, text_output) = CurveService().make_curve('temperature-day',
                                                                                        first_year, last_year,
                                                                                        last_year, begin_year_rain_perc)
        self.assertIsInstance(json_data, str)
        self.assertIsInstance(title, str)
        self.assertIsInstance(vertical, str)
        self.assertIsInstance(horizontal, str)
        self.assertIsInstance(text_output, str)