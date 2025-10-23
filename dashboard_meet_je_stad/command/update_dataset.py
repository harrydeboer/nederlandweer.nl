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
csv.writer(file).writerows(results_old + results)
file.close()
