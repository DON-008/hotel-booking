from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import datetime, timedelta
from .models import SpecialDate, Event, EventBooking
from .serializers import (
    SpecialDateSerializer, 
    EventSerializer, 
    EventDetailSerializer,
    EventBookingSerializer
)

class SpecialDateViewSet(viewsets.ModelViewSet):
    """ViewSet for SpecialDate model"""
    
    queryset = SpecialDate.objects.all()
    serializer_class = SpecialDateSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_queryset(self):
        """Filter special dates based on query parameters"""
        queryset = SpecialDate.objects.all()
        
        # Filter by special date type
        date_type = self.request.query_params.get('type', None)
        if date_type:
            queryset = queryset.filter(special_date_type=date_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming special dates"""
        today = timezone.now().date()
        upcoming_dates = SpecialDate.objects.filter(date__gte=today).order_by('date')
        
        serializer = self.get_serializer(upcoming_dates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def this_month(self, request):
        """Get special dates for this month"""
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        # Calculate end of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        this_month_dates = SpecialDate.objects.filter(
            date__gte=start_of_month,
            date__lte=end_of_month
        ).order_by('date')
        
        serializer = self.get_serializer(this_month_dates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics for special dates"""
        total_dates = SpecialDate.objects.count()
        birthday_count = SpecialDate.objects.filter(special_date_type='Birthday').count()
        anniversary_count = SpecialDate.objects.filter(special_date_type='Wedding Anniversary').count()
        other_count = SpecialDate.objects.filter(special_date_type='Other').count()
        
        return Response({
            'total_dates': total_dates,
            'birthday_count': birthday_count,
            'anniversary_count': anniversary_count,
            'other_count': other_count
        })

class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event model"""
    
    queryset = Event.objects.all()
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer
    
    def get_queryset(self):
        """Filter events based on query parameters"""
        queryset = Event.objects.all()
        
        # Filter by event type
        event_type = self.request.query_params.get('type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """Book an event"""
        event = self.get_object()
        customer_id = request.data.get('customer_id')
        number_of_guests = request.data.get('number_of_guests', 1)
        
        if not customer_id:
            return Response({'error': 'Customer ID is required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if event has available spots
        if event.available_spots < number_of_guests:
            return Response({'error': 'Not enough available spots'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create booking
        total_price = event.price * number_of_guests
        booking = EventBooking.objects.create(
            event=event,
            customer_id=customer_id,
            number_of_guests=number_of_guests,
            total_price=total_price
        )
        
        # Update event bookings count
        event.current_bookings += number_of_guests
        event.save()
        
        serializer = EventBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventBookingViewSet(viewsets.ModelViewSet):
    """ViewSet for EventBooking model"""
    
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_queryset(self):
        """Filter bookings based on query parameters"""
        queryset = EventBooking.objects.all()
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # Filter by event
        event_id = self.request.query_params.get('event_id', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset