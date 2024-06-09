from django.shortcuts import get_object_or_404, render
from learning.models import CompletionQuestion, FreeResponseQuestion, MultipleChoiceQuestion, ProblemSet, Question

# Create your views here.
def dashboard_view(request):
    return render(request, 'dashboard/base.html')


def problemset_view(request, pk):
    problemset = get_object_or_404(ProblemSet, pk=pk)
    questions = []
    
    # Fetch all questions related to the problem set
    questions += list(Question.objects.filter(problem_set=problemset))
    questions += list(FreeResponseQuestion.objects.filter(problem_set=problemset))
    questions += list(MultipleChoiceQuestion.objects.filter(problem_set=problemset))
    questions += list(CompletionQuestion.objects.filter(problem_set=problemset))
    
    # Generate HTML for each question
    questions_html = [question.get_html() for question in questions]
    
    context = {
        'problemset': problemset,
        'questions_html': questions_html,
    }
    return render(request, 'dashboard/problemset.html', context)
