from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrizeViewSet, SpinWheelGameViewSet, GameSessionViewSet

router = DefaultRouter()
router.register(r'prizes', PrizeViewSet)
router.register(r'games', SpinWheelGameViewSet)
router.register(r'sessions', GameSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
