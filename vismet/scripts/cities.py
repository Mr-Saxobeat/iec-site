from vismet.models import ElementCategory, ElementSource, ElementVariable, DataModel
from vismet.models import City
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

def setCityVariables():
    # Pega o elemento "Categoria"
    category, created = ElementCategory.objects.get_or_create(
                    name='simulados'
                    )

    # Pega o objeto "Fonte da estação"
    eta, created = ElementSource.objects.get_or_create(
                        name = 'eta por cidade',
                        category = category,
                        )

    datamodel_eta5km_45, created = DataModel.objects.get_or_create(
                            name = 'RCP 4.5, 5Km'
                            )

    precip, created = ElementVariable.objects.get_or_create(
        name = 'precipitação',
        init = 'precip',
        unit = 'mm³',
        chartType = 'bar',
        chartColor = 'blue',
    )

    eta.variables.add(precip)
    eta.data_model.add(datamodel_eta5km_45)
    eta.save()

def LoadCities(shp_path = os.path.join(os.getcwd(), 'vismet/scripts/data/city/esmunicpios/ES_Municipios.shp'), verbose=True):
    setCityVariables()
    lm = LayerMapping(City, shp_path, city_mapping)
    lm.save(strict=True, verbose=True)

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
