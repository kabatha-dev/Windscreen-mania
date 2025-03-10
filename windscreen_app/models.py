from django.db import models
from django.utils import timezone  
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from django.core.validators import FileExtensionValidator




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
    vehicle_model = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, related_name="vehicles", null=True, blank=True
    )  


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

    quote_number = models.CharField(max_length=255, unique=True, blank=True)
    vehicle = models.ForeignKey("Vehicle", on_delete=models.SET_NULL, related_name="quotes", null=True, blank=True)
    registration_number = models.CharField(max_length=15, blank=True)
    make = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    services = models.ManyToManyField("Service", blank=True)
    windscreen_type = models.ForeignKey("WindscreenType", on_delete=models.SET_NULL, related_name="quotes", null=True, blank=True)
    windscreen_customization = models.ForeignKey("WindscreenCustomization", on_delete=models.SET_NULL, related_name="quotes", null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.quote_number

    def save(self, *args, **kwargs):
        """Auto-generate quote_number and fetch vehicle details."""
        if not self.quote_number:
            self.quote_number = f"QT-{get_random_string(5).upper()}"

        if self.vehicle:
            self.registration_number = self.vehicle.registration_number
            if self.vehicle.vehicle_model:
                self.make = self.vehicle.vehicle_model.make.name
                self.model = self.vehicle.vehicle_model.model
            else:
                self.make = "Unknown"
                self.model = "Unknown"

        super().save(*args, **kwargs)  # Save first before adding ManyToMany relations

    def approve(self):
        """Approve the quote and create an order if it doesn’t exist."""
        if self.status != "Approved":
            self.status = "Approved"
            self.save()
            Order.objects.get_or_create(quote=self, order_number=f"ORD-{self.quote_number}")



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

