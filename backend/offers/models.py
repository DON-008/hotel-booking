from django.db import models
from customer_management.models import Customer
import uuid

class Offer(models.Model):
    """Special offers and promotions"""
    
    OFFER_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    valid_from = models.DateField()
    valid_to = models.DateField()
    max_usage = models.PositiveIntegerField(null=True, blank=True)
    current_usage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
    
    def __str__(self):
        return f"{self.title} - {self.discount_value}{'%' if self.offer_type == 'percentage' else '$'}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.valid_from <= today <= self.valid_to and self.status == 'active'
    
    @property
    def is_available(self):
        if not self.is_valid:
            return False
        if self.max_usage is None:
            return True
        return self.current_usage < self.max_usage

class OfferUsage(models.Model):
    """Track usage of offers by customers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='usages')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='offer_usages')
    used_at = models.DateTimeField(auto_now_add=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-used_at']
        verbose_name = 'Offer Usage'
        verbose_name_plural = 'Offer Usages'
        unique_together = ['offer', 'customer']  # Each customer can use an offer only once
    
    def __str__(self):
        return f"{self.customer.name} used {self.offer.title}"