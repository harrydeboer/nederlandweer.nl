from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.model.sensor import Sensor
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository


class HomepageView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.sensor_utrecht_repository = SensorUtrechtRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        sensors= {}
        pm_ids = []
        [pm, inactive, id_sensor, type_sensor] = self._validate(request)

        rows = self.sensor_utrecht_repository.get()
        utrecht_rows = []
        for index_row, row in rows.items():
            if pm == 'on' and row[len(self.service.row_keys) + 6] != '0':
                pm_ids.append(row[1])
            utrecht_rows.append(row)
        rows = self.sensor_repository.get_small_utrecht()
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
                  {'sensors': sorted(sensors.items()), 'inactive': inactive, 'id_sensor': id_sensor, 'pm': pm,
                   'type_sensor': type_sensor, 'utrecht_rows': utrecht_rows, 'row_keys': self.service.row_keys})

    def _validate(self, request: WSGIRequest):
        pm = request.GET.get('pm')
        inactive = request.GET.get('inactive')
        id_sensor = request.GET.get('sensor')
        type_sensor = request.GET.get('type')
        if pm != 'on' and pm != 'off':
            pm = None
        if inactive != 'on' and inactive != 'off':
            inactive = None
        if (type_sensor != 'temperature' and type_sensor != 'humidity'
                and type_sensor != 'pm25' and type_sensor != 'pm10'):
            type_sensor = None
        if id_sensor is not None and not id_sensor.isdigit():
            id_sensor = None
        elif id_sensor is not None and id_sensor.isdigit():
            id_sensor = int(id_sensor)

        return [pm, inactive, id_sensor, type_sensor]
