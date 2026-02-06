from nederland_weer.models import Station
from typing import Dict


class StationRepository:

    def find_all(self) -> Dict[str, Station]:
        stations = {}
        for station in Station.objects.all():
            stations[station.name] = station

        return stations

    def create(self, params: Dict) -> Station:
        station = Station()
        station.id = params['id']
        station.name = params['name']
        station.begin_year = params['begin_year']
        station.end_year = params['end_year']
        station.begin_year_perc_rain = params['begin_year_perc_rain']
        station.begin_year_amount_rain = params['begin_year_amount_rain']
        station.save()
        return station

    def write(self, stations: Dict[str, Station]):
        for index, station in stations.items():
            station.save()