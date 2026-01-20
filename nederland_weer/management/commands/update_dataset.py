from django.core.management.base import BaseCommand
import urllib.request
import zipfile
import os
import pathlib


class Command(BaseCommand):
    help = "Updates the dataset"

    def handle(self, *args, **options):
        station_id = 260
        path_project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        urllib.request.urlretrieve("https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_"
                                   + str(station_id) + ".zip", 'data/test.zip')
        with zipfile.ZipFile(path_project + '/data/test.zip', 'r') as zip_ref:
            zip_ref.extractall(path_project + '/data')
        pathlib.Path.unlink(path_project + '/data/test.zip')
