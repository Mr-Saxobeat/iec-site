from vismet.models import ElementSource
from vismet.models import Station
from vismet.models import XavierStationData
from django.shortcuts import get_object_or_404

# Esta retorna em os dados das estações Xavier,
# dado o inmet_code e o intervalo de data.
def GetXavierStationData(source, inmet_code, startDate, finalDate):
    delta = finalDate - startDate

    source = ElementSource.objects.get(name=source)
    station = Station.objects.get(source=source, inmet_code=inmet_code)

    try:
        station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
    except ErrName:
        print(ErrName)

    return station_data

# Esta retorna em os dados das estações INMET,
# dado o inmet_code e o intervalo de data.
def GetInmetStationData(code, startDate, finalDate):
    deltaDays = finalDate - startDate
    source = ElementSource.objects.get(name='inmet')
    station = Station.objects.get(source=source, inmet_code=code)

    station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    if station_data.count() < deltaDays.days:
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

        station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
        return station_data
