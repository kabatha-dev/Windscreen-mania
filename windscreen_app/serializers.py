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
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.Meta.model = apps.get_model('windscreen_app', 'Quote')
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        Order = apps.get_model('windscreen_app', 'Order')  # Lazy reference

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
        model = None  # Temporarily set to None
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

