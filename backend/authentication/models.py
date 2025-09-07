from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return self.email