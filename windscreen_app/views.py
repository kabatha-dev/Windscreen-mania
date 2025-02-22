from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework import status
from .models import (
    InsuranceProvider, Vehicle, Service, Quote, Order, VehicleMake,
    VehicleModel, WindscreenCustomization, WindscreenType, UserDetails
)
from .serializers import (
    InsuranceProviderSerializer, VehicleMakeSerializer, VehicleModelSerializer, VehicleSerializer,
    ServiceSerializer, QuoteSerializer, OrderSerializer, WindscreenCustomizationSerializer, WindscreenTypeSerializer
)
import uuid
from rest_framework.generics import ListAPIView
from .serializers import QuoteSerializer, OrderSerializer
from rest_framework.decorators import action

class RegisterVehicleAPIView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = serializer.save()
            services = Service.objects.all()
            return Response({
                "message": "Vehicle registered successfully!",
                "services": ServiceSerializer(services, many=True).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateQuoteAPIView(APIView):
    def post(self, request):
        vehicle_id = request.data.get("vehicle_id")
        service_ids = request.data.get("selected_services", [])

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            services = Service.objects.filter(id__in=service_ids)

            if not services.exists():
                return Response({"error": "Invalid services selected"}, status=status.HTTP_400_BAD_REQUEST)

            total_cost = sum(service.cost for service in services)
            quote_number = str(uuid.uuid4())[:8]

            quote = Quote.objects.create(
                quote_number=quote_number,
                vehicle=vehicle,
                total_cost=total_cost
            )
            quote.services.set(services)

            return Response({"quote_number": quote.quote_number, "total_cost": total_cost}, status=status.HTTP_201_CREATED)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

class ApproveQuoteAPIView(APIView):
    def post(self, request, quote_number):
        try:
            quote = Quote.objects.get(quote_number=quote_number)
            quote.status = "Approved"
            quote.save()

            order_number = str(uuid.uuid4())[:8]
            order = Order.objects.create(order_number=order_number, quote=quote, status="Working Progress")

            return Response({"order_number": order.order_number, "status": order.status}, status=status.HTTP_201_CREATED)
        except Quote.DoesNotExist:
            return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

class GetServicesAPIView(APIView):
    def get(self, request):
        services = Service.objects.all()
        return Response(ServiceSerializer(services, many=True).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def vehicle_makes(request):
    makes = VehicleMake.objects.all()
    serializer = VehicleMakeSerializer(makes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vehicle_models(request, make_id):
    models = VehicleModel.objects.filter(make_id=make_id)
    serializer = VehicleModelSerializer(models, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def windscreen_types(request):
    types = WindscreenType.objects.all()
    serializer = WindscreenTypeSerializer(types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def windscreen_customizations(request, type_id):
    customizations = WindscreenCustomization.objects.filter(windscreen_type_id=type_id)
    serializer = WindscreenCustomizationSerializer(customizations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def insurance_providers(request):
    providers = InsuranceProvider.objects.all()
    serializer = InsuranceProviderSerializer(providers, many=True)
    return Response(serializer.data)

class SubmitServiceAPIView(APIView):
    def post(self, request):
        user_details_data = request.data.get("user_details", {})
        selected_services = request.data.get("selected_services", [])

        # Validate required fields
        required_fields = ["fullName", "kraPin", "phone"]
        if any(not user_details_data.get(field) for field in required_fields):
            return Response({"error": "Missing required user details"}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create user details
        user_details, _ = UserDetails.objects.get_or_create(
            full_name=user_details_data.get("fullName"),
            kra_pin=user_details_data.get("kraPin"),
            phone=user_details_data.get("phone")
        )

        # Validate selected services
        services = Service.objects.filter(id__in=selected_services)
        if not services.exists():
            return Response({"error": "Invalid services selected"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total cost
        total_cost = sum(service.cost for service in services)

        # Create a quote (without vehicle)
        quote = Quote.objects.create(
            quote_number=str(uuid.uuid4())[:8],
            total_cost=total_cost
        )
        quote.services.set(services)

        return Response(
            {
                "message": "Service request submitted successfully!",
                "quote_number": quote.quote_number,
                "total_cost": total_cost,
            },
            status=status.HTTP_201_CREATED,
        )
    

class GetQuotesAPIView(APIView):
    def get(self, request):
        quotes = Quote.objects.exclude(status="Rejected")  # Exclude rejected quotes
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateQuoteStatusAPIView(APIView):
    def post(self, request, quote_number):
        try:
            quote = Quote.objects.get(quote_number=quote_number)
            new_status = request.data.get("status", "").capitalize()

            if new_status not in ["Approved", "Rejected", "Pending"]:
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            quote.status = new_status
            quote.save()

            # If the quote is approved, create an order
            if new_status == "Approved":
                order_number = str(uuid.uuid4())[:8]
                Order.objects.create(order_number=order_number, quote=quote, status="Working Progress")
            
            return Response({"message": f"Quote {quote_number} updated to {new_status}"}, status=status.HTTP_200_OK)
        
        except Quote.DoesNotExist:
            return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)
        


class GetApprovedOrdersAPIView(ListAPIView):
    queryset = Order.objects.filter(quote__status="Approved")
    serializer_class = OrderSerializer  


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        quote = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['Approved', 'Rejected', 'Pending']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        quote.status = new_status
        quote.save()

        # Create an order if quote is approved
        if new_status == 'Approved' and not Order.objects.filter(quote=quote).exists():
            Order.objects.create(quote=quote, order_number=f"ORD-{quote.quote_number}")

        return Response(QuoteSerializer(quote).data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer          
