from django.contrib import admin
from .models import Prize, SpinWheelGame, GameSession

@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'probability', 'is_active']
    list_filter = ['is_active', 'probability']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-probability']

@admin.register(SpinWheelGame)
class SpinWheelGameAdmin(admin.ModelAdmin):
    list_display = ['customer', 'prize_won', 'played_at', 'is_claimed']
    list_filter = ['is_claimed', 'played_at', 'prize_won']
    search_fields = ['customer__name', 'prize_won__name']
    readonly_fields = ['id', 'played_at']
    ordering = ['-played_at']

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'has_played', 'first_play_date']
    list_filter = ['has_played', 'first_play_date']
    search_fields = ['customer__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']