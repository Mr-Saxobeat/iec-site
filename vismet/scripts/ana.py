import os
import csv
import datetime
from vismet.models import ElementCategory, ElementSource, Station

# Este script carrega as estações PLUVIOMÉTRICAS ANA a partir do arquivo csv especificado
# na variável csv_path
def LoadANAStations(csv_path = os.path.join(os.getcwd(), 'vismet/scripts/data/ana/'), file='ANA_Precip_Estações_Metadata.csv'):

    csv_path = csv_path + file

    # Pega o objeto "Fonte da estação"
    source, created = ElementSource.objects.get_or_create(
                        name = 'ana',
                        category = ElementCategory.objects.get(name='observados'),
                        )

    state = 'ES'

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            omm_code = row[0] if row[0] != '' else None
            city = row[6] if row[6] != '' else None
            type = row[8] if row[8] != '' else None
            latitude = row[9] if row[9] != '' else None
            longitude = row[10] if row[10] != '' else None
            altitude = row[11] if row[11] != '' else None
            startDate = datetime.date(int(row[12]), 1, 1)
            finalDate = datetime.date(int(row[13]), 12, 31)

            newObj, created = Station.objects.get_or_create(
                source = source,
                omm_code = omm_code,
                state = state,
                city = city,
                type = type,
                latitude = latitude,
                longitude = longitude,
                altitude = altitude,
                startDate = startDate,
                finalDate = finalDate,
            )

            print(newObj)

    csv_file.close()
    print('Estações PLUVIOMÉTRICAS ANA foram carregadas.')


# Este script carrega as estações FLUVIOMÉTRICAS ANA a partir do arquivo csv especificado
# na variável csv_path
def LoadANAStations2(csv_path = os.path.join(os.getcwd(), 'vismet/scripts/data/ana/'), file='ANA_Estação_Fluviometrica_Metadata.csv'):

    csv_path = csv_path + file

    # Pega o objeto "Fonte da estação"
    source, created = ElementSource.objects.get_or_create(
                        name = 'ana',
                        category = ElementCategory.objects.get(name='observados'),
                        )

    state = 'ES'

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            omm_code = row[0] if row[0] != '' else None
            city = row[8] if row[8] != '' else None
            type = row[10] if row[10] != '' else None
            latitude = row[11] if row[1] != '' else None
            longitude = row[12] if row[12] != '' else None
            altitude = row[13] if row[13] != '' else None
            startDate = datetime.date(int(row[15]), 1, 1)
            finalDate = datetime.date(int(row[16]), 12, 31)

            newObj, created = Station.objects.get_or_create(
                source = source,
                omm_code = omm_code,
                state = state,
                city = city,
                type = type,
                latitude = latitude,
                longitude = longitude,
                altitude = altitude,
                startDate = startDate,
                finalDate = finalDate,
            )

            print(newObj)

    csv_file.close()
    print('Estações FLUVIOMÉTRICAS ANA foram carregadas.')
