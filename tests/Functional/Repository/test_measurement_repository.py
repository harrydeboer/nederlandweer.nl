from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
import datetime


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()

    def test_repository(self) -> None:
        measurement_id = 226785
        measurement = self.measurement_repository.get(measurement_id)
        self.assertEqual(measurement.get_id(), measurement_id)
        measurement.set_id(None)
        measurement.set_timestamp(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc))
        self.measurement_repository.create(measurement)
        measurement.set_id(None)
        measurement.set_timestamp(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
                                  + datetime.timedelta(days=1))
        self.measurement_repository.bulk_create([measurement])
        measurements = self.measurement_repository.get_days(measurement.get_sensor_id(), 91)
        self.assertGreater(len(measurements),0)
        self.measurement_repository.delete(measurement)
        self.assertIsNone(measurement.get_id())
