from django.shortcuts import get_object_or_404, render
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from utils.AI.question_generator import generate_question
from utils.group_required import group_required  # Import your custom decorator

@require_POST
@group_required(['Teacher'])
def AI_generate(request):
    description = request.POST.get('description', '')
    # generated_problems = generate_question(description)
    generated_problems = {
        "questions": ["hello ___", "How ___ you?", "What did you do ___?"],
        "answers": ["world", "are", "today"]
    }

    return HttpResponse(json.dumps(generated_problems))


from .models import BaseQuestion, Question

def question_view(request, pk):
    # Determine the question type dynamically if necessary
    question = get_object_or_404(Question, pk=pk)
    return HttpResponse(question.get_html())



