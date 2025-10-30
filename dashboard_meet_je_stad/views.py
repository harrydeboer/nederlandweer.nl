from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
import os
import csv
import json


def index(request: WSGIRequest) -> HttpResponse:
    sensors= {}
    pm_ids = []
    pm = request.GET.get('pm')
    inactive = request.GET.get('inactive')
    service = MeetJeStadAPIService()
    utrecht_rows = []
    with open(os.path.dirname(os.path.abspath(__file__)) + '/utrecht_ids.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if pm == 'on' and row[len(service.row_keys) + 6] != '0':
                pm_ids.append(row[1])
            utrecht_rows.append(row)
    ids = []
    with open(os.path.dirname(os.path.abspath(__file__)) + '/dataset_small_utrecht.csv') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if pm == 'on' and row[1] not in pm_ids:
                continue
            if int(row[1]) not in sensors:
                sensor = Sensor(int(row[1]))
                sensors[int(row[1])] = sensor
                sensor.add_row(row)
                ids.append(row[1])
            else:
                sensors[int(row[1])].add_row(row)

    return render(request, 'homepage/index.html',
                  {'sensors': sorted(sensors.items()), 'sensorIds': json.dumps(ids), 'inactive': inactive,
                   'pm': pm, 'utrecht_rows': utrecht_rows, 'row_keys': service.row_keys})
