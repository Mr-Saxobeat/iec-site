from django.shortcuts import render, get_object_or_404
from djgeojson.views import GeoJSONLayerView
from .models import XavierStation, XavierStationData
from .models import INMETStationData
from .models import Pixel, PixelData
from .models import City, CityData
from .models import ElementCategory, ElementSource, WeatherStation
from django.http import HttpResponse, JsonResponse, Http404
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

def Api_WeatherStations(request):
    weather_stations = WeatherStation.objects.all()

    if format == 'json':
        response = serializers.serialize('json', weather_stations)
        return HttpResponse(response, content_type='application/json')
    elif format == 'csv':
        response = weather_stations.values()
        return render_to_csv_response(response)


def Api_WeatherStations_Source(request, format, source):
    station_source = ElementSource.objects.get(name=source)

    weather_stations = WeatherStation.objects.filter(source=station_source)

    if format == 'json':
        response = serializers.serialize('json', weather_stations)
        return HttpResponse(response, content_type="application/json")
    elif format == 'csv':
        response = weather_stations.values()
        return render_to_csv_response(response)

def Api_WeatherStations_Data(request, format, source, code, start_day, start_month, start_year, final_day, final_month, final_year):
    try:
        startDate = datetime.date(start_year, start_month, start_day)
        finalDate = datetime.date(final_year, final_month, final_day)
    except ValueError as e:
        print(e)
        raise Http404("Data inserida errada. Verifique os dias e os meses.")

    if format == 'inmet':
        queryset = GetInmetStations(code, startDate, finalDate)

    if(format == 'json'):
        queryset_serialized = serializers.serialize('json', queryset)
        response = HttpResponse(queryset_serialized, content_type="application/json")
        return response

    elif format == 'csv':
        qs_csv = queryset.values()
        return render_to_csv_response(qs_csv)

# Esta view retorna um json com as opções de categorias, fontes e variáveis
# para ser usado na construção dos menus de seleção da plataforma.
def Api_Data_Options(request):
    categories_list = []

    categories = ElementCategory.objects.all()

    for aCategory in categories:
        category_sources = ElementSource.objects.filter(category=aCategory)

        category_dict = {
            "category": aCategory.name,
            "sources": []
        }

        for aSource in category_sources:
            source_dict = {
                "name": aSource.name,
                "variables": aSource.variables,
            }

            category_dict["sources"].append(source_dict)

        categories_list.append(category_dict)

    return JsonResponse(categories_list, safe=False)

# Esta retorna em os dados das estações Xavier,
# dado o omm_code e o intervalo.
def Api_XavierStations_Data(request, format, inmet_code, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)
    delta = finalDate - startDate

    station = get_object_or_404(XavierStation, inmet_code=inmet_code)

    try:
        station_data = station.data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')
    except ErrName:
        print(ErrName)

    if(format == "json"):
        data_serialized = serializers.serialize('json', station_data)
        response = HttpResponse(data_serialized, content_type="application/json")
        return response

    elif format == "csv":
        qs_csv = station_data.values('date', 'evapo', 'relHum', 'solarIns', 'maxTemp', 'minTemp', 'windSpeed')
        return render_to_csv_response(qs_csv)

def Api_INMETStations(request):
    inmet_stations = INMETStation.objects.all()

    fields = ('city',
    'state',
    'inmet_code',
    'latitude',
    'longitude',
    'startDate',
    'status',
    'popup_content',
    )
    serialized = serializers.serialize('json', inmet_stations, fields=fields)


    return HttpResponse(serialized, content_type="application/json")


def GetInmetStations(code, startDate, finalDate):
    deltaDays = finalDate - startDate
    source = ElementSource.objects.get(name='inmet')
    station = WeatherStation.objects.get(source=source, inmet_code=code)

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

    if(format == "json"):
        data_serialized = serializers.serialize('json', station_data)
        response = HttpResponse(data_serialized, content_type="application/json")
        return response

    elif format == "csv":
        qs_csv = station_data.values('date', 'relHum', 'maxTemp', 'minTemp', 'precip')
        return render_to_csv_response(qs_csv)



# Esta view retorna os pixels do Espírito Santo
# para serem usados como uma layer no mapa.
class Api_Pixel(GeoJSONLayerView):
    model = Pixel
    properties = ['latitude', 'longitude', 'boundings']


def Api_Pixel_Data(request, format, pk, start_day, start_month, start_year, final_day, final_month, final_year):
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

    if(format == "json"):
        return JsonResponse(queryset, safe=False)
        return response

    elif format == "csv":
        return render_to_csv_response(data)



# Esta view retorna as cidades do Espírito Santo
# para serem usadas como uma layer no mapa.
class Api_Cities(GeoJSONLayerView):
    model = City
    properties = ('nome', 'geom')

def Api_Cities_Data(request, format, name, start_day, start_month, start_year, final_day, final_month, final_year):
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

    if format == "json":
        return JsonResponse(response, safe=False)
    elif format == "csv":
        return render_to_csv_response(data)
