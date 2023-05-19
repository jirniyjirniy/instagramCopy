from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message

class MessageTestCase(TestCase):
    def setUp(self):
        self.from_user = User.objects.create_user(
            username='test_user1', password='test_password1')
        self.to_user = User.objects.create_user(
            username='test_user2', password='test_password2')
        self.body = 'test message'

    def test_send_message(self):
        Message.send_message(self.from_user, self.to_user, self.body)
        message = Message.objects.filter(sender=self.from_user, recipient=self.to_user, body=self.body)
        self.assertTrue(message.exists())

