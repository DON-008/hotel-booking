from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import uuid

class Customer(models.Model):
    """Customer model for hotel booking system"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} ({self.phone})"

class CustomerProfile(models.Model):
    """Extended customer profile with additional information"""
    
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True, null=True)
    is_vip = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Profile for {self.customer.name}"