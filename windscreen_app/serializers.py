from rest_framework import serializers
from .models import (
    InsuranceProvider, Vehicle, Service, Quote, Order,
    VehicleMake, VehicleModel, WindscreenCustomization, WindscreenType
)

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        fields = ['id', 'name']


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'


class WindscreenCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindscreenCustomization
        fields = '__all__'


class WindscreenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindscreenType
        fields = '__all__'


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
   