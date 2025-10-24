from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.models import Sensor
import os
import csv
import json


def index(request: WSGIRequest) -> HttpResponse:
    sensors= {}
    pm_ids = []
    pm = request.GET.get('pm')
    if pm == 'on':
        with open(os.path.dirname(os.path.abspath(__file__)) + '/utrecht_ids.csv') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if row[5] != '0':
                   pm_ids.append(row[0])

    ids = []
    with open(os.path.dirname(os.path.abspath(__file__)) + '/dataset_small.csv') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if pm == 'on' and row[1] not in pm_ids:
                continue
            if row[1] not in sensors:
                sensor = Sensor(int(row[1]))
                sensors[row[1]] = sensor
                sensor.add_row(row)
                ids.append(row[1])
            else:
                sensors[row[1]].add_row(row)

    return render(request, 'homepage/index.html',
                  {'sensors': sensors, 'sensorIds': json.dumps(ids)})
