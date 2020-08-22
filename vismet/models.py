from django.contrib.gis.db import models
import os
import csv

# Estações meteorológicas que foram usadas
# nos dados compilados por Xavier.
class XavierWeatherStation(models.Model):
    station_id = models.BigIntegerField()
    omm_code = models.BigIntegerField()
    inmet_code = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    type = models.CharField(max_length=254)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    state = models.CharField(max_length=254)
    geom = models.PointField(srid=4326)

    def __str__(self):
        return self.name

    @property
    def popup_content(self):
        popup = "<span>Código OMM: </span>{}<br>".format(self.omm_code)
        popup += "<span>Código Inmet: </span>{}<br>".format(self.inmet_code)
        popup += "<span>Cidade: </span>{}<br>".format(self.name)
        popup += "<span>Tipo: </span>{}<br>".format(self.type)
        popup += "<span>Latitude: </span>{}<br>".format(self.latitude)
        popup += "<span>Longitude: </span>{}<br>".format(self.longitude)
        popup += "<span>Altitude: </span>{}<br>".format(self.latitude)
        popup += "<span>Estado: </span>{}<br>".format(self.state)

        return popup

    @property
    def stationId(self):
        return self.station_id

# Dados das estações meteorológicas de Xavier
class StationData(models.Model):
    date = models.DateField()
    station_id = models.ForeignKey(XavierWeatherStation, related_name='data', on_delete=models.CASCADE)
    evapo = models.FloatField('evapotranspiration')
    relHum = models.FloatField('relative humidity')
    solarRad = models.FloatField('solar radiation')
    maxTemp = models.FloatField('maximum temperature')
    minTemp = models.FloatField('minimum temperature')
    windSpeed = models.FloatField('wind speed')

    def __str__(self):
        return str('nº ' + str(self.station_id.station_id) + '---' + str(self.date))

# Pixels do estado do Espírito Santo.
# Não são necessariamente pixel de calor (eu sei, nome errado).
# Cada pixel tem 5Km de lado.
class HeatPixel(models.Model):
    pixel_id = models.BigIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    geom = models.PointField(srid=4326)
    boundings = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{ self.latitude }, { self.longitude }'

# Dados dos pixels do estado do Espírito Santo
class HeatPixelData(models.Model):
    date = models.DateField()
    pixel = models.ForeignKey(HeatPixel, related_name='data', on_delete=models.CASCADE)
    preciptation = models.FloatField()

    def __str__(self):
        return f'{ self.pixel.pixel_id }: { self.date }'

# Este modelo é usado como uma layer no mapa
# para destacar os municípios do Espírito Santo.
class City(models.Model):
    fid = models.BigIntegerField(blank=True,null=True)
    nome = models.CharField(max_length=50,blank=True,null=True)
    cod_ibge = models.FloatField(blank=True,null=True)
    microestad = models.CharField(max_length=50,blank=True,null=True)
    macroestad = models.CharField(max_length=50,blank=True,null=True)
    fonte = models.CharField(max_length=30,blank=True,null=True)
    data = models.CharField(max_length=50,blank=True,null=True)
    area_km2 = models.FloatField(blank=True,null=True)
    perim_m = models.FloatField(blank=True,null=True)
    percen_are = models.FloatField(blank=True,null=True)
    origem = models.CharField(max_length=100,blank=True,null=True)
    regional = models.CharField(max_length=20,blank=True,null=True)
    estrutura = models.CharField(max_length=30,blank=True,null=True)
    esc_local = models.CharField(max_length=30,blank=True,null=True)
    lei_criaca = models.CharField(max_length=250,blank=True,null=True)
    geom = models.PolygonField(srid=4326,blank=True,null=True)
