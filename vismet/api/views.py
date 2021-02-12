from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from vismet.models import City, DataModel, CityData, Pixel, PixelData
from vismet.api.serializers import CityDataSerializer, PixelDataSerializer
import datetime
from vismet.api.core.chirps import retrieveChirpsData


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

class PixelDataRetrieveCreateAPIView(APIView):
    queryset = PixelData.objects.all()
    serializer_class = PixelDataSerializer

    def get(self, request):
        try:
            lat = request.GET['latitude']
            lon = request.GET['longitude']
            data_model_name = request.GET['data_model_name']
            startDate = request.GET['startDate']
            finalDate = request.GET['finalDate']
        except KeyError:
            return Response(
                        data= {
                            'message': 'Preencha todos os parâmetros corretamente: latitude, longitude, data_model_name, startDate, finalDate.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        try:
            startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
            finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                        data={
                            'message': 'As datas devem estar no formato YYYY-MM-DD.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                )

        try:
            pixel = Pixel.objects.get(latitude=lat, longitude=lon)
        except Pixel.DoesNotExist:
            return Response(
                        data = {
                            'message': 'As coordenadas fornecidas não representam nenhum pixel disponível.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        try:
            data_model = DataModel.objects.get(name=data_model_name)
        except DataModel.DoesNotExist:
            return Response(
                        data = {
                            'message': 'O data_model_name fornecido não existe.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        pixel_data_queryset = PixelData.objects.filter(
                        pixel=pixel,
                        data_model=data_model,
                        date__gte=startDate,
                        date__lte=finalDate
                    )
        
        deltadays = (finalDate - startDate).days

        if pixel_data_queryset.count() < deltadays:
            if data_model_name.lower() == 'chirps':
                retrieved_data = retrieveChirpsData(pixel, startDate, finalDate)

                if retrieved_data['status'] == 200:
                    # Tratar os dados e salvar no banco.
                    chirps_data = retrieved_data['data']

                    for data in chirps_data:
                        date = datetime.datetime.strptime(data['date'], '%m/%Y').date()
                        precip = data['value']['avg'] # RESOLVER ESSA QUESTÃO DOS VÁRIOS TIPOS DE VALORES

                        data_pixel, created = PixelData.objects.get_or_create(
                                                pixel=pixel,
                                                data_model=data_model,
                                                date=date,
                                                precip=precip
                                            )
                        
                    pixel_data_queryset = PixelData.objects.filter(
                        pixel=pixel,
                        data_model=data_model,
                        date__gte=startDate,
                        date__lte=finalDate
                    )
                else:
                    return Response(data=retrieved_data)

        serializer = PixelDataSerializer(pixel_data_queryset, many=True)

        return Response(data=serializer.data)


    def post(self, request):

        # Get parameters to filter Pixel and DataModel
        try:
            lat = request.data['latitude']
            lon = request.data['longitude']
            data_model_name = request.data['data_model_name']
            date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d')
        except KeyError:
            return Response(
                    data={'message': 'Preencha todos os parâmetros corretamente: latitude, longitude, data_model_name, date, e as variáveis.'}
            )

        pixel = Pixel.objects.get(latitude=lat, longitude=lon)
        data_model = DataModel.objects.get(name=data_model_name)

        # Verify if the PixelData already exists
        queryset = PixelData.objects.filter(
                    pixel=pixel,
                    data_model=data_model,
                    date=date,
        )

        if queryset.count() != 0:
            print(queryset)
            return Response(
                    data={'message': 'Já existe um dado com as coordenadas e data fornecida.'}
            )

        serializer = PixelDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                pixel=pixel,
                data_model=data_model
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def test():
        {
            "latitude": -20.75,
            "longitude": -41.85,
            "data_model_name": "Chirps",
            "date": "2006-01-01",
            "evapo": 4.955981731414795,
            "minTemp": 18.73649024963379,
            "maxTemp": 27.216341018676758,
            "ocis": 268.4227294921875,
            "precip": 11.016281127929688,
            "rnof": 0.6231554746627808,
            "tp2m": 22.5782413482666
        }

        a = '/api2/pixeldata/?latitude=20.75&longitude=-41.85&data_model_name=Chirps&startDate=2006-01-01&finalDate=2006-01-05'
        

        

    
