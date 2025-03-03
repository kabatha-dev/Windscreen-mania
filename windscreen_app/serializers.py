from rest_framework import serializers
from .models import (  # Import models explicitly
    Vehicle, Service, VehicleMake, VehicleModel, WindscreenCustomization, WindscreenType,
    InsuranceProvider, Quote, Order, WorkProgress, Invoice, StatementOfAccount
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
    registration_number = serializers.CharField(required=False, allow_null=True)  # Explicitly define it
    class Meta:
        model = Quote
        fields = ['id', 'quote_number', 'total_cost', 'status', 'registration_number', 'services']  # Explicitly include it


    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()

            # If approved, create an order
            if instance.status == 'Approved' and not Order.objects.filter(quote=instance).exists():
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


class WorkProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkProgress
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class StatementOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementOfAccount
        fields = '__all__'
