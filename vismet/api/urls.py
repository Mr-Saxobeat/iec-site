from django.urls import path
from vismet.api.views import CityDataAPIView, PixelDataListCreateAPIView


urlpatterns = [
    path('citydata/', CityDataAPIView.as_view(), name='city-data-list'),
    path('pixeldata/', PixelDataListCreateAPIView.as_view(), name='pixel-data-list'),
]