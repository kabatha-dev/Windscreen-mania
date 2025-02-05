from rest_framework import serializers
from .models import VehicleMake, VehicleModel, Windscreen, InsuranceProvider

class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        fields = '__all__'

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'

class WindscreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Windscreen
        fields = '__all__'

class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'
