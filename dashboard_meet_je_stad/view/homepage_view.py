from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm


class HomepageView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.measurement_repository = MeasurementRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        pm = False
        inactive = False
        form = DashboardForm(request.GET, inactive=inactive, sensors={})
        if form.is_valid():
            pm = form['pm'].value()
            inactive = form['inactive'].value()
        sensors = self.sensor_repository.get(pm=pm)
        sensors = self.measurement_repository.get_small_utrecht(sensors=sensors)
        form = DashboardForm(request.GET, inactive=inactive, sensors=sensors)

        return render(request, 'homepage/index.html',{'form': form, 'sensors': sensors})
