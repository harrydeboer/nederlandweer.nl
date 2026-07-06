from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from django.core.management.base import BaseCommand
import os
import math
import datetime
import dotenv
from dashboard_meet_je_stad.models import Sensor


class Command(BaseCommand):
    help = "Updates the dataset"

    def handle(self, *args, **options):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        measurement_repository = MeasurementRepository()
        sensor_repository = SensorRepository()
        last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
        if os.getenv('END_DATE') == '':
            end_date = (datetime.datetime.strptime(os.getenv('START_DATE'), '%Y-%m-%d,%H:%M:%S')
                        .replace(tzinfo=datetime.timezone.utc))
        else:
            end_date = (datetime.datetime.strptime(os.getenv('END_DATE'), "%Y-%m-%d,%H:%M:%S")
                        .replace(tzinfo=datetime.timezone.utc))
            end_date += datetime.timedelta(seconds=1)
        date_now = datetime.datetime.now(datetime.timezone.utc)
        delta = date_now - end_date
        sensor_step = math.ceil(50 / (delta.days + 1) * 7)
        sensors = sensor_repository.find_all()
        first_measurements = {}
        last_measurements = {}
        for sensor_id_50 in range(0, int(last_sensor_id / sensor_step) + 2):
            ids_range = str(sensor_id_50 * sensor_step + 1) + '-' + str((sensor_id_50 + 1) * sensor_step)
            results = MeetJeStadAPIService().get_data(
                end_date.strftime('%Y-%m-%d,%H:%M:%S'),
                date_now.strftime('%Y-%m-%d,%H:%M:%S'),
        'sensors',
        'json',
                ids_range,
        False,
                (delta.days + 1) * 24 * 4 * sensor_step,
        False)
            if len(results) == 0:
                continue
            measurements = []
            for row in results:
                measurement = measurement_repository.row_to_measurement(row)
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
                    sensor_repository.create(sensor)
                    first_measurements[measurement.sensor_id] = measurement
                    last_measurements[sensor.id] = measurement
                elif measurement.is_in_utrecht() and measurement.sensor_id in sensors:
                    sensor = sensors[measurement.sensor.id]
                    measurements.append(measurement)
                    last_measurements[sensor.id] = measurement
            measurement_repository.bulk_create(measurements)

        for sensor_id, sensor in sensors.items():
            if sensor_id in first_measurements:
                sensor.first_measurement = (measurement_repository.
                                            get_by_sensor_and_timestamp(sensor_id,
                                                                        first_measurements[sensor_id].timestamp).id)
            if sensor_id in last_measurements:
                sensor.last_measurement = (measurement_repository.
                                           get_by_sensor_and_timestamp(sensor_id,
                                                                       last_measurements[sensor_id].timestamp).id)
            sensor_repository.update(sensor)
        dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')
