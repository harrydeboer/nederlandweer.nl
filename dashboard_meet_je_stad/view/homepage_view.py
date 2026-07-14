from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
import json
from dashboard_meet_je_stad.models import Measurement, Sensor
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.sensor_cached_repository import SensorCachedRepository
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
from dashboard_meet_je_stad.service.make_grid_service import MakeGridService


class HomepageView:

    def __init__(self):
        self.sensor_repository = SensorRepository()
        self.make_grid_service = MakeGridService()
        self.sensor_cached_repository = SensorCachedRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        sensors_json = self.sensor_cached_repository.find_all()
        form = DashboardForm(request.GET)
        if form.is_valid():
            if form['interval'].value() == '3month':
                self.sensor_repository.get_days(int(form['sensor'].value()), 91)

        sensors_json_transposed = {}
        for sensor_id, sensor in sensors_json.items():
            sensor_transposed = {}
            for field in Sensor._meta.fields:
                sensor_transposed[field.attname] = sensor[field.attname]
            count = 0
            for field in Measurement._meta.fields:
                if field.attname == 'id':
                    count += 1
                    continue
                for measurement in sensor['measurements']:
                    if field.attname in sensor_transposed:
                        sensor_transposed[field.attname].append(measurement[count])
                    else:
                        sensor_transposed[field.attname] = [measurement[count]]
                count += 1
            sensors_json_transposed[sensor_id] = sensor_transposed

        return render(request, 'homepage/index.html',{'form': form,
                                                      'sensors_json': json.dumps(sensors_json_transposed)})
