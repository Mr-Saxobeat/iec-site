from django.shortcuts import render
from djgeojson.views import GeoJSONLayerView
from .models import XavierWeatherStation, StationData
from django.http import HttpResponse, JsonResponse
import json
import datetime
from django.core import serializers
from rest_framework import serializers as rest_serializers

def VisMetView(request):
    return render(request, 'vismet/vismet.html')

class XavierStationWeatherGeoJson(GeoJSONLayerView):
    model = XavierWeatherStation
    properties = ('popup_content', 'stationId', 'name', 'state', 'omm_code', 'latitude', 'longitude')

def ajaxrequest(request):
    stationId = request.GET.get('stationId')
    startDate = request.GET.get('startDate')
    finalDate = request.GET.get('finalDate')

    # Create the correct start date object to execute the filter
    startDay = startDate[:2]
    startMonth = startDate[3:5]
    startYear = startDate[6:10]
    sDate = datetime.date(int(startYear), int(startMonth), int(startDay))

    # Create the correct end date object to execute the filter
    finalDay = finalDate[:2]
    finalMonth = finalDate[3:5]
    finalYear = finalDate[6:10]
    eDate = datetime.date(int(finalYear), int(finalMonth), int(finalDay))

    # Get the station object
    station = XavierWeatherStation.objects.get(station_id=stationId)

    # Get the the data objects between the specified dates
    station_timestamp = station.data.filter(date__gte=sDate, date__lte=eDate).order_by('date')
    myData = serializers.serialize('json', station_timestamp)

    return HttpResponse(myData, content_type="application/json")
    # return JsonResponse(myData, safe=False)
