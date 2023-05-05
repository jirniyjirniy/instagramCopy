from django.contrib import admin
from post.models import Tag, Follow, Post, Stream, Likes
# Register your models here.

admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Stream)
admin.site.register(Likes)