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
                last_good_row = None
                for row in reader:

                    if not row:
                        continue

                    if row[0] != '  ' + str(station.get_id()):
                        continue

                    # During the war a lot of data is not available. The gaps are filled with the last good row.
                    if len(row) > 10 and row[3] == '     ' and int(row[0]) > 19060101:
                        if last_good_row is None:
                            last_good_row = txt_list[-1:][0]
                        new_list = last_good_row
                        new_list[1] = row[1]
                        txt_list.append(new_list)
                    else:
                        last_good_row = None
                        txt_list.append(row)

            last_measurement = self.measurement_repository.find_last(station.get_id())
            measurements = []
            for row in txt_list:
                measurements.append(Measurement(row=row))

            # Remove the days of the first years until most data is available.
            for index, measurement in enumerate(measurements):

                year = int(measurement.get_timestamp().year)

                # Most data is available from 1904 and onwards.
                if year == 1906:
                    measurements = measurements[index:]
                    break

            # Remove the days of the last year if it is not complete.
            year_to_delete = None
            for index, measurement in enumerate(reversed(measurements)):

                year = int(measurement.get_timestamp().year)
                if (index == 0 and str(measurement.get_timestamp().month) +
                        str(measurement.get_timestamp().day) != '1231'):
                    year_to_delete = year
                    continue

                if year_to_delete is not None:
                    if year == year_to_delete - 1:
                        measurements = measurements[:-index]
                        break

            stations[name].set_begin_year(measurements[0].get_timestamp().year)
            stations[name].set_end_year(measurements[-1].get_timestamp().year)

            for measurement in measurements:
                if (last_measurement is None or measurement.get_timestamp().replace(tzinfo=datetime.timezone.utc)
                        > last_measurement.get_timestamp()):
                    self.measurement_repository.create(measurement)

        for index, station in stations.items():
            self.station_repository.update(station)
