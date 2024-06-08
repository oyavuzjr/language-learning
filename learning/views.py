from django.shortcuts import render
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
        "questions": ["Question 1", "Question 2", "Question 3", "Question 4"],
        "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]
    }

    return HttpResponse(json.dumps(generated_problems))
