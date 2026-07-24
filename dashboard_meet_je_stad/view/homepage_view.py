from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService
import json


class HomepageView:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.make_grid_service = MakeGridService()
        self.sensor_cached_repository = SensorCachedRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        sensors = self.sensor_repository.find_all()
        form = DashboardForm(request.GET, sensors=sensors)
        inactive = False
        pm = False
        sensor_id = None
        sensor_selected = None
        if form.is_valid():
            sensor_id = form['sensor'].value()
            sensor_selected = sensors[int(sensor_id)]
            if sensor_id is not None and sensor_id != '':
                sensor_id = int(sensor_id)
            else:
                sensor_id = None
            inactive = form['inactive'].value()
            pm = form['pm'].value()
            interval = form['interval'].value()
            if sensor_id is not None and interval == '3month' and len(form.errors) == 0:
                sensor_selected.set_measurements_cached(self.make_grid_service.make_grid(
                    self.measurement_repository.get_days(sensor_id, 91), sensor_id, 91))
                sensor_selected = sensor_selected.to_dict()
        sensors_filtered = {}
        for sensor_id_old, sensor in sensors.items():
            if not inactive and not sensor.is_active_sensor():
                continue
            if pm and not sensor.is_particulate_matter:
                continue
            sensors_filtered[sensor_id_old] = sensor
        form = DashboardForm(request.GET, sensors=sensors_filtered)
        if not form.is_valid():
            if 'sensor' in form.errors:
                form.errors.pop('sensor')
            if not sensor_id is None and not inactive and not sensors[sensor_id].is_active_sensor():
                form.add_error('inactive',
                               'De gekozen sensor is inactief en er is gekozen voor alleen actieve sensors.')
            if not sensor_id is None and pm and not sensors[sensor_id].is_particulate_matter:
                form.add_error('pm',
                               'De gekozen sensor is fijnstof en er is gekozen voor alleen fijnstof sensors.')

        return render(request, 'homepage/index.html',
                      {'form': form, 'sensor_json': json.dumps(sensor_selected),
                       'sensors_json': self.sensor_cached_repository.find_all_as_string()})
