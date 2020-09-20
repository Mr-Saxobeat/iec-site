from vismet.models import XavierStation, XavierStationData
from datetime import datetime
import os
import csv

def run():
    csv_path = "/home/weiglas/Documents/iec/Xavier_TempMax_1980-2017.csv"
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        dates  = []
        finish = -999
        station_id = "0"

        for i, row in enumerate(reader):
            for j, value in enumerate(row):

                if i == 0 and j != 0:
                    dt = datetime.strptime(value, '%d/%m/%Y')
                    dates.append(dt)

                    if dt.year > 1980:
                        finish = j
                        break

                elif i > 0:
                    if j == 0:
                        station_id = value
                    else:
                        station_data = XavierStationData.objects.get_or_create(
                            date = dates[j - 1],
                            station = XavierStation.objects.get(inmet_code=station_id),
                            maxTemp = value
                        )

                        print(station_data)

                if station_id != "0":
                    print(station_id)

                if j == finish:
                    break

        file.close()
        print("acabou")
