from django.urls import path
from direct.views import inbox, directs, send_direct, search_user
urlpatterns = [
   	path('', inbox, name='inbox'),
   	path('directs/<str:username>', directs, name='directs'),
   	path('send/', send_direct, name='send_direct'),
   	path('new/', search_user, name='search_user'),
   	# path('new/<str:username>', new_conversation, name='new_conversation'),
]