from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages_from_chat")
    ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE, related_name="chat_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender} at {self.timestamp}"
