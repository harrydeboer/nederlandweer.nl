from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from django.core.management.base import BaseCommand
import os
import datetime
import dotenv


class Command(BaseCommand):
    help = "Updates the dataset"

    def handle(self, *args, **options):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        measurement_repository = MeasurementRepository()
        sensor_step = 50
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
        for sensor_id_50 in range(0, int(last_sensor_id / sensor_step) + 2):
            ids_range = str(sensor_id_50 * sensor_step + 1) + '-' + str((sensor_id_50 + 1) * sensor_step)
            results = MeetJeStadAPIService().get_data(
                end_date.strftime('%Y-%m-%d,%H:%M:%S'),
                date_now.strftime('%Y-%m-%d,%H:%M:%S'),
        'sensors',
        'json',
                ids_range,
        False,
                2 * (delta.days + 1) * 24 * 4 * sensor_step,
        False)
            measurement_repository.bulk_create(results)

        dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
        dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')
