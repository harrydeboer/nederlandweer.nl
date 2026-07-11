from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.model.sensor import Sensor
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm


class HomepageView:

    def __init__(self):
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        pm = False
        inactive = False
        interval = '24hour'
        sensor_id = None
        sensors = self.sensor_repository.find_all()
        form = DashboardForm(request.GET, inactive=True, sensors=sensors)
        if form.is_valid():
            pm = form['pm'].value()
            inactive = form['inactive'].value()
            interval = form['interval'].value()
            sensor_id = form['sensor'].value()
            if sensor_id == '':
                sensor_id = None
            else:
                sensor_id = int(sensor_id)
        if sensor_id is not None:
            sensor = sensors[sensor_id]
        else:
            sensor = Sensor()
        sensors = self.sensor_repository.filter_and_dress_with_measurements(sensors, pm, interval, inactive, sensor_id)

        form = DashboardForm(request.GET, inactive=inactive, sensors=sensors)
        if not form.is_valid() and sensor_id is not None and sensor_id not in sensors:
            if 'sensor' in form.errors:
                form.errors.pop('sensor')
            if pm and not sensor.is_particulate_matter:
                form.add_error('sensor', 'Niet fijnstof sensor gekozen met optie alleen fijnstof sensoren.')
            elif not inactive:
                form.add_error('sensor', 'Inactieve sensor gekozen met optie alleen actieve sensoren.')

        return render(request, 'homepage/index.html',{'form': form, 'sensors': sensors})
