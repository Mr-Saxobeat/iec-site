from .models import StationData
import datetime
import os
import csv

def load_csv(verbose=True):
    cont = 1
    csv_path = os.path.join(os.getcwd(), 'data', 'janeiro-1980-estacao-1.csv')
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            str_date = row[0]
            str_day = str_date[:2]
            str_month = str_date[3:5]
            str_year = str_date[6:10]
            date = datetime.date(int(str_year), int(str_month), int(str_day))

            created = StationMaxTemp.objects.get_or_create(
                date = date,
                station_id = int(row[1]),
                evapo = float(row[2]),
                relHum = float(row[3]),
                solarRad = float(row[4]),
                maxTemp = float(row[5]),
                minTemp = float(row[6]),
                windSpeed = float(row[7]),
            )
            print(cont)
            cont = cont + 1
    print('CABOUPORRA')

def a1():
    csv_path = os.path.join(os.getcwd(), 'pwiec', 'stations','soco.csv')
    file = open(csv_path, 'r')
    r = csv.reader(file)

    for row in r:
        for d in row:
            if len(d) > 5:
                print(d[:5])
            else:
                print(d)
