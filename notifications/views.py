from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from .models import Notification
# Create your views here.


def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    template = loader.get_template('notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))


def delete_notification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show_notifications')