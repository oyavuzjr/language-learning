from django.db import models


class ProblemSet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Subject of the problem set")

    def __str__(self):
        return self.name

class BaseQuestion(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user_answer = models.TextField(blank=True, null=True)
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)

    def get_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    class Meta:
        abstract = True

class Question(BaseQuestion):
    correct_answer = models.CharField(max_length=100)

    def is_correct(self):
        return self.user_answer.strip().lower() == self.correct_answer.strip().lower()

    def get_html(self):
        return f"""
        <div x-data="question({self.id})">
            <h2>{self.title}</h2>
            <p>{self.text}</p>
            <input type="text" x-model="user_answer" />
        </div>
        """

class FreeResponseQuestion(BaseQuestion):

    def get_html(self):
        return f"""
        <div x-data="freeResponseQuestion({self.id})">
            <h2>{self.title}</h2>
            <p>{self.text}</p>
            <textarea x-model="user_answer"></textarea>
        </div>
        """

class MultipleChoiceQuestion(BaseQuestion):
    choices = models.JSONField()
    correct_choice = models.IntegerField()

    def is_correct(self):
        return int(self.user_answer) == self.correct_choice

    def get_html(self):
        choices_html = ''.join([f'<button x-on:click="selectChoice({i})">{choice}</button>' for i, choice in enumerate(self.choices)])
        return f"""
        <div x-data="multipleChoiceQuestion({self.id})">
            <h2>{self.title}</h2>
            <p>{self.text}</p>
            <div>{choices_html}</div>
        </div>
        """
