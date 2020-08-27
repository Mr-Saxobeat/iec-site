from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),

    path('api/xavierstations/', views.Api_XavierStations.as_view(), name='xavier_stations_layer'),
    path('api/xavierstations/<int:omm_code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_XavierStations_TimeStamp,
         name='xavier_stations_timestamp'),
         
    path('api/cities/', views.CityGeoJson.as_view(), name='cities_layer'),
    path('api/pixels/', views.PixelGeoJson.as_view(), name='pixels_layer'),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
    path('api/pixeldata/', views.PixelDataView, name='pixeldata'),
    path('api/pixeldata/<int:pixel_id>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.PixelDataView),
]
