from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),
    path('xavierweathergeojson/', views.XavierStationWeatherGeoJson.as_view(), name="xavierweathergeojson"),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
]
