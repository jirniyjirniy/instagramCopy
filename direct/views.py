from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template import loader
from django.db.models import Q

from .models import Message


@login_required
def inbox(request):
    messages = Message.get_messages(user=request.user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    return render(request, 'direct.html', context)



@login_required
def directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'user': user,
    }

    return render(request, 'direct.html', context)


def send_direct_message(request):
    from_user = request.user
    print(from_user)
    to_user_username = request.POST.get('to_user')
    print(to_user_username)
    body = request.POST.get('body')
    print(body)

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('direct')
    else:
        HttpResponseBadRequest()


def notification(request):
    return render(request, 'notifications.html')