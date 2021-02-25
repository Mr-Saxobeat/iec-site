from django.contrib.gis.geos import LinearRing, Polygon
from vismet.models import Pixel

# Script para criar models Pixel 
# de resolução 0.25º que cobrem o estado do Espírito Santo
def run():
    minLat = -21.5
    minLon = -42
    maxLat = -17.75
    maxLon = -39.5

    step = 0.125
    curLat = minLat
    while(curLat <= maxLat):
        curLon = minLon
        while(curLon <= maxLon):
            x1 = curLon - step
            y1 = curLat - step
            x2 = curLon + step
            y2 = curLat + step

            pt1 = (x1, y1)
            pt2 = (x2, y1)
            pt3 = (x2, y2)
            pt4 = (x1, y2)

            points = LinearRing(pt1, pt2, pt3, pt4, pt1)
            polygon_geom = Polygon(points)

            pixel, created = Pixel.objects.get_or_create(
                                latitude=curLat,
                                longitude=curLon,
                                geom=polygon_geom,
                                resolution=0.25
                            )
            curLon += 0.25
        
        curLat += 0.25

        







