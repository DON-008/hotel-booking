from django.db import models
from customer_management.models import Customer
import uuid

class Prize(models.Model):
    """Prizes available in the spin wheel game"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🎁')  # Emoji icon
    probability = models.PositiveIntegerField(default=20)  # Probability percentage
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-probability']
        verbose_name = 'Prize'
        verbose_name_plural = 'Prizes'
    
    def __str__(self):
        return f"{self.name} ({self.probability}%)"

class SpinWheelGame(models.Model):
    """Track spin wheel game sessions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='spin_games')
    played_at = models.DateTimeField(auto_now_add=True)
    prize_won = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name='games_won')
    is_claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-played_at']
        verbose_name = 'Spin Wheel Game'
        verbose_name_plural = 'Spin Wheel Games'
    
    def __str__(self):
        return f"{self.customer.name} won {self.prize_won.name}"

class GameSession(models.Model):
    """Track customer game sessions and prevent multiple plays"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='game_session')
    has_played = models.BooleanField(default=False)
    first_play_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Game Session'
        verbose_name_plural = 'Game Sessions'
    
    def __str__(self):
        return f"Game session for {self.customer.name} - {'Played' if self.has_played else 'Not played'}"