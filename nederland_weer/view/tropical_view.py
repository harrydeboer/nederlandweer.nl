from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.model.curve import Curve
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
from nederland_weer.service.curve_service import CurveService
import numpy as np


class TropicalView:

    def __init__(self, knmi_data: KNMIData):
        self.knmiData = knmi_data
        self.knmi_data_repository = KNMIDataRepository()
        self.curve_service = CurveService(knmi_data)

    def tropical(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'tropical/index.html', {'minYear': self.knmiData.minYearFile,
                                                       'maxYear': self.knmiData.maxYearFile, 'text_output': ''})

    def tropical_year(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        temperatures = self.knmi_data_repository.get(self.knmiData.array, first_year, last_year, 'max_temp')
        data_temp = np.zeros(temperatures.shape[1])
        index_year = 0
        for year in np.transpose(temperatures):
            for temp in year:
                if temp >= 30:
                    data_temp[index_year] += 1
            index_year += 1
        data['json'] = self.curve_service.curve_to_json(Curve(data_temp, False, first_year, last_year))
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Tropische dagen'
        data['vertical'] = 'aantal'
        data['horizontal'] = 'jaar'
        return render(request, 'tropical/index.html', data)