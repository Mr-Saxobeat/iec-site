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
def Api_XavierStations_Data(request, omm_code, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    station = XavierStation.objects.get(omm_code=omm_code)

    station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
    data_serialized = serializers.serialize('json', station_data)

    response = HttpResponse(data_serialized, content_type="applications/json")

    return response


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

    for data in data:
        pixel_id = data.pixel.pk
        date  = data.date.strftime("%Y-%m-%d")
        coords = {
                    'latitude': data.pixel.latitude,
                    'longitude': data.pixel.longitude
                 }
        preciptation = data.preciptation

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
    data = City.city_data.filter(date__gte=startDate, date__lte=finalDate)

    response = data

    return JsonResponse(response)


# Esta view faz as requisições para o banco de dados
# das estações meteorológicas Xavier.
def ajaxrequest(request):
    omm_code = request.GET.get('omm_code')
    startDate = request.GET.get('startDate')
    finalDate = request.GET.get('finalDate')

    # Create the correct start date object to execute the filter
    startDay = startDate[:2]
    startMonth = startDate[3:5]
    startYear = startDate[6:10]
    sDate = datetime.date(int(startYear), int(startMonth), int(startDay))

    # Create the correct end date object to execute the filter
    finalDay = finalDate[:2]
    finalMonth = finalDate[3:5]
    finalYear = finalDate[6:10]
    eDate = datetime.date(int(finalYear), int(finalMonth), int(finalDay))

    # Get the station object
    station = XavierStation.objects.get(omm_code=omm_code)

    # Get the the data objects between the specified dates
    station_timestamp = station.data.filter(date__gte=sDate, date__lte=eDate).order_by('date')
    myData = serializers.serialize('json', station_timestamp)

    return HttpResponse(myData, content_type="application/json")
    # return JsonResponse(myData, safe=False)
