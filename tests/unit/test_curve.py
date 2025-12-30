import unittest
import numpy as np
import datetime as datetime
from nederland_weer.services import DayYearArrayBuildService
from nederland_weer.models import KNMIData
from nederland_weer.models import Curve
from nederland_weer.models import DataColumn


class TestCurve(unittest.TestCase):

    def setUp(self) -> None:

        self.first_year = 1906
        self.last_year = 2019
        self.knmi_data = KNMIData()
        temp_array = DayYearArrayBuildService.make_array(self.knmi_data.array,
                                                         self.first_year, self.last_year, DataColumn.mean_temp)
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
        mean = Curve.get_month_mean(y_smooth, 1, 2019)

        self.assertEqual(mean, 1)

    def testMeanOfAngle(self) -> None:

        first_year = 1906
        last_year = 2019
        speed_2d = DayYearArrayBuildService.make_array(self.knmi_data.array, first_year,
                                                       last_year, DataColumn.wind_speed_va)
        angle_2d = DayYearArrayBuildService.make_array(self.knmi_data.array, first_year,
                                                       last_year, DataColumn.wind_direction)
        angle = self.curve.mean_of_angle(speed_2d, angle_2d)

        self.assertEqual(angle.size, 365)
