import os
import csv
import datetime
from vismet.models import ElementCategory, ElementSource, Station
from django.contrib.gis.geos import Point, LinearRing, Polygon
import requests

# Esse script pega as estações xavier da API do INMET
# e salva no banco de dados.
def LoadINMETStations(csv_path=os.path.join(os.getcwd(), 'vismet', 'scripts', 'data', 'inmet', 'inmet-codes.csv')):

    # Pega o objeto "Fonte da estação"
    source, created = ElementSource.objects.get_or_create(
                        name = 'inmet',
                        category = ElementCategory.objects.get(name='observados'),
                        )

    # Links da API do INMET para recuperar os dados das estações respectivamente
    # automáticas e manuais.
    automatic_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/T").json()
    manual_stations_response = requests.get("https://apitempo.inmet.gov.br/estacoes/M").json()

    # list_inmet_codes = []

    # # Lê os códigos INMET das estações necessárias.
    # with open(csv_path, 'r') as file:
    #     reader = csv.reader(file)
    #
    #     for row in reader:
    #         list_inmet_codes.append(row[0])
    # file.close()

    startDate = None
    finalDate = None
    created_station = None

    minLat = -22.0
    minLon = -44.0
    maxLat = -16.0
    maxLon = -39.0

    pt1 = (minLon, minLat)
    pt2 = (minLon, maxLat)
    pt3 = (maxLon, maxLat)
    pt4 = (maxLon, minLat)

    polygon_es = Polygon(LinearRing(pt1, pt2, pt3, pt4, pt1))

    for station in automatic_stations_response:
        station_lat = float(station["VL_LATITUDE"])
        station_lon = float(station["VL_LONGITUDE"])

        if(station["CD_ESTACAO"] == "A612"):
            print(str(station_lat) + " >= -20.0  = " + str(station_lat >= minLat))
            print(str(station_lon) + " >= -43.0  = " + str(station_lat >= minLon))
            print(str(station_lat) + " <= -15.0  = " + str(station_lat <= maxLat))
            print(str(station_lat) + " <= -38.0  = " + str(station_lat >= maxLon))

        if (station_lat >= minLat and station_lon >= minLon and
            station_lat <= maxLat and station_lon <= maxLon):

            print(str(station_lat) + " -- " + str(station_lon))
    # # Cria models das estações automáticas
    # for station in automatic_stations_response:
    #     if station["CD_ESTACAO"] in list_inmet_codes:
            station_point = Point(station_lon, station_lat, None, 4326)
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

            # if station["CD_ESTACAO"] in list_inmet_codes:

            newObj, created = Station.objects.get_or_create(
                source = source,
                inmet_code = station["CD_ESTACAO"],
                state = station["SG_ESTADO"],
                city = station["DC_NOME"],
                type = station["TP_ESTACAO"],
                altitude = station["VL_ALTITUDE"],
                startDate = startDate,
                finalDate = finalDate,
                status = station["CD_SITUACAO"],
                geom = station_point,
            )

            if created:
                print(newObj)

    # Cria models das estações convecionais
    for station in manual_stations_response:
        station_lat = float(station["VL_LATITUDE"])
        station_lon = float(station["VL_LONGITUDE"])

        if (station_lat >= minLat and station_lon >= minLon and
            station_lat <= maxLat and station_lon <= maxLon):

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

            # if station["CD_ESTACAO"] in list_inmet_codes:
            station_point = Point(station_lon, station_lat, None, 4326)
            newObj, created = Station.objects.get_or_create(
                source = source,
                inmet_code = station["CD_ESTACAO"],
                state = station["SG_ESTADO"],
                city = station["DC_NOME"],
                type = station["TP_ESTACAO"],
                altitude = station["VL_ALTITUDE"],
                startDate = startDate,
                finalDate = finalDate,
                status = station["CD_SITUACAO"],
                geom = station_point,
            )

            if created:
                print(newObj)

    return print("Estações INMET foram carregadas.")

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

        xavier_station = Station.objects.get(source=xavier_source, inmet_code=inmet_code)

        try:
            inmet_station = Station.objects.get(source=inmet_source, inmet_code=inmet_code)
        except Station.DoesNotExist:
            file_missing_stations.write(str(xavier_station.inmet_code) + ";" + str(xavier_station.omm_code) + ";" + str(xavier_station.city) + ";" + str(xavier_station.type) +"\n")

    file_inmet_codes.close()
    file_missing_stations.close()
