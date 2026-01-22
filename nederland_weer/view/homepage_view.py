from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.service.curve_service import CurveService
from nederland_weer.model.station import Station
from nederland_weer.repository.station_repository import StationRepository


class HomepageView:

    def __init__(self):
        self.curve_service = CurveService()
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
        station = station_de_bilt
        if form.is_valid():
            station_id = int(form['station'].value())
            for index, station in stations.items():
                if station.station_id == station_id:
                    break
            if self._validate(form, station):
                (json_data, title,
                 vertical, horizontal, text_output) = (
                    self.curve_service.make_curve(int(station_id), form['type'].value(),
                                                  int(form['begin_year'].value()),
                                                  int(form['end_year'].value()),
                                                  int(station.end_year)))

        return render(request, 'homepage/index.html', {
            'form': form,
            'json': json_data,
            'minYear': int(station.begin_year),
            'maxYear': int(station.end_year),
            'title': title,
            'vertical': vertical,
            'horizontal': horizontal,
            'text_output': text_output,
        })

    def _validate(self, form: DashboardForm, station: Station) -> bool:
        type_graph = form['type'].value()
        first_year = int(form['begin_year'].value())
        last_year = int(form['end_year'].value())
        error_message = ''
        if last_year < first_year:
            error_message = 'Het laatste jaar kan niet eerder zijn dan het eerste jaar.'
        elif first_year < station.begin_year or last_year > station.end_year:
            error_message = 'Jaren buiten het bereik ' + str(station.begin_year) + '-' + str(station.end_year) + '.'
        elif type_graph == 'perc-rain' and first_year < station.begin_year_perc_rain:
            error_message = 'Begin jaar kan niet voor ' + str(station.begin_year_perc_rain) + ' zijn.'
        elif type_graph == 'amount-rain' and first_year < station.begin_year_amount_rain:
            error_message = 'Begin jaar kan niet voor ' + str(station.begin_year_amount_rain) + ' zijn.'
        elif type_graph == 'temperature-year' and last_year - first_year + 1 < 9:
            error_message = 'Bereik moet ten minste 9 jaar zijn als er een jaar grafiek gemaakt wordt.'
        elif type_graph == 'extreme' and first_year < station.begin_year_amount_rain:
            error_message = 'Begin jaar kan niet voor ' + str(station.begin_year_amount_rain) + ' zijn.'
        if error_message:
            form.add_error('begin_year', error_message)
            return False

        return True
