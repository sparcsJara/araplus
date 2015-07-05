from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.TextField(max_length=12)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "User %s (%s)'s profile object" % (self.user, self.nickname)


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey('UserProfile', related_name='message_sent')
    receiver = models.ForeignKey('UserProfile', related_name='message_received')
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Message from %s to %s at %s" % \
            (sender, receiver, created_time)
