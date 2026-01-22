from django.core.management.base import BaseCommand
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.repository.station_repository import StationRepository
import urllib.request
import zipfile
import os
import pathlib


class Command(BaseCommand):
    help = "Updates the dataset"

    def handle(self, *args, **options):
        station_repository = StationRepository()
        stations = station_repository.find_all()
        path_project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        for index, station in enumerate(stations):
            urllib.request.urlretrieve("https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_"
                                       + station[0] + ".zip", 'data/test.zip')
            with zipfile.ZipFile(path_project + '/data/test.zip', 'r') as zip_ref:
                zip_ref.extractall(path_project + '/data')
            pathlib.Path.unlink(path_project + '/data/test.zip')
            measurements = MeasurementRepository().find_all(int(station[0]))
            stations[index][2] = measurements[0][1][:4]
            stations[index][3] = measurements[-1][1][:4]

        station_repository.write(path_project, stations)
