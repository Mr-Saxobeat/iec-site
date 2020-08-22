from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),
    path('xavierweathergeojson/', views.XavierStationWeatherGeoJson.as_view(), name="xavierweathergeojson"),
    path('cities/', views.CityGeoJson.as_view()),
    path('ajaxrequest/', views.ajaxrequest, name='ajaxrequest'),
    path('apiprojeta/', views.ApiProjeta, name='apiprojeta'),
    path('api/xavier/<str:variable>/<int:station_id>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.ApiXavier, name='apixavier'),
    path('api/pixeldata/', views.HeatPixelDataView, name='pixeldata'),
    path('api/pixeldata/<int:lat>/<int:lng>/<int:start_day>-<int:start_month>-<int:start_year>/<int:final_day>-<int:final_month>-<int:final_year>/', views.HeatPixelData2View),
    path('pixel/', views.HeatPixelGeoJson.as_view()),
]
