from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.model.sensor import Sensor
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository


def index(request: WSGIRequest) -> HttpResponse:
    sensors= {}
    pm_ids = []
    pm = request.GET.get('pm')
    inactive = request.GET.get('inactive')
    service = MeetJeStadAPIService()
    sensor_utrecht_repository = SensorUtrechtRepository()
    sensor_repository = SensorRepository()
    rows = sensor_utrecht_repository.get()
    utrecht_rows = []
    for index_row, row in rows.items():
        if pm == 'on' and row[len(service.row_keys) + 6] != '0':
            pm_ids.append(row[1])
        utrecht_rows.append(row)
    rows = sensor_repository.get_small_utrecht()
    for row in rows:
        if pm == 'on' and row[1] not in pm_ids:
            continue
        if int(row[1]) not in sensors:
            sensor = Sensor(int(row[1]))
            sensors[int(row[1])] = sensor
            sensor.add_row(row)
        else:
            sensors[int(row[1])].add_row(row)

    return render(request, 'homepage/index.html',
                  {'sensors': sorted(sensors.items()), 'inactive': inactive,
                   'pm': pm, 'utrecht_rows': utrecht_rows, 'row_keys': service.row_keys})
