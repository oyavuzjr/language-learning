from django.db import models


class ProblemSet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=200)
    answer = models.CharField(max_length=100)
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name