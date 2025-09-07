from django.contrib import admin
from .models import SpecialDate, Event, EventBooking

@admin.register(SpecialDate)
class SpecialDateAdmin(admin.ModelAdmin):
    list_display = ['customer', 'special_date_type', 'date', 'created_at']
    list_filter = ['special_date_type', 'date', 'created_at']
    search_fields = ['customer__name', 'customer__phone', 'notes']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['date']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'capacity', 'current_bookings', 'is_active']
    list_filter = ['event_type', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'current_bookings', 'created_at', 'updated_at']
    ordering = ['-start_date']

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'event', 'booking_date', 'number_of_guests', 'status']
    list_filter = ['status', 'booking_date', 'event__event_type']
    search_fields = ['customer__name', 'event__title']
    readonly_fields = ['id', 'booking_date']
    ordering = ['-booking_date']