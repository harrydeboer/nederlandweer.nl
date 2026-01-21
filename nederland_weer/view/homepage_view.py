from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.service.curve_service import CurveService
import csv


class HomepageView:

    def __init__(self):
        self.curve_service = CurveService()

    def index(self, request: WSGIRequest) -> HttpResponse:
        stations = []
        station_de_bilt = []
        with open('data/station.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                stations.append(row)
                if row[0] == '260':
                    station_de_bilt = row
        form = DashboardForm(request.GET, stations = stations)
        json_data = ''
        text_output = ''
        title = ''
        vertical = ''
        horizontal = ''
        station = station_de_bilt
        if form.is_valid():
            station_id = form['station'].value()
            for station in stations:
                if station[0] == station_id:
                    break
            if self._validate(form, station):
                (json_data, title,
                 vertical, horizontal, text_output) = (
                    self.curve_service.make_curve(int(station_id), form['type'].value(),
                                                  int(form['begin_year'].value()),
                                                  int(form['end_year'].value()),
                                                  int(station[3])))

        return render(request, 'homepage/index.html', {
            'form': form,
            'json': json_data,
            'minYear': int(station[2]),
            'maxYear': int(station[3]),
            'title': title,
            'vertical': vertical,
            'horizontal': horizontal,
            'text_output': text_output,
        })

    def _validate(self, form: DashboardForm, station: list) -> bool:
        type_graph = form['type'].value()
        first_year = int(form['begin_year'].value())
        last_year = int(form['end_year'].value())
        error_message = ''
        if last_year < first_year:
            error_message = 'Het laatste jaar kan niet eerder zijn dan het eerste jaar.'
        elif first_year < int(station[2]) or last_year > int(station[3]):
            error_message = 'Jaren buiten het bereik ' + station[2] + '-' + station[3] + '.'
        elif type_graph == 'perc-rain' and first_year < int(station[4]):
            error_message = 'Begin jaar kan niet voor ' + station[4] + ' zijn.'
        elif type_graph == 'amount-rain' and first_year < int(station[5]):
            error_message = 'Begin jaar kan niet voor ' + station[5] + ' zijn.'
        elif type_graph == 'temperature-year' and last_year - first_year + 1 < 9:
            error_message = 'Bereik moet ten minste 9 jaar zijn als er een jaar grafiek gemaakt wordt.'
        if error_message:
            form.add_error('begin_year', error_message)
            return False

        return True
