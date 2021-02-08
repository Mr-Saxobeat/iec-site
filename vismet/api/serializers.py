from rest_framework import serializers
from vismet.models import CityData, PixelData


class CityDataSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    data_model = serializers.StringRelatedField()
    
    class Meta:
        model = CityData
        fields = '__all__'

class PixelDataSerializer(serializers.ModelSerializer):
    pixel = serializers.StringRelatedField()
    data_model = serializers.StringRelatedField()

    class Meta:
        model = PixelData
        fields = '__all__'