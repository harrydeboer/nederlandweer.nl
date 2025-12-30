from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.model.curve import Curve
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
from nederland_weer.service.curve_service import CurveService
import numpy as np


class ExtremeView:

    def __init__(self):
        self.knmiData = KNMIData()
        self.knmi_data_repository = KNMIDataRepository()
        self.curve_service = CurveService()

    def extreme(self, request: WSGIRequest) -> HttpResponse:
        data = {}
        rain_amounts = self.knmi_data_repository.get(self.knmiData.array, 1930,
                                                           self.knmiData.maxYearFile, 'amount_rain')
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
        data['json'] = self.curve_service.curve_to_json(Curve(data_temp, False, 1930, self.knmiData.maxYearFile))
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Maximaal neerslag tekort'
        data['vertical'] = 'tekort'
        data['horizontal'] = 'jaar'
        return render(request, 'extreme/index.html', data)