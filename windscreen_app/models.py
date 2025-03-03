from django.db import models
from django.utils import timezone  
from django.core.validators import FileExtensionValidator


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
    registration_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.quote_number

    def approve(self):
        if self.status != "Approved":
            self.status = "Approved"
            self.save()
            if not hasattr(self, "order"):  # Prevent duplicate orders
                from .models import Order
                order_number = f"ORD-{self.quote_number}"
                Order.objects.create(quote=self, order_number=order_number)


class Order(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True)
    approval_time = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField(Service, related_name="orders")  

    def __str__(self):
        return f"Order {self.order_number} - Services: {', '.join(service.name for service in self.services.all())}"


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
  
class WorkProgress(models.Model):
    vehicle_reg_no = models.CharField(max_length=20)
    description = models.TextField()
    image1 = models.ImageField(upload_to='work_progress/', blank=True, null=True)
    image2 = models.ImageField(upload_to='work_progress/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='work_progress/', 
                                validators=[FileExtensionValidator(['pdf'])], 
                                blank=True, null=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="work_progress",null=True,blank=True)  # Added Order
    services = models.ManyToManyField("Service", related_name="work_progress")  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_reg_no} - Order: {self.order.order_number} - Services: {', '.join(service.name for service in self.services.all())}"

   


#invoice model
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid','Paid'),
        ('overdue','Overdue'),
    ]
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'Mpesa'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
    ]

    invoice_number = models.CharField(max_length=255, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    customer = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='invoices')
    services = models.ManyToManyField(Service)
    total_cost = models.DecimalField(max_digits=10,decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unpaid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date= models.DateTimeField(auto_now_add=True)
    due_date=models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.unpaid_amount = self.total_cost - self.paid_amount
        if self.unpaid_amount <= 0:
            self.status = 'paid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.full_name}"

#statement of account model
class StatementOfAccount(models.Model):
    customer = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="statements")
    statement_period_start = models.DateField()
    statement_period_end = models.DateField()
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    total_invoiced = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transactions = models.ManyToManyField(Invoice)
    generated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.closing_balance = self.opening_balance + self.total_invoiced - self.total_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Statement ({self.statement_period_start} - {self.statement_period_end}) for {self.customer.full_name}"

