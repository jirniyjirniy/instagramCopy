from django.urls import path
from direct.views import inbox, directs, send_direct_message, notification

urlpatterns = [
    path('', inbox, name='direct'),
    path('<str:username>/', directs, name='directs'),
    path('send/', send_direct_message, name='send_direct_message'),
]
