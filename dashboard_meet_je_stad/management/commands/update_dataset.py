from dashboard_meet_je_stad.service.cleanup_service import CleanupService
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from django.core.management.base import BaseCommand
import os
import math
import datetime
import dotenv
import sys
from dashboard_meet_je_stad.models import Sensor


class Command(BaseCommand):
    help = "Updates the dataset"

    def __init__(self):
        super().__init__()
        self.measurement_repository = MeasurementRepository()
        self.sensor_cached_repository = SensorCachedRepository()
        self.sensor_repository = SensorRepository()
        self.cleanup_service = CleanupService()

    def handle(self, *args, **options):
        if sys.argv[1:2] == ['test']:
            dotenv_file = '.env.test'
        else:
            dotenv_file = '.env'

        last_measurements = {}
        sensors = self.sensor_cached_repository.find_all()
        for sensor_id, sensor in sensors.items():
            last_measurements[int(sensor_id)] = sensor.get_measurements_cached()[-1]

        last_sensor_id = os.getenv('LAST_SENSOR_ID')
        if last_sensor_id is not None and last_sensor_id != '':
            last_sensor_id = int(last_sensor_id)
        else:
            self.stdout.write(self.style.ERROR('Last sensor missing in .env.'))
            sys.exit(1)

        end_date = os.getenv('END_DATE')
        if end_date == '':
            start_date = os.getenv('START_DATE')
            if start_date is None or start_date == '':
                self.stdout.write(self.style.ERROR('Start date missing in .env.'))
                sys.exit(1)
            end_date = (datetime.datetime.strptime(start_date, '%Y-%m-%d,%H:%M:%S')
                        .replace(tzinfo=datetime.timezone.utc))
        else:
            if end_date is None:
                self.stdout.write(self.style.ERROR('End date missing in .env.'))
                sys.exit(1)
            end_date = (datetime.datetime.strptime(end_date, "%Y-%m-%d,%H:%M:%S")
                        .replace(tzinfo=datetime.timezone.utc))
            end_date += datetime.timedelta(seconds=1)
        date_now = datetime.datetime.now(datetime.timezone.utc)
        delta = date_now - end_date
        earlier_day = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=1)

        sensor_range = math.ceil(50 / (delta.days + 1) * 7)
        measurements = []
        for sensor_id_range in range(0, int(last_sensor_id / sensor_range) + 2):
            ids_range = str(sensor_id_range * sensor_range + 1) + '-' + str((sensor_id_range + 1) * sensor_range)
            measurements_range = MeetJeStadAPIService().get_measurements(
                end_date.strftime('%Y-%m-%d,%H:%M:%S'),
                date_now.strftime('%Y-%m-%d,%H:%M:%S'),
        'sensors',
        'json',
                sensors,
                ids_range,
        False,
                (delta.days + 1) * 24 * 4 * sensor_range,
        False)
            measurements += measurements_range
        measurements = self.cleanup_service.clean(measurements)

        measurements_utrecht = {}
        for measurement in measurements:
            if measurement.sensor_id > last_sensor_id:
                last_sensor_id = measurement.sensor_id
            if measurement.is_in_utrecht():
                if measurement.sensor_id in measurements_utrecht:
                    measurements_utrecht[measurement.sensor_id].append(measurement)
                else:
                    measurements_utrecht[measurement.sensor_id]= [measurement]
            else:
                continue
            if measurement.sensor_id not in sensors:
                sensor = Sensor()
                sensor.set_measurements_cached([])
                sensor.is_particulate_matter = False
                sensor.is_lux = False
                sensor.id = measurement.sensor_id
                self.sensor_repository.create(sensor)
                sensors[measurement.sensor_id] = sensor
            else:
                sensor = sensors[measurement.sensor_id]
            last_measurements[sensor.id] = measurement
            sensors[measurement.sensor_id].add_measurement_cached(measurement)
            if measurement.pm25 is not None or measurement.pm10 is not None:
                sensor.is_particulate_matter = True
            if measurement.lux is not None:
                sensor.is_lux = True

        for sensor_id, sensor in sensors.items():
            if sensor.id in measurements_utrecht:
                self.measurement_repository.bulk_create(measurements_utrecht[sensor_id])
            measurements = []
            for index, measurement in enumerate(sensor.get_measurements_cached()):
                if (measurement.timestamp > earlier_day
                        or last_measurements[measurement.sensor_id].id == measurement.id):
                    measurements.append(measurement)
            sensor.set_measurements_cached(measurements)
            if sensor.get_measurements_cached()[-1].timestamp >= earlier_day:
                sensor.is_active = True
            self.sensor_repository.update(sensor)
        self.sensor_cached_repository.write(sensors)

        dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')

        self.stdout.write(self.style.SUCCESS('Successfully updated dataset.'))
