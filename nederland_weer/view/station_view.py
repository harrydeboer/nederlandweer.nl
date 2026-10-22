from nederland_weer.models import Station
from nederland_weer.repository.station_repository import StationRepository
from nederland_weer.form.station_form import StationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest


class StationView:

    def __init__(self):
        self.station_repository = StationRepository()

    @method_decorator(staff_member_required)
    def index(self, request: WSGIRequest) -> HttpResponse:
        stations = self.station_repository.find_all()
        return render(request, 'admin/station.html', {'stations': stations})

    @method_decorator(staff_member_required)
    def new(self, request: WSGIRequest) -> HttpResponse:
        station = Station()
        form = StationForm(request.POST, station=station)
        if form.is_valid():
            self._dress(station, form)
            self.station_repository.create(station)

            return redirect('stations')

        return render(request, 'admin/new.html', {'form': form, 'station': station})

    @method_decorator(staff_member_required)
    def edit(self, request: WSGIRequest, station_id) -> HttpResponse:
        station = self.station_repository.get(station_id)
        form = StationForm(request.POST, station=station)
        if form.is_valid():
            self._dress(station, form)
            self.station_repository.update(station)

            return redirect('stations')

        return render(request, 'admin/edit.html', {'form': form, 'station': station})

    @method_decorator(staff_member_required)
    def delete(self, request: WSGIRequest, station_id) -> HttpResponse:
        request.is_secure()
        station = self.station_repository.get(station_id)
        self.station_repository.delete(station)

        return redirect('stations')

    def _dress(self, station: Station, form: StationForm):
        station.set_id(form.cleaned_data['id'])
        station.set_name(form.cleaned_data['name'])
        station.set_begin_year(form.cleaned_data['begin_year'])
        station.set_end_year(form.cleaned_data['end_year'])
        station.set_begin_year_perc_rain(form.cleaned_data['begin_year_perc_rain'])
        station.set_begin_year_amount_rain(form.cleaned_data['begin_year_amount_rain'])
        station.set_longitude(form.cleaned_data['longitude'])
        station.set_latitude(form.cleaned_data['latitude'])
