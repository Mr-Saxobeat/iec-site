from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),

    path('api/xavierstations/', views.Api_XavierStations.as_view(), name='xavier_stations'),
    path('api/xavierstations/<str:format>/<int:omm_code>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_XavierStations_Data,
         name='xavier_stations_timestamp'),

    path('api/pixels/', views.Api_Pixel.as_view(), name='pixel'),
    path('api/pixels/<str:format>/<int:pk>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Pixel_Data),

    path('api/cities/', views.Api_Cities.as_view(), name='cities'),
    path('api/cities/<str:name>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/',
         views.Api_Cities_Data),

]
