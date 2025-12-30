from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.service.curve_service import CurveService


class RainView:

    def __init__(self):
        self.knmiData = KNMIData()
        self.curve_service = CurveService()

    def rain(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'rain/index.html', {'minYear': self.knmiData.minYearFile,
                                                   'maxYear': self.knmiData.maxYearFile, 'text_output': ''})

    def rain_amount(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('amount_rain', 1, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Regen hoeveelheid'
        data['vertical'] = 'regen hoeveelheid mm'
        data['horizontal'] = 'dag'
        return render(request, 'rain/index.html', data)

    def rain_percentage(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('perc_rain', 1, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Regen percentage'
        data['vertical'] = 'regen percentage'
        data['horizontal'] = 'dag'
        return render(request, 'rain/index.html', data)