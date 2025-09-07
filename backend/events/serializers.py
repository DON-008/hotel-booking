from rest_framework import serializers
from .models import SpecialDate, Event, EventBooking
from customer_management.serializers import CustomerSerializer

class SpecialDateSerializer(serializers.ModelSerializer):
    """Serializer for SpecialDate model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    
    class Meta:
        model = SpecialDate
        fields = ['id', 'customer', 'customer_name', 'customer_phone', 'special_date_type', 
                 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'start_date', 'end_date',
                 'capacity', 'current_bookings', 'available_spots', 'is_full', 'price',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_bookings', 'created_at', 'updated_at']

class EventBookingSerializer(serializers.ModelSerializer):
    """Serializer for EventBooking model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = EventBooking
        fields = ['id', 'event', 'event_title', 'customer', 'customer_name', 
                 'booking_date', 'number_of_guests', 'total_price', 'status', 'notes']
        read_only_fields = ['id', 'booking_date']

class EventDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Event with bookings"""
    
    bookings = EventBookingSerializer(many=True, read_only=True)
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'start_date', 'end_date',
                 'capacity', 'current_bookings', 'available_spots', 'is_full', 'price',
                 'is_active', 'bookings', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_bookings', 'created_at', 'updated_at']
