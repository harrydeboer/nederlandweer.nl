import csv
from nederland_weer.model.station import Station
from typing import Dict


class StationRepository:

    def find_all(self) -> Dict[str, Station]:
        stations = {}
        with open('data/station.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                stations[row[1]] = Station(row)
        return stations

    def write(self, path_project: str, stations: list):
        file = open(path_project + "/data/station.csv", "w", newline='')
        csv.writer(file).writerows(stations)
        file.close()