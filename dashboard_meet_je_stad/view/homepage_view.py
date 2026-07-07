from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm


class HomepageView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        pm = False
        inactive = False
        interval = '24hour'
        id_sensor = None
        form = DashboardForm(request.GET, inactive=True, sensors=self.sensor_repository.find_all())
        if form.is_valid():
            pm = form['pm'].value()
            inactive = form['inactive'].value()
            interval = form['interval'].value()
            id_sensor = form['sensor'].value()
            if id_sensor == '':
                id_sensor = None
            else:
                id_sensor = int(id_sensor)
        sensors = self.sensor_repository.find_all(pm=pm)
        sensors = self.sensor_repository.get_small(sensors, interval, inactive, id_sensor)
        form = DashboardForm(request.GET, inactive=inactive, sensors=sensors)

        return render(request, 'homepage/index.html',{'form': form, 'sensors': sensors})
