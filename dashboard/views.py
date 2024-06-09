from django.shortcuts import get_object_or_404, render, redirect
from learning.models import CompletionQuestion, FreeResponseQuestion, MultipleChoiceQuestion, ProblemSet, Question
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
# Create your views here.
def dashboard_view(request):
    return render(request, 'dashboard/base.html')

@login_required
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
    print("@@@@",questions_html)

    context = {
        'problemset': problemset,
        'questions_html': questions_html,
    }
    return render(request, 'dashboard/problemset.html', context)




@login_required
def create_chat_view(request):
    chat = Chat.objects.create(user=request.user)
    # Add an initial message from the AI
    Message.objects.create(chat=chat, sender=None, text="Hello! How can I assist you today?")
    return redirect('chat-view', pk=chat.pk)

@login_required
def chat_view(request, pk):
    chat = get_object_or_404(Chat, pk=pk, user=request.user)
    if request.method == "POST":
        text = request.POST.get('text')
        Message.objects.create(chat=chat, sender=request.user, text=text)
        # Add AI response logic here
        ai_response = "This is a response from the AI."
        Message.objects.create(chat=chat, sender=None, text=ai_response)
    return render(request, 'dashboard/chat.html', {'chat': chat})
