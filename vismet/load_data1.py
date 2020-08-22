import os
from django.contrib.gis.utils import LayerMapping
from .models import XavierWeatherStation, HeatPixel, City

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

shp_xavierWeather = os.path.abspath(os.path.join('stations_data', 'data', 'Weather2_XavierDomain_Shapefile.shp'))

def run_xavier_weather_stations(verbose=True):
    lm = LayerMapping(XavierWeatherStation, shp_xavierWeather, xavierweatherstation_mapping)
    lm.save(strict=True, verbose=True)

heatpixel_mapping = {
    'pixel_id': 'PIXEL ID',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'geom': 'POINT',
}

shp_heat_pixel = os.path.abspath(os.path.join('stations_data', 'eta', 'shapefile',
    'Eta 5km HADGEM2-ES Shapefile Espírito Santo', 'ES_Pixel_Eta5km_Shapefile.shp'))

def load_heat_pixel(verbose=True):
    lm = LayerMapping(HeatPixel, shp_heat_pixel, heatpixel_mapping)
    lm.save(strict=True, verbose=True)

# Auto-generated `LayerMapping` dictionary for City model
city_mapping = {
    'fid': 'FID',
    'nome': 'nome',
    'cod_ibge': 'cod_ibge',
    'microestad': 'microestad',
    'macroestad': 'macroestad',
    'fonte': 'fonte',
    'data': 'data',
    'area_km2': 'area_km2',
    'perim_m': 'perim_m',
    'percen_are': 'percen_are',
    'origem': 'origem',
    'regional': 'regional',
    'estrutura': 'estrutura',
    'esc_local': 'esc_local',
    'lei_criaca': 'lei_criaca',
    'geom': 'POLYGON',
}

shp_city = os.path.abspath(os.path.join('stations_data', 'esmunicipios', 'ES_Municipios.shp'))

def load_city(verbose=True):
    lm = LayerMapping(City, shp_city, city_mapping)
    lm.save(strict=True, verbose=True)
