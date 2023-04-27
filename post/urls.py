from django.urls import path

from post.views import index, new_post, post_details, tag_page

urlpatterns = [
    path('', index, name='index'),
    path('upload_post/', new_post, name='upload_post'),
    path('<uuid:post_id>/', post_details, name='post_details'),
    path('tag/<slug:slug>/', tag_page, name='tags'),
]