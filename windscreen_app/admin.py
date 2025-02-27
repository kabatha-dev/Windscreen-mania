from django.contrib import admin
from .models import (
    Vehicle, Service, Quote, Order, VehicleMake, VehicleModel,
    WindscreenType, WindscreenCustomization, InsuranceProvider, UserDetails
)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'year_of_make')
    search_fields = ('registration_number',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')
    search_fields = ('name',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_number', 'total_cost', 'status')
    search_fields = ('quote_number',)
    list_filter = ('status',)
    actions = ['approve_quotes']

    def approve_quotes(self, request, queryset):
        for quote in queryset:
            quote.approve()
        self.message_user(request, "Selected quotes have been approved.")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'quote', 'approval_time')
    search_fields = ('order_number', 'quote__quote_number')

@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model')
    search_fields = ('model',)
    list_filter = ('make',)

@admin.register(WindscreenType)
class WindscreenTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WindscreenCustomization)
class WindscreenCustomizationAdmin(admin.ModelAdmin):
    list_display = ('windscreen_type', 'customization_details')
    search_fields = ('customization_details',)
    list_filter = ('windscreen_type',)

@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'kra_pin', 'phone')
    search_fields = ('full_name', 'kra_pin', 'phone')
