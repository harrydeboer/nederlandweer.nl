from nederland_weer.models import Station
from typing import Dict


class StationRepository:

    def find_all(self) -> Dict[str, Station]:
        stations = {}
        for station in Station.objects.all():
            stations[station.name] = station

        return stations

    def write(self, stations: Dict[str, Station]):
        for index, station in stations.items():
            station.save()