from .models import StationData, XavierStation
import datetime
import os
import csv

## ESTE SCRIPT PRECISA SER REESCRITO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def load_csv(verbose=True):
    cont = 1
    csv_path = '/home/weiglas/Documents/iec/Xavier_TempMax_1980-2017.csv'
    # csv_path = os.path.join(os.getcwd(), 'data', 'estacao-1-1980.csv')
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

            if row[2] == "NaN":
                evapo = "-9999"
            else:
                evapo = row[2]
            if row[3] == "NaN":
                relHum = "-9999"
            else:
                relHum = row[3]
            if row[4] == "NaN":
                solarRad = "-9999"
            else:
                solarRad = row[4]
            if row[5] == "NaN":
                maxTemp = "-9999"
            else:
                maxTemp = row[5]
            if row[6] == "NaN":
                minTemp = "-9999"
            else:
                minTemp = row[6]
            if row[7] == "NaN":
                windSpeed = "-9999"
            else:
                windSpeed = row[7]

            created = StationData.objects.get_or_create(
                date = date,
                station = XavierStation.objects.get(station=row[1]), ## AQUI TÁ ERRADO NÃO EXITE MAIS O CAMPO STATION_ID
                evapo = float(evapo),
                relHum = float(relHum),
                solarRad = float(solarRad),
                maxTemp = float(maxTemp),
                minTemp = float(minTemp),
                windSpeed = float(windSpeed),
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
