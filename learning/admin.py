from django.contrib import admin
from .models import ProblemSet, Question
from django.urls import path
from .views import AI_generate

class QuestionInline(admin.TabularInline):
    model = Question
    extra=1

class ProblemSetAdmin(admin.ModelAdmin):
    baton_form_includes = [
        ('AI-generate-button.html', 'description', 'bottom', ),
    ]
    inlines = [
        QuestionInline,
    ]
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ai-generate/', self.admin_site.admin_view(AI_generate), name='problemset_ai_generate')
        ]
        return custom_urls + urls

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__",'text', 'correct_answer', 'problem_set')
    list_filter = ('problem_set',)

admin.site.register(ProblemSet,ProblemSetAdmin)
admin.site.register(Question,QuestionAdmin)

