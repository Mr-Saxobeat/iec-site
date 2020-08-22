from django.shortcuts import render
from djgeojson.views import GeoJSONLayerView
from .models import XavierStation, XavierStationData, HeatPixel, HeatPixelData, City
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
class XavierStationWeatherGeoJson(GeoJSONLayerView):
    model = XavierStation
    properties = ('popup_content', 'stationId', 'name', 'state', 'omm_code', 'latitude', 'longitude')

# Esta view retorna as cidades do Espírito Santo
# para serem usadas como uma layer no mapa.
class CityGeoJson(GeoJSONLayerView):
    model = City
    properties = ('nome', 'geom')

# Esta view faz as requisições para o banco de dados
# das estações meteorológicas Xavier.
def ajaxrequest(request):
    stationId = request.GET.get('stationId')
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
    station = XavierStation.objects.get(station_id=stationId)

    # Get the the data objects between the specified dates
    station_timestamp = station.data.filter(date__gte=sDate, date__lte=eDate).order_by('date')
    myData = serializers.serialize('json', station_timestamp)

    return HttpResponse(myData, content_type="application/json")
    # return JsonResponse(myData, safe=False)

# Esta view é um teste para criar uma API mais correta
# das estações Xavier.
def ApiXavier(request, variable, station_id, start_day, start_month, start_year, final_day, final_month, final_year):
    sDate = datetime.date(start_year, start_month, start_day)
    eDate = datetime.date(final_year, final_month, final_day)

    station = XavierStation.objects.get(station_id=station_id)

    station_timestamp = station.data.filter(date__gte=sDate, date__lte=eDate).order_by('date')
    myData = serializers.serialize('json', station_timestamp)

    response = HttpResponse(myData, content_type="applications/json")
    # response = JsonResponse(myData, safe=False)
    # response['Content-Disposition'] = "attachment; filename=%s" %'time_series.json'
    return response

# Esta view retorna os dados dos pixels do mapa.
def HeatPixelDataView(request):
    startDate = datetime.date(1960, 1, 1)
    finalDate = datetime.date(1960, 12, 31)
    heat_pixels_data = HeatPixelData.objects.filter(date=startDate)

    queryset = []

    for heat_pixel_data in heat_pixels_data:
        pixel_id = heat_pixel_data.pixel.pixel_id
        coords = [heat_pixel_data.pixel.longitude, heat_pixel_data.pixel.latitude]
        preciptation = heat_pixel_data.preciptation

        pixel_data = {
            'pixel_id': pixel_id,
            'coords': coords,
            'preciptation': preciptation
        }

        queryset.append(pixel_data)

    return JsonResponse(queryset, safe=False)

def HeatPixelData2View(request, lat, lng, start_day, start_month, start_year, final_day, final_month, final_year):
    sDate = datetime.date(start_year, start_month, start_day)
    eDate = datetime.date(final_year, final_month, final_day)

    pixel = HeatPixel.objects.filter(latitude=lat, longitude=lng)
    data = pixel.data.filter(date__lte=sData, date__gte=eDate)

    queryset = []

    for heat_pixel_data in data:
        pixel_id = heat_pixel_data.pixel.pixel_id
        coords = [heat_pixel_data.pixel.longitude, heat_pixel_data.pixel.latitude]
        preciptation = heat_pixel_data.preciptation

        pixel_data = {
            'pixel_id': pixel_id,
            'coords': coords,
            'preciptation': preciptation
        }

        queryset.append(pixel_data)


    return JsonResponse(queryset, safe=False)


# Esta view retorna os pixels do Espírito Santo
# para serem usados como uma layer no mapa.
class HeatPixelGeoJson(GeoJSONLayerView):
    model = HeatPixel
    properties = ['boundings']
