import os
from django.contrib.gis.utils import LayerMapping
from .models import XavierWeatherStation

xavierweatherstation_mapping = {
    'station_id': 'MATLAB ind',
    'omm_code': 'Codigo OMM',
    'inmet_code': 'Codigo INM',
    'name': 'Nome da es',
    'type': 'Typo de es',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'altitude': 'Altitude',
    'state': 'Estado',
    'geom': 'POINT',
}

shp_xavierWeather = os.path.abspath(os.path.join('data', 'data', 'Weather2_XavierDomain_Shapefile.shp'))

def run_xavier_weather_stations(verbose=True):
    lm = LayerMapping(XavierWeatherStation, shp_xavierWeather, xavierweatherstation_mapping)
    lm.save(strict=True, verbose=True)
