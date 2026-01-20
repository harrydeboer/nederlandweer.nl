from django.core.management.base import BaseCommand
import urllib.request
import zipfile
import os
import pathlib
import csv


class Command(BaseCommand):
    help = "Updates the dataset"

    def handle(self, *args, **options):
        stations = []
        with open('data/station.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                stations.append(row)

        for station in stations:
            path_project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            urllib.request.urlretrieve("https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_"
                                       + station[0] + ".zip", 'data/test.zip')
            with zipfile.ZipFile(path_project + '/data/test.zip', 'r') as zip_ref:
                zip_ref.extractall(path_project + '/data')
            pathlib.Path.unlink(path_project + '/data/test.zip')
