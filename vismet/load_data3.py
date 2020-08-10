from .models import HeatPixel, HeatPixelData
import os
import csv
from datetime import datetime

def load_pixel_timeseries():
    csv_path = os.path.join(os.getcwd(), 'PREC ES Eta5km Hist. 1960-2005.csv')

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        pixel_id = []
        date = False

        for i, row in enumerate(reader):
            for j, value in enumerate(row):

                if i == 0 and j > 0:
                    pixel_id.append(int(value))

                elif i != 0 and j == 0:
                    date = datetime.strptime(value, '%d-%m-%Y')
                    if date.year > 1960:
                        return print('acabou porra')

                elif date:
                    pixel = HeatPixelData.objects.get_or_create(
                        date = date,
                        pixel = HeatPixel.objects.get(pixel_id=pixel_id[j-1]),
                        preciptation = value
                    )
                    print(pixel)

        file.close()
        print('ACABOOOOOOOOOOOOOOOOU')

def fix_date():
    pixels_data = HeatPixelData.objects.all()

    for pixel_data in pixels_data:
        date = pixel_data.date
        year = date.year
        month = date.month
        day = date.day
        new_date = datetime.date(year - 100, month, day)

        print('old = ', date, ' -- new = ', new_date)
        pixel_data.date = new_date
        pixel_data.save()

    print('louvado seja o senhor nosso deus acabou')
