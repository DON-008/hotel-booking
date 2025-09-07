from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Customer, CustomerProfile
from .serializers import (
    CustomerSerializer, 
    CustomerDetailSerializer, 
    CustomerCreateSerializer,
    CustomerProfileSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer model"""
    
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerSerializer
    
    def get_queryset(self):
        """Filter customers based on query parameters"""
        queryset = Customer.objects.all()
        
        # Filter by name
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Filter by phone
        phone = self.request.query_params.get('phone', None)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        
        # Filter by email
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search customers by various criteria"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        customers = Customer.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(phone__icontains=query) |
            models.Q(email__icontains=query)
        )
        
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def special_dates(self, request, pk=None):
        """Get special dates for a customer"""
        customer = self.get_object()
        special_dates = customer.special_dates.all()
        
        from events.serializers import SpecialDateSerializer
        serializer = SpecialDateSerializer(special_dates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def game_status(self, request, pk=None):
        """Check if customer has played the spin wheel game"""
        customer = self.get_object()
        
        try:
            game_session = customer.game_session
            return Response({
                'has_played': game_session.has_played,
                'first_play_date': game_session.first_play_date
            })
        except:
            return Response({
                'has_played': False,
                'first_play_date': None
            })

class CustomerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for CustomerProfile model"""
    
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    @action(detail=True, methods=['patch'])
    def update_preferences(self, request, pk=None):
        """Update customer preferences"""
        profile = self.get_object()
        preferences = request.data.get('preferences', {})
        
        if isinstance(preferences, dict):
            profile.preferences.update(preferences)
            profile.save()
            return Response({'message': 'Preferences updated successfully'})
        
        return Response({'error': 'Preferences must be a valid JSON object'}, 
                       status=status.HTTP_400_BAD_REQUEST)