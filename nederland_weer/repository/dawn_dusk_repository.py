import csv
from nederland_weer.model.dawn_dusk import DawnDusk
from typing import List


class DawnDuskRepository:

    def find_all(self) -> List[DawnDusk]:
        dawn_dusks = []
        with open('data/dawn_dusk.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for index, row in enumerate(reader):
                dawn = int(row[1][-2:]) / 60 + int(row[1][:-2])
                sunset = int(row[2][-2:]) / 60 + int(row[2][:-2])
                dawn_dusks.append(DawnDusk(int(row[0]), dawn, sunset))
        return dawn_dusks
