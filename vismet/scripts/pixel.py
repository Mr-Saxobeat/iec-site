import os
import csv
import json
from vismet.models import Pixel

def run():
    csv_path = os.path.join(os.getcwd(), 'vismet', 'data', 'Eta5km_pixel-2stat_ES.csv')

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            if i > 100:
                break

            pixel_id = row[0]
            lat = row[1]
            lng = row[2]

            dist = 0.025

            x1 = float(lat) - dist
            y1 = float(lng) + dist

            x2 = float(lat) + dist
            y2 = float(lng) - dist

            boudings = json.dumps([[x1, y1], [x2, y2]])

            Pixel.objects.get_or_create(
                pixel_id = pixel_id,
                latitude = lat,
                longitude = lng,
                boundings = boudings
            )

    print("ACABOU")
