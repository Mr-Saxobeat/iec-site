from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),

    path('api/xavierstations/', views.Api_XavierStations.as_view(), name='xavier_stations'),
    path('api/xavierstations/<int:omm_code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_XavierStations_TimeStamp,
         name='xavier_stations_timestamp'),

    path('api/pixels/', views.Api_Pixel.as_view(), name='pixels'),
    path('api/pixels/<int:pk>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Pixel_Data,
         name='pixel_data'),

    path('api/cities/', views.CityGeoJson.as_view(), name='cities'),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
]
