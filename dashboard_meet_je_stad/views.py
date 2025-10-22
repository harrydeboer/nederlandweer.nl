from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
import os
import csv
import json


def index(request: WSGIRequest) -> HttpResponse:
    sensors = []
    longitudes_sensor = []
    latitudes_sensor = []
    pm_ids = []
    pm = request.GET.get('pm')
    temperatures = []
    temperature_dates = []
    humidities = []
    humidity_dates = []
    pm25 = []
    pm25_dates = []
    pm10 = []
    pm10_dates = []

    if pm == 'on':
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/utrecht_ids.csv') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if row[5] != '0':
                   pm_ids.append(row[0])

    with open(os.path.dirname(os.path.abspath(__file__)) + '/out.csv') as csvfile:
        reader = csv.reader(csvfile)
        id_sensor = 0
        longitudes = []
        latitudes = []

        for row in reader:
            if pm == 'on' and row[1] not in pm_ids:
                continue
            if id_sensor == int(row[1]):
                if row[3] != '':
                    longitudes.append(float(row[3]))
                if row[4] != '':
                    latitudes.append(float(row[4]))
                if row[2] != '':
                    temperatures.pop()
                    if row[2] != '':
                        temperatures.append(float(row[2]))
                    else:
                        temperatures.append(0)
                    temperature_dates.pop()
                    temperature_dates.append(row[0])
                if row[5] != '':
                    humidities.pop()
                    if row[5] != '':
                        humidities.append(float(row[5]))
                    else:
                        humidities.append(0)
                    humidity_dates.pop()
                    humidity_dates.append(row[0])
                if row[9] != '':
                    pm25.pop()
                    if row[9] != '':
                        pm25.append(float(row[9]))
                    else:
                        pm25.append(0)
                    pm25_dates.pop()
                    pm25_dates.append(row[0])
                if row[10] != '':
                    pm10.pop()
                    if row[10] != '':
                        pm10.append(float(row[10]))
                    else:
                        pm10.append(0)
                    pm10_dates.pop()
                    pm10_dates.append(row[0])
            else:
                if id_sensor != 0:
                    if longitudes != [] and latitudes != []:
                        longitudes_sensor.append(sum(longitudes) / len(longitudes))
                        latitudes_sensor.append(sum(latitudes) / len(latitudes))
                    else:
                        longitudes_sensor.append(0)
                        latitudes_sensor.append(0)
                sensors.append(int(row[1]))
                id_sensor = int(row[1])
                if row[2] != '':
                    temperatures.append(float(row[2]))
                else:
                    temperatures.append(0)
                temperature_dates.append(row[0])
                if row[5] != '':
                    humidities.append(float(row[5]))
                else:
                    humidities.append(0)
                humidity_dates.append(row[0])
                if row[9] != '':
                    pm25.append(float(row[9]))
                else:
                    pm25.append(0)
                pm25_dates.append(row[0])
                if row[10] != '':
                    pm10.append(float(row[10]))
                else:
                    pm10.append(0)
                pm10_dates.append(row[0])
                if row[3] != '':
                    longitudes = [float(row[3])]
                else:
                    longitudes = []
                if row[4] != '':
                    latitudes = [float(row[4])]
                else:
                    latitudes = []
        if longitudes != [] and latitudes != []:
            longitudes_sensor.append(sum(longitudes) / len(longitudes))
            latitudes_sensor.append(sum(latitudes) / len(latitudes))
        else:
            longitudes_sensor.append(0)
            latitudes_sensor.append(0)

    return render(request, 'homepage/index.html',
                  {'sensors': sensors, 'pm': pm,
                   'longitudes': longitudes_sensor, 'latitudes': latitudes_sensor,
                   'temperatures': temperatures, 'temperature_dates': json.dumps(temperature_dates),
                   'humidities': humidities, 'humidity_dates': json.dumps(humidity_dates),
                   'pm25': pm25, 'pm25_dates': json.dumps(pm25_dates),
                   'pm10': pm10, 'pm10_dates': json.dumps(pm10_dates)})
