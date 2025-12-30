from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
import locale
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.service.curve_service import CurveService

class TemperatureView:

    def __init__(self, knmi_data: KNMIData):
        self.knmiData = knmi_data
        self.curve_service = CurveService(knmi_data)

    def temperature(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'temperature/index.html', {'minYear': self.knmiData.minYearFile,
                                                          'maxYear': self.knmiData.maxYearFile, 'text_output': ''})

    def temperature_day(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('mean_temp', 1, first_year, last_year)
        locale.setlocale(locale.LC_TIME, "nl_NL")
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['text_output'] = 'Eerste zomer dag: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
        data['title'] = 'Temperatuur'
        data['vertical'] = 'temperatuur °C'
        data['horizontal'] = 'dag'
        return render(request, 'temperature/index.html', data)

    def temperature_year(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('mean_temp', 0, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['text_output'] = 'Temperatuur stijging: ' + str(
            int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
        data['title'] = 'Temperatuur'
        data['vertical'] = 'temperatuur °C'
        data['horizontal'] = 'jaar'
        return render(request, 'temperature/index.html', data)