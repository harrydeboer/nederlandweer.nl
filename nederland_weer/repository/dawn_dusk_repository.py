import csv
from nederland_weer.model.dawn_dusk import DawnDusk
from typing import List


class DawnDuskRepository:

    def find_all(self) -> List[DawnDusk]:
        dawn_dusks = []
        with open('data/dawn_dusk.csv', newline='') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                dawn = int(row[1][-2:]) / 60 + int(row[1][:-2])
                sunset = int(row[2][-2:]) / 60 + int(row[2][:-2])
                if row[0] == 'ï»¿1':
                    row[0] = '1'
                dawn_dusks.append(DawnDusk(int(row[0]), dawn, sunset))
        return dawn_dusks
