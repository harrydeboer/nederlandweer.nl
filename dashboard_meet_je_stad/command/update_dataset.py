from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
import os
import datetime
import dotenv


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
measurement_repository = MeasurementRepository()
sensor_repository = SensorRepository()
rows_new = {}
sensor_step = 50
last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
end_date = datetime.datetime.strptime(os.getenv('END_DATE'),"%Y-%m-%d,%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
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
        2 * delta.days * 24 * 4 * sensor_step,
        False)
    for row in results:
        if row[1] not in rows_new:
            rows_new[row[1]] = [row]
        else:
            rows_new[row[1]] += [row]

for index, rows in rows_new.items():
    measurement_repository.add_to_full(index, rows)
    if index > last_sensor_id:
        last_sensor_id = index
    measurement_repository.add_to_small(rows)

measurements = measurement_repository.get_small_last_24(date_now)
measurement_repository.write_to_small(measurements)

dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')

sensors = sensor_repository.update(measurements)

measurements_utrecht = {}
for index, measurements_out in measurements.items():
    if index in sensors:
        for measurement in measurements_out:
            if measurement.id in measurements_utrecht:
                measurements_utrecht[measurement.id].append(measurement)
            else:
                measurements_utrecht[measurement.id] = [measurement]
measurement_repository.write_to_small_utrecht(measurements_utrecht)
