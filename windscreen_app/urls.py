from django.urls import path
from .views import VehicleDetailsAPIView, GenerateQuoteAPIView

urlpatterns = [
    path('vehicle-details/', VehicleDetailsAPIView.as_view(), name='vehicle-details'),
    path('generate-quote/', GenerateQuoteAPIView.as_view(), name='generate-quote'),
]
