from django.urls import path, include
from rest_framework.routers import DefaultRouter
from windscreen_app import views
from windscreen_app.views import (
    RegisterVehicleAPIView, GenerateQuoteAPIView, GetServicesAPIView, 
    SubmitServiceAPIView, GetQuotesAPIView, GetApprovedOrdersAPIView, 
    ApproveQuoteAPIView, CreateOrderAPIView, SubmitWorkProgressAPIView, 
    StatementOfAccountViewSet,InvoiceViewSet
)

# Initialize the router
router = DefaultRouter()

# Register ViewSets
router.register(r'statements', StatementOfAccountViewSet, basename="statement-of-account")
router.register(r'invoices', InvoiceViewSet, basename="invoice")

urlpatterns = [
    path('api/', include(router.urls)),  # Includes all router-based endpoints
    
    # Function-based views
    path('api/vehicle-makes/', views.vehicle_makes, name='vehicle-makes'),
    path('api/vehicle-models/<int:make_id>/', views.vehicle_models, name='vehicle-models'),
    path('api/windscreen-types/', views.windscreen_types, name='windscreen-types'),
    path('api/windscreen-customizations/<int:type_id>/', views.windscreen_customizations, name='windscreen-customizations'),
    path('api/insurance-providers/', views.insurance_providers, name='insurance-providers'),

    # Class-based API views
    path('api/register-vehicle/', RegisterVehicleAPIView.as_view(), name='register-vehicle'),
    path('api/generate-quote/', GenerateQuoteAPIView.as_view(), name='generate-quote'),
    path('api/get-services/', GetServicesAPIView.as_view(), name='get-services'),
    path('api/submit-service/', SubmitServiceAPIView.as_view(), name='submit-service'),
    path('api/get-quotes/', GetQuotesAPIView.as_view(), name='get-quotes'),
    path('api/orders/', GetApprovedOrdersAPIView.as_view(), name='get-approved-orders'),
    path('api/quotes/<int:pk>/update-status/', ApproveQuoteAPIView.as_view(), name='update-quote-status'),
    path('api/orders/create/', CreateOrderAPIView.as_view(), name='create-order'),
    path('api/work-progress/submit/', SubmitWorkProgressAPIView.as_view(), name='submit-work-progress'),
]
