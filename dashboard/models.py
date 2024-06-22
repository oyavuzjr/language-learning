from django.db import models
from django.contrib.auth.models import User
import jsonfield
from polymorphic.models import PolymorphicModel
from django.template.loader import render_to_string

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    json_history = jsonfield.JSONField(default=dict)  # Add this field to store the chat history

class BaseMessage(PolymorphicModel):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class HumanMessage(BaseMessage):
    text = models.TextField()
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    def get_html(self):
        return render_to_string('question/message.html', {'message': self, 'question_type': 'completionQuestion'})


class AIMessage(BaseMessage):
    text = models.TextField()
    def get_html(self):
        return render_to_string('question/message.html', {'message': self, 'question_type': 'completionQuestion'})


class ToolMessage(BaseMessage):
    tool_name = models.CharField(max_length=100, editable=False)
    response = models.TextField()
    tool_args = jsonfield.JSONField(default=dict)
    def save(self, *args, **kwargs):
        if not self.tool_name:
            self.tool_name = self.get_tool_name()
        super().save(*args, **kwargs)

    def get_tool_name(self):
        # This method should be overridden in subclasses to set the correct tool_name
        raise NotImplementedError("Subclasses must implement get_tool_name method")

class CompletionQuestion(ToolMessage):
    correct_answer = models.CharField(max_length=100)
    text = models.TextField()

    def is_correct(self, answer):
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def get_html(self):
        return render_to_string('question/sentence_completion.html', {'message': self})

    def get_tool_name(self):
        return "create_sentence_completion_problems"

class MultipleChoiceQuestion(ToolMessage):
    text = models.TextField()
    choices = models.JSONField()
    correct_answer = models.IntegerField()

    def is_correct(self, answer):
        return int(answer) == self.correct_answer

    def get_html(self):
        return render_to_string('question/question_multiple_choice.html', {'message': self, 'question_type': 'multipleChoiceQuestion'})

    def get_tool_name(self):
        return "create_multiple_choice_problems"

class Lecture(ToolMessage):
    text = models.TextField()

    def get_html(self):
        return render_to_string('question/lecture.html', {'lecture': self})

    def get_tool_name(self):
        return "create_lecture"
