import unittest
import numpy as np
import datetime as datetime
from nederland_weer.service.curve_service import CurveService
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.model.curve import Curve
import csv


class TestCurve(unittest.TestCase):

    def setUp(self) -> None:

        stations = []
        station_de_bilt = []
        with open('data/station.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                stations.append(row)
                if row[0] == '260':
                    station_de_bilt = row
        self.first_year = int(station_de_bilt[2])
        self.last_year = int(station_de_bilt[3])
        measurements = MeasurementRepository().find_all(260)
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
        speed_2d = CurveService().make_array(MeasurementRepository().find_all(260), first_year,
                                                       last_year, 'wind_speed_va')
        angle_2d = CurveService().make_array(MeasurementRepository().find_all(260), first_year,
                                                       last_year, 'wind_direction')
        angle = self.curve.mean_of_angle(speed_2d, angle_2d)

        self.assertEqual(angle.size, 365)
