from django.test import TestCase
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
import datetime


class TestMeasurementRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.measurement_repository = MeasurementRepository()

    def test_repository(self) -> None:
        measurement_id = 1
        measurement = self.measurement_repository.get(measurement_id)
        self.assertEqual(measurement.get_id(), measurement_id)
        measurement.set_id(None)
        measurement.set_timestamp(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc))
        self.measurement_repository.create(measurement)
        measurement_id_new = measurement.get_id()
        measurement.set_id(None)
        measurement.set_timestamp(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
                                  + datetime.timedelta(days=1))
        self.measurement_repository.bulk_create([measurement])
        measurement.set_timestamp(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) -
                                  datetime.timedelta(days=1))
        self.measurement_repository.bulk_create([measurement])
        measurements = self.measurement_repository.get_previous_month(measurement.get_sensor_id())
        self.assertGreater(len(measurements),0)
        measurement.set_id(measurement_id_new)
        self.measurement_repository.delete(measurement)
        self.assertIsNone(measurement.get_id())
