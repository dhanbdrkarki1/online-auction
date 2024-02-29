from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Message, ChatRoom
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q

User = get_user_model()

@login_required
def chat(request, other_user_id=None):
    user = request.user
    other_user = None
    messages = []

    if other_user_id:
        other_user = get_object_or_404(User, id=other_user_id)
        chat_room = ChatRoom.objects.filter(members=user).filter(members=other_user).first()
        # only include those sent by the current user and the other user
        messages = Message.objects.filter(room=chat_room).filter(Q(sender=user) | Q(sender=other_user)).order_by('timestamp')

    users_chatted_with = set()
    sent_messages = Message.objects.filter(sender=user)
    received_messages = Message.objects.filter(room__members=user)
    for message in sent_messages:
        users_chatted_with.add(message.room.members.exclude(id=user.id).first())
    for message in received_messages:
        users_chatted_with.add(message.sender)

    users_chatted_with.discard(user)

    context = {
        'other_user': other_user,
        'messages': messages,
        'users_chatted_with': users_chatted_with
    }
    return render(request, 'chat/chat.html', context)


