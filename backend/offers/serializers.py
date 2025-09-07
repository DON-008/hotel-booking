from rest_framework import serializers
from .models import Offer, OfferUsage
from customer_management.serializers import CustomerSerializer

class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model"""
    
    is_valid = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'offer_type', 'discount_value', 
                 'status', 'valid_from', 'valid_to', 'max_usage', 'current_usage',
                 'is_valid', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_usage', 'created_at', 'updated_at']

class OfferUsageSerializer(serializers.ModelSerializer):
    """Serializer for OfferUsage model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    
    class Meta:
        model = OfferUsage
        fields = ['id', 'offer', 'offer_title', 'customer', 'customer_name',
                 'used_at', 'discount_applied', 'order_id']
        read_only_fields = ['id', 'used_at']

class OfferDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Offer with usage history"""
    
    usages = OfferUsageSerializer(many=True, read_only=True)
    is_valid = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'offer_type', 'discount_value', 
                 'status', 'valid_from', 'valid_to', 'max_usage', 'current_usage',
                 'is_valid', 'is_available', 'usages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_usage', 'created_at', 'updated_at']

class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new offers"""
    
    class Meta:
        model = Offer
        fields = ['title', 'description', 'offer_type', 'discount_value', 
                 'valid_from', 'valid_to', 'max_usage']
    
    def validate(self, data):
        """Validate offer data"""
        if data['valid_from'] >= data['valid_to']:
            raise serializers.ValidationError("Valid from date must be before valid to date.")
        
        if data['discount_value'] <= 0:
            raise serializers.ValidationError("Discount value must be greater than 0.")
        
        if data['offer_type'] == 'percentage' and data['discount_value'] > 100:
            raise serializers.ValidationError("Percentage discount cannot exceed 100%.")
        
        return data
