import unittest
import numpy as np
import datetime as datetime
from nederland_weer.service.curve_service import CurveService
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.model.curve import Curve
from dotenv import load_dotenv
import os


class TestCurve(unittest.TestCase):

    def setUp(self) -> None:

        load_dotenv()
        self.first_year = int(os.getenv('BEGIN_YEAR'))
        self.last_year = int(os.getenv('END_YEAR'))
        measurements = MeasurementRepository().find_all()
        temp_array = CurveService().make_array(measurements,
                                              self.first_year, self.last_year, 'mean_temp')
        self.curve = Curve(temp_array.mean(axis=1), True, self.first_year, self.last_year)
        self.curve_lin_extrapolate = Curve(temp_array.mean(axis=0), False, self.first_year, self.last_year)

    def testSmoothCurve(self) -> None:

        self.assertEqual(self.curve.y_smooth.size, 365)

    def testSmoothCurveLinExtrapolate(self) -> None:

        self.assertEqual(self.curve_lin_extrapolate.y_smooth.size, self.last_year - self.first_year + 1)

    def testFirstDateSummer(self) -> None:

        date = self.curve.get_first_date_summer()

        self.assertIsInstance(date, datetime.date)

    def testCalcMonthMean(self) -> None:

        y_smooth = np.ones(365)
        mean = Curve.get_month_mean(y_smooth, 1, self.last_year)

        self.assertEqual(mean, 1)

    def testMeanOfAngle(self) -> None:

        first_year = self.first_year
        last_year = self.last_year
        speed_2d = CurveService().make_array(MeasurementRepository().find_all(), first_year,
                                                       last_year, 'wind_speed_va')
        angle_2d = CurveService().make_array(MeasurementRepository().find_all(), first_year,
                                                       last_year, 'wind_direction')
        angle = self.curve.mean_of_angle(speed_2d, angle_2d)

        self.assertEqual(angle.size, 365)
