from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Chat, BaseMessage, HumanMessage, AIMessage, ToolMessage,CompletionQuestion

# class MessageInline(admin.TabularInline):
#     model = BaseMessage
#     list_display = ('created_at')
#     extra = 1  # Number of empty message forms to display

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    # inlines = [MessageInline]

admin.site.register(Chat, ChatAdmin)
# admin.site.register(BaseMessage)

# Polymorphic admin for messages
class BaseMessageChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseMessage  # Optional, explicitly set here.

@admin.register(HumanMessage)
class HumanMessageAdmin(BaseMessageChildAdmin):
    base_model = HumanMessage

@admin.register(AIMessage)
class AIMessageAdmin(BaseMessageChildAdmin):
    base_model = AIMessage

@admin.register(ToolMessage)
class ToolMessageAdmin(BaseMessageChildAdmin):
    base_model = ToolMessage

@admin.register(CompletionQuestion)
class CompletionQuestionMessageAdmin(BaseMessageChildAdmin):
    base_model = CompletionQuestion

@admin.register(BaseMessage)
class BaseMessageAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = BaseMessage  # Optional, explicitly set here.
    child_models = (HumanMessage, AIMessage, ToolMessage,CompletionQuestion)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
