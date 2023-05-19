from django.db import models
from django.contrib.auth.models import User

# from post.models import Post

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))

    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.sender} - {self.NOTIFICATION_TYPES[self.notification_type - 1][1]} - {self.user}'