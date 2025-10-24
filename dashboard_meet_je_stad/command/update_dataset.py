from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.service.utrecht_ids_service import UpdateUtrechtIdsService
import csv
import os
import datetime
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
ids = {}
sensor_step = 50
last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
end_date = datetime.datetime.strptime(os.getenv('END_DATE'),"%Y-%m-%d,%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
date_now = datetime.datetime.now(datetime.timezone.utc)
delta = date_now - end_date
for sensor_id_50 in range(0, int(last_sensor_id / sensor_step) + 2):
    ids_range = str(sensor_id_50 * sensor_step + 1) + '-' + str((sensor_id_50 + 1) * sensor_step)
    end_date += datetime.timedelta(seconds=1)
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
        if row[1] not in ids:
            ids[row[1]] = [row]
        else:
            ids[row[1]] += [row]
UpdateUtrechtIdsService().update(ids, end_date.strftime('%Y-%m-%d'))
utrecht_ids = []
with open(os.path.dirname(os.getcwd()) + '/utrecht_ids.csv') as csvfile:
    reader = csv.reader(csvfile)
    for index, row in enumerate(reader):
        utrecht_ids.append(row[0])


for index, rows in ids.items():
    os.makedirs(os.path.dirname(os.getcwd()) + '/ids/' + str(index), exist_ok=True)
    file = open(os.path.dirname(os.getcwd()) + "/ids/" + str(index) + "/out.csv", "a", newline='')
    csv.writer(file).writerows(rows)
    file.close()
    if index > last_sensor_id:
        last_sensor_id = index

    if str(index) in utrecht_ids:
        file = open(os.path.dirname(os.getcwd()) + "/dataset_small.csv", "a", newline='')
        csv.writer(file).writerows(rows)
        file.close()

rows = []
with open(os.path.dirname(os.getcwd()) + '/dataset_small.csv') as csvfile:
    reader = csv.reader(csvfile)
    for index, row in enumerate(reader):
        date_row = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        if date_now - date_row < datetime.timedelta(hours=48):
            rows.append(row)
file = open(os.path.dirname(os.getcwd()) + "/dataset_small.csv", "w", newline='')
csv.writer(file).writerows(rows)
file.close()

dotenv.set_key(dotenv_file, "LAST_SENSOR_ID", str(last_sensor_id), quote_mode='never')
dotenv.set_key(dotenv_file, "END_DATE", date_now.strftime('%Y-%m-%d,%H:%M:%S'), quote_mode='never')
