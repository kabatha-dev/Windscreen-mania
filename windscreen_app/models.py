from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_type = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WindscreenCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Windscreen(models.Model):
    type = models.CharField(max_length=255)
    category = models.ForeignKey(WindscreenCategory, related_name='windscreens', on_delete=models.CASCADE)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} - {self.make} {self.model}"

class VehicleMake(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    make = models.ForeignKey(VehicleMake, related_name='models', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.make.name} {self.name}"

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=15, unique=True)
    year_of_make = models.IntegerField()
    make = models.ForeignKey(VehicleMake, related_name='vehicles', on_delete=models.CASCADE)
    model = models.ForeignKey(VehicleModel, related_name='vehicles', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.registration_number} ({self.make.name} {self.model.name}, {self.year_of_make})"
