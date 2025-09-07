from django.contrib import admin
from .models import Offer, OfferUsage

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_type', 'discount_value', 'status', 'valid_from', 'valid_to', 'current_usage']
    list_filter = ['offer_type', 'status', 'valid_from', 'valid_to']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'current_usage', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(OfferUsage)
class OfferUsageAdmin(admin.ModelAdmin):
    list_display = ['customer', 'offer', 'used_at', 'discount_applied']
    list_filter = ['used_at', 'offer__offer_type']
    search_fields = ['customer__name', 'offer__title']
    readonly_fields = ['id', 'used_at']
    ordering = ['-used_at']