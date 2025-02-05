from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VehicleMake, VehicleModel, Vehicle, Windscreen, InsuranceProvider
from .serializers import VehicleMakeSerializer, VehicleModelSerializer, WindscreenSerializer, InsuranceProviderSerializer

class VehicleDetailsAPIView(APIView):
    def post(self, request):
        number_plate = request.data.get('numberPlate')
        year_of_make = request.data.get('yearOfMake')

        # Retrieve data from the database
        windscreen_types = Windscreen.objects.all()
        vehicle_makes = VehicleMake.objects.all()
        vehicle_models = VehicleModel.objects.all()
        insurance_providers = InsuranceProvider.objects.all()

        # Serialize the data
        windscreen_data = WindscreenSerializer(windscreen_types, many=True).data
        vehicle_makes_data = VehicleMakeSerializer(vehicle_makes, many=True).data
        vehicle_models_data = VehicleModelSerializer(vehicle_models, many=True).data
        insurance_providers_data = InsuranceProviderSerializer(insurance_providers, many=True).data

        return Response({
            'windscreenTypes': windscreen_data,
            'vehicleMakes': vehicle_makes_data,
            'vehicleModels': vehicle_models_data,
            'insuranceProviders': insurance_providers_data
        }, status=status.HTTP_200_OK)

class GenerateQuoteAPIView(APIView):
    def post(self, request):
        number_plate = request.data.get('numberPlate')
        year_of_make = request.data.get('yearOfMake')
        windscreen_type = request.data.get('windscreenType')
        make = request.data.get('make')
        model = request.data.get('model')
        insurance_provider = request.data.get('insuranceProvider')

        # Simulated quote calculation from database values
        insurance = InsuranceProvider.objects.filter(name=insurance_provider).first()
        insurance_cost = insurance.cost if insurance else "N/A"

        quote = f"Estimated cost for {make} {model} ({year_of_make}): {insurance_cost} USD"
        windscreen_status = Windscreen.objects.filter(type=windscreen_type, model=model).exists()

        return Response({
            'quote': quote,
            'windscreenStatus': windscreen_status
        }, status=status.HTTP_200_OK)
