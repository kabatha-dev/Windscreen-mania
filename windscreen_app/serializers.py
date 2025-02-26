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


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()

            # If approved, create an order
            if instance.status == 'Approved':
                Order.objects.create(quote=instance, order_number=f"ORD-{instance.quote_number}")

        return instance
    
class OrderSerializer(serializers.ModelSerializer):
    quote_number = serializers.CharField(source="quote.quote_number", read_only=True)
    services = serializers.SerializerMethodField()
    total_cost = serializers.DecimalField(source="quote.total_cost", max_digits=10, decimal_places=2, read_only=True)
    approval_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = ['order_number', 'quote_number', 'services', 'total_cost', 'approval_time']

    def get_services(self, obj):
        return [service.name for service in obj.quote.services.all()]



   