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

class SubSourceDetail(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class SubSource(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100, verbose_name="nome de visualização")
    details = models.ManyToManyField(SubSourceDetail)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

# Modelo que representa a fonte de uma estação, pixel... (INMET, ANA, CEMADEN...)
class ElementSource(models.Model):
    display_name = models.CharField(max_length=100, verbose_name="Nome de visualização", default="null")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ElementCategory, related_name='sources', on_delete=models.CASCADE)
    data_model = models.ManyToManyField(DataModel)
    variables = models.ManyToManyField(ElementVariable)
    subsources = models.ManyToManyField(SubSource)

    def __str__(self):
        return self.name

# Modelo que representa uma única estação meteorológica
class Station(models.Model):
    source = models.ForeignKey(ElementSource, verbose_name='fonte', related_name='stations', on_delete=models.CASCADE)
    omm_code = models.CharField(max_length=100, verbose_name='código OMM', blank=True, null=True)
    inmet_code = models.CharField(max_length=100, verbose_name='código INMET', blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name='estado')
    city = models.CharField(max_length=100, verbose_name='cidade')
    type = models.CharField(max_length=100, verbose_name='tipo')
    altitude = models.FloatField(verbose_name='altitude', blank=True, null=True)
    startDate = models.DateField(verbose_name='Data de início de operação', blank=True, null=True)
    finalDate = models.DateField(verbose_name='Data de fim de operação', blank=True, null=True)
    status = models.CharField(verbose_name='estado de operação', max_length=100, blank=True, null=True)
    geom = models.PointField(verbose_name='localização', null=True)

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
        popup += "<span>Latitude: </span>{:.2f}<br>".format(self.geom.y)
        popup += "<span>Longitude: </span>{:.2f}<br>".format(self.geom.x)
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
    solarIns = models.FloatField('Radiação Solar', blank=True, null=True, default=None)

    def __str__(self):
        return str('nº ' + str(self.station.inmet_code) + '---' + str(self.date))

class ANAStationData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(Station, related_name='ana_data', on_delete=models.CASCADE)
    value = models.FloatField('Valor', blank=True, null=True)

# Pixels do estado do Espírito Santo.
# Cada pixel tem 5Km de lado. (verificar isso)
class Pixel(models.Model):
    state = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    geom = models.PolygonField(null=True)
    resolution = models.FloatField(default=0.05)

    def __str__(self):
        return f'{ self.latitude }, { self.longitude }, res = { self.resolution }º'

    @property
    def popup_content(self):
        # popup = "<span>ID: </span>{}<br>".format(self.id)
        # popup += "<span>Cidade: </span>{}<br>".format(self.city)
        # popup += "<span>Estado: </span>{}<br>".format(self.state)
        popup = "<span>Latitude: </span>{}<br>".format(self.latitude)
        popup += "<span>Longitude: </span>{}<br>".format(self.longitude)

        return popup

class PixelData(models.Model):
    pixel = models.ForeignKey(Pixel, related_name='pixel_data', on_delete=models.CASCADE)
    data_model = models.ForeignKey(DataModel, related_name='pixel_data', on_delete=models.CASCADE)
    date = models.DateField()
    time_interval = models.CharField('intervalo de tempo', default='mensal', max_length=7)
    evapo = models.FloatField('evapotranspiração (mm)', default=None, null=True, blank=True)
    minTemp = models.FloatField('temperatura mínima (ºC)', default=None, null=True, blank=True)
    maxTemp = models.FloatField('temperatura máxima (ºC)', default=None, null=True, blank=True)
    ocis = models.FloatField('radiação de onda curta incidente à superficie (W/m²)', default=None, null=True, blank=True)
    precip = models.FloatField('precipitação (mm)', default=None, null=True, blank=True)
    rnof = models.FloatField('escoamento superficial (mm)', default=None, null=True, blank=True)
    tp2m = models.FloatField('temperatura a 2m da superfície (ºC)', default=None, null=True, blank=True)
    relHum = models.FloatField('umidade relativa do ar (%)', default=None, null=True, blank=True)
    u10 = models.FloatField('10m u-component of wind ', default=None, null=True, blank=True)
    v10 = models.FloatField('10m v-component of wind', default=None, null=True, blank=True)
    slhf = models.FloatField('surface latent heat flux', default=None, null=True, blank=True)
    sshf = models.FloatField('surface sensible heat flux', default=None, null=True, blank=True)

    def __str__(self):
        return f'{ self.pixel.latitude }, { self.pixel.longitude } --- { self.date }'


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
    pixels = models.ManyToManyField(Pixel)

    def __str__(self):
        return self.name


class CityData(models.Model):
    city = models.ForeignKey(City, related_name='city_data', on_delete=models.CASCADE)
    data_model = models.ForeignKey(DataModel, related_name='city_data', on_delete=models.CASCADE, default=None)
    date = models.DateField()
    evapo = models.FloatField(default=None, null=True, blank=True)
    minTemp = models.FloatField(default=None, null=True, blank=True)
    maxTemp = models.FloatField(default=None, null=True, blank=True)
    ocis = models.FloatField(default=None, null=True, blank=True)
    precip = models.FloatField(default=None, null=True, blank=True)
    rnof = models.FloatField(default=None, null=True, blank=True)
    tp2m = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return f'{ self.city.name }: { self.date }'
