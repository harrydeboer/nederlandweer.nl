from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
import os
import datetime
import dotenv


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
sensor_repository = SensorRepository()
sensor_utrecht_repository = SensorUtrechtRepository()
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
    sensor_repository.add_to_full(index, rows)
    if index > last_sensor_id:
        last_sensor_id = index
    sensor_repository.add_to_small(rows)

rows = sensor_repository.get_small_last_24(date_now)
sensor_repository.write_to_small(rows)

dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')

utrecht_ids = sensor_utrecht_repository.update(date_now.strftime('%Y-%m-%d'), rows)

rows_utrecht = []
for row in rows:
    if int(row[1]) in utrecht_ids:
        rows_utrecht.append(row)
sensor_repository.write_to_small_utrecht(rows_utrecht)
