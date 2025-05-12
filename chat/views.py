import uuid

from django import urls
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from chat.models import ChatSession


# Create your views here.


def index(request):
    return render(request, 'chat/index.html')


def check_for_room(request):
    users = request.POST['users']
    room = ChatSession.objects.filter(first_user__username__in=users, second_user__username__in=users)
    if room.exists():
        room = room[0]
    else:
        room = ChatSession.objects.create(
            first_user=get_object_or_404(User, username=users[0]),
            second_user=get_object_or_404(User, username=users[1]),
            uuid=uuid.uuid4(),
        )
    return redirect(urls.reverse(room, args=[room.uuid]))


def room(request, room_name):
    # room = get_object_or_404(ChatSession, uuid=room_name)
    # messages = room.message_set.all()
    # return render(request, "chat/room.html", {"room_name": room_name, 'messages': messages})
    return render(request, "chat/room.html", {"room_name": room_name})
