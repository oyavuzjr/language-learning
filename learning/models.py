import re
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
        return f"""
        <div class="mb-8" x-data="question({self.id})">
            <h3 class="font-medium text-xl">{self.text}</h3>
        <div>
            <div class="relative mt-2">
                <input  x-model="user_answer" type="text" name="name" id="name" class="input input-bordered input-md w-full max-w-xs" autocomplete="off" placeholder="Answer">
            </div>
        </div>
        """

class FreeResponseQuestion(BaseQuestion):

    def get_html(self):
        return f"""
        <div class="mb-8" x-data="freeResponseQuestion({self.id})">
            <h3 class="font-medium text-xl">{self.text}</h3>
            <div>
                <div class="mt-2">
                    <textarea x-model="user_answer" rows="4" name="comment" id="comment" class="textarea textarea-bordered md:w-3/5"></textarea>
                </div>
            </div>
        </div>
        """

class MultipleChoiceQuestion(BaseQuestion):
    choices = models.JSONField()
    correct_answer = models.IntegerField()

    def is_correct(self, answer):
        return int(answer) == self.correct_answer

    def get_html(self):
        choices_html = ''.join([
            f'''<button  x-on:click="selectChoice({i}) type="button" class="btn btn-accent mr-2">{choice}</button>'''
                                 for i, choice in enumerate(self.choices)])
        return f"""
        <div class="mb-8" x-data="multipleChoiceQuestion({self.id})">
            <h3 class="mb-2 font-medium text-xl">{self.text}</h3>
            <div>{choices_html}</div>
        </div>
        """


class CompletionQuestion(BaseQuestion):
    correct_answer = models.CharField(max_length=100)

    def is_correct(self, answer):
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def get_html(self):
        # Replace sequences of underscores with a single input field
        html_parts = []
        parts = re.split(r'(_+)', self.text)
        input_index = 0
        for part in parts:
            if '_' in part:
                html_parts.append(f'<input type="text" class="text-center border-b border-gray-300 focus:border-accent outline-none" x-model="user_answers[{input_index}]" />')
                input_index += 1
            else:
                html_parts.append(f'<span>{part}</span>')

        html_content = ''.join(html_parts)

        return f"""
        <div class="mb-8" x-data="completionQuestion({self.id})">
            <h3 class="font-medium text-xl">{html_content}</h3>
        </div>
        """



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