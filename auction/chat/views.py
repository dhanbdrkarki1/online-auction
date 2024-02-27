from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Message, ChatRoom
from django.http import HttpResponseForbidden

User = get_user_model()

def chat_view(request):
    try:
        messages = Message.objects.all()
    except:
        return HttpResponseForbidden()
    context = {
        'messages': messages
    }
    return render(request, 'chat/chat.html', context)

def user_chat(request, other_user_id):
    user = request.user
    other_user = get_object_or_404(User, id=other_user_id)

    # Get the chat room where both users are members
    chat_room = ChatRoom.objects.filter(members__in=[user, other_user]).first()

    if chat_room:
        # Filter messages based on the chat room and users
        messages = Message.objects.filter(room=chat_room)
    else:
        messages = []

    context = {
        "other_user": other_user,
        'messages': messages
    }
    return render(request, 'chat/chat.html', context)
