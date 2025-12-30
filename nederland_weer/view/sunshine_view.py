from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.service.curve_service import CurveService


class SunshineView:

    def __init__(self):
        self.knmiData = KNMIData()
        self.curve_service = CurveService()

    def sunshine(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'sunshine/index.html', {'minYear': self.knmiData.minYearFile,
                                                       'maxYear': self.knmiData.maxYearFile, 'text_output': ''})

    def sunshine_percentage(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('perc_sunshine', 1, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Zonneschijn'
        data['vertical'] = 'percentage zon'
        data['horizontal'] = 'dag'
        return render(request, 'sunshine/index.html', data)