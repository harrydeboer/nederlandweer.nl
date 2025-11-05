from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
from dashboard_meet_je_stad.model.sensor import Sensor
from dashboard_meet_je_stad.model.sensor_utrecht import SensorUtrecht


class HomepageView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.sensor_utrecht_repository = SensorUtrechtRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        row_keys = Sensor.row_keys
        row_keys_utrecht = SensorUtrecht.row_keys
        pm = False
        inactive = 'off'
        if request.GET:
            if 'inactive' in request.GET:
                inactive = request.GET['inactive']
            else:
                inactive = 'off'
            form = DashboardForm(request.GET, is_inactive=inactive, sensors={}, pm=False)
        else:
            form = DashboardForm(is_inactive=inactive, sensors= {}, pm=False)
        if form.is_valid():
            pm = form['pm'].value()
        utrecht_rows = self.sensor_utrecht_repository.get(pm=pm)
        sensors = self.sensor_repository.get_small_utrecht(utrecht_rows=utrecht_rows)
        if request.GET:
            form = DashboardForm(request.GET, is_inactive=inactive, sensors=sensors, pm=pm)
        else:
            form = DashboardForm(is_inactive=inactive, sensors=sensors, pm=pm)

        return render(request, 'homepage/index.html',
                  {'sensors': sorted(sensors.items()), 'form': form,
                   'utrecht_rows': utrecht_rows, 'row_keys': row_keys, 'row_keys_utrecht': row_keys_utrecht})
