from django.urls import path

from post.views import index, new_post, post_details, tag_page, favorite, like
from direct.views import inbox

urlpatterns = [
    path('', index, name='index'),
    path('upload_post/', new_post, name='upload_post'),
    path('<uuid:post_id>/', post_details, name='post_details'),
    path('tag/<slug:slug>/', tag_page, name='tags'),
    path('<uuid:post_id>/like', like, name='post_like'),
    path('<uuid:post_id>/favorite', favorite, name='post_favorite'),
]
