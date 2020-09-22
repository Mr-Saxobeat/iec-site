from vismet.models import City, CityData
import os
import csv
import datetime

def run():
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
