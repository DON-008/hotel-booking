from django.db import models
from customer_management.models import Customer
import uuid

class SpecialDate(models.Model):
    """Special dates for customers (birthdays, anniversaries, etc.)"""
    
    SPECIAL_DATE_TYPES = [
        ('Birthday', 'Birthday'),
        ('Wedding Anniversary', 'Wedding Anniversary'),
        ('Anniversary', 'Anniversary'),
        ('Other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='special_dates')
    special_date_type = models.CharField(max_length=20, choices=SPECIAL_DATE_TYPES)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Special Date'
        verbose_name_plural = 'Special Dates'
    
    def __str__(self):
        return f"{self.customer.name} - {self.special_date_type} ({self.date})"

class Event(models.Model):
    """Hotel events and activities"""
    
    EVENT_TYPES = [
        ('Restaurant', 'Restaurant'),
        ('Bar', 'Bar'),
        ('Conference', 'Conference'),
        ('Wedding', 'Wedding'),
        ('Party', 'Party'),
        ('Other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    current_bookings = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return f"{self.title} ({self.start_date.date()})"
    
    @property
    def available_spots(self):
        return self.capacity - self.current_bookings
    
    @property
    def is_full(self):
        return self.current_bookings >= self.capacity

class EventBooking(models.Model):
    """Bookings for events"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='event_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ], default='Confirmed')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Event Booking'
        verbose_name_plural = 'Event Bookings'
    
    def __str__(self):
        return f"{self.customer.name} - {self.event.title}"