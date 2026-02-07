from nederland_weer.models import Station
from typing import Dict


class StationRepository:

    def find_all(self) -> Dict[str, Station]:
        stations = {}
        for station in Station.objects.all():
            stations[station.name] = station

        return stations

    def get(self, station_id: int) -> Station:
        return Station.objects.get(pk=station_id)

    def create(self, station: Station) -> Station:
        station.save()
        return station

    def update(self, station: Station) -> Station:
        station.save()
        return station

    def delete(self, station: Station) -> None:
        station.delete()