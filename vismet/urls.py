from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),
    path('api/xavierstations/', views.XavierStationWeatherGeoJson.as_view(), name='xavier_stations_layer'),
    path('api/cities/', views.CityGeoJson.as_view(), name='cities_layer'),
    path('api/pixels/', views.PixelGeoJson.as_view(), name='pixels_layer'),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
    path('api/xavier/<str:variable>/<int:station_id>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.ApiXavier, name='apixavier'),
    path('api/pixeldata/', views.PixelDataView, name='pixeldata'),
    path('api/pixeldata/<int:pixel_id>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.PixelDataView),
]
