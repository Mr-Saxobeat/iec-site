from django.shortcuts import render, get_object_or_404
from djgeojson.views import GeoJSONLayerView
from .models import ElementCategory, ElementSource, Station, Pixel, City
from django.http import HttpResponse, JsonResponse, Http404
import json
import datetime
import requests
from django.core import serializers
from rest_framework import serializers as rest_serializers
from django.core.serializers import serialize as sr
from djqscsv import render_to_csv_response
from vismet.retrieve_functions import GetXavierStationData, GetINMETStationData, GetANAStationData

# Esta view apenas retorna o template pricipal
# da plataforma de dados.
def VisMetView(request):
    return render(request, 'vismet/index.html')

def Api_Stations(request):
    response = Station.objects.all()
    return HttpResponse(response, content_type='application/json')

def Api_Stations_Source(request, format, source):
    station_source = ElementSource.objects.get(name=source)
    stations = Station.objects.filter(source=station_source)

    if format == 'json':
        response = serializers.serialize('json', stations)
        return HttpResponse(response, content_type="application/json")
    elif format == 'csv':
        response = stations.values()
        return render_to_csv_response(response)

def Api_Stations_Data(request, format, source, code, start_day, start_month, start_year, final_day, final_month, final_year):
    try:
        startDate = datetime.date(start_year, start_month, start_day)
        finalDate = datetime.date(final_year, final_month, final_day)
    except ValueError as e:
        print(e)
        raise Http404("Data inserida errada. Verifique os dias e os meses.")

    if source == 'xavier':
        queryset = GetXavierStationData(source, code, startDate, finalDate)
    elif source == 'inmet':
        queryset = GetINMETStationData(source, code, startDate, finalDate)
    elif source == 'ana':
        queryset = GetANAStationData(source, code, startDate, finalDate)

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
    # Esta é a lista final que será retornada como um Json
    categories_list = {}

    categories_queryset = ElementCategory.objects.all()

    for cat in categories_queryset:
        category_dict = {
            "name": cat.name,
            "sources": {}
        }

        sources = ElementSource.objects.filter(category=cat)
        for src in sources:

            # Este dictionary armazena as variáveis que cada
            # fonte de dados disponibiliza.
            src_dict = {}

            variables = src.variables.all()
            if variables is not None:
                for var in variables:
                    # Adiciona uma key ao "src_dict" que é o nome
                    # da variável e relaciona com a unidade de medida.
                    src_dict[var.name] = {
                        'init': var.init,
                        'unit': var.unit,
                        'chartType': var.chartType,
                        'chartColor': var.chartColor
                    }

            dt_model_list = []
            data_models = src.data_model.all()
            if data_models is not None:
                for model in data_models:
                    dt_model_list.append(model.name)

            category_dict["sources"][src.name] = src_dict
            category_dict["sources"][src.name]["models"] = dt_model_list
            category_dict["sources"][src.name]["display_name"] = src.display_name
            # Por fim adiciona o dict com as relações
            # variável - unidade de medida ao "category_dict"
            # relacionando a fonte de dados com as suas variáveis.

        # Por fim adiciona o dict da categoria totalmente construída
        # à lista de categorias de dados.
        categories_list[cat.name] = category_dict

    return JsonResponse(categories_list, safe=False)

# Esta view retorna os pixels do Espírito Santo
# para serem usados como uma layer no mapa.
class Api_Pixel(GeoJSONLayerView):
    model = Pixel
    properties = ['id', 'city', 'state', 'latitude', 'longitude', 'popup_content']


# def Api_Pixel_Data(request, format, pk, start_day, start_month, start_year, final_day, final_month, final_year):
#     startDate = datetime.date(start_year, start_month, start_day)
#     finalDate = datetime.date(final_year, final_month, final_day)
#
#     pixel = Pixel.objects.get(pk=pk)
#     data = pixel.data.filter(date__gte=startDate, date__lte=finalDate)
#
#     queryset = []
#
#     for dt in data:
#         pixel_id = dt.pixel.pk
#         date  = dt.date.strftime("%Y-%m-%d")
#         coords = {
#                     'latitude': dt.pixel.latitude,
#                     'longitude': dt.pixel.longitude
#                  }
#         preciptation = dt.preciptation
#
#         pixel_data_timestamp = {
#             'pixel_id': pixel_id,
#             'date': date,
#             'coords': coords,
#             'preciptation': preciptation
#         }
#
#         queryset.append(pixel_data_timestamp)
#
#     if(format == "json"):
#         return JsonResponse(queryset, safe=False)
#         return response
#
#     elif format == "csv":
#         return render_to_csv_response(data)



# Esta view retorna as cidades do Espírito Santo
# para serem usadas como uma layer no mapa.
class Api_Cities(GeoJSONLayerView):
    model = City
    properties = ('id', 'name')

def Api_Cities_Data(request, format, name, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    city = City.objects.get(name=name)
    queryset = city.city_data.filter(date__gte=startDate, date__lte=finalDate).order_by('date')

    if format == "json":
        queryset_serialized = serializers.serialize('json', queryset)
        response = HttpResponse(queryset_serialized, content_type="application/json")
        return response
    elif format == "csv":
        return render_to_csv_response(queryset)
