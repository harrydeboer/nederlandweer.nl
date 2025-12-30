from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.model.curve import Curve
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
from nederland_weer.service.curve_service import CurveService


class WindView:

    def __init__(self):
        self.knmiData = KNMIData()
        self.curve_service = CurveService()
        self.knmi_data_repository = KNMIDataRepository()

    def wind(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'wind/index.html', {'minYear': self.knmiData.minYearFile,
                                                   'maxYear': self.knmiData.maxYearFile, 'text_output': ''})

    def wind_speed(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        curve = self.curve_service.get_curve('wind_speed', 1, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Wind snelheid'
        data['vertical'] = 'snelheid m/s'
        data['horizontal'] = 'dag'
        return render(request, 'wind/index.html', data)

    def wind_vector(self, request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
        data = {}
        # The vector average speed and direction are retrieved as a 2-dimensional day year array.
        speed_2d = self.knmi_data_repository.get(self.knmiData.array, first_year,
                                                       last_year, 'wind_speed_va')
        angle_2d = self.knmi_data_repository.get(self.knmiData.array,
                                                       first_year, last_year, 'wind_direction')

        # The 2-dimensional angle and speed are averaged over the years.
        angle = Curve.mean_of_angle(speed_2d, angle_2d)

        curve = Curve(angle, True, first_year, last_year)
        data['json'] = self.curve_service.curve_to_json(curve)
        data['minYear'] = self.knmiData.minYearFile
        data['maxYear'] = self.knmiData.maxYearFile
        data['title'] = 'Wind richting'
        data['vertical'] = 'hoek'
        data['horizontal'] = 'dag'
        return render(request, 'wind/index.html', data)