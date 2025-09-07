from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
import random
from .models import Prize, SpinWheelGame, GameSession
from .serializers import (
    PrizeSerializer, 
    SpinWheelGameSerializer, 
    GameSessionSerializer,
    SpinWheelPlaySerializer,
    PrizeResultSerializer
)

class PrizeViewSet(viewsets.ModelViewSet):
    """ViewSet for Prize model"""
    
    queryset = Prize.objects.filter(is_active=True)
    serializer_class = PrizeSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active prizes"""
        active_prizes = Prize.objects.filter(is_active=True)
        serializer = self.get_serializer(active_prizes, many=True)
        return Response(serializer.data)

class SpinWheelGameViewSet(viewsets.ModelViewSet):
    """ViewSet for SpinWheelGame model"""
    
    queryset = SpinWheelGame.objects.all()
    serializer_class = SpinWheelGameSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    def get_queryset(self):
        """Filter games based on query parameters"""
        queryset = SpinWheelGame.objects.all()
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # Filter by claimed status
        is_claimed = self.request.query_params.get('claimed', None)
        if is_claimed is not None:
            queryset = queryset.filter(is_claimed=is_claimed.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def play(self, request):
        """Play the spin wheel game"""
        serializer = SpinWheelPlaySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        customer_id = serializer.validated_data['customer_id']
        
        # Get customer
        from customer_management.models import Customer
        customer = Customer.objects.get(id=customer_id)
        
        # Determine prize based on probability
        prize = self._determine_prize()
        
        # Create game session if it doesn't exist
        game_session, created = GameSession.objects.get_or_create(
            customer=customer,
            defaults={'has_played': True, 'first_play_date': timezone.now()}
        )
        
        if not created:
            # Update existing session
            game_session.has_played = True
            if not game_session.first_play_date:
                game_session.first_play_date = timezone.now()
            game_session.save()
        
        # Create spin wheel game record
        game = SpinWheelGame.objects.create(
            customer=customer,
            prize_won=prize
        )
        
        # Return result
        result_serializer = PrizeResultSerializer({
            'prize': prize,
            'customer_name': customer.name,
            'played_at': game.played_at,
            'is_first_play': created
        })
        
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)
    
    def _determine_prize(self):
        """Determine prize based on probability"""
        prizes = Prize.objects.filter(is_active=True)
        if not prizes.exists():
            # Default prize if no prizes are configured
            return Prize.objects.create(
                name="Thank You",
                description="Thank you for playing!",
                icon="🎉",
                probability=100
            )
        
        # Create weighted list based on probability
        weighted_prizes = []
        for prize in prizes:
            weighted_prizes.extend([prize] * prize.probability)
        
        return random.choice(weighted_prizes)
    
    @action(detail=True, methods=['patch'])
    def claim(self, request, pk=None):
        """Claim a prize"""
        game = self.get_object()
        
        if game.is_claimed:
            return Response({'error': 'Prize has already been claimed'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        game.is_claimed = True
        game.claimed_at = timezone.now()
        game.notes = request.data.get('notes', '')
        game.save()
        
        serializer = self.get_serializer(game)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get spin wheel game statistics"""
        total_games = SpinWheelGame.objects.count()
        claimed_prizes = SpinWheelGame.objects.filter(is_claimed=True).count()
        unclaimed_prizes = SpinWheelGame.objects.filter(is_claimed=False).count()
        
        # Prize distribution
        prize_stats = {}
        for prize in Prize.objects.filter(is_active=True):
            count = SpinWheelGame.objects.filter(prize_won=prize).count()
            prize_stats[prize.name] = count
        
        return Response({
            'total_games': total_games,
            'claimed_prizes': claimed_prizes,
            'unclaimed_prizes': unclaimed_prizes,
            'prize_distribution': prize_stats
        })

class GameSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for GameSession model"""
    
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    permission_classes = [AllowAny]  # Temporarily allow unauthenticated access for development
    
    @action(detail=False, methods=['get'])
    def played_customers(self, request):
        """Get list of customers who have played"""
        played_sessions = GameSession.objects.filter(has_played=True)
        serializer = self.get_serializer(played_sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available_customers(self, request):
        """Get list of customers who haven't played yet"""
        from customer_management.models import Customer
        
        played_customer_ids = GameSession.objects.filter(has_played=True).values_list('customer_id', flat=True)
        available_customers = Customer.objects.exclude(id__in=played_customer_ids)
        
        from customer_management.serializers import CustomerSerializer
        serializer = CustomerSerializer(available_customers, many=True)
        return Response(serializer.data)