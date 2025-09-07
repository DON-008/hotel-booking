from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecialDateViewSet, EventViewSet, EventBookingViewSet

router = DefaultRouter()
router.register(r'special-dates', SpecialDateViewSet)
router.register(r'events', EventViewSet)
router.register(r'bookings', EventBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
