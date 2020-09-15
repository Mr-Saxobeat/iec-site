from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),

    path('api/xavierstations/', views.Api_XavierStations.as_view(), name='xavier_stations'),
    path('api/xavierstations/<str:format>/<int:omm_code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_XavierStations_Data,
         name='xavier_stations_timestamp'),

    path('api/pixels/', views.Api_Pixel.as_view(), name='pixels'),
    path('api/pixels/<int:pk>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Pixel_Data,
         name='pixel_data'),

    path('api/cities/', views.Api_Cities.as_view(), name='cities'),
    path('api/cities/<str:name>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Cities_Data,
         name='cities_data'),

    path('inmet/', views.pega_capitais),
    path('api/inmet/<int:day>-<int:month>-<int:year>', views.Api_Inmet_Capitais, name='inmet_capitais'),
]
