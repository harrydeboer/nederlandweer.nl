from django.test import TestCase
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.repository.station_repository import StationRepository
from nederland_weer.service.curve_service import CurveService
import datetime


class TestCurveService(TestCase):
    fixtures = ['fixture.json']

    def testFindAll(self) -> None:
        stations = StationRepository().find_all()
        measurements = MeasurementRepository().find_all(stations['De Bilt'].get_id(),
                                                        datetime.datetime.strptime('01-01-1901',
                                                                                   '%d-%m-%Y')
                                                        .replace(tzinfo=datetime.timezone.utc),
                                                        datetime.datetime.strptime('01-01-2026',
                                                                                   '%d-%m-%Y')
                                                        .replace(tzinfo=datetime.timezone.utc))
        (json_data, title,
         vertical, horizontal, text_output) = CurveService().make_curves('temperature-day',
                                                                         measurements)
        self.assertIsInstance(json_data, str)
        self.assertIsInstance(title, str)
        self.assertIsInstance(vertical, str)
        self.assertIsInstance(horizontal, str)
        self.assertIsInstance(text_output, str)
