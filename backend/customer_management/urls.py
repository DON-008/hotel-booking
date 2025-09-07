from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CustomerProfileViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'profiles', CustomerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
