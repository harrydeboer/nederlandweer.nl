from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.service.curve_service import CurveService
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
from nederland_weer.model.curve import Curve
from dotenv import load_dotenv
import locale
import os
import numpy as np


class HomepageView:

    def __init__(self):
        self.knmi_data_repository = KNMIDataRepository()

    def index(self, request: WSGIRequest) -> HttpResponse:
        load_dotenv()
        begin_year = int(os.getenv('BEGIN_YEAR'))
        end_year = int(os.getenv('END_YEAR'))
        begin_year_rain_perc = int(os.getenv('BEGIN_YEAR_RAIN_PERCENTAGE'))
        form = DashboardForm(request.GET, begin_year=begin_year, end_year=end_year)
        json_data = {}
        text_output = ''
        title = ''
        vertical = ''
        horizontal = ''
        if form.is_valid() and self._validate(form, begin_year, end_year, begin_year_rain_perc):
            knmi_data = KNMIData()
            curve_service = CurveService(knmi_data)
            type_graph = form['type'].value()
            begin_year = int(form['begin_year'].value())
            end_year = int(form['end_year'].value())
            if type_graph == 'temperature-day':
                curve = curve_service.get_curve('mean_temp', 1, begin_year, end_year)
                locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
                json_data = curve_service.curve_to_json(curve)
                text_output = 'Eerste zomer dag: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
                title = 'Temperatuur'
                vertical = 'temperatuur °C'
                horizontal = 'dag'
            elif type_graph == 'temperature-year':
                curve = curve_service.get_curve('mean_temp', 0, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                text_output = 'Temperatuur stijging: ' + str(
                    int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
                title = 'Temperatuur'
                vertical = 'temperatuur °C'
                horizontal = 'jaar'
            elif type_graph == 'amount-rain':
                curve = curve_service.get_curve('amount_rain', 1, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                title = 'Regen hoeveelheid'
                vertical = 'regen hoeveelheid mm'
                horizontal = 'dag'
            elif type_graph == 'perc-rain':
                curve = curve_service.get_curve('perc_rain', 1, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                title = 'Regen percentage'
                vertical = 'regen percentage'
                horizontal = 'dag'
            elif type_graph == 'perc-sunshine':
                curve = curve_service.get_curve('perc_sunshine', 1, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                title = 'Zonneschijn'
                vertical = 'percentage zon'
                horizontal = 'dag'
            elif type_graph == 'wind-speed':
                curve = curve_service.get_curve('wind_speed', 1, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                title = 'Wind snelheid'
                vertical = 'snelheid m/s'
                horizontal = 'dag'
            elif type_graph == 'wind-speed-va':
                # The vector average speed and direction are retrieved as a 2-dimensional day year array.
                speed_2d = self.knmi_data_repository.get(knmi_data.array, begin_year,
                                                         end_year, 'wind_speed_va')
                angle_2d = self.knmi_data_repository.get(knmi_data.array,
                                                         begin_year, end_year, 'wind_direction')

                # The 2-dimensional angle and speed are averaged over the years.
                angle = Curve.mean_of_angle(speed_2d, angle_2d)

                curve = Curve(angle, True, begin_year, end_year)
                json_data = curve_service.curve_to_json(curve)
                title = 'Wind richting'
                vertical = 'hoek'
                horizontal = 'dag'
            elif type_graph == 'tropical':
                temperatures = self.knmi_data_repository.get(knmi_data.array, begin_year, end_year, 'max_temp')
                data_temp = np.zeros(temperatures.shape[1])
                index_year = 0
                for year in np.transpose(temperatures):
                    for temp in year:
                        if temp >= 30:
                            data_temp[index_year] += 1
                    index_year += 1
                json_data = curve_service.curve_to_json(Curve(data_temp, False, begin_year, end_year))
                title = 'Tropische dagen'
                vertical = 'aantal'
                horizontal = 'jaar'
            elif type_graph == 'extreme':
                rain_amounts = self.knmi_data_repository.get(knmi_data.array, 1930,
                                                             knmi_data.maxYearFile, 'amount_rain')
                data_temp = np.zeros(rain_amounts.shape[1])
                index_year = 0
                rain_amount_average = 0
                for year in np.transpose(rain_amounts):
                    for amount in year:
                        rain_amount_average += amount
                rain_amount_average = rain_amount_average / len(np.transpose(rain_amounts))
                for year in np.transpose(rain_amounts):
                    index_day = 0
                    rain_amount_realized = 0
                    deficit_days = np.zeros(len(year))
                    for amount in year:
                        rain_amount_average_day = rain_amount_average / 365.24 * (index_day + 1)
                        rain_amount_realized += amount
                        deficit_days[index_day] = rain_amount_realized - rain_amount_average_day
                        index_day += 1
                    data_temp[index_year] = np.max(deficit_days)
                    index_year += 1
                json_data = curve_service.curve_to_json(
                    Curve(data_temp, False, 1930, knmi_data.maxYearFile))
                title = 'Maximaal neerslag tekort'
                vertical = 'tekort'
                horizontal = 'jaar'

        return render(request, 'homepage/index.html', {
            'form': form,
            'json': json_data,
            'minYear': begin_year,
            'maxYear': end_year,
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
