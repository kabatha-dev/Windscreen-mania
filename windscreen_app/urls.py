from django.urls import path,include
from windscreen_app.views import (
    CreateOrderAPIView, GetApprovedOrdersAPIView, GetOrderByIdAPIView, GetQuotesAPIView, GetServicesAPIView, 
    RegisterVehicleAPIView, GenerateQuoteAPIView, ApproveQuoteAPIView, SubmitServiceAPIView, SubmitWorkProgressAPIView,InvoiceViewSet,StatementOfAccountViewSet
)

from windscreen_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Invoices', InvoiceViewSet)
router.register(r'statements', StatementOfAccountViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
 
    path('register-vehicle/', RegisterVehicleAPIView.as_view(), name='register-vehicle'),
    path('get-vehicles/', RegisterVehicleAPIView.as_view(), name='get-vehicles'),  # Endpoint to get registered vehicles
    path('generate-quote/', GenerateQuoteAPIView.as_view(), name='generate-quote'),
    path('get-services/', GetServicesAPIView.as_view(), name='get-services'),
    path('vehicle-makes/', views.vehicle_makes, name='vehicle-makes'),
    path('vehicle-models/<int:make_id>/', views.vehicle_models, name='vehicle-models'),
    path('windscreen-types/', views.windscreen_types, name='windscreen-types'),
    path('windscreen-customizations/<int:type_id>/', views.windscreen_customizations, name='windscreen-customizations'),
    path('insurance-providers/', views.insurance_providers, name='insurance-providers'),
    path('submit-service/', SubmitServiceAPIView.as_view(), name='submit-service'),
    path('get-user-details/', SubmitServiceAPIView.as_view(), name='get-user-details'),  # Endpoint to get user details
    path('get-quotes/', GetQuotesAPIView.as_view(), name='get-quotes'),
    path('orders/', GetApprovedOrdersAPIView.as_view(), name='get-approved-orders'),
    path("quotes/<int:pk>/update-status/", ApproveQuoteAPIView.as_view(), name="update-quote-status"),
    path("orders/create/", CreateOrderAPIView.as_view(), name='create-order'),
    path('work-progress/submit/', SubmitWorkProgressAPIView.as_view(), name='submit-work-progress'),
    path('orders/<str:order_id>/', GetOrderByIdAPIView.as_view(), name='get-order-by-id'),
]

