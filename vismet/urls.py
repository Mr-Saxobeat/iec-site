from django.urls import path
from . import views

app_name = 'vismet'

urlpatterns = [
    path('', views.VisMetView, name='vismet'),
]
