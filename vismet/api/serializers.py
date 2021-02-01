from rest_framework import serializers
from vismet.models import CityData

class CityDataSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    data_model = serializers.StringRelatedField()
    
    class Meta:
        model = CityData
        fields = '__all__'