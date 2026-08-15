from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.models import Sensor
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
import json


class HomepageView:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.sensor_cached_repository = SensorCachedRepository()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseRedirect('inloggen')

        """First the form is build with all sensors in order to read the requested sensor_id."""
        inactive = False
        pm = False
        sensors = self.sensor_repository.find_all()
        form = DashboardForm(request.GET, sensors=sensors, inactive=inactive, pm=pm)
        sensor_id = None
        sensor_selected = Sensor()
        if hasattr(request.user, 'dashboarduser'):
            dashboard_user = request.user.dashboarduser
            sensor_selected = sensors[dashboard_user.get_sensor_id()]
            if not sensor_selected.is_active_sensor():
                inactive = True
        if form.is_valid():
            sensor_id = form['sensor'].value()
            if sensor_id is not None and sensor_id != '':
                sensor_id = int(sensor_id)
                sensor_selected = sensors[int(sensor_id)]
            else:
                sensor_id = None
            inactive = form['inactive'].value()
            pm = form['pm'].value()
            interval = form['interval'].value()

            if sensor_id is not None and sensor_id != '' and interval == '1month' and len(form.errors) == 0:
                sensor_selected.set_measurements_cached(
                    self.measurement_repository.get_previous_month(sensor_id))

        """The sensors that are not chosen are filtered away and the form is made again with the filtered sensors.
        If a sensor is chosen that is not valid an error message is added.
        """
        sensors_filtered = {}
        for sensor_id_old, sensor in sensors.items():
            if not inactive and not sensor.is_active_sensor():
                continue
            if pm and not sensor.is_particulate_matter():
                continue
            sensors_filtered[sensor_id_old] = sensor
        form = DashboardForm(request.GET, sensors=sensors_filtered, inactive=inactive, pm=pm)
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
                      {'form': form, 'sensor_json': json.dumps(sensor_selected.to_dict()),
                       'sensors_json': self.sensor_cached_repository.find_all_as_string()})
