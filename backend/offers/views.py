from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Offer, OfferUsage
from .serializers import (
    OfferSerializer, 
    OfferDetailSerializer, 
    OfferCreateSerializer,
    OfferUsageSerializer
)

class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for Offer model"""
    
    queryset = Offer.objects.all()
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OfferCreateSerializer
        elif self.action == 'retrieve':
            return OfferDetailSerializer
        return OfferSerializer
    
    def get_queryset(self):
        """Filter offers based on query parameters"""
        queryset = Offer.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by offer type
        offer_type = self.request.query_params.get('type', None)
        if offer_type:
            queryset = queryset.filter(offer_type=offer_type)
        
        # Filter by active offers only
        active_only = self.request.query_params.get('active_only', None)
        if active_only and active_only.lower() == 'true':
            today = timezone.now().date()
            queryset = queryset.filter(
                status='active',
                valid_from__lte=today,
                valid_to__gte=today
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active offers"""
        today = timezone.now().date()
        active_offers = Offer.objects.filter(
            status='active',
            valid_from__lte=today,
            valid_to__gte=today
        )
        
        serializer = self.get_serializer(active_offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get all expired offers"""
        today = timezone.now().date()
        expired_offers = Offer.objects.filter(valid_to__lt=today)
        
        serializer = self.get_serializer(expired_offers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def use(self, request, pk=None):
        """Use an offer"""
        offer = self.get_object()
        customer_id = request.data.get('customer_id')
        
        if not customer_id:
            return Response({'error': 'Customer ID is required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if offer is valid and available
        if not offer.is_valid:
            return Response({'error': 'Offer is not valid'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        if not offer.is_available:
            return Response({'error': 'Offer is not available'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if customer has already used this offer
        if OfferUsage.objects.filter(offer=offer, customer_id=customer_id).exists():
            return Response({'error': 'Customer has already used this offer'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create offer usage
        discount_applied = offer.discount_value
        usage = OfferUsage.objects.create(
            offer=offer,
            customer_id=customer_id,
            discount_applied=discount_applied
        )
        
        # Update offer usage count
        offer.current_usage += 1
        offer.save()
        
        serializer = OfferUsageSerializer(usage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get offer statistics"""
        total_offers = Offer.objects.count()
        active_offers = Offer.objects.filter(status='active').count()
        expired_offers = Offer.objects.filter(status='expired').count()
        total_usage = OfferUsage.objects.count()
        
        return Response({
            'total_offers': total_offers,
            'active_offers': active_offers,
            'expired_offers': expired_offers,
            'total_usage': total_usage
        })

class OfferUsageViewSet(viewsets.ModelViewSet):
    """ViewSet for OfferUsage model"""
    
    queryset = OfferUsage.objects.all()
    serializer_class = OfferUsageSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_queryset(self):
        """Filter offer usages based on query parameters"""
        queryset = OfferUsage.objects.all()
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # Filter by offer
        offer_id = self.request.query_params.get('offer_id', None)
        if offer_id:
            queryset = queryset.filter(offer_id=offer_id)
        
        return queryset