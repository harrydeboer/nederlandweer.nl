import unittest
from nederland_weer.service.curve_service import CurveService


class TestCurveService(unittest.TestCase):

    def testFindAll(self) -> None:
        (json_data, title,
         vertical, horizontal, text_output) = CurveService().make_curve('temperature-day',
                                                                                        1906, 2025,
                                                                                        2025, 1930)
        self.assertIsInstance(json_data, str)
        self.assertIsInstance(title, str)
        self.assertIsInstance(vertical, str)
        self.assertIsInstance(horizontal, str)
        self.assertIsInstance(text_output, str)