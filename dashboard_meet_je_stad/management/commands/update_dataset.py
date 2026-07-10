from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.measurement_cached_repository import MeasurementCachedRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from django.core.management.base import BaseCommand
import os
import math
import datetime
import dotenv
import sys
from dashboard_meet_je_stad.models import Sensor, Measurement


class Command(BaseCommand):
    help = "Updates the dataset"

    def __init__(self):
        super().__init__()
        self.measurement_repository = MeasurementRepository()
        self.measurement_cached_repository = MeasurementCachedRepository()
        self.sensor_repository = SensorRepository()

    def handle(self, *args, **options):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        sensors = self.sensor_repository.find_all()

        measurements_cached_dict = self.measurement_cached_repository.find_all(sensors)
        measurements_cached = []
        last_measurements = {}
        for index, measurements in measurements_cached_dict.items():
            for measurement in measurements:
                measurements_cached.append(measurement)
                last_measurements[measurement.sensor_id] = measurement

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
        rows = []
        for sensor_id_range in range(0, int(last_sensor_id / sensor_range) + 2):
            ids_range = str(sensor_id_range * sensor_range + 1) + '-' + str((sensor_id_range + 1) * sensor_range)
            results = MeetJeStadAPIService().get_data(
                end_date.strftime('%Y-%m-%d,%H:%M:%S'),
                date_now.strftime('%Y-%m-%d,%H:%M:%S'),
        'sensors',
        'json',
                sensors,
                ids_range,
        False,
                (delta.days + 1) * 24 * 4 * sensor_range,
        False)
            rows += results

        measurements = []
        last_sensor_id = 1
        for row in rows:
            measurement = Measurement(row=row)
            if measurement.sensor_id > last_sensor_id:
                last_sensor_id = measurement.sensor_id
            if measurement.is_in_utrecht() and measurement.sensor_id not in sensors:
                measurements.append(measurement)
                sensor = Sensor()
                if measurement.pm25 is not None or measurement.pm10 is not None:
                    sensor.is_particulate_matter = True
                else:
                    sensor.is_particulate_matter = False
                if measurement.lux is not None:
                    sensor.is_lux = True
                else:
                    sensor.is_lux = False
                sensor.id = measurement.sensor_id
                self.sensor_repository.create(sensor)
                last_measurements[sensor.id] = measurement
            elif measurement.sensor_id in sensors:
                sensor = sensors[measurement.sensor.id]
                if measurement.pm25 is not None or measurement.pm10 is not None:
                    sensor.is_particulate_matter = True
                if measurement.lux is not None:
                    sensor.is_lux = True
                measurements.append(measurement)
                last_measurements[sensor.id] = measurement

        self.measurement_repository.bulk_create(measurements)
        for index, sensor in sensors.items():
            self.sensor_repository.update(sensor)

        for measurement in measurements:
            if measurement.timestamp > earlier_day or measurement == last_measurements[measurement.sensor_id]:
                measurements_cached.append(measurement)
        for measurement in measurements_cached:
            if measurement.timestamp < earlier_day and last_measurements[measurement.sensor.id].id != measurement.id:
                measurements_cached.remove(measurement)
        self.measurement_cached_repository.write(measurements_cached)

        dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')

        self.stdout.write(self.style.SUCCESS('Successfully updated dataset.'))
