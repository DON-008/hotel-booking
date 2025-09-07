from django.contrib import admin
from .models import Customer, CustomerProfile

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'birth_date', 'created_at']
    list_filter = ['created_at', 'birth_date']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'country', 'is_vip']
    list_filter = ['is_vip', 'city', 'country']
    search_fields = ['customer__name', 'customer__phone', 'city', 'country']
    readonly_fields = ['id']