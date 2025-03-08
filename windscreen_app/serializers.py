from rest_framework import serializers
from django.apps import apps

from windscreen_app import models


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Vehicle')
        super().__init__(*args, **kwargs)



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Service')
        super().__init__(*args, **kwargs)


class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'name']

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'VehicleMake')
        super().__init__(*args, **kwargs)


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'VehicleModel')
        super().__init__(*args, **kwargs)


class WindscreenCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'WindscreenCustomization')
        super().__init__(*args, **kwargs)


class WindscreenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'WindscreenType')
        super().__init__(*args, **kwargs)


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'InsuranceProvider')
        super().__init__(*args, **kwargs)

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Dynamically assigned in __init__
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Quote')
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        Order = apps.get_model('windscreen_app', 'Order')  # Lazy reference

        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()

            # Ensure an order is created only once per approved quote
            if instance.status == 'Approved' and not Order.objects.filter(quote=instance).exists():
                Order.objects.create(quote=instance, order_number=f"ORD-{instance.quote_number}")
                print(f"✅ Order created for Quote: {instance.quote_number}")  # Debugging message
            else:
                print(f"⚠️ Order already exists or quote is not approved: {instance.quote_number}")

        return instance
    
class OrderSerializer(serializers.ModelSerializer):
    quote_number = serializers.CharField(source="quote.quote_number", read_only=True)
    services = serializers.SerializerMethodField()
    total_cost = serializers.DecimalField(source="quote.total_cost", max_digits=10, decimal_places=2, read_only=True)
    approval_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = None
        fields = ['order_number', 'quote_number', 'services', 'total_cost', 'approval_time']

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Order')
        super().__init__(*args, **kwargs)

    def get_services(self, obj):
        return [service.name for service in obj.quote.services.all()]


class WorkProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'WorkProgress')
        super().__init__(*args, **kwargs)



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = None 
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'UserDetails')
        super().__init__(*args, **kwargs)


class vehicle( serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'vehicle')
        super().__init__(*args, **kwargs)


class OrderByNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'        

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Invoice')  
        super().__init__(*args, **kwargs)

class StatementOfAccountSerializer(serializers.ModelSerializer):
    invoices = serializers.SerializerMethodField()  

    class Meta:
        model = None  
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'StatementOfAccount') 
        super().__init__(*args, **kwargs)

    def get_invoices(self, obj):
        Invoice = apps.get_model('windscreen_app', 'Invoice')  
        invoices = Invoice.objects.filter(statement_of_account=obj)
        return InvoiceSerializer(invoices, many=True).data