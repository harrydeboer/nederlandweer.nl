from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.model.sensor import Sensor
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm


class HomepageView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.sensor_utrecht_repository = SensorUtrechtRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        sensors= {}
        pm_ids = []
        pm = False
        if request.GET:
            if 'inactive' in request.GET:
                inactive = request.GET['inactive']
            else:
                inactive = 'off'
            form = DashboardForm(request.GET, is_inactive=inactive)
        else:
            form = DashboardForm(is_inactive='off')
        if form.is_valid():
            pm = form['pm'].value()
        rows = self.sensor_utrecht_repository.get()
        utrecht_rows = []
        for index_row, row in rows.items():
            if pm and row[len(self.service.row_keys) + 6] != '0':
                pm_ids.append(row[1])
            utrecht_rows.append(row)
        rows = self.sensor_repository.get_small_utrecht()
        for row in rows:
            if pm and row[1] not in pm_ids:
                continue
            if int(row[1]) not in sensors:
                sensor = Sensor(int(row[1]))
                sensors[int(row[1])] = sensor
                sensor.add_row(row)
            else:
                sensors[int(row[1])].add_row(row)

        return render(request, 'homepage/index.html',
                  {'sensors': sorted(sensors.items()), 'form': form,
                   'utrecht_rows': utrecht_rows, 'row_keys': self.service.row_keys})
