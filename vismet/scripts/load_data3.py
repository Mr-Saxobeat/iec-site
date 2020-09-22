from vismet.models import Pixel, PixelData
import os
import csv
from datetime import datetime
import json

def run():
    csv_path = "/home/weiglas/git/iec-site/vismet/data/PREC ES Eta5km Hist. 1960-2005.csv"

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        pixel_id = []
        date = False

        for i, row in enumerate(reader):
            for j, value in enumerate(row):

                if i == 0 and j > 0:
                    pixel_id.append(int(value))

                elif i > 0 and j == 0:
                    date = datetime.strptime(value, '%d-%m-%Y')
                    if date.year > 1960:
                        return print('acabou')

                elif date:
                    pixel = PixelData.objects.get_or_create(
                        date = date,
                        pixel = Pixel.objects.get(pixel_id=pixel_id[j-1]),
                        preciptation = value
                    )
                    print(pixel)

        file.close()
        print('ACABOOOOOOOOOOOOOOOOU')

def add_bounding():
    pixels = Pixel.objects.all()
    dist = 0.025

    for px in pixels:
        x1 = px.longitude - dist
        y1 = px.latitude + dist

        x2 = px.longitude + dist
        y2 = px.latitude - dist

        px.boundings = json.dumps([[x1, y1], [x2, y2]])
        px.save()
        print(px.pk)

    print("acabouporra")
