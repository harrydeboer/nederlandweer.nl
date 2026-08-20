from dashboard_meet_je_stad.service.cleanup_service import CleanupService
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.user_repository import UserRepository
from django.core.management.base import BaseCommand
import os
import math
import datetime
import dotenv
import sys
from dashboard_meet_je_stad.models import Sensor
from django.core import mail
from django.template.loader import render_to_string


"""The command retrieves new measurements, updates the sensor and the cache."""
class Command(BaseCommand):
    help = "Updates the dataset"

    def __init__(self):
        super().__init__()
        self.measurement_repository = MeasurementRepository()
        self.sensor_cached_repository = SensorCachedRepository()
        self.sensor_repository = SensorRepository()
        self.user_repository = UserRepository()
        self.cleanup_service = CleanupService()
        self.make_grid_service = MakeGridService()

    def handle(self, *args, **options):
        if sys.argv[1:2] == ['test']:
            dotenv_file = '.env.test'
        else:
            dotenv_file = '.env'

        last_measurements = {}
        sensors = self.sensor_cached_repository.find_all()
        for sensor_id, sensor in sensors.items():
            for measurement in sensor.get_measurements_cached():
                if not measurement.get_supply() is None:
                    last_measurements[int(sensor_id)] = measurement

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
        earlier_day = date_now - datetime.timedelta(days=1)

        """The measurements are retrieved from the api. 
        Not all ids are requested at once but a range of ids are requested.
        Afterwards the measurements are getting a cleanup.
        """
        sensor_range = math.ceil(50 / (delta.days + 1) * 7)
        measurements = []
        for sensor_id_range in range(0, int(last_sensor_id / sensor_range) + 2):
            ids_range = str(sensor_id_range * sensor_range + 1) + '-' + str((sensor_id_range + 1) * sensor_range)
            measurements_range = MeetJeStadAPIService().get_measurements(
                end_date.strftime('%Y-%m-%d,%H:%M:%S'),
                date_now.strftime('%Y-%m-%d,%H:%M:%S'),
        'sensors',
                sensors,
                ids_range,
        False,
                (delta.days + 1) * 24 * 4 * sensor_range,
        False)
            measurements += measurements_range
        measurements = self.cleanup_service.clean(measurements)

        """The last sensor found is stored in last_sensor_id and get written to the .env.
        When a measurement is in Utrecht is is stored in measurements_utrecht.
        If a measurement has a sensor which is not in the cache it is created.
        The last measurements are updated.
        When a measurement has pm or lux the sensor is updated.
        """
        measurements_utrecht = []
        measurements_new = {}
        for measurement in measurements:
            if measurement.get_sensor_id() > last_sensor_id:
                last_sensor_id = measurement.get_sensor_id()
            if not measurement.is_in_utrecht():
                continue
            if measurement.get_sensor_id() not in sensors:
                sensor = Sensor()
                sensor.set_id(measurement.get_sensor_id())
                self.sensor_repository.create(sensor)
                sensors[measurement.get_sensor_id()] = sensor
            else:
                sensor = sensors[measurement.get_sensor_id()]
            last_measurements[sensor.get_id()] = measurement
            if measurement.get_pm25() is not None or measurement.get_pm10() is not None:
                sensor.set_is_particulate_matter(True)
            if measurement.get_lux() is not None:
                sensor.set_is_lux(True)
            if measurement.get_timestamp() >= earlier_day:
                if measurement.get_sensor_id() in measurements_new:
                    measurements_new[measurement.get_sensor_id()].append(measurement)
                else:
                    measurements_new[measurement.get_sensor_id()] = [measurement]
            measurements_utrecht.append(measurement)

        """The measurements are created.
        The sensors get the correct cached measurements. 
        These are the last measurements or the measurements more recent than a day earlier.
        If the measurements are more recent than a day earlier they are put in a grid.
        If the sensor has a measurement that is more recent than a day earlier it is set to active.
        """
        self.measurement_repository.bulk_create(measurements_utrecht)
        sensors_old = []
        for sensor_id, sensor in sensors.items():
            if sensor.is_active_sensor():
                sensors_old.append(sensor_id)
        for sensor_id, sensor in sensors.items():
            measurements_cached = []
            sensor.set_is_active_sensor(False)
            for index, measurement in enumerate(sensor.get_measurements_cached()):
                if (measurement.get_timestamp() >= earlier_day
                        or last_measurements[measurement.get_sensor_id()].get_id() == measurement.get_id()):
                    measurements_cached.append(measurement)
            if sensor_id in measurements_new:
                measurements_cached += measurements_new[sensor_id]
            for index, measurement in enumerate(measurements_cached):
                if measurement.get_timestamp() >= earlier_day and measurement.get_supply() is not None:
                    sensor.set_is_active_sensor(True)
            if sensor.is_active_sensor():
                sensor.set_measurements_cached(self.make_grid_service.make_grid(measurements_cached, sensor_id, 1))
            else:
                sensor.set_measurements_cached([last_measurements[sensor_id]])
            self.sensor_repository.update(sensor)
        self.sensor_cached_repository.write(sensors)

        newly_inactive = []
        for sensor_id in sensors_old:
            if not sensors[sensor_id].is_active_sensor():
                newly_inactive.append(str(sensor_id))

        dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')

        if len(newly_inactive) > 0:
            subject = 'Sensors inactief'
            html_message = render_to_string('admin/message.html',
                                            {'sensor_ids': ','.join(newly_inactive)})
            plain_message = html_message
            from_email = 'Meet Je Stad Utrecht <noreply@meetjestadutrecht.nl>'
            for user in self.user_repository.find_all():
                if user.is_superuser:
                    to = user.email
                    try:
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    except (TimeoutError, OSError):
                        self.stdout.write(self.style.ERROR('Could not send mail.'))

        self.stdout.write(self.style.SUCCESS('Successfully updated dataset.'))
