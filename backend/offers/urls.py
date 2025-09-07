from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, OfferUsageViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'usages', OfferUsageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
