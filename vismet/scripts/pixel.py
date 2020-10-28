import os
import csv
import json
from vismet.models import Pixel, ElementSource, ElementCategory
from django.contrib.gis.geos import LinearRing, Polygon
import geopandas as gpd

def LoadPixels(shp_path = os.path.join(os.getcwd(), 'vismet/scripts/data/pixel/ES_Pixel_Eta5km_Shapefile.shp')):

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

    shp_df = gpd.read_file(shp_path)
    dist = 0.025
    for index, row in shp_df.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]

        centroid = row["geometry"]
        x1 = float(centroid.x) - dist
        y1 = float(centroid.y) + dist
        x2 = float(centroid.x) + dist
        y2 = float(centroid.y) - dist

        pt1 = (x1, y1)
        pt2 = (x2, y1)
        pt3 = (x2, y2)
        pt4 = (x1, y2)

        coords = LinearRing(pt1, pt2, pt3, pt4, pt1)
        polygon_geom = Polygon(coords)

        pixel, created = Pixel.objects.get_or_create(
            latitude = lat,
            longitude = lon,
        )

        if created:
            geom = polygon_geom
            pixel.save()

    print("\n\n")
    print("Os pixels foram carregados.")
    print("\n\n")
