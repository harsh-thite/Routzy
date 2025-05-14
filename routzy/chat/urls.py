# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ride/<int:ride_id>/chat/', views.ride_chat, name='ride_chat'),
]
