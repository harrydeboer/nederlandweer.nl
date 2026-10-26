from django.core.management.base import BaseCommand
from nederland_weer.models import Measurement
from nederland_weer.repository.measurement_repository import MeasurementRepository
from nederland_weer.repository.station_repository import StationRepository
import urllib.request
import zipfile
import os
from django.apps import apps
import csv
import datetime
import sys
from pathlib import Path


class Command(BaseCommand):
    help = "Updates the dataset"

    def __init__(self):
        super().__init__()
        self.measurement_repository = MeasurementRepository()
        self.station_repository = StationRepository()
        path = os.path.dirname(apps.get_app_config('nederland_weer').path)
        if sys.argv[1:2] == ['test']:
            self.path_data = path + '/tests/data/'
        else:
            self.path_data = path + '/data/'
        if not os.path.exists(self.path_data):
            Path(self.path_data).mkdir(parents=True, exist_ok=True)

    def handle(self, *args, **options):
        stations = self.station_repository.find_all()
        for name, station in stations.items():
            urllib.request.urlretrieve("https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_"
                                       + str(station.get_id()) + ".zip", self.path_data + 'test.zip')
            with zipfile.ZipFile(self.path_data + 'test.zip', 'r') as zip_ref:
                zip_ref.extractall(self.path_data)
            os.unlink(self.path_data + 'test.zip')

            # Read txt file as list.
            txt_list = []
            with open(self.path_data + 'etmgeg_' + str(station.get_id()) + '.txt', newline='') as input_file:
                reader = csv.reader(input_file)
                for row in reader:

                    if not row:
                        continue

                    if row[0] != '  ' + str(station.get_id()):
                        continue

                    txt_list.append(row)

            last_measurement = self.measurement_repository.find_last(station.get_id())
            measurements = []
            for row in txt_list:
                measurements.append(Measurement(row=row))

            for measurement in measurements:
                if (last_measurement is None or measurement.get_timestamp().replace(tzinfo=datetime.timezone.utc)
                        > last_measurement.get_timestamp()):
                    self.measurement_repository.create(measurement)
