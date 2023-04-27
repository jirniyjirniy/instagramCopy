from django.contrib import admin
from post.models import Tag, Follow, Post, Stream
# Register your models here.

admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Stream)