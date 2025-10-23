from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
import csv
import os
import datetime


date = datetime.datetime.now(datetime.timezone.utc)
sensors = []
results_old = []
with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/dataset.csv') as csvfile:
    reader = csv.reader(csvfile)
    for index, row in enumerate(reader):
        if row[1] not in sensors:
            sensors.append(row[1])
        if index == 0:
            start_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        end_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        if (datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=datetime.timezone.utc) - date).days > -366:
            results_old.append(row)
csvfile.close()

delta = date - end_date
results = MeetJeStadAPIService().get_data(
            end_date.strftime('%Y-%m-%d,%H:%M:%S'),
            date.strftime('%Y-%m-%d,%H:%M:%S'),
    'sensors',
'json',
            'Utrecht',
        False,
        2 * delta.days * 24 * 4 * len(sensors),
False)
file = open(os.path.dirname(os.getcwd()) + "/dataset.csv", "w", newline='')
full_dataset = results_old + results
csv.writer(file).writerows(full_dataset)
file.close()

ids = {}
with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/dataset.csv') as csvfile:
    reader = csv.reader(csvfile)
    for index, row in enumerate(reader):
        if row[1] not in ids:
            ids[row[1]] = [row]
        else:
            ids[row[1]] += [row]
for index, id_sensor in ids.items():
    os.makedirs(os.path.dirname(os.getcwd()) + '/ids/' + index, exist_ok=True)
    file = open(os.path.dirname(os.getcwd()) + "/ids/" + index + "/out.csv", "w", newline='')
    csv.writer(file).writerows(id_sensor)
    file.close()

rows = []
for row in full_dataset:
    date_row = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    if date - date_row < datetime.timedelta(hours=48):
        rows.append(row)

file = open(os.path.dirname(os.getcwd()) + "/dataset_small.csv", "w", newline='')
csv.writer(file).writerows(rows)
file.close()