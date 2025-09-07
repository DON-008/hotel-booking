from rest_framework import serializers
from .models import Prize, SpinWheelGame, GameSession
from customer_management.serializers import CustomerSerializer

class PrizeSerializer(serializers.ModelSerializer):
    """Serializer for Prize model"""
    
    class Meta:
        model = Prize
        fields = ['id', 'name', 'description', 'icon', 'probability', 'is_active', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SpinWheelGameSerializer(serializers.ModelSerializer):
    """Serializer for SpinWheelGame model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    prize_name = serializers.CharField(source='prize_won.name', read_only=True)
    prize_icon = serializers.CharField(source='prize_won.icon', read_only=True)
    
    class Meta:
        model = SpinWheelGame
        fields = ['id', 'customer', 'customer_name', 'played_at', 'prize_won', 
                 'prize_name', 'prize_icon', 'is_claimed', 'claimed_at', 'notes']
        read_only_fields = ['id', 'played_at']

class GameSessionSerializer(serializers.ModelSerializer):
    """Serializer for GameSession model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = GameSession
        fields = ['id', 'customer', 'customer_name', 'has_played', 'first_play_date', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SpinWheelPlaySerializer(serializers.Serializer):
    """Serializer for playing the spin wheel game"""
    
    customer_id = serializers.UUIDField()
    
    def validate_customer_id(self, value):
        """Validate that customer exists and hasn't played before"""
        from customer_management.models import Customer
        
        try:
            customer = Customer.objects.get(id=value)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found")
        
        # Check if customer has already played
        if hasattr(customer, 'game_session') and customer.game_session.has_played:
            raise serializers.ValidationError("Customer has already played the game")
        
        return value

class PrizeResultSerializer(serializers.Serializer):
    """Serializer for spin wheel result"""
    
    prize = PrizeSerializer()
    customer_name = serializers.CharField()
    played_at = serializers.DateTimeField()
    is_first_play = serializers.BooleanField()
