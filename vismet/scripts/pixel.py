import os
import csv
import json
from vismet.models import Pixel, ElementSource, ElementCategory
from django.contrib.gis.geos import LinearRing, Polygon

def LoadPixels(csv_path = os.path.join(os.getcwd(), 'vismet/scripts/data/pixel/pixel_cities.csv')):

    # Pega o elemento "Categoria"
    category, created = ElementCategory.objects.get_or_create(
                    name='simulados'
                    )

    # Pega o objeto "Fonte da estação"
    source, created = ElementSource.objects.get_or_create(
                        name = 'eta',
                        category = category
                        )

    state = 'ES'

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            city = row[1]
            lat = row[3]
            lng = row[4]

            dist = 0.025
            x1 = float(lat) - dist
            y1 = float(lng) + dist
            x2 = float(lat) + dist
            y2 = float(lng) - dist

            pt1 = (x1, y1)
            pt2 = (x2, y1)
            pt3 = (x2, y2)
            pt4 = (x1, y2)

            coords = LinearRing(pt1, pt2, pt3, pt4, pt1)
            polygon_geom = Polygon(coords)

            Pixel.objects.get_or_create(
                city = city,
                latitude = lat,
                longitude = lng,
                geom = polygon_geom,
            )

    print("\n\n")
    print("Os pixels foram carregados.")
    print("\n\n")
