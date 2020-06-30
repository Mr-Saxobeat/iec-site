# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
import os
import csv

# class XavierWeatherStation(models.Model):
#     station_id = models.BigIntegerField()
#     omm_code = models.BigIntegerField()
#     inmet_code = models.CharField(max_length=254)
#     name = models.CharField(max_length=254)
#     type = models.CharField(max_length=254)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     altitude = models.FloatField()
#     state = models.CharField(max_length=254)
#     geom = models.PointField(srid=4326)
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def popup_content(self):
#         popup = "<span>Código OMM: </span>{}<br>".format(self.omm_code)
#         popup += "<span>Código Inmet: </span>{}<br>".format(self.inmet_code)
#         popup += "<span>Cidade: </span>{}<br>".format(self.name)
#         popup += "<span>Tipo: </span>{}<br>".format(self.type)
#         popup += "<span>Latitude: </span>{}<br>".format(self.latitude)
#         popup += "<span>Longitude: </span>{}<br>".format(self.longitude)
#         popup += "<span>Altitude: </span>{}<br>".format(self.latitude)
#         popup += "<span>Estado: </span>{}<br>".format(self.state)
#
#         return popup
#
#     @property
#     def stationId(self):
#         return self.station_id
#
# class StationData(models.Model):
#     date = models.DateField()
#     station_id = models.ForeignKey(XavierWeatherStation, related_name='data', on_delete=models.CASCADE)
#     evapo = models.FloatField('evapotranspiration')
#     relHum = models.FloatField('relative humidity')
#     solarRad = models.FloatField('solar radiation')
#     maxTemp = models.FloatField('maximum temperature')
#     minTemp = models.FloatField('minimum temperature')
#     windSpeed = models.FloatField('wind speed')
#
#     def __str__(self):
#         return str('nº ' + str(self.station_id.station_id) + '---' + str(self.date))
