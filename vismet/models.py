from django.contrib.gis.db import models
import django.contrib.postgres.fields as pgField
import os
import csv

class DataModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ElementVariable(models.Model):
    name = models.CharField(max_length=200)
    init = models.CharField(max_length=10)
    unit = models.CharField(max_length=10)
    chartType = models.CharField(max_length=10)
    chartColor = models.CharField(max_length=15)

    def __str__(self):
        return self.init

# Categoria de dados, (dados observados, reanálise ou simulados)
class ElementCategory(models.Model):
    display_name = models.CharField(max_length=100, default="none")
    name = models.CharField(max_length=100)
    desc = models.TextField(verbose_name="Descrição da categoria", blank=True, null=True)

    def __str__(self):
        return self.name

# Modelo que representa a fonte de uma estação, pixel... (INMET, ANA, CEMADEN...)
class ElementSource(models.Model):
    display_name = models.CharField(max_length=100, verbose_name="Nome de visualização", default="null")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ElementCategory, related_name='sources', on_delete=models.CASCADE)
    data_model = models.ManyToManyField(DataModel)
    variables = models.ManyToManyField(ElementVariable)

    def __str__(self):
        return self.name

class SubSource(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, verbose_name="nome de visualização")
    desc = models.TextField(max_length=200, verbose_name="descrição adicional", null=True, blank=True)
    related_source = models.ForeignKey(ElementSource, verbose_name="fonte relacionada", related_name='subsource', on_delete=models.CASCADE)
    time_interval = models.CharField(max_length=100, verbose_name="intervalo de ano")

# Modelo que representa uma única estação meteorológica
class Station(models.Model):
    source = models.ForeignKey(ElementSource, related_name='stations', on_delete=models.CASCADE)
    omm_code = models.CharField(max_length=100, blank=True, null=True)
    inmet_code = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(blank=True, null=True)
    startDate = models.DateField('Data de início de operação', blank=True, null=True)
    finalDate = models.DateField('Data de fim de operação', blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(null=True)

    def get_station_codes(self):
        popup_codes_content = ""

        if self.source.name == 'ana':
            popup_codes_content += "<span>Código ANA: </span>{}<br>".format(self.omm_code)
        else:
            if self.omm_code != None:
                popup_codes_content += "<span>Código OMM: </span>{}<br>".format(self.omm_code)
            if self.inmet_code != None:
                popup_codes_content += "<span>Código INMET: </span>{}<br>".format(self.inmet_code)

        return popup_codes_content

    def get_interval_date(self):
        popup_date_content = ""

        if self.startDate is not None:
            popup_date_content += "<span>Data Inicial: </span>{}<br>".format(self.startDate.strftime("%d/%m/%Y"))

            if self.finalDate is not None:
                popup_date_content += "<span>Data Final: </span>{}<br>".format(self.finalDate.strftime("%d/%m/%Y"))
            else:
                popup_date_content += "<span>Data Final: até o presente</span><br>"

        return popup_date_content

    @property
    def popup_content(self):
        popup = "<span>Estado: </span>{}<br>".format(self.state)
        popup += "<span>Cidade: </span>{}<br>".format(self.city)
        popup += self.get_station_codes()
        popup += "<span>Tipo: </span>{}<br>".format(self.type)
        popup += "<span>Latitude: </span>{:.2f}<br>".format(self.latitude)
        popup += "<span>Longitude: </span>{:.2f}<br>".format(self.longitude)
        if self.altitude != None:
            popup += "<span>Altitude: </span>{:.2f} m<br>".format(self.altitude)
        popup += self.get_interval_date()

        return popup

    def __str__(self):
        if self.omm_code != None:
            return self.omm_code + " " + self.city
        elif self.inmet_code != None:
            return self.inmet_code + " " + self.city
        else:
            return self.city

# Dados diários das estações meteorológicas de Xavier
class XavierStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(Station, related_name='xavier_data', on_delete=models.CASCADE)
    evapo = models.FloatField('Evapotranspiração', blank=True, null=True)
    relHum = models.FloatField('Umidade Relativa', blank=True, null=True)
    solarIns = models.FloatField('Radiação Solar', blank=True, null=True)
    maxTemp = models.FloatField('Temperatura Máxima', blank=True, null=True)
    minTemp = models.FloatField('Temperatura Mínima', blank=True, null=True)
    windSpeed = models.FloatField('Velocidade do Vento', blank=True, null=True)

    def __str__(self):
        return str('nº ' + str(self.station.omm_code) + '---' + str(self.date))

class INMETStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(Station, related_name='inmet_data', on_delete=models.CASCADE)
    maxTemp = models.FloatField('Temperatura Máxima', blank=True, null=True)
    minTemp = models.FloatField('Temperatura Mínima', blank=True, null=True)
    relHum = models.FloatField('Umidade Relativa', blank=True, null=True)
    precip = models.FloatField('Precipitação', blank=True, null=True)

    def __str__(self):
        return str('nº ' + str(self.station.inmet_code) + '---' + str(self.date))

class ANAStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(Station, related_name='ana_data', on_delete=models.CASCADE)
    value = models.FloatField('Valor', blank=True, null=True)

# Pixels do estado do Espírito Santo.
# Cada pixel tem 5Km de lado. (verificar isso)
class Pixel(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    geom = models.PolygonField(null=True)

    def __str__(self):
        return f'{ self.latitude }, { self.longitude }'

    @property
    def popup_content(self):
        popup = "<span>ID: </span>{}<br>".format(self.id)
        # popup += "<span>Cidade: </span>{}<br>".format(self.city)
        # popup += "<span>Estado: </span>{}<br>".format(self.state)
        popup += "<span>Latitude: </span>{}<br>".format(self.latitude)
        popup += "<span>Longitude: </span>{}<br>".format(self.longitude)

        return popup


# Dados dos pixels do estado do Espírito Santo
# class PixelData(models.Model):
#     pixel = models.ForeignKey(Pixel, related_name='pixel_data', on_delete=models.CASCADE)
#     date = models.DateField()
#     preciptation = models.FloatField()
#
#     def __str__(self):
#         return f'{ self.pixel.pixel_id }: { self.date }'


# Este modelo é usado como uma layer no mapa
# para destacar os municípios do Espírito Santo.
class City(models.Model):
    fid = models.BigIntegerField(blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    ibge_code = models.FloatField(blank=True,null=True)
    microestado = models.CharField(max_length=50,blank=True,null=True)
    macroestado = models.CharField(max_length=50,blank=True,null=True)
    fonte = models.CharField(max_length=30,blank=True,null=True)
    data = models.CharField(max_length=50,blank=True,null=True)
    area_km2 = models.FloatField(blank=True,null=True)
    perim_m = models.FloatField(blank=True,null=True)
    percen_area = models.FloatField(blank=True,null=True)
    origem = models.CharField(max_length=100,blank=True,null=True)
    regional = models.CharField(max_length=20,blank=True,null=True)
    estrutura = models.CharField(max_length=30,blank=True,null=True)
    esc_local = models.CharField(max_length=30,blank=True,null=True)
    lei_criacao = models.CharField(max_length=250,blank=True,null=True)
    geom = models.PolygonField(srid=4326,blank=True,null=True)

    def __str__(self):
        return self.name


class CityData(models.Model):
    date = models.DateField()
    city = models.ForeignKey(City, related_name='city_data', on_delete=models.CASCADE)
    precip = models.FloatField(null=True)
    medTemp = models.FloatField(null=True)

    def __str__(self):
        return f'{ self.city.name }: { self.date }'
