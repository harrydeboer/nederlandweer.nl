class Station:

    def __init__(self, row: list):
        self.station_id = int(row[0])
        self.name = row[1]
        self.begin_year = int(row[2])
        self.end_year = int(row[3])
        self.begin_year_perc_rain = int(row[4])
        self.begin_year_amount_rain = int(row[5])