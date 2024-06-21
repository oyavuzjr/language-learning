from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import jsonfield

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    json_history = jsonfield.JSONField(default=dict)  # Add this field to store the chat history

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    json_data = jsonfield.JSONField(default=dict)  # Add this field to store the chat history
