from rest_framework import serializers
from windscreen_app.models import (
    Vehicle, Service, VehicleMake, VehicleModel, WindscreenCustomization, 
    WindscreenType, InsuranceProvider, Quote, Order, WorkProgress, 
    UserDetails, Invoice, StatementOfAccount
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
    vehicle = VehicleSerializer(read_only=True)  # ✅ Nested serializer to return full vehicle details
    services = ServiceSerializer(many=True, read_only=True)  # ✅ Nested services

    class Meta:
        model = Quote
        fields = '__all__'

    def update(self, instance, validated_data):
        """Handles updating the quote and auto-creating an order if approved."""
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()

            # ✅ Ensure an order is created only once per approved quote
            if instance.status == 'Approved' and not Order.objects.filter(quote=instance).exists():
                Order.objects.create(quote=instance, order_number=f"ORD-{instance.quote_number}")
                print(f"✅ Order created for Quote: {instance.quote_number}")  
            else:
                print(f"⚠️ Order already exists or quote is not approved: {instance.quote_number}")

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
        """Returns a list of service names for the quote associated with the order."""
        return [service.name for service in obj.quote.services.all()]


class WorkProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkProgress
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class StatementOfAccountSerializer(serializers.ModelSerializer):
    invoices = serializers.SerializerMethodField()  # ✅ Fetch related invoices

    class Meta:
        model = StatementOfAccount
        fields = '__all__'

    def get_invoices(self, obj):
        """Fetches invoices related to the statement of account."""
        invoices = Invoice.objects.filter(statement_of_account=obj)
        return InvoiceSerializer(invoices, many=True).data
