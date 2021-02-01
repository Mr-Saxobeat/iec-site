from rest_framework import generics
from vismet.models import City, DataModel, CityData
from vismet.api.serializers import CityDataSerializer


class CityDataAPIView(generics.ListCreateAPIView):
    queryset = CityData.objects.all()
    serializer_class = CityDataSerializer

    
    def perform_create(self, serializer):
        city_fid = self.request.data['city_fid']
        data_model_name = self.request.data['data_model']
        
        city = City.objects.get(fid=city_fid)
        data_model = DataModel.objects.get(name=data_model_name)

        serializer.save(city=city, data_model=data_model)
        

    
