from django.shortcuts import render, get_object_or_404
from djgeojson.views import GeoJSONLayerView
from .models import ElementCategory, ElementSource, Station, Pixel, PixelData, City, DataModel
from django.http import HttpResponse, JsonResponse, Http404
import json
import datetime
import requests
from django.core import serializers
from rest_framework import serializers as rest_serializers
from django.core.serializers import serialize as sr
from djqscsv import render_to_csv_response
from vismet.retrieve_functions import GetXavierStationData, GetINMETStationData, GetANAStationData
from django.db.models import Q

# Esta view apenas retorna o template pricipal
# da plataforma de dados.
def VisMetView(request):
    value = request.POST.get('selected_source')
    return render(request, 'vismet/index.html', {'selected_source': value})

def Api_Stations(request):
    response = Station.objects.all()
    return HttpResponse(response, content_type='application/json')

class Api_Stations_Source(GeoJSONLayerView):
    def get_queryset(self):
        station_source = ElementSource.objects.get(name=self.kwargs['source'])
        if self.kwargs['type'] == '0':
            stations = Station.objects.filter(source=station_source)
        else:
            stations = Station.objects.filter(source=station_source, type=self.kwargs['type'])

        return stations

    properties = [
                    'id',
                    'source',
                    'omm_code',
                    'inmet_code',
                    'state',
                    'city',
                    'type',
                    'latitude',
                    'longitude',
                    'altitude',
                    'startDate',
                    'finalDate',
                    'status',
                    'popup_content',
                ]

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

        sources = ElementSource.objects.filter(category=cat).exclude(name__in=['eta por cidade', 'xavier'])
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


def Api_Pixel_Data(request, format, pk, data_model, start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, start_day)
    finalDate = datetime.date(final_year, final_month, final_day)

    try:
        pixel = Pixel.objects.get(pk=pk)
        data = pixel.pixel_data.filter(Q(data_model__name='Histórico, 5Km') | Q(data_model__name=data_model), date__gte=startDate, date__lte=finalDate).order_by('date')
    except Pixel.DoesNotExist:
        return JsonResponse({'mensagem': 'Pixel não encontrado.'}, status=404)
    except PixelData.DoesNotExist:
        return JsonResponse({'mensagem': 'PixelData não encontrado.'}, status=404)

    if(format == 'json'):
        queryset_serialized = serializers.serialize('json', data)
        response = HttpResponse(queryset_serialized, content_type="application/json")
        return response
    elif format == 'csv':
        qs_csv = data.values()
        return render_to_csv_response(qs_csv)

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

def Api_Cities_PixelData(request, format, name, data_model,start_day, start_month, start_year, final_day, final_month, final_year):
    startDate = datetime.date(start_year, start_month, 1)
    finalDate = datetime.date(final_year, final_month, 28)
    delta = finalDate  - startDate
    date = startDate

    city = City.objects.get(name=name)
    city_pixels = city.pixels.all()
    dm = DataModel.objects.get(name=data_model)

    queryset = CityData.objects.filter(city=city, data_model=dm, date__gte=startDate, date__lte=finalDate).order_by('date')

    n_months = round(delta.days / 28)
    if queryset.count() < n_months:
        n_pixel = city_pixels.count()

        while date <= finalDate:
            evapo = 0
            minTemp = 0
            maxTemp = 0
            ocis = 0
            precip = 0
            rnof = 0
            tp2m = 0

            for pixel in city_pixels:

                try:
                    # pixel_data = pixel.pixel_data.filter(date=date).first()
                    pixel_data = PixelData.objects.get(pixel=pixel, date=date)
                except PixelData.DoesNotExist:
                    continue

                evapo += pixel_data.evapo
                minTemp += pixel_data.minTemp
                maxTemp += pixel_data.maxTemp
                ocis += pixel_data.ocis
                precip += pixel_data.precip
                rnof += pixel_data.rnof
                tp2m += pixel_data.tp2m

            city_data, created = CityData.objects.get_or_create(
                                    city = city,
                                    data_model = dm,
                                    date = date,
                                    defaults = {
                                        'evapo': evapo / n_pixel,
                                        'minTemp': minTemp / n_pixel,
                                        'maxTemp': maxTemp / n_pixel,
                                        'ocis': ocis /n_pixel,
                                        'precip': precip /n_pixel,
                                        'rnof': rnof / n_pixel,
                                        'tp2m': tp2m / n_pixel,
                                    }
                                )

            if date.month < 12:
                date = datetime.date(date.year, date.month + 1, date.day)
            else:
                date = datetime.date(date.year + 1, 1, date.day)

        queryset = CityData.objects.filter(city=city, data_model=dm, date__gte=startDate, date__lte=finalDate).order_by('date')

    if(format == 'json'):
        queryset_serialized = serializers.serialize('json', queryset)
        response = HttpResponse(queryset_serialized, content_type="application/json")
        return response
    elif format == 'csv':
        qs_csv = queryset.values()
        return render_to_csv_response(qs_csv)
