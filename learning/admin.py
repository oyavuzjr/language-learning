from django.contrib import admin
from .models import Language, Lecture, ProblemSet, Question, FreeResponseQuestion, MultipleChoiceQuestion, CompletionQuestion, Submission
from django.urls import path
from .views import AI_generate

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    classes = ('collapse', 'collapse-entry', )

class FreeResponseQuestionInline(admin.TabularInline):
    model = FreeResponseQuestion
    extra = 1
    classes = ('collapse', 'collapse-entry', )

class MultipleChoiceQuestionInline(admin.TabularInline):
    model = MultipleChoiceQuestion
    extra = 1
    classes = ('collapse', 'collapse-entry', )

class CompletionQuestionInline(admin.TabularInline):
    model = CompletionQuestion
    extra = 1
    classes = ('collapse', 'collapse-entry', )

class ProblemSetAdmin(admin.ModelAdmin):
    baton_form_includes = [
        ('AI-generate-button.html', 'description', 'bottom'),
    ]
    inlines = [
        QuestionInline,
        FreeResponseQuestionInline,
        MultipleChoiceQuestionInline,
        CompletionQuestionInline,
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ai-generate/', self.admin_site.admin_view(AI_generate), name='problemset_ai_generate')
        ]
        return custom_urls + urls

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'text', 'correct_answer', 'problem_set', 'created_at')
    list_filter = ('problem_set',)
    search_fields = ('text',)

class FreeResponseQuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'text', 'problem_set', 'created_at')
    list_filter = ('problem_set',)
    search_fields = ('text',)

class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'text', 'choices', 'correct_answer', 'problem_set', 'created_at')
    list_filter = ('problem_set',)
    search_fields = ('text',)

class CompletionQuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'text', 'correct_answer', 'problem_set', 'created_at')
    list_filter = ('problem_set',)
    search_fields = ('text',)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'date', 'correct', 'user_answer')
    list_filter = ('correct', 'date', 'user')
    search_fields = ('question__text', 'user__username', 'user_answer')

class LectureToolAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'problem_set', 'created_at')
    list_filter = ('problem_set',)
    search_fields = ('title', 'text')

admin.site.register(Lecture, LectureToolAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FreeResponseQuestion, FreeResponseQuestionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(CompletionQuestion, CompletionQuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Language)
