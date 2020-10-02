import os
import requests
import csv
from vismet.models import INMETStation, XavierStation
import datetime

# Esse script pega as estações xavier da API do INMET
# e salva no banco de dados.
def run():

    automatic_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/T").json()
    manual_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/M").json()

    csv_path = os.path.join(os.getcwd(), 'vismet', 'scripts', 'inmet-codes.csv')

    list_inmet_codes = []

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            list_inmet_codes.append(row[0])


    startDate = None
    finalDate = None
    st = None

    for station in automatic_stations_response:
        if station["CD_ESTACAO"] in list_inmet_codes:

            startDate = station["DT_INICIO_OPERACAO"]
            finalDate = station["DT_FIM_OPERACAO"]

            if startDate:
                startDate = datetime.datetime.strptime(startDate[:10], "%Y-%m-%d")
            else:
                # startDate = datetime.timedelta(0)
                startDate = None

            if finalDate:
                finalDate = datetime.datetime.strptime(finalDate[:10], "%Y-%m-%d")
            else:
                # finalDate = datetime.timedelta(0)
                finalDate = None

            if station["CD_ESTACAO"] in list_inmet_codes:
                st = INMETStation.objects.get_or_create(
                    inmet_code = station["CD_ESTACAO"],
                    state = station["SG_ESTADO"],
                    city = station["DC_NOME"],
                    type = station["TP_ESTACAO"],
                    latitude = station["VL_LATITUDE"],
                    longitude = station["VL_LONGITUDE"],
                    altitude = station["VL_ALTITUDE"],
                    startDate = startDate,
                    finalDate = finalDate,
                    status = station["CD_SITUACAO"],
                )
            print(st)

    for station in manual_stations_response:

        startDate = station["DT_INICIO_OPERACAO"]
        finalDate = station["DT_FIM_OPERACAO"]

        if startDate:
            startDate = datetime.datetime.strptime(startDate[:10], "%Y-%m-%d")
        else:
            # startDate = datetime.timedelta(0)
            startDate = None

        if finalDate:
            finalDate = datetime.datetime.strptime(finalDate[:10], "%Y-%m-%d")
        else:
            # finalDate = datetime.timedelta(0)
            finalDate = None

        if station["CD_ESTACAO"] in list_inmet_codes:
            INMETStation.objects.get_or_create(
                inmet_code = station["CD_ESTACAO"],
                state = station["SG_ESTADO"],
                city = station["DC_NOME"],
                type = station["TP_ESTACAO"],
                latitude = station["VL_LATITUDE"],
                longitude = station["VL_LONGITUDE"],
                altitude = station["VL_ALTITUDE"],
                startDate = startDate,
                finalDate = finalDate,
                status = station["CD_SITUACAO"],
            )
        print(st)

    file.close()
    return print("acabou")

# Esse script compara os códigos inmet usados pelo xavier
# e as estações que foram salvas através da api do inmet
# e escreve no arquivo "missing_stations.txt" as estações
# que não foram encontradas na api inmet.
def verify():
    file_inmet_codes = open(os.path.join(os.getcwd(), 'vismet', 'scripts', 'inmet-codes.csv'), 'r')
    file_missing_stations = open(os.path.join(os.getcwd(), 'vismet', 'scripts', 'missing_stations.csv'), 'w')

    inmet_station = None
    xavier_station = None
    reader = csv.reader(file_inmet_codes)

    file_missing_stations.write("inmet;omm;cidade;tipo\n")
    for row in reader:
        inmet_code = row[0]

        xavier_station = XavierStation.objects.get(inmet_code=inmet_code)

        try:
            inmet_station = INMETStation.objects.get(inmet_code=inmet_code)
        except INMETStation.DoesNotExist:
            file_missing_stations.write(str(xavier_station.inmet_code) + ";" + str(xavier_station.omm_code) + ";" + str(xavier_station.name) + ";" + str(xavier_station.type) +"\n")

    file_inmet_codes.close()
    file_missing_stations.close()
