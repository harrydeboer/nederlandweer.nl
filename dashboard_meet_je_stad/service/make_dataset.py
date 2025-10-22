import os
import csv


sensors = []
with open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/utrecht_ids.csv') as csvfile:
    reader = csv.reader(csvfile)
    for index_sensor, row in enumerate(reader):
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) +
                  '/ids/' + row[0] + '/out.csv') as output_file:
            reader = csv.reader(output_file)
            for row_output in enumerate(reader):
                sensors.append(row_output[1])