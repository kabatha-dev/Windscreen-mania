from django.db import models
from django.utils import timezone  
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.core.validators import FileExtensionValidator

from windscreen_app.serializers import WorkProgressSerializer


class VehicleMake(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, related_name='models')
    model = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.make.name} - {self.model}"

class WindscreenType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class WindscreenCustomization(models.Model):
    windscreen_type = models.ForeignKey(WindscreenType, on_delete=models.CASCADE, related_name='customizations')
    customization_details = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.windscreen_type.name} - {self.customization_details}"

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class UserDetails(models.Model):
    full_name = models.CharField(max_length=255)
    kra_pin = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name    
  

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=15, unique=True)
    year_of_make = models.IntegerField()

    def __str__(self):
        return self.registration_number

class Service(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

        
class Quote(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    quote_number = models.CharField(max_length=255, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="quotes", default=140)
    services = models.ManyToManyField('Service')
    windscreen_type = models.ForeignKey(WindscreenType, on_delete=models.CASCADE, related_name="quotes", default=57)
    windscreen_customization = models.ForeignKey(WindscreenCustomization, on_delete=models.CASCADE, related_name="qoutes", default=52)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.quote_number

    def approve(self):
        if self.status != "Approved":
            self.status = "Approved"
            self.save()
            if not hasattr(self, "order"):  # Prevent duplicate orders
                order_number = f"ORD-{self.quote_number}"
                Order.objects.create(quote=self, order_number=order_number)


class Order(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name="order")
    order_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default="Pending")  
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"Order from Quote {self.quote.quote_number}"

   


class WorkProgress(models.Model):
    vehicle_reg_no = models.CharField(max_length=20, blank=True, null= True)
    description = models.TextField()
    image1 = models.ImageField(upload_to='work_progress/', blank=True, null=True)
    image2 = models.ImageField(upload_to='work_progress/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='work_progress/', 
                                validators=[FileExtensionValidator(['pdf'])], 
                                blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_reg_no
    

class WorkProgressViewSet(viewsets.ModelViewSet):
    queryset = WorkProgress.objects.all().order_by('-created_at')
    serializer_class = WorkProgressSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Optional: Endpoint to filter by vehicle registration number
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_by_vehicle(self, request):
        reg_no = request.query_params.get('vehicle_reg_no')
        if reg_no:
            queryset = self.get_queryset().filter(vehicle_reg_no=reg_no)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "Please provide a vehicle_reg_no parameter."}, 
                        status=status.HTTP_400_BAD_REQUEST)    

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid','Paid'),
        ('Unpaid','Unpaid'),
    ]

    invoice_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=255)
    vehicle_registration = models.CharField(max_length=20)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    services = models.JSONField()  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"
    

class StatementOfAccount(models.Model):
    customer_name = models.CharField(max_length=255)
    invoices = models.ManyToManyField(Invoice)  # One statement links to multiple invoices
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_payment_date = models.DateField(null=True, blank=True)

    def update_total_due(self):
        """Calculate total unpaid amount for the customer."""
        self.total_due = sum(invoice.total_amount for invoice in self.invoices.filter(status='Unpaid'))
        self.save()

    def __str__(self):
        return f"Statement for {self.customer_name} - Due: {self.total_due}"
