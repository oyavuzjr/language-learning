import re
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProblemSet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Subject of the problem set")

    def __str__(self):
        return self.name

class BaseQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)

    def get_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def is_correct(self, answer):
        raise NotImplementedError("Subclasses should implement this method.")

    class Meta:
        abstract = True

class Question(BaseQuestion):
    correct_answer = models.CharField(max_length=100)

    def is_correct(self, answer):
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def get_html(self):
        return render_to_string('question/question_text.html', {'question': self, 'question_type': 'question'})

class FreeResponseQuestion(BaseQuestion):

    def get_html(self):
        return render_to_string('question/question_free_response.html', {'question': self, 'question_type': 'freeResponseQuestion'})

class MultipleChoiceQuestion(BaseQuestion):
    choices = models.JSONField()
    correct_answer = models.IntegerField()

    def is_correct(self, answer):
        return int(answer) == self.correct_answer

    def get_html(self):
        return render_to_string('question/question_multiple_choice.html', {'question': self, 'question_type': 'multipleChoiceQuestion'})

class CompletionQuestion(BaseQuestion):
    correct_answer = models.CharField(max_length=100)

    def is_correct(self, answer):
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def get_html(self):
        return render_to_string('question/sentence_completion.html', {'question': self, 'question_type': 'completionQuestion'})


class Submission(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_answer = models.TextField()

    # Generic foreign key to any question type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        # Call the is_correct method on the question instance
        self.correct = self.question.is_correct(self.user_answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Submission for Question {self.object_id} by {self.user.username}"