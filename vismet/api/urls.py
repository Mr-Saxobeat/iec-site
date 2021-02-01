from django.urls import path
from vismet.api.views import CityDataAPIView


urlpatterns = [
    path('citydata/', CityDataAPIView.as_view(), name='city-data-list'),
]