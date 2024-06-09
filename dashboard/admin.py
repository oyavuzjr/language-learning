from django.contrib import admin
from .models import Chat, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Number of empty message forms to display

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [MessageInline]

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
