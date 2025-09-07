from django.urls import path
from . import views

urlpatterns = [
    path('send-wish/', views.send_whatsapp_wish, name='send_whatsapp_wish'),
    path('send-message/', views.send_whatsapp_message, name='send_whatsapp_message'),
]
