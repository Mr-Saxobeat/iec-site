from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),

    path('api/xavierstations/', views.Api_XavierStations.as_view(), name='xavier_stations'),
    path('api/xavierstations/<str:format>/<int:inmet_code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_XavierStations_Data,
         name='xavier_stations_timestamp'),

    path('api/opcoes/', views.Api_Data_Options, name='data_options'),
    path('api/estacoes/', views.Api_WeatherStations, name='api_stations'),
    path('api/estacoes/<str:format>/<str:source>/', views.Api_WeatherStations_Source, name='api_stations_source'),
    path('api/estacoes/<str:format>/<str:source>/<int:code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_WeatherStations_Data,
         name='weather_station_data'),

    path('api/pixels/', views.Api_Pixel.as_view(), name='pixel'),
    path('api/pixels/<str:format>/<int:pk>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Pixel_Data),

    path('api/cities/', views.Api_Cities.as_view(), name='cities'),
    path('api/cities/<str:format>/<str:name>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Cities_Data),

]
