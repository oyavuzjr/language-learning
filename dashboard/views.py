from django.shortcuts import get_object_or_404, render, redirect
from learning.models import FreeResponseQuestion, MultipleChoiceQuestion, ProblemSet, Question
from django.contrib.auth.decorators import login_required
from .models import BaseMessage, Chat, AIMessage, HumanMessage, ToolGroup, ToolMessage
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
    # questions += list(CompletionQuestion.objects.filter(problem_set=problemset))
    
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
    AIMessage.objects.create(chat=chat, text="Hello! How can I assist you today?")
    return redirect('chat-view', pk=chat.pk)

@login_required
def chat_view(request, pk):
    generated_content = []
    chat = get_object_or_404(Chat, pk=pk, user=request.user)
    if request.method == "POST":
        text = request.POST.get('text')

        # Get AI response
        json_data, text, output, tools = send_message(chat.id, text)  # Pass chat_id to send_message
        # Save human message to the database
        HumanMessage.objects.create(chat=chat, sender=request.user, text=text)


        if isinstance(tools, list) and len(tools) > 0:
            tool_group = ToolGroup.objects.create(chat=chat)
            ids = []
            for tool in tools:
                tool_to_use, args = tool
                if "ids" in args:
                    ids.extend(args["ids"])
            query_results = ToolMessage.objects.filter(id__in=ids)
            for q in query_results:
                # q.chat = chat
                # q.save()
                tool_group.tool_messages.add(q)
            tool_group.save()

        else:
            ai_msg = AIMessage.objects.create(chat=chat, text=output)
            ai_msg.save()
            # tool_group.tool_messages.add(ai_msg)
            # tool_group.save()

        # Message.objects.create(chat=chat, sender=None, text=output, json_data=json_data,tools_data=tools)
    messages = BaseMessage.objects.filter(chat=chat)
    generated_content = "".join([m.get_html() for m in messages])
    return render(request, 'dashboard/chat.html', {'chat': chat, 'nav_items': get_nav_items(), 'generated_content': generated_content})