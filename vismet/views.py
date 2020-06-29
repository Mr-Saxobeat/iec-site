from django.shortcuts import render
from djgeojson.views import GeoJSONLayerView
from .models import XavierWeatherStation, StationData
from django.http import HttpResponse
import json
import datetime
from django.core import serializers

def VisMetView(request):
    return render(request, 'vismet/vismet.html')

class XavierStationWeatherGeoJson(GeoJSONLayerView):
    model = XavierWeatherStation
    properties = ('popup_content', 'stationId', 'name', 'state', 'omm_code', 'latitude', 'longitude')

def ajaxrequest(request):
    stationId = request.GET.get('stationId')
    startDate = request.GET.get('startDate')
    finalDate = request.GET.get('finalDate')

    startDay = startDate[:2]
    startMonth = startDate[3:5]
    startYear = startDate[6:10]
    sDate = datetime.date(int(startYear), int(startMonth), int(startDay))

    finalDay = finalDate[:2]
    finalMonth = finalDate[3:5]
    finalYear = finalDate[6:10]
    eDate = datetime.date(int(finalYear), int(finalMonth), int(finalDay))

    station_timestamp = StationMaxTemp.objects.filter(station_id = stationId, date__gte=sDate, date__lte=eDate).order_by('date')
    myData = serializers.serialize('json', station_timestamp)

    return HttpResponse(myData, content_type="application/json")
