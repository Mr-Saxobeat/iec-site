from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),
    path('xavierweathergeojson/', views.XavierStationWeatherGeoJson.as_view(), name="xavierweathergeojson"),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
    path('apiprojeta/', views.ApiProjeta, name='apiprojeta'),
    path('download/<str:variable>/<int:station_id>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.Download, name='download'),
    path('heat/', views.HeatPixelDataView, name='heatpixel'),
]
