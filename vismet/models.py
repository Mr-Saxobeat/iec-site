from django.contrib.gis.db import models
import os
import csv

# Estações meteorológicas que foram usadas
# nos dados compilados por Xavier.
class XavierStation(models.Model):
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
        popup = "<span>Estado: </span>{}<br>".format(self.state)
        popup += "<span>Cidade: </span>{}<br>".format(self.name)
        popup += "<span>Código OMM: </span>{}<br>".format(self.omm_code)
        popup += "<span>Código Inmet: </span>{}<br>".format(self.inmet_code)
        popup += "<span>Tipo: </span>{}<br>".format(self.type)
        popup += "<span>Latitude: </span>{:.2f}<br>".format(self.latitude)
        popup += "<span>Longitude: </span>{:.2f}<br>".format(self.longitude)
        popup += "<span>Altitude: </span>{:.2f} m<br>".format(self.altitude)

        return popup


# Dados diários das estações meteorológicas de Xavier
class XavierStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(XavierStation, related_name='data', on_delete=models.CASCADE)
    evapo = models.FloatField('evapotranspiration', blank=True, null=True)
    relHum = models.FloatField('relative humidity', blank=True, null=True)
    solarIns = models.FloatField('solar insolation', blank=True, null=True)
    maxTemp = models.FloatField('maximum temperature', blank=True, null=True)
    minTemp = models.FloatField('minimum temperature', blank=True, null=True)
    windSpeed = models.FloatField('wind speed', blank=True, null=True)

    def __str__(self):
        return str('nº ' + str(self.station.omm_code) + '---' + str(self.date))

class INMETStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(XavierStation, related_name='inmet_data', on_delete=models.CASCADE)
    maxTemp = models.FloatField('maximum temperature', blank=True, null=True)
    minTemp = models.FloatField('minimum temperature', blank=True, null=True)
    relHum = models.FloatField('relative humidity', blank=True, null=True)
    precip = models.FloatField('preciptatioin', blank=True, null=True)

    def __str__(self):
        return str('nº ' + str(self.station.inmet_code) + '---' + str(self.date))

# Pixels do estado do Espírito Santo.
# Cada pixel tem 5Km de lado. (verificar isso)
class Pixel(models.Model):
    pixel_id = models.BigIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    geom = models.PointField(srid=4326, null=True)

    # Lista com as coordenadas da vértice superior esquerda
    # e da inferior direita, formando um quadrado de lado
    # 5Km. (sim eu ainda tenho que verificar se são 5Km msm,
    # a função que gerou esses pontos está em scripts/load_data3.py
    boundings = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{ self.latitude }, { self.longitude }'


# Dados dos pixels do estado do Espírito Santo
class PixelData(models.Model):
    date = models.DateField()
    pixel = models.ForeignKey(Pixel, related_name='data', on_delete=models.CASCADE)
    preciptation = models.FloatField()

    def __str__(self):
        return f'{ self.pixel.pixel_id }: { self.date }'


# Este modelo é usado como uma layer no mapa
# para destacar os municípios do Espírito Santo.
######################################################################
# Foram adicionados os atributos blank e null como True, pois estava
# dando algum erro ao subir os dados do .cvs, Portanto, ainda é
# necessário verificar se ainda pode ter algum erro nessa questão.
######################################################################
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

    def __str__(self):
        return self.nome


class CityData(models.Model):
    date = models.DateField()
    city = models.ForeignKey(City, related_name='city_data', on_delete=models.CASCADE)
    preciptation = models.FloatField(null=True)
    medTemp = models.FloatField(null=True)

    def __str__(self):
        return f'{ self.city.nome }: { self.date }'
