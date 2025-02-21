from django.urls import path
from windscreen_app.views import GetQuotesAPIView, GetServicesAPIView, RegisterVehicleAPIView, GenerateQuoteAPIView, ApproveQuoteAPIView, SubmitServiceAPIView
from windscreen_app import views

urlpatterns = [
    path('register-vehicle/', RegisterVehicleAPIView.as_view(), name='register-vehicle'),
    path('generate-quote/', GenerateQuoteAPIView.as_view(), name='generate-quote'),
    path('approve-quote/<str:quote_number>/', ApproveQuoteAPIView.as_view(), name='approve-quote'),
     path('get-services/', GetServicesAPIView.as_view(), name='get-services'),
     path('vehicle-makes/', views.vehicle_makes, name='vehicle-makes'),
    path('vehicle-models/<int:make_id>/', views.vehicle_models, name='vehicle-models'),
    path('windscreen-types/', views.windscreen_types, name='windscreen-types'),
    path('windscreen-customizations/<int:type_id>/', views.windscreen_customizations, name='windscreen-customizations'),
    path('insurance-providers/', views.insurance_providers, name='insurance-providers'),
    path('submit-service/', SubmitServiceAPIView.as_view(), name='submit-service'),
    path('get-quotes/', GetQuotesAPIView.as_view(), name='get-quotes'),  # New API for fetching quotes
         
]
