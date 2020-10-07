import os
import requests
import csv
import datetime
from vismet.models import ElementCategory, ElementSource, WeatherStation

# Esse script pega as estações xavier da API do INMET
# e salva no banco de dados.
def loadstations(csv_path=os.path.join(os.getcwd(), 'vismet', 'scripts', 'data', 'inmet', 'inmet-codes.csv')):

    # Pega o objeto "Fonte da estação"
    source, created = ElementSource.objects.get_or_create(
                        name = 'inmet',
                        category = ElementCategory.objects.get(name='observados'),
                        variables = ['temperatura máxima',
                                     'temperatura mínima',
                                     'umidade relativa',
                                     'precipitação'],
                                     )

    # Links da API do INMET para recuperar os dados das estações respectivamente
    # automáticas e manuais.
    automatic_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/T").json()
    manual_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/M").json()

    list_inmet_codes = []

    # Lê os códigos INMET das estações necessárias.
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            list_inmet_codes.append(row[0])
    file.close()

    startDate = None
    finalDate = None
    created_station = None

    # Cria models das estações automáticas
    for station in automatic_stations_response:
        if station["CD_ESTACAO"] in list_inmet_codes:

            startDate = station["DT_INICIO_OPERACAO"]
            finalDate = station["DT_FIM_OPERACAO"]

            if startDate:
                startDate = datetime.datetime.strptime(startDate[:10], "%Y-%m-%d")
            else:
                startDate = None

            if finalDate:
                finalDate = datetime.datetime.strptime(finalDate[:10], "%Y-%m-%d")
            else:
                finalDate = None

            if station["CD_ESTACAO"] in list_inmet_codes:
                created_station = WeatherStation.objects.get_or_create(
                    source = source,
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
            print(created_station)

    # Cria models das estações convecionais
    for station in manual_stations_response:

        startDate = station["DT_INICIO_OPERACAO"]
        finalDate = station["DT_FIM_OPERACAO"]

        if startDate:
            startDate = datetime.datetime.strptime(startDate[:10], "%Y-%m-%d")
        else:
            startDate = None

        if finalDate:
            finalDate = datetime.datetime.strptime(finalDate[:10], "%Y-%m-%d")
        else:
            finalDate = None

        if station["CD_ESTACAO"] in list_inmet_codes:
            created_station = WeatherStation.objects.get_or_create(
                source = source,
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
        print(created_station)

    return print("acabou")

# Esse script compara os códigos inmet usados pelo xavier
# e as estações que foram salvas através da api do inmet
# e escreve no arquivo "missing_stations.txt" as estações
# que não foram encontradas na api inmet.
def verify(csv_inmet_codes=os.path.join(os.getcwd(), 'vismet', 'scripts', 'data', 'inmet','inmet-codes.csv'),
           csv_missing_stations=os.path.join(os.getcwd(), 'vismet', 'scripts', 'data', 'inmet','missing_stations.csv')):

    file_inmet_codes = open(csv_inmet_codes, 'r')
    file_missing_stations = open(csv_missing_stations, 'w')

    inmet_source = ElementSource.objects.get(name='inmet')
    xavier_source = ElementSource.objects.get(name='xavier')

    inmet_station = None
    xavier_station = None
    reader = csv.reader(file_inmet_codes)

    file_missing_stations.write("inmet;omm;cidade;tipo\n")
    for row in reader:
        inmet_code = row[0]

        xavier_station = WeatherStation.objects.get(source=xavier_source, inmet_code=inmet_code)

        try:
            inmet_station = WeatherStation.objects.get(source=inmet_source, inmet_code=inmet_code)
        except WeatherStation.DoesNotExist:
            file_missing_stations.write(str(xavier_station.inmet_code) + ";" + str(xavier_station.omm_code) + ";" + str(xavier_station.city) + ";" + str(xavier_station.type) +"\n")

    file_inmet_codes.close()
    file_missing_stations.close()
