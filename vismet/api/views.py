from rest_framework import generics, status
from rest_framework.response import Response
from vismet.models import City, DataModel, CityData, Pixel, PixelData
from vismet.api.serializers import CityDataSerializer, PixelDataSerializer
import datetime


class CityDataAPIView(generics.ListCreateAPIView):
    queryset = CityData.objects.all()
    serializer_class = CityDataSerializer
    
    def perform_create(self, serializer):
        city_fid = self.request.data['city_fid']
        data_model_name = self.request.data['data_model']
        date = datetime.datetime.strptime(self.request.data['date'], '%Y-%m-%d')

        pd = CityData.objects.filter(
                city__fid=city_fid, 
                data_model__name__contains=data_model_name,
                date=date
                )
        
        if pd == None:
            print('bora criar')
            city = City.objects.get(fid=city_fid)
            data_model = DataModel.objects.get(name__icontains=data_model_name)
            serializer.save(city=city, data_model=data_model)

class PixelDataAPIView(generics.ListCreateAPIView):
    queryset = PixelData.objects.all()
    serializer_class = PixelDataSerializer

    def perform_create(self, serializer):
        lat = self.request.data['latitude']
        lon = self.request.data['longitude']
        data_model_name = self.request.data['data_model_name']

        pixel = Pixel.objects.get(latitude=lat, longitude=lon)
        data_model = DataModel.objects.get(name__icontains=data_model_name)

        serializer.save(
            pixel=pixel,
            data_model=data_model
        )


        

        

    
