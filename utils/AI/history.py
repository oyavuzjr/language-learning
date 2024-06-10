import json
from typing import List, Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict
from dashboard.models import Chat

class DjangoChatMessageHistory(BaseChatMessageHistory):
    """Chat message history that stores history in a Django JSON field."""

    def __init__(self, chat_id: int) -> None:
        """Initialize with the chat ID to fetch the corresponding chat instance."""
        self.chat_id = chat_id
        self.chat_instance = Chat.objects.get(id=self.chat_id)

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from the Django JSON field."""
        items = self.chat_instance.json_history
        messages = messages_from_dict(items)
        return messages

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in the Django JSON field."""
        messages = messages_to_dict(self.messages)
        messages.append(messages_to_dict([message])[0])
        self.chat_instance.json_history = messages
        self.chat_instance.save()

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Append multiple messages to the record in the Django JSON field."""
        existing_messages = messages_to_dict(self.messages)
        new_messages = messages_to_dict(messages)
        existing_messages.extend(new_messages)
        self.chat_instance.json_history = existing_messages
        self.chat_instance.save()

    def clear(self) -> None:
        """Clear session memory from the Django JSON field."""
        self.chat_instance.json_history = []
        self.chat_instance.save()
