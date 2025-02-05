from django.contrib import admin
from .models import (
    Category, InsuranceProvider, WindscreenCategory, 
    Windscreen, VehicleMake, VehicleModel, Vehicle
)

admin.site.register(Category)
admin.site.register(InsuranceProvider)
admin.site.register(WindscreenCategory)
admin.site.register(Windscreen)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)
admin.site.register(Vehicle)
