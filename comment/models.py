from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from post.models import Post
from notifications.models import Notification


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def user_comment(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.comment[:90]
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        notify.save()

    @staticmethod
    def user_del_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user, notification_type=2)
        notify.delete()

    def __str__(self):
        return f'{self.user} comment {self.post}'


post_save.connect(Comment.user_comment, sender=Comment)
post_save.connect(Comment.user_del_comment_post, sender=Comment)