from rest_framework import serializers
from .models import Customer, CustomerProfile

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'birth_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for CustomerProfile model"""
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'address', 'city', 'country', 'preferences', 'notes', 'is_vip']
        read_only_fields = ['id']

class CustomerDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Customer with profile"""
    
    profile = CustomerProfileSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'birth_date', 'created_at', 'updated_at', 'profile']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CustomerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new customers"""
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'birth_date']
    
    def validate_phone(self, value):
        """Validate phone number uniqueness"""
        if Customer.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A customer with this phone number already exists.")
        return value
