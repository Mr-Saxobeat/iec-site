import os
import csv
import datetime
from django.contrib.gis.utils import LayerMapping
from vismet.models import ElementCategory, ElementSource, WeatherStation

def run():
    csv_path = os.path.join(os.getcwd(), 'vismet/scripts/data/ana/ANA_Precip_Estações_Metadata.csv')

    obj, created = ElementSource.objects.get_or_create(
        name = 'ana',
        category = ElementCategory.objects.get(name='observados'),
        variables = ['precipitação', 'vazão']
    )

    source = obj
    state = 'ES'

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):

            if i == 0:
                continue



            omm_code = row[0] if row[0] != '' else None
            city = row[6] if row[6] != '' else None
            latitude = row[9] if row[9] != '' else None
            longitude = row[10] if row[10] != '' else None
            altitude = row[11] if row[11] != '' else None
            startDate = datetime.date(int(row[12]), 1, 1)
            finalDate = datetime.date(int(row[13]), 12, 31)



            newObj = WeatherStation.objects.create(
                source = source,
                omm_code = omm_code,
                state = state,
                city = city,
                type = 'Pluviométrica',
                latitude = latitude,
                longitude = longitude,
                altitude = altitude,
                startDate = startDate,
                finalDate = finalDate,
            )

            print(newObj)

    csv_file.close()
    print('acabou')
