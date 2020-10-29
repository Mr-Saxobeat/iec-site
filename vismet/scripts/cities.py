from vismet.models import ElementCategory, ElementSource, ElementVariable
from vismet.models import City, CityData
from django.contrib.gis.utils import LayerMapping
import os
import csv
import datetime

city_mapping = {
    'fid': 'FID',
    'name': 'nome',
    'ibge_code': 'cod_ibge',
    'microestado': 'microestad',
    'macroestado': 'macroestad',
    'fonte': 'fonte',
    'data': 'data',
    'area_km2': 'area_km2',
    'perim_m': 'perim_m',
    'percen_area': 'percen_are',
    'origem': 'origem',
    'regional': 'regional',
    'estrutura': 'estrutura',
    'esc_local': 'esc_local',
    'lei_criacao': 'lei_criaca',
    'geom': 'POLYGON',
}

shp_city = os.path.abspath(os.path.join('stations_data', 'esmunicipios', 'ES_Municipios.shp'))

def LoadCities(verbose=True):
    lm = LayerMapping(City, shp_city, city_mapping)
    lm.save(strict=True, verbose=True)


def setCityVariables():
    # Pega o elemento "Categoria"
    category, created = ElementCategory.objects.get_or_create(
                    name='simulados'
                    )

    # Pega o objeto "Fonte da estação"
    eta, created = ElementSource.objects.get_or_create(
                        name = 'eta por cidade',
                        category = category
                        )

    # Cria as variáveis dos pixels
    maxTemp, created = ElementVariable.objects.get_or_create(
        name = 'temperatura máxima',
        init = 'maxTemp',
        unit = 'ºC',
        chartType = 'line',
        chartColor = 'red',
    )

    minTemp, created = ElementVariable.objects.get_or_create(
        name = 'temperatura mínima',
        init = 'minTemp',
        unit = 'ºC',
        chartType = 'line',
        chartColor = 'blue',
    )

    evapo, created = ElementVariable.objects.get_or_create(
        name = 'evapotranspiração',
        init = 'evapo',
        unit = 'mm³',
        chartType = 'line',
        chartColor = 'red',
    )

    eta.variables.add(maxTemp, minTemp, evapo)
    eta.save()

def LoadCityData():
    csv_path = os.path.join(os.getcwd(),
                            'stations_data',
                            'esmunicipios',
                            'Etakm_HADGEM2-ES_Historico_Temp_Mensal_Media.csv')

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        city_id = []
        date = False

        for i, row in enumerate(reader):
            rowLen = len(row)
            j = 0

            while j < rowLen - 1:
                value = row[j]

                # O primeiro e segundo valor das células da primeira linha
                # são os nomes das respectivas colunas "year" e "month",
                # então a partir da terceira coluna (index 2) começam os
                # valores dos ids das cidadaes, por isso a partir daí
                # são adicionados à lista.
                if i == 0:
                    if j == 0:
                        j = 2
                        value = row[j]

                    city_id.append(value)

                elif i > 0 and j == 0:
                    year = int(value)
                    month = int(row[1])
                    date = datetime.date(year, month, 1)

                    # if year > 1960:
                    #     return print("acabou")

                    j = 2
                    continue

                elif date:
                    city_data = CityData.objects.get_or_create(
                        date = date,
                        city = City.objects.get(fid=city_id[j-2]),
                        preciptation = None,
                        medTemp = value
                    )
                    print(city_data)

                j = j + 1


        file.close()
        print("acbouasflaskdjfalskdfj")
