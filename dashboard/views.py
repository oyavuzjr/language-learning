from django.shortcuts import get_object_or_404, render, redirect
from learning.models import CompletionQuestion, FreeResponseQuestion, MultipleChoiceQuestion, ProblemSet, Question
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from utils.AI.chat import send_message  # Import the send_message function
from django.urls import reverse



def get_nav_items(x=5):
    recent_chats = Chat.objects.order_by('-created_at')[:x]
    homeworks = ProblemSet.objects.order_by('-created_at')[:x]
    
    nav_items = [
        {
            'title': 'Chats',
            'items': [{'id': chat.id, 'user': chat.user, 'created_at': chat.created_at, 'url': reverse('chat-view', args=[chat.id])} for chat in recent_chats],
        },
        {
            'title': 'Problem Sets',
            'items': [{'id': homework.id, 'created_at': homework.created_at, 'url': reverse('problemset-view', args=[homework.id])} for homework in homeworks],
        },
    ]
    
    return nav_items

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

    context = {
        'problemset': problemset,
        'questions_html': questions_html,
        'nav_items': get_nav_items()
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
        
        # Get AI response
        json_data, ai_response = send_message(chat.id, text)  # Pass chat_id to send_message
        # Save AI response to the database
        Message.objects.create(chat=chat, sender=None, text=ai_response, json_data=json_data)
    
    return render(request, 'dashboard/chat.html', {'chat': chat,'nav_items': get_nav_items()})
