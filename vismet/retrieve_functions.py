from vismet.models import ElementSource
from vismet.models import Station, XavierStationData, INMETStationData, ANAStationData
from django.shortcuts import get_object_or_404
import requests
import xml.etree.ElementTree as ET
import re
import datetime

# Esta retorna em os dados das estações Xavier,
# dado o inmet_code e o intervalo de data.
def GetXavierStationData(source, inmet_code, startDate, finalDate):
    delta = finalDate - startDate
    source = ElementSource.objects.get(name=source)
    station = Station.objects.get(source=source, inmet_code=inmet_code)

    try:
        station_data = station.xavier_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
    except ErrName:
        print(ErrName)

    return station_data

# Esta retorna em os dados das estações INMET,
# dado o inmet_code e o intervalo de data.
def GetINMETStationData(source, code, startDate, finalDate):
    delta = finalDate - startDate
    source = ElementSource.objects.get(name=source)
    station = Station.objects.get(source=source, inmet_code=code)

    station_data = station.inmet_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    if station_data.count() < delta.days:
        station_data = requests.get('https://apitempo.inmet.gov.br/estacao/diaria/' +
                                    startDate.strftime("%Y-%m-%d") + '/' +
                                    finalDate.strftime("%Y-%m-%d") + '/' +
                                    station.inmet_code)

        for oneDay in station_data.json():
            INMETStationData.objects.get_or_create(
                date = datetime.datetime.strptime(oneDay["DT_MEDICAO"], "%Y-%m-%d"),
                station = station,
                defaults = {
                    'maxTemp': oneDay["TEMP_MAX"],
                    'minTemp': oneDay["TEMP_MIN"],
                    'relHum': oneDay["UMID_MED"],
                    'precip': oneDay["CHUVA"],
                }
            )

        station_data = station.inmet_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
    return station_data

def GetANAStationData(source, code, startDate, finalDate):
    delta = finalDate - startDate
    source = ElementSource.objects.get(name=source)
    station = Station.objects.get(source=source, omm_code=code)

    station_data = station.ana_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    if station_data.count() < delta.days:
        # Verificar o tipo da estação
        tipoDados = 2
        if station.type.upper() == 'PLUVIOMÉTRICA':
            tipoDados = 2
            regex_value = re.compile("Chuva..$")
        elif station.type.upper() == 'FLUVIOMÉTRICA':
            tipoDados = 3
            regex_value = re.compile("Vazao..$")

        url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica'
        nivelConsistencia = 2

        params = {
            'codEstacao': str(code),
            'dataInicio': startDate.strftime("%d/%m/%Y"),
            'dataFim': finalDate.strftime("%d/%m/%Y"),
            'tipoDados': str(tipoDados),
            'nivelConsistencia': str(nivelConsistencia),
            }

        response = requests.get(url, params=params)
        xml = ET.fromstring(response.text)
        data = xml[1][0][0]
        regex_date = re.compile("DataHora")

        for month in xml[1][0]:
            date = None
            for child in month:
                if re.match(regex_date, child.tag):
                    date = datetime.datetime.strptime(child.text[:10], "%Y-%m-%d")

                if re.match(regex_value, child.tag) and date:
                    day = child.tag[5:]
                    try:
                        date = datetime.date(date.year, date.month, int(day))

                    except ValueError:
                        continue

                    try:
                        station_data = ANAStationData.objects.get(date=date, station=station)
                        continue
                    except ANAStationData.DoesNotExist:
                        if child.text:
                            try:
                                ANAStationData.objects.get_or_create(
                                    date = date,
                                    station = station,
                                    defaults = {
                                    'value': float(child.text)
                                    }
                                )
                            except TypeError:
                                continue

                elif child.tag == "DataHora":
                    response_startDate = datetime.datetime.strptime(child.text[:10], "%Y-%m-%d")


        station_data = station.ana_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    return station_data
