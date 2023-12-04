from django.contrib import admin
from .models import ProblemSet, Question
# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question

class ProblemSetAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]

admin.site.register(ProblemSet,ProblemSetAdmin)
