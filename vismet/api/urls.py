from django.urls import path
from vismet.api.views import CityDataAPIView, PixelDataRetrieveCreateAPIView


urlpatterns = [
    path('citydata/', CityDataAPIView.as_view(), name='city-data-list'),
    path('pixeldata/', PixelDataRetrieveCreateAPIView.as_view(), name='pixel-data-list'),
]