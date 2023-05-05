from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from authy.views import UserProfile, follow

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authy.urls')),
    path('post/', include('post.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', UserProfile, name='profile_favorite'),
    path('<username>/follow/<option>', follow, name='follow')
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)