from django.shortcuts import render
from djgeojson.views import GeoJSONLayerView
from .models import XavierStation, XavierStationData, Pixel, PixelData, City, CityData
from django.http import HttpResponse, JsonResponse
import json
import datetime
import requests
from django.core import serializers
from rest_framework import serializers as rest_serializers
from django.core.serializers import serialize as sr
from djqscsv import render_to_csv_response

# Esta view apenas retorna o template pricipal
# da plataforma de dados.
def VisMetView(request):
    return render(request, 'vismet/index.html')

# Esta view retorna as estações meteorógicas Xavier.
class Api_XavierStations(GeoJSONLayerView):
    model = XavierStation
    properties = ('popup_content', 'station_id', 'name', 'state', 'omm_code', 'latitude', 'longitude')

# Esta retorna em os dados das estações Xavier,
# dado o omm_code e o intervalo.
def Api_XavierStations_Data(request, format, omm_code, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    station = XavierStation.objects.get(omm_code=omm_code)

    station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    if(format == "json"):
        data_serialized = serializers.serialize('json', station_data)
        response = HttpResponse(data_serialized, content_type="applications/json")
        return response

    elif format == "csv":
        qs_csv = station_data.values('date', 'station_id', 'evapo', 'relHum', 'solarRad', 'maxTemp', 'minTemp', 'windSpeed')
        return render_to_csv_response(qs_csv)




# Esta view retorna os pixels do Espírito Santo
# para serem usados como uma layer no mapa.
class Api_Pixel(GeoJSONLayerView):
    model = Pixel
    properties = ['boundings']


def Api_Pixel_Data(request, pk, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    pixel = Pixel.objects.get(pk=pk)
    data = pixel.data.filter(date__gte=startDate, date__lte=finalDate)

    queryset = []

    for dt in data:
        pixel_id = dt.pixel.pk
        date  = dt.date.strftime("%Y-%m-%d")
        coords = {
                    'latitude': dt.pixel.latitude,
                    'longitude': dt.pixel.longitude
                 }
        preciptation = dt.preciptation

        pixel_data_timestamp = {
            'pixel_id': pixel_id,
            'date': date,
            'coords': coords,
            'preciptation': preciptation
        }

        queryset.append(pixel_data_timestamp)

    return JsonResponse(queryset, safe=False)

# Esta view retorna as cidades do Espírito Santo
# para serem usadas como uma layer no mapa.
class Api_Cities(GeoJSONLayerView):
    model = City
    properties = ('nome', 'geom')

def Api_Cities_Data(request, name, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    city = City.objects.get(nome=name)
    data = city.city_data.filter(date__gte=startDate, date__lte=finalDate)

    queryset = []

    for dt in data:
        city = dt.city.nome
        date  = dt.date.strftime("%Y-%m-%d")
        preciptation = dt.preciptation
        medTemp = dt.medTemp

        city_timestamp = {
            'city': city,
            'date': date,
            'preciptation': preciptation,
            'medTemp': medTemp
        }

        queryset.append(city_timestamp)

    response = queryset

    return JsonResponse(response, safe=False)

def pega_capitais(request):
    return render(request, 'vismet/api_inmet.html')

def Api_Inmet_Capitais(request, date):
    url = "https://apitempo.inmet.gov.br/condicao/capitais/"
