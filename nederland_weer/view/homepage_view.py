from typing import List
import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.service.curve_service import CurveService
from nederland_weer.models import Measurement
from nederland_weer.repository.station_repository import StationRepository
import json


class HomepageView:

    def __init__(self):
        self.curve_service = CurveService()
        self.measurement_repository = MeasurementRepository()
        self.station_repository = StationRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        stations = self.station_repository.find_all()
        station_de_bilt = stations['De Bilt']
        form = DashboardForm(request.GET, stations = stations)
        json_data = ''
        text_output = ''
        title = ''
        vertical = ''
        horizontal = ''
        stations_dict = {}
        for station_name, station in stations.items():
            stations_dict[station_name] = station.to_dict()
        station = station_de_bilt
        if form.is_valid():
            station_id = int(form['station'].value())
            for index, station in stations.items():
                if station.get_id() == station_id:
                    break
            measurements = self.measurement_repository.find_all(int(station.get_id()),
                                                                datetime.datetime.strptime(
                                                                    form['begin_year'].value(), '%d-%m-%Y')
                                                                .replace(tzinfo=datetime.timezone.utc),
                                                                datetime.datetime.strptime(
                                                                    form['end_year'].value(), '%d-%m-%Y')
                                                                .replace(tzinfo=datetime.timezone.utc))
            if self._validate(form, measurements):
                (json_data, title,
                 vertical, horizontal, text_output) = (
                    self.curve_service.make_curves(form['component'].value(), measurements))

        return render(request, 'homepage/index.html', {
            'form': form,
            'json': json_data,
            'stations_json': json.dumps(stations_dict),
            'title': title,
            'vertical': vertical,
            'horizontal': horizontal,
            'text_output': text_output,
        })

    def _validate(self, form: DashboardForm, measurements: List[Measurement]) -> bool:
        component = form['component'].value()
        first_year = (datetime.datetime.strptime(form['begin_year'].value(), '%d-%m-%Y')
                      .replace(tzinfo=datetime.timezone.utc).year)
        last_year = (datetime.datetime.strptime(form['end_year'].value(), '%d-%m-%Y')
                     .replace(tzinfo=datetime.timezone.utc).year)
        begin_year = measurements[0].get_timestamp().year
        end_year = measurements[-1].get_timestamp().year
        error_message = ''
        if last_year < first_year:
            error_message = 'Het laatste jaar kan niet eerder zijn dan het eerste jaar.'
        elif first_year < begin_year or last_year > end_year:
            error_message = ('Jaren buiten het bereik ' + str(begin_year) + '-'
                             + str(end_year) + '.')
        elif ((component == 'temperature-year' or component == 'tropical' or component == 'extreme')
              and last_year - first_year + 1 < 9):
            error_message = 'Bereik moet ten minste 9 jaar zijn als er een jaar grafiek gemaakt wordt.'
        if error_message:
            form.add_error('begin_year', error_message)
            return False

        return True
