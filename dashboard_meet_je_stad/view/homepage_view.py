from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm


class HomepageView:

    def __init__(self):
        self.sensor_repository = SensorRepository()
        self.sensor_cached_repository = SensorCachedRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        sensors_json = self.sensor_cached_repository.find_all()
        form = DashboardForm(request.GET)
        if form.is_valid():
            if form['interval'].value() == '3month':
                self.sensor_repository.get_days(int(form['sensor'].value()), 91)

        return render(request, 'homepage/index.html',{'form': form, 'sensors_json': sensors_json})
