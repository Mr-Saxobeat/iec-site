from rest_framework import generics, status
from rest_framework.response import Response
from vismet.models import City, DataModel, CityData
from vismet.api.serializers import CityDataSerializer
import datetime


class CityDataAPIView(generics.ListCreateAPIView):
    queryset = CityData.objects.all()
    serializer_class = CityDataSerializer

    
    def perform_create(self, serializer):
        city_fid = self.request.data['city_fid']
        data_model_name = self.request.data['data_model']
        date = self.request.data['date']

        try:
            date_aux = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            citydata = CityData.objects.get(
                            city__fid=city_fid, 
                            data_model__name=data_model_name, 
                            date=date_aux
                        )
            
            if citydata != None:
                return Response(
                            data={
                                'mensagem': 'O dado para a data, modelo e cidade fornecidos já existe.'
                                }, 
                            status=status.HTTP_401_UNAUTHORIZED
                            )

        except CityData.DoesNotExist:
            city = City.objects.get(fid=city_fid)
            print(data_model_name)
            data_model = DataModel.objects.get(name__icontains=data_model_name)

            serializer.save(city=city, data_model=data_model)
        

    
