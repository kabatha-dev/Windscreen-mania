from django.db import models
from django.utils import timezone  

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
    services = models.ManyToManyField('Service')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.quote_number


class Order(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True)
    approval_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order from Quote {self.quote.quote_number}"

    
   

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
  
