from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.service.curve_service import CurveService
from nederland_weer.repository.measurement_repository import MeasurementRepository
from dotenv import load_dotenv
import os


class HomepageView:

    def __init__(self):
        self.curve_service = CurveService()
        self.measurement_repository = MeasurementRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        load_dotenv()
        min_year = int(os.getenv('BEGIN_YEAR'))
        max_year = int(os.getenv('END_YEAR'))
        begin_year_rain_perc = int(os.getenv('BEGIN_YEAR_RAIN_PERCENTAGE'))
        form = DashboardForm(request.GET, begin_year=min_year, end_year=max_year)
        json_data = ''
        text_output = ''
        title = ''
        vertical = ''
        horizontal = ''
        if form.is_valid() and self._validate(form, min_year, max_year, begin_year_rain_perc):
            (json_data, title,
             vertical, horizontal, text_output) = self.curve_service.make_curve(form['type'].value(),
                                                                                int(form['begin_year'].value()),
                                                                                int(form['end_year'].value()),
                                                                                max_year, begin_year_rain_perc)

        return render(request, 'homepage/index.html', {
            'form': form,
            'json': json_data,
            'minYear': min_year,
            'maxYear': max_year,
            'title': title,
            'vertical': vertical,
            'horizontal': horizontal,
            'text_output': text_output,
        })

    def _validate(self, form: DashboardForm, min_year: int, max_year: int, min_year_rain_perc: int) -> bool:
        type_graph = form['type'].value()
        first_year = int(form['begin_year'].value())
        last_year = int(form['end_year'].value())
        error_message = ''
        if last_year < first_year:
            error_message = 'Het laatste jaar kan niet eerder zijn dan het eerste jaar.'
        elif first_year < min_year or last_year > max_year:
            error_message = 'Jaren buiten het bereik ' + str(min_year) + '-' + str(max_year) + '.'
        elif type_graph == 'perc-rain' and first_year < min_year_rain_perc:
            error_message = 'Begin jaar kan niet voor ' + str(min_year_rain_perc) + ' zijn.'
        elif type_graph == 'temperature-year' and last_year - first_year + 1 < 9:
            error_message = 'Bereik moet ten minste 9 jaar zijn als er een jaar grafiek gemaakt wordt.'
        if error_message:
            form.add_error('begin_year', error_message)
            return False

        return True
