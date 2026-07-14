from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
import json
from dashboard_meet_je_stad.repository.measurement_repository import MeasurementRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class HomepageView:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()
        self.make_grid_service = MakeGridService()
        self.sensor_cached_repository = SensorCachedRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        sensors = self.sensor_cached_repository.find_all()
        form = DashboardForm(request.GET)
        sensor_id = None
        if form.is_valid():
            sensor_id = form['sensor'].value()
            if sensor_id != '' and form['interval'].value() == '3month':
                sensors[int(sensor_id)].set_measurements_cached(
                    self.measurement_repository.get_days(int(form['sensor'].value()), 91))
        for sensor_id_new, sensor in sensors.items():
            days = 1
            if sensor_id is not None and int(sensor_id) == sensor_id_new:
                days = 91
            sensors[sensor_id_new].set_measurements_cached(
                self.make_grid_service.make_grid(sensor.get_measurements_cached(), days))
        sensors_json_transposed = self.sensor_cached_repository.transpose_measurements(sensors)

        return render(request, 'homepage/index.html',{'form': form,
                                                      'sensors_json': json.dumps(sensors_json_transposed)})
